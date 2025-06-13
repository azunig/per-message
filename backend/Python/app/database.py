from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------------------------------------------------------
# ¡IMPORTANTE! Actualiza esta línea con los datos de tu base de datos MySQL.
# Formato: "mysql+mysqlclient://USER:PASSWORD@HOST:PORT/DB_NAME"
# -----------------------------------------------------------------------------
DATABASE_URL = "mysql+pymysql://root:toor!@127.0.0.1:3306/per_message"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()