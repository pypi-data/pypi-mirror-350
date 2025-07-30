from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from generatecv.cv_generator import (
    CVData,
    CVGenerator,
    CVTemplate,
    EducationEntry,
    PersonalInfo,
    create_sample_cv,
)


@pytest.fixture
def sample_cv_data() -> CVData:
    """Fixture providing sample CV data for testing."""
    return create_sample_cv()


@pytest.fixture
def sample_yaml_file(sample_cv_data: CVData, tmp_path: Path) -> Path:
    """Create a sample YAML file from CV data."""
    yaml_path = tmp_path / "sample_cv.yaml"

    # Convert to dict and save as YAML
    cv_dict = sample_cv_data.model_dump()
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(cv_dict, f)

    return yaml_path


@pytest.fixture
def custom_template() -> CVTemplate:
    """Fixture providing a custom CV template."""
    return {
        "primary_color": "#1A237E",
        "secondary_color": "#4CAF50",
        "font_name": "Times-Roman",
        "header_size": 16,
        "body_size": 11,
        "margin": 54,
    }


class TestCVGenerator:
    """Test suite for CVGenerator class."""

    def test_init_default_template(self) -> None:
        """Test initializing with default template."""
        generator = CVGenerator()
        assert generator.template["primary_color"] == "#2C3E50"
        assert generator.template["font_name"] == "Helvetica"
        assert generator.output_format == "pdf"

    def test_init_custom_template(self, custom_template: CVTemplate) -> None:
        """Test initializing with custom template."""
        generator = CVGenerator(template=custom_template, output_format="html")
        assert generator.template == custom_template
        assert generator.output_format == "html"

    def test_load_data_from_yaml(self, sample_yaml_file: Path) -> None:
        """Test loading CV data from YAML file."""
        generator = CVGenerator()
        cv_data = generator.load_data_from_yaml(sample_yaml_file)

        assert isinstance(cv_data, CVData)
        assert cv_data.personal_info.name == "Jane Smith"
        assert len(cv_data.experience) == 2
        assert cv_data.experience[0].company == "Tech Solutions Inc."

    def test_load_data_nonexistent_file(self) -> None:
        """Test loading from a non-existent file raises error."""
        generator = CVGenerator()
        with pytest.raises(FileNotFoundError):
            generator.load_data_from_yaml("nonexistent_file.yaml")

    def test_generate_pdf(self, sample_cv_data: CVData, tmp_path: Path) -> None:
        """Test generating PDF output."""
        generator = CVGenerator(output_format="pdf")
        output_path = tmp_path / "output.pdf"

        result_path = generator.generate(sample_cv_data, output_path)

        assert result_path.exists()
        assert result_path.suffix == ".pdf"
        # Basic check that the file is not empty
        assert result_path.stat().st_size > 0

    def test_generate_html(self, sample_cv_data: CVData, tmp_path: Path) -> None:
        """Test generating HTML output."""
        generator = CVGenerator(output_format="html")
        output_path = tmp_path / "output.html"

        result_path = generator.generate(sample_cv_data, output_path)

        assert result_path.exists()
        assert result_path.suffix == ".html"

        # Check content of HTML file
        content = result_path.read_text(encoding="utf-8")
        assert f"<title>{sample_cv_data.personal_info.name} - CV</title>" in content
        assert f"<h1>{sample_cv_data.personal_info.name}</h1>" in content
        assert "Tech Solutions Inc." in content

    def test_invalid_output_format(
        self, sample_cv_data: CVData, tmp_path: Path
    ) -> None:
        """Test error when invalid output format is specified."""
        # We need to use type ignore here because mypy correctly identifies this as an
        # error
        generator = CVGenerator(output_format="invalid")  # type: ignore
        output_path = tmp_path / "output.txt"

        with pytest.raises(ValueError, match="Unsupported output format"):
            generator.generate(sample_cv_data, output_path)


class TestCVDataValidation:
    """Test validation of CV data structures."""

    def test_personal_info_validation(self) -> None:
        """Test validation of PersonalInfo."""
        # Valid
        info = PersonalInfo(
            name="John Doe", email="john@example.com", phone="+1234567890"
        )
        assert info.name == "John Doe"

        # Invalid email
        with pytest.raises(ValidationError):
            PersonalInfo(name="John Doe", email="invalid-email", phone="+1234567890")

    def test_education_entry_validation(self) -> None:
        """Test validation of EducationEntry."""
        # Valid
        entry = EducationEntry(
            institution="University",
            degree="BS",
            field="Computer Science",
            start_date="2018",
            gpa=3.5,
        )
        assert entry.gpa == 3.5

        # Invalid GPA
        with pytest.raises(ValidationError):
            EducationEntry(
                institution="University",
                degree="BS",
                field="Computer Science",
                start_date="2018",
                gpa=5.0,  # Invalid: must be <= 4.0
            )

    def test_create_sample_cv(self) -> None:
        """Test the create_sample_cv function."""
        cv = create_sample_cv()
        assert isinstance(cv, CVData)
        assert cv.personal_info.name == "Jane Smith"
        assert len(cv.experience) == 2
        assert len(cv.education) == 1
        assert len(cv.skills) == 2
