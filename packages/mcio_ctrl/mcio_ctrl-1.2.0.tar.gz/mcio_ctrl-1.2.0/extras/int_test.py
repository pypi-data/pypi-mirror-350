"""Start of integration test"""

import argparse
import pprint
import sys
import time

import mcio_remote as mcio
from mcio_remote.envs import mcio_env

# import gymnasium as gym


def test() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = mcio_env.MCioEnv(opts, render_mode="human")

    setup_commands = [
        "say one",
        "time set 23000t",  # Sunrise
        "say two",
        "teleport @s ~ ~ ~ -90 0",  # face East
        "say three",
        # "summon minecraft:sheep ~2 ~2 ~2",
        # "summon minecraft:cow ~-2 ~2 ~-2",
    ]
    observation, info = env.reset(options={"commands": setup_commands})
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(
            env.get_noop_action()
        )
    print(obs_to_string(observation))
    input("Next ")

    done = False
    i = 0
    while not done:
        print(i)
        i += 1
        action = env.get_noop_action()

        # Limit some actions
        action["cursor_delta"][:] = [10, 0]

        # # tion["W"] = mcio_env.PRESS
        observation, reward, terminated, truncated, info = env.step(action)
        print(obs_to_string(observation))
        input("Next ")
        done = terminated or truncated

    env.close()


def setup() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = mcio_env.MCioEnv(opts, render_mode="human")

    env.reset()
    skipn(env, 20)
    print("Set day")
    cmds(env, ["time set day"])
    cmds(env, ["teleport @s ~ ~ ~ 0 45"])
    skipn(env, 25)
    # skipx(env)
    print("Pause")
    time.sleep(1)
    print("Set night")
    cmds(env, ["time set night"])
    cmds(env, ["teleport @s ~ ~ ~ 0 -45"])
    skipn(env, 25)
    # skipx(env)
    env.close()


def cmds(env: mcio_env.MCioEnv, commands: list[str]) -> None:
    env.step(env.get_noop_action(), options={"commands": commands})


def skipn(env: mcio_env.MCioEnv, steps: int) -> None:
    for i in range(steps):
        observation, reward, terminated, truncated, info = env.step(
            env.get_noop_action()
        )
        time.sleep(0.1)
        print(f"Skip {i+1}")


def skipx(env: mcio_env.MCioEnv) -> None:
    done = False
    i = 0
    while not done:
        observation, reward, terminated, truncated, info = env.step(
            env.get_noop_action()
        )
        i += 1
        key = input(f"{i}: Step? ")
        if key.lower() == "n":
            done = True


def obs_to_string(obs: mcio_env.MCioObservation) -> str:
    """Return a pretty version of the observation as a string.
    Prints the shape of the frame rather than the frame itself"""
    frame = obs["frame"]
    obs["frame"] = frame.shape
    formatted = pprint.pformat(obs)
    obs["frame"] = frame
    return formatted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test")

    mcio.util.logging_add_arg(parser)

    parser.add_argument(
        "mode",
        metavar="mode",
        type=str,
    )

    args = parser.parse_args()
    mcio.util.logging_init(args=args)
    return args


if __name__ == "__main__":
    args = parse_args()

    if args.mode == "test":
        test()
    elif args.mode == "setup":
        setup()
    else:
        print(f"Unknown mode: {args.mode}")
