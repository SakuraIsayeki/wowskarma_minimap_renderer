from pathlib import Path
from renderer.render import Renderer
from replay_parser import ReplayParser
from renderer.utils import LOGGER


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--replay", type=str, required=True)
    parser.add_argument("--target-player-id", type=int, required=False)
    namespace = parser.parse_args()
    # Debug: Readback the arguments
    path = Path(namespace.replay)
    target_player_id: int | None = namespace.target_player_id

    LOGGER.info(f"Replay file: {path}")
    LOGGER.info(f"Target player ID: {target_player_id}")
    video_path = path.parent.joinpath(f"{path.stem}.mp4")
    with open(namespace.replay, "rb") as f:
        LOGGER.info("Parsing the replay file...")
        replay_info = ReplayParser(
            f, strict=True, raw_data_output=False
        ).get_info()
        LOGGER.info(f"Replay has version {replay_info['open']['clientVersionFromExe']}")
        LOGGER.info("Rendering the replay file...")
        renderer = Renderer(
            replay_info["hidden"]["replay_data"],
            logs=True,
            enable_chat=True,
            use_tqdm=True,
            target_player_id=target_player_id,

        )
        renderer.start(str(video_path))
        LOGGER.info(f"The video file is at: {str(video_path)}")
        LOGGER.info("Done.")
