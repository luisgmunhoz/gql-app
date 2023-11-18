from main import JobObject, EmployerObject, employers_data, jobs_data


class TestEmployerObject:
    def setup_method(self) -> None:
        self.employer = EmployerObject()

    def test_attributes(self) -> None:
        assert hasattr(self.employer, "id")
        assert hasattr(self.employer, "name")
        assert hasattr(self.employer, "contact_email")
        assert hasattr(self.employer, "industry")
        assert hasattr(self.employer, "jobs")

    def test_resolve_jobs(self) -> None:
        root = {"id": 1}
        expected_jobs = [job for job in jobs_data if job["employer_id"] == 1]
        assert self.employer.resolve_jobs(root, None) == expected_jobs

        root = {"id": 999}
        assert self.employer.resolve_jobs(root, None) == []


class TestJobObject:
    def setup_method(self) -> None:
        self.job = JobObject()

    def test_attributes(self) -> None:
        assert hasattr(self.job, "id")
        assert hasattr(self.job, "title")
        assert hasattr(self.job, "description")
        assert hasattr(self.job, "employer_id")
        assert hasattr(self.job, "employer")

    def test_resolve_employer(self) -> None:
        root = {"employer_id": 1}
        expected_employer = next(
            (employer for employer in employers_data if employer["id"] == 1), None
        )
        assert self.job.resolve_employer(root, None) == expected_employer

        root = {"employer_id": 999}
        assert self.job.resolve_employer(root, None) is None
