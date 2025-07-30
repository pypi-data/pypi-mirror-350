"""Single step tests"""

import argparse
from collections import defaultdict

import mcio_remote as mcio
from mcio_remote.envs import mcio_env, minerl_env


def minerl_test() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = minerl_env.MinerlEnv(opts, render_mode="human")

    # north=-180 east=-90 south=0 west=90
    # up=-90 down=90

    setup_commands = [
        "time set 0t",  # Just after sunrise
        "teleport @s ~ ~ ~ -90 0",  # face East
        # "summon minecraft:sheep ~2 ~2 ~2",
        # "summon minecraft:cow ~-2 ~2 ~-2",
    ]
    observation, info = env.reset(options={"commands": setup_commands})
    env.skip_steps(25)
    env.render()
    input("Setup complete")

    # This will return 0 for any unspecified key
    action: minerl_env.MinerlAction = defaultdict(int)
    action["camera"] = [0, 90]

    for i in range(int(360 / 90)):
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        print(i)
        env.render()
        # time.sleep(0.2)
        # input()
    # print_step(action, observation)
    env.skip_steps(20)
    env.render()

    input("Done")

    env.close()


def mcio_test() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = mcio_env.MCioEnv(opts, render_mode="human")

    # north=-180 east=-90 south=0 west=90
    # up=-90 down=90

    setup_commands = [
        "time set 0t",  # Just after sunrise
        "teleport @s ~ ~ ~ -90 0",  # face East
        # "summon minecraft:sheep ~2 ~2 ~2",
        # "summon minecraft:cow ~-2 ~2 ~-2",
    ]
    observation, info = env.reset(options={"commands": setup_commands})
    env.skip_steps(25)
    env.render()
    input("Setup complete")

    # This will return 0 for any unspecified key
    action: minerl_env.MinerlAction = defaultdict(int)
    action["camera"] = [0, 90]

    for i in range(int(360 / 90)):
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        print(i)
        env.render()
        # time.sleep(0.2)
        # input()
    # print_step(action, observation)
    env.skip_steps(20)
    env.render()

    input("Done")

    env.close()


def cmds(env: minerl_env.MinerlEnv, commands: list[str]) -> None:
    env.step({}, options={"commands": commands})


def skipx(env: minerl_env.MinerlEnv) -> None:
    done = False
    i = 0
    while not done:
        observation, reward, terminated, truncated, info = env.step({})
        i += 1
        key = input(f"{i}: Step? ")
        if key.lower() == "n":
            done = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test")

    mcio.util.logging_add_arg(parser)

    # parser.add_argument(
    #     "mode",
    #     metavar="mode",
    #     type=str,
    # )

    args = parser.parse_args()
    mcio.util.logging_init(args=args)
    return args


if __name__ == "__main__":
    args = parse_args()
    minerl_test()
