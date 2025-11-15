import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True, index=True, nullable=False)
    base_url = sa.Column(sa.String, nullable=False)
    rss_url = sa.Column(sa.String, nullable=True)
    type = sa.Column(sa.String, nullable=False)
    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")

class Article(Base):
    __tablename__ = "articles"

    id = sa.Column(sa.Integer, primary_key=True)
    source_id = sa.Column(sa.Integer, sa.ForeignKey("sources.id"), nullable=False)
    url = sa.Column(sa.String, nullable=False)
    title = sa.Column(sa.String, nullable=False)
    summary = sa.Column(sa.String, nullable=True)
    full_text = sa.Column(sa.Text, nullable=True)
    published_at = sa.Column(sa.DateTime, nullable=True)
    scraped_at = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    tickers = sa.Column(JSONB, nullable=True)
    language = sa.Column(sa.String, nullable=True)
    hash_for_dedup = sa.Column(sa.String, nullable=False, unique=True, index=True)
    source = relationship("Source", back_populates="articles")
    sentiments = relationship("ArticleSentiment", back_populates="article", cascade="all, delete-orphan")

class Price(Base):
    __tablename__ = "prices"

    id = sa.Column(sa.Integer, primary_key=True)
    ticker = sa.Column(sa.String, index=True, nullable=False)
    date = sa.Column(sa.Date, index=True, nullable=False)
    open = sa.Column(sa.Float)
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    volume = sa.Column(sa.BigInteger)

class ArticleSentiment(Base):
    __tablename__ = "article_sentiment"

    id = sa.Column(sa.Integer, primary_key=True)
    article_id = sa.Column(sa.Integer, sa.ForeignKey("articles.id"), nullable=False)
    sentiment_label = sa.Column(sa.String, nullable=False)
    sentiment_score = sa.Column(sa.Float, nullable=False)
    model_name = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    article = relationship("Article", back_populates="sentiments")

class TickerAggregate(Base):
    __tablename__ = "ticker_aggregates"

    id = sa.Column(sa.Integer, primary_key=True)
    ticker = sa.Column(sa.String, index=True, nullable=False)
    date = sa.Column(sa.Date, index=True, nullable=False)
    avg_sentiment = sa.Column(sa.Float)
    pos_share = sa.Column(sa.Float)
    neg_share = sa.Column(sa.Float)
    article_count = sa.Column(sa.Integer)
    return_1d = sa.Column(sa.Float)
    return_5d = sa.Column(sa.Float)