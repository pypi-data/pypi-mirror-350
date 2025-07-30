from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Literal, TypedDict

import yaml
from pydantic import BaseModel, EmailStr, Field, field_validator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class PersonalInfo(BaseModel):
    """Personal information for CV."""

    name: str
    email: EmailStr
    phone: str
    address: str | None = None
    website: str | None = None
    linkedin: str | None = None
    github: str | None = None


class EducationEntry(BaseModel):
    """Educational experience entry."""

    institution: str
    degree: str
    field: str
    start_date: str
    end_date: str | None = None
    gpa: float | None = None
    achievements: list[str] = Field(default_factory=list)

    # Define GPA range constants
    MAX_GPA: ClassVar[float] = 4.0
    MIN_GPA: ClassVar[float] = 0.0

    @field_validator("gpa")
    @classmethod
    def validate_gpa(cls, v: float | None) -> float | None:
        """Validate GPA is in a reasonable range."""
        if v is not None and (v < cls.MIN_GPA or v > cls.MAX_GPA):
            raise ValueError(f"GPA must be between {cls.MIN_GPA} and {cls.MAX_GPA}")
        return v


class ExperienceEntry(BaseModel):
    """Work experience entry."""

    company: str
    position: str
    start_date: str
    end_date: str | None = None
    location: str | None = None
    description: str | None = None
    achievements: list[str] = Field(default_factory=list)


class SkillCategory(BaseModel):
    """Skill category with list of skills."""

    category: str
    skills: list[str]


class CVData(BaseModel):
    """Complete CV data structure."""

    personal_info: PersonalInfo
    summary: str | None = None
    education: list[EducationEntry] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    skills: list[SkillCategory] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)


class CVTemplate(TypedDict):
    """Configuration for CV template styling."""

    primary_color: str
    secondary_color: str
    font_name: str
    header_size: int
    body_size: int
    margin: int


