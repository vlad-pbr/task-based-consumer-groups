from datetime import timedelta, datetime
from os import environ, listdir
from dataclasses import dataclass
from pathlib import Path

from redis.client import Redis


@dataclass
class Config:
    redis_host: str = environ["REDIS_HOST"]
    redis_port: int = int(environ["REDIS_PORT"])
    redis_out_stream: str = environ["REDIS_OUT_STREAM"]
    FPS: int = int(environ["FPS"])


def main():

    redis: Redis = Redis(Config.redis_host, Config.redis_port, 0)
    frame_dir: Path = Path("./frames")
    interval: timedelta = timedelta(milliseconds=(1000.0 / Config.FPS))
    next_yield: datetime = datetime.now()

    while True:

        for image_name in listdir(frame_dir):
            with open(frame_dir / image_name, "rb") as image_file:

                while next_yield > datetime.now():
                    pass

                redis.xadd(Config.redis_out_stream, {"data": image_file.read()})
                next_yield += interval


if __name__ == "__main__":
    main()
