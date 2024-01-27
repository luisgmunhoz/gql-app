from graphene import ObjectType, Int, String, Field, List as GrapheneList
from typing import Any


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = GrapheneList(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root: Any, info: Any) -> Any:
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root: Any, info: Any) -> Any:
        return root.employer
