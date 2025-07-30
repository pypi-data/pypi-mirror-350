import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api-qore.quantit.io"

ACCESS_KEY = os.getenv("QORE_ACCESS_KEY")
SECRET_KEY = os.getenv("QORE_SECRET_KEY")
