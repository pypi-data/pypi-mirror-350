import logging

import logging_loki

# Ensure Loki uses structured logging with "level" as a tag
logging_loki.emitter.LokiEmitter.level_tag = "level"

# Loki URL (Update with your actual endpoint)
LOKI_URL = "http://54.247.93.138:3100/loki/api/v1/push"


def setup_logger(name: str) -> logging.Logger:
    """Setup logger with Loki integration, filtering out DEBUG logs."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # 🔥 Capture ONLY INFO & ERROR logs

    # Ensure FastAPI & dependencies do not override this
    logging.basicConfig(level=logging.INFO, force=True)

    # Console Logging
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Loki Logging (With Structured Tags Applied Globally)
    try:
        loki_handler = logging_loki.LokiHandler(
            url=LOKI_URL,
            tags={"application": "AmbientLibrary", "environment": "production"},
            version="1",
        )
        loki_handler.setFormatter(formatter)
        loki_handler.setLevel(logging.INFO)  # 🔥 Capture ONLY INFO & ERROR logs
        logger.addHandler(loki_handler)
        logger.info(f"✅ Loki logging enabled for {name}!")
    except Exception as e:
        logger.warning(
            f"⚠️ Loki logging setup failed: {e}. Falling back to console logging."
        )

    return logger
