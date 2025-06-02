import os
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    func,
    Integer,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from utils.logger_config import logger

load_dotenv(dotenv_path=".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()


def connect_db():
    """
    Database connector
    """
    try:
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine, autoflush=False)
        Base.metadata.create_all(engine)
        logger.info("Database succesfully connected to.")
    except SQLAlchemyError as e:
        logger.error("Databse connection error: %s", e, exc_info=True)
    return Session, engine


class AiAgent(Base):
    """
    Agents table model creation
    Args:
        Base (): SQLAlchemy Base model
    """

    __tablename__ = "ai_agents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    homepage_url = Column(String)
    category = Column(String)
    source = Column(String)
    trending = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


def load_data(df: pd.DataFrame):
    """
    Function to load data into the Database (PostgreSQL).
    Args:
        df (pd.DataFrame): Cleaned and Transformed data to be loaded.
    """
    Session, engine = connect_db()
    data = df

    with Session.begin() as session:
        try:
            for _, row in data.iterrows():
                ai_tool = session.query(AiAgent).filter_by(
                    name=str(row["name"]),
                    homepage_url=row['homepage_url']                                 
                    ).first()

                if ai_tool:
                    ai_tool.description = row.get("description", ai_tool.description)
                    ai_tool.category = row.get("category", ai_tool.category)
                    ai_tool.source = row.get("source", ai_tool.source)
                    ai_tool.updated_at = row.get("updated_at", ai_tool.updated_at)
                else:
                    ai_tool = AiAgent(
                        name=str(row["name"]),
                        description=str(row["description"]),
                        homepage_url=row["homepage_url"],
                        category=row["category"],
                        source=row["source"],
                        trending=row["trending"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                    )
                    session.add(ai_tool)
            session.commit()
            logger.info("Data successfully loaded in database!")
        except Exception as e:
            logger.error("Data upload failed: %s", e, exc_info=True)
            session.rollback()
        finally:
            session.close()

