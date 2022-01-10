from dotenv import load_dotenv
from os import getenv, path
from loguru import logger


def get_psql_env(path_to_env: str = '.env'):
    """
    Getting from .env variables for psql. There is two types: necessary and not. Those that are not
    will be replaced with default if .env miss them. Those, that are necessary will raise exception
    if .env miss them.
    :type path_to_env: str path to .env file (better to be full path to avoid errors)
    :return:
    """
    if path.exists(path_to_env) is False:
        logger.error('There is no .env on your path')
        raise FileExistsError
    load_dotenv(path_to_env)
    database = getenv("DATABASE")
    if database == '':
        logger.error('fill .env with database name, please')
        quit()
    user = getenv("USER")
    if user == '':
        user = 'postgres'
    password = getenv("PASSWORD")
    if password == '':
        logger.error('fill .env with password, please')
        quit()
    host = getenv("HOST")
    if host == '':
        host = '127.0.0.1'
    port = getenv("PORT")
    if port == '':
        port = '5432'
    return database, user, password, host, port
