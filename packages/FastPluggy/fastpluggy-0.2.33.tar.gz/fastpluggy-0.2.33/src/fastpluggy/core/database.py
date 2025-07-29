import datetime
import logging
import os
from contextlib import contextmanager
from typing import Dict, Any, Generator

from loguru import logger
from sqlalchemy import (
    DateTime,
    Integer, Column, orm, func, inspect,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Function to get the database URL dynamically
def get_database_url():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.warning("No Database URL provided. Using default database.")
        database_url = "sqlite:///./config.db"  # Default URL
    return database_url


# Create engine and session dynamically
def get_engine():
    connect_args = {}
    DATABASE_URL = get_database_url()
    if DATABASE_URL.startswith("sqlite"):
        # Needed for SQLite
        connect_args.update({"check_same_thread": False})

    return create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_size=200,
       # echo_pool="debug",
    )


def get_sessionmaker():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


class Base(DeclarativeBase):
    __abstract__ = True  # Make it an abstract base class

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=datetime.datetime.now(datetime.UTC))

    def _repr(self, **fields: Dict[str, Any]) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


# Dépendance pour obtenir la session DB
def get_db():
    db_maker = get_sessionmaker()
    db = db_maker()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, Any, None]:
    """Provide a transactional scope around a series of operations."""
    session_local = get_sessionmaker()
    db: Session = session_local()  # ✨ call it to get a Session
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def create_table_if_not_exist(model):
    engine = get_engine()
    inspector = inspect(engine)
    exist = inspector.has_table(model.__tablename__)
    created = False
    if not exist:
        model.__table__.create(bind=engine)
        logging.info(f"Created '{model}' table")
        created = True
    else:
        logging.info(f"Table '{model}' already exists")

    return exist, created
