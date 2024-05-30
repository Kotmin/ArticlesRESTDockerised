from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime

import time

DATABASE_URL = "postgresql://user1:password1@db:5432/isolation_demo"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()


SLEEP_TIME = 1000 * 10

try:
    session.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
    session.begin()
    session.execute("INSERT INTO articles (id, name, tags, creation_date, category, content_path, thumbnail) VALUES (:id, :name, :tags, :creation_date, :category, :content_path, :thumbnail)", {
        'id': str(uuid4()),
        'name': 'User 1 Article',
        'tags': ['tag1', 'tag2'],
        'creation_date': datetime.utcnow(),
        'category': 'Category 1',
        'content_path': '/path/to/content1',
        'thumbnail': '/path/to/thumbnail1'
    })
    # Uncomment to commit the transaction

    time.sleep(SLEEP_TIME)
    session.commit()
except SQLAlchemyError as e:
    print(f"An error occurred: {e}")
    session.rollback()
finally:
    session.close()
