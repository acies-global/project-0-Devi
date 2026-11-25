import logging

from app.config import get_settings


def main() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    logging.getLogger(__name__).info("app started (env=%s)", settings.app_env)


if __name__ == "__main__":
    main()
