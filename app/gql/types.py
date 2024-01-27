from graphene import ObjectType, Int, String, Field, List as GrapheneList
from typing import Any, Dict, List, Optional
from app.db.data import employers_data, jobs_data


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
