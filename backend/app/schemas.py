from pydantic import BaseModel

class PaperBase(BaseModel):
    title: str
    abstract: str
    publication_date: str
    keywords: str

class PaperCreate(PaperBase):
    researcher_id: int

class Paper(PaperBase):
    id: int

    class Config:
        orm_mode = True

class ResearcherBase(BaseModel):
    name: str
    affiliation: str
    expertise: str

class ResearcherCreate(ResearcherBase):
    pass

class Researcher(ResearcherBase):
    id: int

    class Config:
        orm_mode = True

class TopicBase(BaseModel):
    name: str

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True

class ExperimentBase(BaseModel):
    name: str
    method: str
    result: str

class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int

    class Config:
        orm_mode = True
