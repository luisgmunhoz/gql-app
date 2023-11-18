from typing import Any, Dict, List, Optional
from graphene import Field, Int, Schema, ObjectType, String, List as GrapheneList
from fastapi import FastAPI
from starlette_graphene import GraphQLApp
import uvicorn


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
]


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
    def resolve_employer(root: Dict[str, Any], info: Any) -> Dict[str, Any]:
        return [
            employer
            for employer in employers_data
            if employer["id"] == root["employer_id"]
        ][0]


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


app = FastAPI()
app.mount("/graphql", GraphQLApp(schema=schema))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
