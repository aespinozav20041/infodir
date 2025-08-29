import logging
import os

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    format="%(message)s",
    level=getattr(logging, log_level, logging.INFO),
)

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger()

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    logger.info("health_check")
    return {"status": "ok"}
