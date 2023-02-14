import os
from dotenv import load_dotenv

load_dotenv()

TOKEN : str = os.getenv('TOKEN')
DATABASE : str = os.getenv('DATABASE')