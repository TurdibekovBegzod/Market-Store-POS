from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
Base = declarative_base()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_LOCAL_URL = os.getenv("DATABASE_LOCAL_URL")

DATABASE_URL = DATABASE_LOCAL_URL