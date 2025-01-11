from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(String)
    publication_date = Column(String)
    keywords = Column(String)
    researcher_id = Column(Integer, ForeignKey('researchers.id'))
    researcher = relationship("Researcher", back_populates="papers")
    topics = relationship("Topic", secondary="paper_topics", back_populates="papers")
    citations = relationship("Paper", secondary="paper_citations", primaryjoin=id==id, secondaryjoin=id==id)

class Researcher(Base):
    __tablename__ = "researchers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    affiliation = Column(String)
    expertise = Column(String)
    papers = relationship("Paper", back_populates="researcher")

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    papers = relationship("Paper", secondary="paper_topics", back_populates="topics")

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    method = Column(String)
    result = Column(String)

class PaperTopic(Base):
    __tablename__ = "paper_topics"
    paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.id'), primary_key=True)

class PaperCitation(Base):
    __tablename__ = "paper_citations"
    citing_paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
    cited_paper_id = Column(Integer, ForeignKey('papers.id'), primary_key=True)
