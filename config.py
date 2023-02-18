import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv('TOKEN')
DATABASE: str = os.getenv('DATABASE')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))

