async def main():
    from os import getenv as env
    from dotenv import load_dotenv
    import logging
    from x_model import init_db
    from xync_schema import models
    from logging import DEBUG

    load_dotenv()
    logging.basicConfig(level=DEBUG)
    await init_db(env("DB_URL"), models, True)


if __name__ == "__main__":
    from asyncio import run

    run(main())
