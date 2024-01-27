from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employer(Base):  # type: ignore[valid-type, misc]
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)
    jobs = relationship("Job", back_populates="employer")


class Job(Base):  # type: ignore[valid-type, misc]
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")
