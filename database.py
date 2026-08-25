from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# Put your MySQL password where YOUR_PASSWORD is
DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost/new_schema"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class TaskDB(Base):
    __tablename__ = "tasks"

    idtasks = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()