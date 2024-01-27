from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, List, Optional
from graphene import Field, Int, Schema, ObjectType, String, List as GrapheneList
from fastapi import FastAPI
from starlette_graphene import GraphQLApp
import uvicorn
from sqlalchemy import Column, ForeignKey, Integer, String as SaString, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

engine = create_engine(os.environ["DB_URL"])

Base = declarative_base()


class Employer(Base):  # type: ignore[valid-type, misc]
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(SaString)
    contact_email = Column(SaString)
    industry = Column(SaString)
    jobs = relationship("Job", back_populates="employer")


class Job(Base):  # type: ignore[valid-type, misc]
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(SaString)
    description = Column(SaString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

# static data
employers_data = [
    {
        "id": 1,
        "name": "MetaTechA",
        "contact_email": "contact@company-a.com",
        "industry": "Tech",
    },
    {
        "id": 2,
        "name": "MoneySoftB",
        "contact_email": "contact@company-b.com",
        "industry": "Finance",
    },
]

jobs_data = [
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Develop web applications",
        "employer_id": 1,
    },
    {
        "id": 2,
        "title": "Data Analyst",
        "description": "Analyze data and create reports",
        "employer_id": 1,
    },
    {
        "id": 3,
        "title": "Accountant",
        "description": "Manage financial records",
        "employer_id": 2,
    },
    {
        "id": 4,
        "title": "Manager",
        "description": "Manage people who manage records",
        "employer_id": 2,
    },
    {
        "id": 5,
        "title": "Plumber",
        "description": "Independent contractor",
        "employer_id": 2,
    },
]


def prepare_db() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    for employer in employers_data:
        session.add(Employer(**employer))
    for job in jobs_data:
        session.add(Job(**job))
    session.commit()
    session.close()


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = GrapheneList(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root: Dict[str, Any], info: Any) -> List[Dict[str, Any]]:
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root: Dict[str, Any], info: Any) -> Optional[Dict[str, Any]]:
        return next(
            (
                employer
                for employer in employers_data
                if employer["id"] == root["employer_id"]
            ),
            None,
        )


class Query(ObjectType):
    jobs = GrapheneList(JobObject)
    employers = GrapheneList(EmployerObject)

    @staticmethod
    def resolve_jobs(root: Optional[Any], info: Any) -> List[Dict[str, Any]]:
        return jobs_data

    @staticmethod
    def resolve_employers(root: Optional[Any], info: Any) -> List[Dict[str, Any]]:
        return employers_data


schema = Schema(query=Query)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    prepare_db()
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)
app.mount("/graphql", GraphQLApp(schema=schema))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
