from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import yaml
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
import os

# Database configuration
DATABASE_URL = "postgresql://user1:password1@db:5432/isolation_demo"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="Article Management API",
    description="API for managing articles with details like name, tags, dates, category, etc.",
    version="1.0.0",
)

# Database models
class Article(Base):
    __tablename__ = "articles"
    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, index=True)
    tags = Column(String)  # Store as comma-separated string
    creation_date = Column(DateTime, default=datetime.utcnow)
    modification_date = Column(DateTime, nullable=True)
    publication_date = Column(DateTime, nullable=True)
    category = Column(String, index=True)
    content_path = Column(String)
    thumbnail = Column(String)
    subtitle = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic models
class ArticleBase(BaseModel):
    name: str
    tags: List[str]
    creation_date: datetime
    modification_date: Optional[datetime] = None
    publication_date: Optional[datetime] = None
    category: str
    content_path: str
    thumbnail: str
    subtitle: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: UUID

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/articles/", response_model=ArticleRead)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    try:
        db_article = Article(
            name=article.name,
            tags=",".join(article.tags),
            creation_date=article.creation_date,
            modification_date=article.modification_date,
            publication_date=article.publication_date,
            category=article.category,
            content_path=article.content_path,
            thumbnail=article.thumbnail,
            subtitle=article.subtitle,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    except Exception as e:
        logger.error(f"Error creating article: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/articles/", response_model=List[ArticleRead])
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    for article in articles:
        article.tags = article.tags.split(",")
    return articles

@app.get("/articles/{article_id}", response_model=ArticleRead)
def get_article(article_id: UUID, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db_article.tags = db_article.tags.split(",")
    return db_article

@app.put("/articles/{article_id}", response_model=ArticleRead)
def update_article(article_id: UUID, updated_article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in updated_article.dict().items():
        if key == "tags":
            value = ",".join(value)
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    db_article.tags = db_article.tags.split(",")
    return db_article

@app.delete("/articles/{article_id}")
def delete_article(article_id: UUID, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return {"message": "Article deleted successfully"}

# Generate OpenAPI YAML file
def generate_openapi_yaml():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    with open("openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False)

generate_openapi_yaml()

@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    file_path = "openapi.yaml"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="OpenAPI YAML file not found")
