import os

TOKEN: str = os.getenv('TOKEN')
COMMAND_EXECUTOR: str = os.getenv('COMMAND_EXECUTOR')
DRIVERNAME: str = os.getenv('DRIVERNAME')
USERNAME: str = os.getenv('USERNAMEDB')
PASSWORD: str = os.getenv('PASSWORD')
HOST: str = os.getenv('HOST')
PORT: int = int(os.getenv('PORT'))
DATABASE: str = os.getenv('DATABASE')