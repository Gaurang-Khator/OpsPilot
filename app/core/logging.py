import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Formats log records as single-line JSON for structured log ingestion."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Allows callers to attach extra structured fields, e.g.
        # logger.info("refund_requested", extra={"order_id": 991, "amount": 250})
        reserved = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys())
        extras = {k: v for k, v in record.__dict__.items() if k not in reserved}
        if extras:
            payload.update(extras)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload)


def configure_logging(log_level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(log_level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    # Avoid duplicate handlers if configure_logging() is called more than once
    root.handlers.clear()
    root.addHandler(handler)