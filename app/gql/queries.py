from graphene import ObjectType, List as GrapheneList
from typing import Any, List, Optional
from app.db.database import Session
from app.db.models import Job, Employer
from app.gql.types import JobObject, EmployerObject
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = GrapheneList(JobObject)
    employers = GrapheneList(EmployerObject)

    @staticmethod
    def resolve_jobs(root: Optional[Any], info: Any) -> List[Job]:
        return Session().query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_employers(root: Optional[Any], info: Any) -> List[Employer]:
        return Session().query(Employer).all()