class CVGenerator:
    """Generator for CV documents."""

    def __init__(
        self,
        template: CVTemplate | None = None,
        output_format: Literal["pdf", "html"] = "pdf",
    ) -> None:
        """
        Initialize CV Generator.

        Args:
            template: Optional styling configuration for the CV
            output_format: Format to generate the CV in (pdf or html)
        """
        self.template = template or self._default_template()
        self.output_format = output_format
        self.styles = self._create_styles()

    @staticmethod
    def _default_template() -> CVTemplate:
        """Create default template configuration."""
        return {
            "primary_color": "#2C3E50",
            "secondary_color": "#3498DB",
            "font_name": "Helvetica",
            "header_size": 14,
            "body_size": 10,
            "margin": 72,  # 1 inch in points
        }

    def _create_styles(self) -> dict[str, ParagraphStyle]:
        """Create paragraph styles for the document."""
        styles = getSampleStyleSheet()

        # Create custom styles based on template
        custom_styles = {
            "Name": ParagraphStyle(
                "Name",
                parent=styles["Heading1"],
                fontName=self.template["font_name"],
                fontSize=self.template["header_size"] + 4,
                textColor=colors.HexColor(self.template["primary_color"]),
            ),
            "Section": ParagraphStyle(
                "Section",
                parent=styles["Heading2"],
                fontName=self.template["font_name"],
                fontSize=self.template["header_size"],
                textColor=colors.HexColor(self.template["primary_color"]),
            ),
            "SubSection": ParagraphStyle(
                "SubSection",
                parent=styles["Heading3"],
                fontName=self.template["font_name"],
                fontSize=self.template["header_size"] - 2,
                textColor=colors.HexColor(self.template["secondary_color"]),
            ),
            "Normal": ParagraphStyle(
                "Normal",
                parent=styles["Normal"],
                fontName=self.template["font_name"],
                fontSize=self.template["body_size"],
            ),
        }
        return custom_styles

    def load_data_from_yaml(self, yaml_path: str | Path) -> CVData:
        """
        Load CV data from YAML file.

        Args:
            yaml_path: Path to the YAML file containing CV data

        Returns:
            Parsed and validated CV data
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(path, encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)

        # Parse and validate using Pydantic
        return CVData.model_validate(yaml_data)

    def generate(self, cv_data: CVData, output_path: str | Path) -> Path:
        """
        Generate CV document.

        Args:
            cv_data: CV data to include in the document
            output_path: Path where the document will be saved

        Returns:
            Path to the generated document
        """
        output_path = Path(output_path)

        if self.output_format == "pdf":
            return self._generate_pdf(cv_data, output_path)
        elif self.output_format == "html":
            return self._generate_html(cv_data, output_path)
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")

    def _generate_pdf(self, cv_data: CVData, output_path: Path) -> Path:
        """Generate PDF version of the CV."""
        # Create the document with the specified page size and margins
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=self.template["margin"],
            rightMargin=self.template["margin"],
            topMargin=self.template["margin"],
            bottomMargin=self.template["margin"],
        )

        # Create the document contents
        elements: list[Any] = []

        # Add personal information
        elements.append(Paragraph(cv_data.personal_info.name, self.styles["Name"]))

        # Contact information as a table
        contact_info = []
        if cv_data.personal_info.email:
            contact_info.append(f"Email: {cv_data.personal_info.email}")
        if cv_data.personal_info.phone:
            contact_info.append(f"Phone: {cv_data.personal_info.phone}")
        if cv_data.personal_info.address:
            contact_info.append(f"Address: {cv_data.personal_info.address}")

        for info in contact_info:
            elements.append(Paragraph(info, self.styles["Normal"]))

        elements.append(Spacer(1, 12))

        # Add summary if available
        if cv_data.summary:
            elements.append(Paragraph("Summary", self.styles["Section"]))
            elements.append(Paragraph(cv_data.summary, self.styles["Normal"]))
            elements.append(Spacer(1, 12))

        # Add experience section
        if cv_data.experience:
            elements.append(
                Paragraph("Professional Experience", self.styles["Section"])
            )
            for exp in cv_data.experience:
                date_range = f"{exp.start_date} - {exp.end_date or 'Present'}"
                elements.append(
                    Paragraph(
                        f"{exp.position} at {exp.company}", self.styles["SubSection"]
                    )
                )
                elements.append(Paragraph(date_range, self.styles["Normal"]))
                if exp.description:
                    elements.append(Paragraph(exp.description, self.styles["Normal"]))

                if exp.achievements:
                    for achievement in exp.achievements:
                        elements.append(
                            Paragraph(f"• {achievement}", self.styles["Normal"])
                        )

                elements.append(Spacer(1, 10))

        # Build the document
        doc.build(elements)
        return output_path

    def _generate_html(self, cv_data: CVData, output_path: Path) -> Path:
        """Generate HTML version of the CV."""
        # Simple HTML generation for demonstration
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{cv_data.personal_info.name} - CV</title>
    <style>
        body {{ 
            font-family: {self.template["font_name"]}, Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
        }}
        h1 {{ color: {self.template["primary_color"]}; }}
        h2 {{ color: {self.template["primary_color"]}; border-bottom: 1px solid #eee; }}
        h3 {{ color: {self.template["secondary_color"]}; }}
    </style>
</head>
<body>
    <h1>{cv_data.personal_info.name}</h1>
    <p>Email: {cv_data.personal_info.email}</p>
    <p>Phone: {cv_data.personal_info.phone}</p>
"""

        if cv_data.summary:
            html_content += f"<h2>Summary</h2>\n<p>{cv_data.summary}</p>\n"

        if cv_data.experience:
            html_content += "<h2>Professional Experience</h2>\n"
            for exp in cv_data.experience:
                date_range = f"{exp.start_date} - {exp.end_date or 'Present'}"
                html_content += f"<h3>{exp.position} at {exp.company}</h3>\n"
                html_content += f"<p>{date_range}</p>\n"

                if exp.description:
                    html_content += f"<p>{exp.description}</p>\n"

                if exp.achievements:
                    html_content += "<ul>\n"
                    for achievement in exp.achievements:
                        html_content += f"<li>{achievement}</li>\n"
                    html_content += "</ul>\n"

        html_content += "</body>\n</html>"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path


def create_sample_cv() -> CVData:
    """Create a sample CV data structure for testing."""
    return CVData(
        personal_info=PersonalInfo(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1 (555) 123-4567",
            address="123 Main St, Anytown, AN 12345",
        ),
        summary="Experienced software engineer with a passion for building "
        "scalable applications.",
        experience=[
            ExperienceEntry(
                company="Tech Solutions Inc.",
                position="Senior Software Engineer",
                start_date="2020-01",
                end_date="Present",
                location="San Francisco, CA",
                description="Lead developer for cloud-based applications.",
                achievements=[
                    "Improved system performance by 40%",
                    "Implemented CI/CD pipeline reducing deployment time by 60%",
                    "Mentored junior developers",
                ],
            ),
            ExperienceEntry(
                company="StartUp Innovations",
                position="Software Developer",
                start_date="2017-06",
                end_date="2019-12",
                location="Boston, MA",
                description="Developed front-end and back-end features "
                "for SaaS platform.",
                achievements=[
                    "Designed and implemented RESTful API",
                    "Reduced page load time by 30%",
                ],
            ),
        ],
        education=[
            EducationEntry(
                institution="University of Technology",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date="2013",
                end_date="2017",
                gpa=3.8,
                achievements=[
                    "Dean's List",
                    "Senior Thesis: Machine Learning Applications",
                ],
            ),
        ],
        skills=[
            SkillCategory(
                category="Programming Languages",
                skills=["Python", "JavaScript", "TypeScript", "Java", "C++"],
            ),
            SkillCategory(
                category="Frameworks & Tools",
                skills=["Django", "React", "Docker", "Kubernetes", "AWS"],
            ),
        ],
        languages=["English (Native)", "Spanish (Intermediate)"],
        interests=["Open Source Contributing", "Hiking", "Photography"],
    )
