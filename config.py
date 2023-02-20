import os
from dotenv import load_dotenv


load_dotenv()


# tg_bot
TOKEN: str = os.getenv('TOKEN')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))
COMMAND_EXECUTOR = os.getenv('COMMAND_EXECUTOR')


# psql_server
DRIVERNAME: str = os.getenv('DRIVERNAME')
USERNAME: str = os.getenv('USERNAMEDB')
PASSWORD: str = os.getenv('PASSWORD')
HOST: str = os.getenv('HOST')
PORT: int = int(os.getenv('PORT'))
DATABASE: str = os.getenv('DATABASE')