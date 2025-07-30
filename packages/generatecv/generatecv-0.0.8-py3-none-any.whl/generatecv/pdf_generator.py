"""PDF Generator for CV Builder.

This module handles the generation of PDF files from CV data.
"""

import os
from collections.abc import Callable, Iterable  # Added cast
from pathlib import Path
from typing import Any, cast

from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import (
    Flowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
)

from generatecv.models import (
    CV,
    Certificate,
    CompanyExperience,
    Education,
    Language,
    PersonalInfo,
    Project,
    Reference,
    Skill,
)  # Updated import
from generatecv.parser.yaml import parse_yaml_file, validate_cv_data

from .styles import get_style


class _PDFGenerator:
    """Class to generate PDF files from CV data."""

    def __init__(
        self,
        output_path: str,
        cv_data: CV,
        style: str = "classic",
        page_size: str = "A4",
    ):
        """Initialize the PDF generator with CV data.

        Args:
            output_path (str): Path to save the generated PDF.
            cv_data (CV): CV data object containing all the information.
            style (str): Style of the CV (default is "classic").
            page_size (str): Size of the PDF page (default is "A4").
        """
        self.output_path = Path(output_path)
        self.cv_data = cv_data
        # applying the style
        try:
            self.cv_style = get_style(style)
            self.styles = self.cv_style.get_styles()
        except ValueError as e:
            print(f"Error applying style: {e}")
            self.cv_style = get_style("classic")
            self.styles = self.cv_style.get_styles()

        # Set page size
        if page_size.lower() == "a4":
            self.page_size = A4
        elif page_size.lower() == "letter":
            self.page_size = letter
        else:
            raise ValueError(
                f"Invalid page size: {page_size}. Choose 'A4' or 'letter'."
            )

        os.makedirs(self.output_path.parent, exist_ok=True)

        self.doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Elements to be added to the PDF
        self.elements: list[Flowable] = []

    def generate(self) -> Path:
        """Generate the PDF document."""
        # Add all sections
        self._add_content()

        # Build the document
        self.doc.build(self.elements)

        return self.output_path

    def _add_content(self) -> None:
        """Add all CV content to the PDF."""
        # Add personal info
        personal_info = self.cv_data.personal_info
        if personal_info:
            self._add_personal_info(personal_info)

        # Add experience
        experience = self.cv_data.experience
        if experience:
            self._add_section("Experience", experience, self._format_company_experience)

        # Add education
        education = self.cv_data.education
        if education:
            self._add_section("Education", education, self._format_education)

        # Add skills
        skills = self.cv_data.skills
        if skills:
            self._add_skills(skills)

        # Add projects
        projects = self.cv_data.projects
        if projects:
            self._add_section("Projects", projects, self._format_project)

        # Add certifications
        certifications = self.cv_data.certifications
        if certifications:
            self._add_section(
                "Certifications", certifications, self._format_certificate
            )

        # Add languages
        languages = self.cv_data.languages
        if languages:
            self._add_section("Languages", languages, self._format_language)

        # Add references
        references = self.cv_data.references
        if references:
            self._add_section("References", references, self._format_reference)

        # Add publications
        publications = self.cv_data.publications
        if publications:
            self._add_simple_list_section("Publications", publications)

        # Add awards
        awards = self.cv_data.awards
        if awards:
            self._add_simple_list_section("Awards", awards)

        # Add interests
        interests = self.cv_data.interests
        if interests:
            self._add_simple_list_section("Interests", interests)

        # Add custom sections
        custom_sections = self.cv_data.custom_sections
        if custom_sections:
            self._add_custom_sections(custom_sections)

    def _add_personal_info(self, personal_info: PersonalInfo) -> None:
        """Add personal information to the PDF."""
        # Add name
        if personal_info.name:
            self.elements.append(Paragraph(personal_info.name, self.styles["Name"]))

        # Add title if present
        if personal_info.title:
            self.elements.append(
                Paragraph(
                    personal_info.title,
                    self.styles.get("ContactInfo", self.styles["Normal"]),
                )
            )  # Use ContactInfo or fallback to Normal

        # Combine contact information
        contact_parts: list[str] = []
        if personal_info.email:
            contact_parts.append(f"Email: {personal_info.email}")
        if personal_info.phone:
            contact_parts.append(f"Phone: {personal_info.phone}")
        if personal_info.location:
            contact_parts.append(f"Location: {personal_info.location}")
        if personal_info.website:
            contact_parts.append(f"Website: {personal_info.website}")
        if personal_info.linkedin:
            contact_parts.append(f"LinkedIn: {personal_info.linkedin}")

        contact_info = " | ".join(contact_parts)
        self.elements.append(Paragraph(contact_info, self.styles["ContactInfo"]))

        if personal_info.summary:
            self.elements.append(
                Paragraph("Summary", self.styles["SectionHeading"])
            )  # Add a section heading for summary
            self.elements.append(
                Paragraph(personal_info.summary, self.styles["Normal"])
            )
        # Add a spacer after personal info

    def _add_section(
        self, title: str, items: Iterable[Any], formatter: Callable[[Any], None]
    ) -> None:
        """Add a section to the PDF with formatted items."""
        self.elements.append(Paragraph(title, self.styles["SectionHeading"]))

        for item in items:
            formatter(item)

    def _format_company_experience(self, company_exp: CompanyExperience) -> None:
        """Format a company experience entry, including all its roles."""
        # Company name and optional location
        company_text = company_exp.company
        if company_exp.location:
            company_text += f" ({company_exp.location})"
        self.elements.append(
            Paragraph(company_text, self.styles["ExperienceTitle"])
        )  # Style for company name

        for role in company_exp.roles:
            # Role title
            self.elements.append(
                Paragraph(
                    role.title,
                    self.styles.get("RoleTitle", self.styles["ExperienceDetails"]),
                )
            )  # Use RoleTitle or fallback to ExperienceDetails

            # Dates for the role
            dates = f"{role.start_date} - {role.end_date or 'Present'}"
            if role.location:  # Role-specific location
                dates += f" | {role.location}"
            self.elements.append(Paragraph(dates, self.styles["ExperienceDetails"]))

            # Description for the role
            if role.description:
                self.elements.append(Paragraph(role.description, self.styles["Normal"]))

            # Achievements for the role
            if role.achievements:
                items: list[Flowable] = []
                for achievement in role.achievements:
                    items.append(
                        cast(
                            "Flowable",
                            ListItem(Paragraph(achievement, self.styles["Normal"])),
                        )
                    )  # Cast ListItem to Flowable
                self.elements.append(
                    ListFlowable(
                        items,
                        bulletType="bullet",
                        leftIndent=12,
                        bulletFontName="Helvetica-Bold",
                        bulletFontSize=self.styles["Normal"].fontSize,
                    )
                )

    def _format_education(self, education: Education) -> None:
        """Format an education entry."""
        # Degree and institution
        degree_text = f"{education.degree} - {education.institution}"
        self.elements.append(
            Paragraph(degree_text, self.styles["ExperienceTitle"])
        )  # Reusing ExperienceTitle for consistency

        # Dates
        dates = f"{education.start_date} - {education.end_date or 'Present'}"
        if education.location:
            dates += f" | {education.location}"
        self.elements.append(Paragraph(dates, self.styles["ExperienceDetails"]))

        # GPA/Details
        if education.gpa:
            self.elements.append(
                Paragraph(f"GPA: {education.gpa}", self.styles["Normal"])
            )
        if education.details:
            self.elements.append(Paragraph(education.details, self.styles["Normal"]))

    def _add_skills(self, skills: Iterable[Skill]) -> None:
        """Add skills section to the PDF."""
        self.elements.append(Paragraph("Skills", self.styles["SectionHeading"]))

        print("Skills:")
        for skill_item in skills:
            # Skill category (e.g., Programming Languages)
            self.elements.append(
                Paragraph(
                    skill_item.category,
                    self.styles.get("ExperienceTitle", self.styles["Normal"]),
                )
            )  # Reusing ExperienceTitle or similar

            print("Category:", skill_item)
            print(skill_item.category)
            # List of skills in that category
            self.elements.append(Paragraph((skill_item.name), self.styles["Normal"]))

    def _format_project(self, project: Project) -> None:
        """Format a project entry."""
        # Project name and optional link
        project_name_text = project.name
        if project.link:
            project_name_text += f" (Link: {project.link})"  # Basic link display
        self.elements.append(
            Paragraph(project_name_text, self.styles["ExperienceTitle"])
        )

        # Dates
        if project.start_date and project.end_date:
            dates = f"{project.start_date} - {project.end_date or 'Ongoing'}"
            self.elements.append(Paragraph(dates, self.styles["ExperienceDetails"]))

        # Description
        if project.description:
            self.elements.append(Paragraph(project.description, self.styles["Normal"]))

        # Technologies used
        if project.technologies:
            tech_text = "Technologies: " + ", ".join(project.technologies)
            self.elements.append(Paragraph(tech_text, self.styles["Normal"]))

        # Achievements/Key Features
        if project.achievements:
            items: list[Flowable] = []
            for achievement in project.achievements:
                items.append(
                    cast(
                        "Flowable",
                        ListItem(Paragraph(achievement, self.styles["Normal"])),
                    )
                )  # Cast ListItem to Flowable
            self.elements.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    leftIndent=12,
                    bulletFontName="Helvetica-Bold",
                    bulletFontSize=self.styles["Normal"].fontSize,
                )
            )

    def _format_certificate(self, certificate: Certificate) -> None:
        """Format a certificate entry."""
        cert_name_text = certificate.name
        if certificate.issuer:
            cert_name_text += f" - {certificate.issuer}"
        self.elements.append(
            Paragraph(
                cert_name_text,
                self.styles.get("ExperienceTitle", self.styles["Normal"]),
            )
        )  # Reusing ExperienceTitle

        if certificate.date:
            self.elements.append(
                Paragraph(
                    f"Date: {certificate.date}",
                    self.styles.get("ExperienceDetails", self.styles["Normal"]),
                )
            )
        if certificate.description:
            self.elements.append(
                Paragraph(certificate.description, self.styles["Normal"])
            )
        if certificate.link:
            self.elements.append(
                Paragraph(f"Link: {certificate.link}", self.styles["Normal"])
            )

    def _format_language(self, lang: Language) -> None:
        """Format a language entry."""
        lang_text = f"{lang.name}: {lang.proficiency}"
        self.elements.append(Paragraph(lang_text, self.styles["Normal"]))

    def _format_reference(self, reference: Reference) -> None:
        """Format a reference entry."""
        self.elements.append(
            Paragraph(
                reference.name,
                self.styles.get("ExperienceTitle", self.styles["Normal"]),
            )
        )  # Reusing ExperienceTitle
        if reference.position:
            self.elements.append(
                Paragraph(
                    reference.position,
                    self.styles.get("ExperienceDetails", self.styles["Normal"]),
                )
            )
        if reference.company:
            self.elements.append(
                Paragraph(
                    reference.company,
                    self.styles.get("ExperienceDetails", self.styles["Normal"]),
                )
            )
        if reference.contact:
            self.elements.append(
                Paragraph(f"Contact: {reference.contact}", self.styles["Normal"])
            )
        if reference.relation:
            self.elements.append(
                Paragraph(f"Relation: {reference.relation}", self.styles["Normal"])
            )

    def _add_simple_list_section(self, title: str, items_list: Iterable[str]) -> None:
        """Add a section with a simple list of strings."""
        self.elements.append(Paragraph(title, self.styles["SectionHeading"]))
        items: list[Flowable] = []
        for item_text in items_list:
            items.append(
                cast("Flowable", ListItem(Paragraph(item_text, self.styles["Normal"])))
            )
        if (
            items
        ):  # Only add ListFlowable if there are items to avoid errors with empty lists
            self.elements.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    leftIndent=12,
                    bulletFontName="Helvetica-Bold",
                    bulletFontSize=self.styles["Normal"].fontSize,
                )
            )

    def _add_custom_sections(self, custom_sections: dict[str, str | list[str]]) -> None:
        """Add custom sections to the PDF."""
        for title, content in custom_sections.items():
            self.elements.append(Paragraph(title, self.styles["SectionHeading"]))
            if isinstance(content, str):
                self.elements.append(Paragraph(content, self.styles["Normal"]))
            elif isinstance(content, list):
                items: list[Flowable] = []
                for item_text in content:  # Assuming content is List[str] as per model
                    items.append(
                        cast(
                            "Flowable",
                            ListItem(Paragraph(str(item_text), self.styles["Normal"])),
                        )
                    )  # Ensure item_text is str
                if items:  # Only add ListFlowable if there are items
                    self.elements.append(
                        ListFlowable(
                            items,
                            bulletType="bullet",
                            leftIndent=12,
                            bulletFontName="Helvetica-Bold",
                            bulletFontSize=self.styles["Normal"].fontSize,
                        )
                    )


def generatepdf(
    cv_data: CV, output_path: str, style: str = "classic", page_size: str = "A4"
) -> str:
    """Generate a PDF CV from the provided data.

    Args:
        cv_data: CV model containing the CV data
        output_path: Path where the PDF will be saved
        style: Style name for the CV (e.g., 'classic', 'modern', 'minimal')
        page_size: Size of the page ('A4' or 'letter')

    Returns:
        Path to the generated PDF file
    """
    generator = _PDFGenerator(output_path, cv_data, style, page_size)
    return str(generator.generate())


def yamltocv(
    output_path: str, yaml_path: str, style: str = "classic", page_size: str = "A4"
) -> CV:
    """Convert YAML file to CV object.

    Args:
        output_path: Path where the PDF will be saved.
            If None, a default path is generated.
        style: Style name for the CV (e.g., 'classic', 'modern', 'minimal')
        page_size: Size of the page ('A4' or 'letter')
        yaml_path: Path to the YAML file containing the CV data

    Returns:
        CV object created from the YAML data
    """  # Add AI summary generation logic here

    yaml_data = parse_yaml_file(yaml_path)
    cv_data = validate_cv_data(yaml_data)

    return cv_data
