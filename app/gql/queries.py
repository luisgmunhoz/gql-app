from graphene import ObjectType, List as GrapheneList
from typing import Any, Dict, List, Optional
from app.gql.types import JobObject, EmployerObject
from app.db.data import employers_data, jobs_data


class Query(ObjectType):
    jobs = GrapheneList(JobObject)
    employers = GrapheneList(EmployerObject)

    @staticmethod
    def resolve_jobs(root: Optional[Any], info: Any) -> List[Dict[str, Any]]:
        return jobs_data

    @staticmethod
    def resolve_employers(root: Optional[Any], info: Any) -> List[Dict[str, Any]]:
        return employers_data
