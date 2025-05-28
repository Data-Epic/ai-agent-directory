"""
Ai_tools ETL Local DB Setup and data upload

Name: Arowosegbe Victor Iyanuoluwa\n
Email: Iyanuvicky@gmail.com\n
GitHub: https://github.com/Iyanuvicky22/projects
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, Boolean, DateTime, func, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from idempotent_etl_job import logger, run_basic_etl
import pandas as pd

# load_dotenv(dotenv_path=".env")

## DB Setup
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_URL = f"postgresql://{"postgres"}:{"apotiks"}@{"localhost"}:{"5432"}/{"db"}"

Base = declarative_base()


def connect_db():
    """
    Database connector
    """
    try:
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        logger.info("Database succesfully connected to.")
        return Session, engine
    except SQLAlchemyError as e:
        logger.error("Databse connection error: %s", e, exc_info=True)


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    homepage_url = Column(String)
    category = Column(String)
    source = Column(String)
    trending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)


def load_data(df: pd.DataFrame):
    Session, engine = connect_db()
    data = df

    with Session.begin() as session:
        for _, row in data.iterrows():
            ai_tool = session.query(Agent).filter_by(name=str(row["name"])).first()

            if not ai_tool:
                agent = Agent(
                    name=str(row["name"]),
                    description=str(row["description"]),
                    homepage_url=row["homepage_url"],
                    category=row["category"],
                    source=row["source"],
                    trending=row["trending"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                session.add(agent)
        session.commit()


if __name__ == '__main__':
    data = run_basic_etl()
    load_data(df=data)