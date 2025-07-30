import sys
from collections import defaultdict
from typing import Any

import mcio_ctrl as mcio
from mcio_ctrl.envs import mcio_env, minerl_env


def gui() -> None:
    # gui = mcio.mcio_gui.MCioGUI(cursor_drawer=mcio.util.CrosshairCursor())
    gui = mcio.mcio_gui.MCioGUI()
    gui.run()


def run() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = minerl_env.MinerlEnv(opts, render_mode="human")

    setup_commands = [
        # "time set 0t",  # Just after sunrise
        # "teleport @s ~ ~ ~ -90 0",  # face East
    ]
    print("RESET")
    observation, info = env.reset(options={"commands": setup_commands})
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [99, 200]
    input("move curs >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["camera"] = [0, 0]
    action["inventory"] = 1
    input("e >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["inventory"] = 0
    input("release >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["camera"] = [0, 0.04]
    input("small move >")
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(action)
        env.render()

    action["camera"] = [0, 0]
    action["inventory"] = 1
    input("e close >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    env.close()


def run_mcio() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = mcio_env.MCioEnv(opts, render_mode="human")

    setup_commands = [
        # "time set 0t",  # Just after sunrise
        # "teleport @s ~ ~ ~ -90 0",  # face East
    ]
    print("RESET")
    observation, info = env.reset(options={"commands": setup_commands})
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["cursor_delta"] = [99, 200]
    input("move curs >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["cursor_delta"] = [0, 0]
    action["E"] = 1
    input("e >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["E"] = 0
    input("release >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    action["cursor_delta"] = [0, 0.04]
    input("small move >")
    for i in range(20):
        observation, reward, terminated, truncated, info = env.step(action)
        env.render()

    action["cursor_delta"] = [0, 0]
    action["E"] = 1
    input("e close >")
    observation, reward, terminated, truncated, info = env.step(action)
    env.render()

    env.close()


def send_e() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = minerl_env.MinerlEnv(opts, render_mode="human")

    print("RESET")
    observation, info = env.reset(options={"commands": []})
    print(env.last_cursor_pos)
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [0, 0]
    action["inventory"] = 1

    observation, reward, terminated, truncated, info = env.step(action)
    print(env.last_cursor_pos)
    env.render()
    input(">")

    env.close()


def noop() -> None:
    opts = mcio.types.RunOptions.for_connect()
    env = minerl_env.MinerlEnv(opts, render_mode="human")

    print("RESET")
    observation, info = env.reset(options={"commands": []})
    print(env.last_cursor_pos)
    env.render()
    print("RESET DONE")
    input("> ")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [0, 0]

    for i in range(10):
        observation, reward, terminated, truncated, info = env.step(action)
        print(env.last_cursor_pos)
        env.render()

    input("> ")
    env.close()


def setup() -> None:
    ctrl = mcio.controller.ControllerSync()

    setup_commands = [
        "time set 0t",  # Just after sunrise
        "teleport @s ~ ~ ~ -90 0",  # face East
    ]
    pkt = mcio.network.ActionPacket(commands=setup_commands)
    ctrl.send_action(pkt)
    obs = ctrl.recv_observation()
    print(f"RESET: curr={obs.cursor_pos}")

    null_pkt = mcio.network.ActionPacket()
    for i in range(25):
        ctrl.send_action(null_pkt)
        obs = ctrl.recv_observation()
        print(f"{i}: curr={obs.cursor_pos}")

    ctrl.close()


def reset_test() -> None:
    opts = mcio.types.RunOptions.for_connect(width=100, height=100)
    env = minerl_env.MinerlEnv(opts, render_mode="human")
    setup_commands = [
        "kill @e[type=!player]",
        "summon minecraft:pillager ~2 ~2 ~2",
        # "time set 0t",  # Just after sunrise
        # "teleport @s ~ ~ ~ -90 0",  # face East
    ]
    print("RESET")
    observation, info = env.reset(options={"commands": setup_commands})
    print(env.health)
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [0, 1]

    while not env.terminated:
        observation, reward, terminated, truncated, info = env.step(action)
        # print(env.health)
        env.render()

    print("Terminated")

    print("RESET 2")
    observation, info = env.reset()
    print(env.health)
    env.render()
    print("RESET 2 DONE")
    while not env.terminated:
        observation, reward, terminated, truncated, info = env.step(action)
        # print(env.health)
        env.render()

    env.close()


def asynk() -> None:
    opts = mcio.types.RunOptions(mcio_mode=mcio.types.MCioMode.ASYNC)
    env = minerl_env.MinerlEnv(opts, render_mode="human")
    setup_commands = [
        "kill @e[type=!player]",
        "summon minecraft:pillager ~2 ~2 ~2",
        # "time set 0t",  # Just after sunrise
        # "teleport @s ~ ~ ~ -90 0",  # face East
    ]
    print("RESET")
    observation, info = env.reset(options={"commands": setup_commands})
    print(env.health)
    env.render()
    print("RESET DONE")

    action: dict[str, Any] = defaultdict(int)
    action["camera"] = [0, 0]

    while not env.terminated:
        observation, reward, terminated, truncated, info = env.step(action)
        # print(env.health)
        env.render()

    print("Terminated")

    print("RESET 2")
    observation, info = env.reset()
    print(env.health)
    env.render()
    print("RESET 2 DONE")
    while not env.terminated:
        observation, reward, terminated, truncated, info = env.step(action)
        # print(env.health)
        env.render()

    env.close()


if __name__ == "__main__":
    mcio.util.logging_init()

    if len(sys.argv) != 2:
        print("Usage: python script.py <function_name>")
        print(
            "Available commands:",
            ", ".join(
                fn
                for fn in globals()
                if callable(globals()[fn]) and not fn.startswith("_")
            ),
        )
        sys.exit(1)

    cmd = sys.argv[1]
    fn = globals().get(cmd)
    if not callable(fn):
        print(f"No such command: {cmd}")
        sys.exit(1)

    fn()
