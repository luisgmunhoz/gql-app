import pytest
from main import JobObject, employers_data


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
        with pytest.raises(IndexError):
            self.job.resolve_employer(root, None)
