import os
from dotenv import load_dotenv


load_dotenv()


# tg_bot
TOKEN: str = os.getenv('TOKEN')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))
COMMAND_EXECUTOR: str = os.getenv('COMMAND_EXECUTOR')
ADMIN_USERNAME: str = os.getenv('ADMIN_USERNAME')

# psql_server
DRIVERNAME: str = os.getenv('DRIVERNAME')
USERNAME: str = os.getenv('USERNAMEDB')
PASSWORD: str = os.getenv('PASSWORD')
HOST: str = os.getenv('HOST')
PORT: int = int(os.getenv('PORT'))
DATABASE: str = os.getenv('DATABASE')