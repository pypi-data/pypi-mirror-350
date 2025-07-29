import asyncio
import logging
import logging.config
import time

import fastapi

from uptick_observability.fastapi import manually_instrument_fastapi
from uptick_observability.logging import (
    DEFAULT_LOGGING_CONFIG_DICT,
    manually_instrument_logging,
)

logging.config.dictConfig(DEFAULT_LOGGING_CONFIG_DICT)
manually_instrument_logging()
manually_instrument_fastapi()


logger = logging.getLogger(__name__)

app = fastapi.FastAPI()


@app.get("/")
def home() -> str:
    logger.info("hi testing logs")
    return ""


@app.get("/pingz")
def pingz() -> str:
    return "pingz"


@app.get("/healthz/")
@app.get("/healthz")
def healthz() -> str:
    return "pingz"


@app.get("/sync")
def test_sync() -> str:
    time.sleep(0.5)
    logger.info("hi testing sync")
    return "test_sync"


@app.get("/async")
async def test_async() -> str:
    await asyncio.sleep(0.5)
    logger.info("hi testing sync")
    return "test_async"
