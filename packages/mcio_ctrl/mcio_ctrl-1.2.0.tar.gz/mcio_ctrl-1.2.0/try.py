import sys

import mcio_ctrl as mcio


def lan() -> None:
    opts = mcio.types.RunOptions(
        instance_name="DemoInstance",
        world_name="DemoWorld",
        mc_username="VPT",
        open_to_lan=True,
        open_to_lan_mode=mcio.types.GameMode.CREATIVE,
    )
    launch = mcio.instance.Launcher(opts)
    launch.launch(wait=True)


def chunk_load_sync() -> None:
    ctrl = mcio.controller.ControllerSync()
    for i in range(200):
        ctrl.send_action(mcio.network.ActionPacket())
        obs = ctrl.recv_observation()
    ctrl.close()


def chunk_load_async() -> None:
    ctrl = mcio.controller.ControllerAsync()
    for i in range(200):
        ctrl.send_action(mcio.network.ActionPacket())
        obs = ctrl.recv_observation()
    ctrl.close()


def _async() -> None:
    ctrl = mcio.controller.ControllerAsync()
    conn = ctrl._mcio_conn
    print(conn._last_action_pkt)
    print(conn._last_observation_pkt)
    vid = mcio.util.VideoWriter()

    for i in range(200):
        # ctrl.send_action(mcio.network.ActionPacket())
        obs = ctrl.recv_observation()
        assert obs is not None
        frame = obs.get_frame_with_cursor()
        aa = conn._last_action_pkt
        oo = conn._last_observation_pkt
        print(f"------------------ {i}")
        # print(aa)
        # print(oo)
        vid.add(frame)

    ctrl.close()
    vid.write("test.mp4", annotate=True)


def sync() -> None:
    ctrl = mcio.controller.ControllerSync()
    conn = ctrl._mcio_conn
    print(conn._last_action_pkt)
    print(conn._last_observation_pkt)
    vid = mcio.util.VideoWriter()

    for i in range(200):
        ctrl.send_action(mcio.network.ActionPacket())
        obs = ctrl.recv_observation()
        assert obs is not None
        frame = obs.get_frame_with_cursor()
        aa = conn._last_action_pkt
        oo = conn._last_observation_pkt
        print(f"------------------ {i}")
        print(aa)
        print(oo)
        vid.add(frame)

    ctrl.close()
    vid.write("test.mp4", annotate=True)


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
