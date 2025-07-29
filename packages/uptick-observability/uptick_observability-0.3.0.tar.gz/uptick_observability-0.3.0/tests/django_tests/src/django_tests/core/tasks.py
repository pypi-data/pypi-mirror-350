import logging
import time

import dramatiq


@dramatiq.actor
def hello_world_task(name: str):
    logging.info(f"Hi {name}")
    time.sleep(5)
