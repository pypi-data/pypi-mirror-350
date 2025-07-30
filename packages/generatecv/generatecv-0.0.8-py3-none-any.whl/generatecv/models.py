"""CV Builder data models using Pydantic.

This module defines the data models for CV builder using Pydantic for validation.
"""

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class PersonalInfo(BaseModel):
    """Model for personal information section."""

    name: str = Field(description="Full name of the individual.")
    email: EmailStr = Field(description="Primary email address.")
    phone: str | None = Field(
        default=None, description="Contact phone number (e.g., +1-555-123-4567)."
    )
    location: str | None = Field(
        default=None,
        description="Current city and country of residence (e.g., San Francisco, CA).",
    )
    website: HttpUrl | None = Field(
        default=None, description="Personal website or portfolio URL."
    )
    linkedin: HttpUrl | None = Field(default=None, description="LinkedIn profile URL.")
    github: HttpUrl | None = Field(default=None, description="GitHub profile URL.")
    summary: str | None = Field(
        default=None, description="A brief professional summary or objective statement."
    )
    title: str | None = Field(
        default=None,
        description="Current job title or professional headline "
        "(e.g., Senior Software Engineer).",
    )


class Education(BaseModel):
    """Model for education entries."""

    institution: str = Field(description="Name of the educational institution.")
    degree: str = Field(
        description="Degree obtained (e.g., Bachelor of Science in Computer Science)."
    )
    start_date: str = Field(
        description="Start date of education (e.g., YYYY-MM or Sep 2018)."
    )
    end_date: str | None = Field(
        default=None,
        description="End date of education (e.g., YYYY-MM, Jun 2022, or 'Present').",
    )
    location: str | None = Field(
        default=None, description="Location of the institution (e.g., Stanford, CA)."
    )
    details: str | None = Field(
        default=None, description="Additional details, such as thesis title or honors."
    )
    gpa: str | None = Field(
        default=None, description="Grade Point Average (e.g., 3.8/4.0)."
    )


class Experience(BaseModel):
    """Model for professional experience for backwards compatibility with tests."""

    company: str = Field(description="Name of the company or organization.")
    title: str = Field(description="Job title or position held.")
    start_date: str = Field(
        description="Start date of this role (e.g., YYYY-MM or Jun 2020)."
    )
    end_date: str | None = Field(
        default=None,
        description="End date of this role (e.g., YYYY-MM, Aug 2022, or 'Present').",
    )
    description: str | None = Field(
        default=None, description="A brief overview of responsibilities and the role."
    )
    achievements: list[str] | None = Field(
        default=None,
        description="List of key achievements or accomplishments for this role.",
    )
    location: str | None = Field(
        default=None, description="Location where this role was performed."
    )


class Role(BaseModel):
    """Model for a specific role within a company."""

    title: str = Field(description="Job title or position held.")
    start_date: str = Field(
        description="Start date of this role (e.g., YYYY-MM or Jun 2020)."
    )
    end_date: str | None = Field(
        default=None,
        description="End date of this role (e.g., YYYY-MM, Aug 2022, or 'Present').",
    )
    location: str | None = Field(
        default=None,
        description="Location where this role was performed "
        "(if different from company's main location).",
    )
    description: str | None = Field(
        default=None, description="A brief overview of responsibilities and the role."
    )
    achievements: list[str] | None = Field(
        default=None,
        description="List of key achievements or accomplishments for this role.",
    )


class CompanyExperience(BaseModel):
    """Model for professional experience at a single company with multiple roles.

    This model allows grouping multiple role entries under a single company.
    """

    company: str = Field(description="Name of the company or organization.")
    location: str | None = Field(
        default=None, description="Main location of the company (e.g., New York, NY)."
    )  # Company-level location
    roles: list[Role] = Field(description="List of roles held at this company.")


class Skill(BaseModel):
    """Model for skills section."""

    category: str = Field(
        description="Category of the skill (e.g., Languages, Tools, Frameworks)."
    )
    name: str = Field(description="Name of the skill (e.g., Python, Docker, React).")


class Project(BaseModel):
    """Model for projects section."""

    name: str = Field(description="Name of the project.")
    description: str | None = Field(
        default=None, description="A brief description of the project."
    )
    technologies: list[str] | None = Field(
        default=None, description="List of technologies used in the project."
    )
    link: HttpUrl | None = Field(
        default=None,
        description="URL to the project (e.g., GitHub repository or live demo).",
    )
    start_date: str | None = Field(
        default=None,
        description="Start date of the project (e.g., YYYY-MM or Jan 2021).",
    )
    end_date: str | None = Field(
        default=None,
        description="End date of the project (e.g., YYYY-MM, Mar 2021, or 'Ongoing').",
    )
    achievements: list[str] | None = Field(
        default=None, description="List of key achievements or outcomes of the project."
    )


class Certificate(BaseModel):
    """Model for certifications section."""

    name: str = Field(description="Name of the certificate.")
    issuer: str = Field(description="Issuing organization or authority.")
    date: str | None = Field(
        default=None, description="Date of certification (e.g., YYYY-MM or Oct 2020)."
    )
    description: str | None = Field(
        default=None, description="A brief description of the certification."
    )
    link: HttpUrl | None = Field(
        default=None, description="URL to the certificate or verification page."
    )


class Language(BaseModel):
    """Model for language proficiency."""

    name: str = Field(description="Name of the language (e.g., English, Spanish).")
    proficiency: str = Field(
        description="Proficiency level (e.g., Native, Fluent, Conversational)."
    )


class Reference(BaseModel):
    """Model for professional references."""

    name: str = Field(description="Name of the reference.")
    position: str = Field(description="Position or title of the reference.")
    company: str = Field(description="Company or organization of the reference.")
    contact: str | None = Field(
        default=None,
        description="Contact information (e.g., email or phone). "
        "'Available upon request' is also valid.",
    )
    relation: str | None = Field(
        default=None,
        description="Relationship to the individual (e.g., Former Manager, Colleague).",
    )


class CV(BaseModel):
    """Main CV model that contains all sections."""

    personal_info: PersonalInfo = Field(
        description="Personal information of the individual."
    )
    education: list[Education] = Field(
        description="List of educational qualifications."
    )
    experience: list[CompanyExperience] = Field(
        description="List of professional experiences, grouped by company."
    )  # Updated here
    skills: list[Skill] | None = Field(
        default=None, description="List of skills categorized by area."
    )
    projects: list[Project] | None = Field(
        default=None, description="List of personal or professional projects."
    )
    certifications: list[Certificate] | None = Field(
        default=None, description="List of certifications obtained."
    )
    languages: list[Language] | None = Field(
        default=None, description="List of languages spoken and their proficiency."
    )
    references: list[Reference] | None = Field(
        default=None, description="List of professional references."
    )
    publications: list[str] | None = Field(
        default=None, description="List of publications, if any."
    )
    awards: list[str] | None = Field(
        default=None, description="List of awards and honors received."
    )
    interests: list[str] | None = Field(
        default=None, description="List of personal interests or hobbies."
    )
    custom_sections: dict[str, str | list[str]] | None = Field(
        default=None,
        description="Allows for adding custom sections to the CV as key-value pairs, "
        "where value can be a string or list of strings.",
    )
