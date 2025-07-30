from __future__ import annotations
import datetime
from typing import Any, Literal
import re

from pydantic import BaseModel, Field, computed_field

from cv_model import consts

Iso8601 = datetime.date | Literal["Present"]

State = str  # two character abbreviation for US states, e.g. CA, NY
AnyUrl = str  # URL as per RFC 3986

DATE_DESCRIPTION = "Date in ISO 8601 format, e.g. YYYY-MM-DD or `Present`"
HIGHLIGHT_DESCRIPTION = (
    "Specify multiple highlights. e.g. `Implemented a new feature`"
    + " or `Worked on a new project`"
)


def build_description(description: str) -> Any:
    return {"description": description}


# support bold, italic, code, link
def markdown_to_typst(text: str) -> str:
    """
    Convert markdown syntax to typst syntax.

    Args:
        text: A string containing markdown syntax

    Returns:
        A string with markdown syntax converted to typst syntax
    """
    # Handle links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'#link("\2")[\1]', text)

    # Handle bold and italic combined: ***text*** -> *_text_*
    text = re.sub(r"\*\*\*([^*]+?)\*\*\*", r"__COMBINED_START__\1__COMBINED_END__", text)

    # Handle bold with ** (using a temporary marker that won't be affected by other replacements)
    text = re.sub(r"\*\*([^*]+?)\*\*", r"__BOLD_START__\1__BOLD_END__", text)

    # Handle italic with *
    text = re.sub(r"\*([^*]+?)\*", r"_\1_", text)

    # Restore bold markers to typst bold syntax
    text = text.replace("__BOLD_START__", "*").replace("__BOLD_END__", "*")

    # Restore combined bold+italic markers to typst syntax
    text = text.replace("__COMBINED_START__", "*_").replace("__COMBINED_END__", "_*")

    # Handle code
    text = re.sub(r"`([^`]+?)`", r"`\1`", text)

    return text


class Basics(BaseModel):
    class Location(BaseModel):
        address: str = ""
        postalCode: str = ""
        city: str = ""
        countryCode: str = Field(
            default="",
            json_schema_extra=build_description("ISO-3166-1 ALPHA-2, e.g. US, AU, IN"),
        )
        region: State = Field(
            default="",
            json_schema_extra=build_description("ISO-3166-2, e.g. CA, NY, ON, BC, etc."),
        )

    class Profiles(BaseModel):
        # e.g. Facebook or Twitter
        network: str = Field(
            default="",
            json_schema_extra=build_description("e.g. Facebook or Twitter"),
        )
        username: str = Field(
            default="",
            json_schema_extra=build_description("a unique identifier for the user"),
        )
        url: AnyUrl | None = Field(
            default=None,
            json_schema_extra=build_description("full URL to the profile"),
        )

    name: str = ""
    # e.g. Web Developer
    label: str = Field(
        default="",
        json_schema_extra=build_description("e.g. Web Developer"),
    )
    # URL (as per RFC 3986) to a image in JPEG or PNG format
    image: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description("URL to a image in JPEG or PNG format"),
    )
    # e.g. thomas@gmail.com
    email: str = ""
    # Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923
    phone: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "Phone numbers are stored as strings so use any "
                + "format you like, e.g. 712-117-2923"
            )
        },
    )
    # URL (as per RFC 3986) to your website, e.g. personal homepage
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description("URL to your website, e.g. personal homepage"),
    )
    # Write a short 2-3 sentence biography about yourself
    summary: str = Field(
        default="",
        json_schema_extra={
            "description": ("Write a short 2-3 sentence biography about yourself")
        },
    )
    location: Location = Location()
    profiles: list[Profiles] = Field(
        default=[],
        json_schema_extra={
            "description": "A list of social media profiles, e.g. Facebook, Twitter, LinkedIn"
        },
    )

    @staticmethod
    def get_empty() -> Basics:
        return Basics()


class Education(BaseModel):
    # e.g. Massachusetts Institute of Technology
    institution: str = Field(
        default="",
        json_schema_extra=build_description("University or college name"),
    )
    location: str = ""
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description("URL to the university or college"),
    )
    # e.g. Arts
    area: str = Field(
        default="",
        json_schema_extra={
            "description": "Majors or minors. e.g. `Computer Science and Physics`"
        },
    )
    studyType: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "e.g. `Bachelor of Science`, `Master of Arts`, `PhD`, `High School`"
            )
        },
    )
    # Start date in ISO 8601 format
    startDate: Iso8601 = Field(
        default="Present",
        json_schema_extra=build_description(DATE_DESCRIPTION),
    )
    # End date in ISO 8601 format
    endDate: Iso8601 = Field(
        default="Present",
        json_schema_extra=build_description(DATE_DESCRIPTION),
    )
    # Grade point average, e.g. 3.67/4.0
    score: str = Field(
        default="",
        json_schema_extra=build_description("Grade point average, e.g. 3.67/4.0. "),
    )
    # List notable courses/subjects
    courses: list[str] = Field(
        default=[],
        json_schema_extra={
            "description": (
                "List notable courses/subjects. e.g. `Data Structures`, `Algorithms`"
            )
        },
    )

    @staticmethod
    def get_empty() -> Education:
        return Education()


class Work(BaseModel):
    name: str = Field(
        default="",
        json_schema_extra=build_description("Company name e.g. Facebook"),
    )
    location: str = Field(
        default="",
        json_schema_extra=build_description("Location of the company. e.g. Menlo Park, CA."),
    )
    description: str = Field(
        default="",
        json_schema_extra={
            "description": "A short description of the company. e.g. Social Media Company"
        },
    )
    position: str = Field(
        default="", json_schema_extra=build_description("Job title e.g. Software Engineer")
    )
    url: AnyUrl | None = Field(
        default=None, json_schema_extra=build_description("URL to the company website.")
    )
    startDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    endDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    # Overview of responsibilities at the company
    summary: str = Field(
        default="",
        json_schema_extra=build_description("Overview of responsibilities at the company"),
    )
    # Specify multiple accomplishments
    highlights: list[str] = Field(
        default=[],
        json_schema_extra=build_description(HIGHLIGHT_DESCRIPTION),
    )

    @computed_field
    def highlights_typst(self) -> list[str]:
        return [markdown_to_typst(highlight) for highlight in self.highlights]

    @staticmethod
    def get_empty() -> Work:
        return Work()


class Project(BaseModel):
    name: str = Field(default="", json_schema_extra=build_description("Project name"))
    description: str = Field(
        default="", json_schema_extra=build_description("A short description of the project")
    )
    highlights: list[str] = Field(
        default=[],
        json_schema_extra=build_description(HIGHLIGHT_DESCRIPTION),
    )
    keywords: list[str] = Field(
        default=[],
        json_schema_extra={
            "description": "Specify special elements involved. e.g. `React`, `Node.js`"
        },
    )
    startDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    endDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description("URL to the project preview"),
    )
    roles: list[str] = Field(
        default=[],
        json_schema_extra={
            "description": (
                "Specify your role on this project. e.g. `Individual Contributor`, `Maintainer`"
                + " or `Team Lead`"
            )
        },
    )
    entity: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "Specify the relevant company/entity affiliations. e.g. `Claremont Colleges`"
            )
        },
    )
    type: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "Specify the relevant company/entity affiliations. e.g. `volunteering`, "
                + "`presentation`, `talk`, `application`, `conference`"
            )
        },
    )
    source_code: AnyUrl | None = Field(
        default=None,
        json_schema_extra={
            "description": (
                "URL (as per RFC 3986) to the source code repository. e.g. `GitHub`, `GitLab`"
            )
        },
    )

    @computed_field
    def highlights_typst(self) -> list[str]:
        return [markdown_to_typst(highlight) for highlight in self.highlights]

    @staticmethod
    def get_empty() -> Project:
        return Project()


class Volunteer(BaseModel):
    # e.g. Facebook
    organization: str = Field(
        default="",
        json_schema_extra=build_description("Organization name e.g. SF SPCA"),
    )
    # e.g. Software Engineer
    position: str = Field(
        default="",
        json_schema_extra=build_description("Position title e.g. Animal Care Volunteer"),
    )
    # e.g. http://facebook.example.com
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description("URL to the organization"),
    )
    # Start date in ISO 8601 format
    startDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    # End date in ISO 8601 format
    endDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    # Overview of responsibilities at the organization
    summary: str = Field(
        default="",
        json_schema_extra=build_description(
            "Overview of responsibilities at the organization"
        ),
    )
    # Specify multiple accomplishments
    highlights: list[str] = Field(
        default=[],
        json_schema_extra=build_description(HIGHLIGHT_DESCRIPTION),
    )
    location: str = ""

    @computed_field
    def highlights_typst(self) -> list[str]:
        return [markdown_to_typst(highlight) for highlight in self.highlights]

    @staticmethod
    def get_empty() -> Volunteer:
        return Volunteer()


class Award(BaseModel):
    # e.g. One of the 100 greatest minds of the century
    title: str = Field(
        default="",
        json_schema_extra=build_description(
            "e.g. One of the 100 greatest minds of the century"
        ),
    )
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra=build_description(
            "URL (as per RFC 3986) to the award or recognition"
        ),
    )
    # Date in ISO 8601 format
    date: Iso8601 = Field(
        default="Present",
        json_schema_extra=build_description(DATE_DESCRIPTION),
    )
    # e.g. Time Magazine
    awarder: str = Field(
        default="",
        json_schema_extra={
            "description": "the organization that awarded you e.g. Time Magazine"
        },
    )
    summary: str = ""

    @staticmethod
    def get_empty() -> Award:
        return Award(
            title="",
            url="",
            awarder="",
            summary="",
        )


class Certificate(BaseModel):
    name: str = Field(
        default="",
        json_schema_extra=build_description("e.g. AWS Certified Solutions Architect"),
    )
    date: Iso8601 = Field(
        default="Present",
        json_schema_extra=build_description(DATE_DESCRIPTION),
    )
    url: AnyUrl | None = Field(
        default=None,
        json_schema_extra={
            "description": "URL (as per RFC 3986) to the certificate or recognition"
        },
    )
    issuer: str = Field(
        default="",
        json_schema_extra={
            "description": "the organization that issued the certificate e.g. CNCF"
        },
    )

    @staticmethod
    def get_empty() -> Certificate:
        return Certificate()


class Publication(BaseModel):
    # e.g. The World Wide Web
    name: str = Field(
        default="",
        json_schema_extra=build_description("e.g. The World Wide Web"),
    )
    # e.g. IEEE, Computer Magazine
    publisher: str = Field(
        default="",
        json_schema_extra=build_description("e.g. IEEE, Computer Magazine"),
    )
    # Release date in ISO 8601 format
    releaseDate: Iso8601 = Field(
        default="Present", json_schema_extra=build_description(DATE_DESCRIPTION)
    )
    url: AnyUrl | None = None
    summary: str = ""

    @staticmethod
    def get_empty() -> Publication:
        return Publication(
            name="",
            publisher="",
            url="",
            summary="",
        )


class Skill(BaseModel):
    name: str = Field(
        default="",
        json_schema_extra=build_description("e.g. Web Development"),
    )
    level: str = Field(
        default="",
        json_schema_extra={
            "description": ("e.g. `Beginner`, `Intermediate`, `Advanced`, `Master`, `Expert`")
        },
    )
    keywords: list[str] = Field(
        default=[],
        json_schema_extra={
            "description": (
                "List some keywords pertaining to this skill. e.g. `HTML`, `CSS`, `JavaScript`"
            )
        },
    )

    @staticmethod
    def get_empty() -> Skill:
        return Skill()


class Language(BaseModel):
    # e.g. English, Spanish
    language: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "e.g. English, Spanish, Mandarin, French, German, etc."
                + " Use ISO 639-1 language codes where possible."
            )
        },
    )
    fluency: str = Field(
        default="",
        json_schema_extra={
            "description": "e.g. `Fluent`, `Conversational`, `Basic`, `Native speaker`"
        },
    )

    @staticmethod
    def get_empty() -> Language:
        return Language()


class Interest(BaseModel):
    # e.g. Philosophy
    name: str = Field(
        default="",
        json_schema_extra={
            "description": ("e.g. Philosophy, Computer Science, Mathematics, Physics, etc.")
        },
    )
    # List some keywords pertaining to this interest
    keywords: list[str] = Field(
        default=[],
        json_schema_extra={
            "description": (
                "List some keywords pertaining to this interest. e.g. `Quantum Computing`, "
                + "`Artificial Intelligence`, `Machine Learning`"
            )
        },
    )

    @staticmethod
    def get_empty() -> Interest:
        return Interest()


class Reference(BaseModel):
    # e.g. Timothy Cook
    name: str = Field(
        default="",
        json_schema_extra=build_description("e.g. Timothy Cook, Bill Gates, Elon Musk, etc."),
    )
    reference: str = Field(
        default="",
        json_schema_extra={
            "description": (
                "e.g. Joe blogs was a great employee, who turned up to work at least once a week."
                + " He exceeded my expectations when it came to doing nothing."
            )
        },
    )

    @staticmethod
    def get_empty() -> Reference:
        return Reference()


class Meta(BaseModel):
    # URL (as per RFC 3986) to the latest version of this document
    canonical: AnyUrl | None = None
    # A version field which follows semver - e.g. v1.0.0
    version: str = ""
    # Using ISO 8601 with YYYY-MM-DDThh:mm:ss
    lastModified: str


class CustomSection(BaseModel):
    class Highlight(BaseModel):
        summary: str = Field(
            default="",
            json_schema_extra=build_description("A short summary of the highlight."),
        )
        description: str = Field(
            default="",
            json_schema_extra={
                "description": (
                    "A detailed description of the highlight. e.g. `Developed a new feature "
                    + "that allows users to...`"
                )
            },
        )

    title: str = ""
    highlights: list[Highlight] = Field(
        default=[],
        json_schema_extra=build_description(HIGHLIGHT_DESCRIPTION),
    )

    @computed_field
    def highlights_typst(self) -> list[CustomSection.Highlight]:
        return [
            CustomSection.Highlight(
                summary=highlight.summary,
                description=markdown_to_typst(highlight.description),
            )
            for highlight in self.highlights
        ]

    @staticmethod
    def get_empty() -> CustomSection:
        return CustomSection()


class Resume(BaseModel):
    json_schema: str = Field(
        default=f"https://raw.githubusercontent.com/austinyu/cv-model/refs/heads/main/schemas/{consts.RESUME_SCHEMA_NAME}",
        alias="$schema",
    )
    basics: Basics = Field(
        default=Basics.get_empty(),
        json_schema_extra=build_description("The basics section of the resume."),
    )
    work: list[Work] = Field(
        default=[],
        json_schema_extra=build_description("The work experience section of the resume."),
    )
    volunteer: list[Volunteer] = Field(
        default=[],
        json_schema_extra=build_description("The volunteer experience section of the resume"),
    )
    education: list[Education] = Field(
        default=[],
        json_schema_extra=build_description("The education section of the resume"),
    )
    awards: list[Award] = Field(
        default=[],
        json_schema_extra=build_description("The awards section of the resume"),
    )
    certificates: list[Certificate] = Field(
        default=[],
        json_schema_extra=build_description("The certificates section of the resume"),
    )
    publications: list[Publication] = Field(
        default=[],
        json_schema_extra=build_description("The publications section of the resume"),
    )
    skills: list[Skill] = Field(
        default=[],
        json_schema_extra=build_description("The skills section of the resume"),
    )
    languages: list[Language] = Field(
        default=[],
        json_schema_extra=build_description("The languages section of the resume"),
    )
    interests: list[Interest] = Field(
        default=[],
        json_schema_extra=build_description("The interests section of the resume"),
    )
    references: list[Reference] = Field(
        default=[],
        json_schema_extra=build_description("The references section of the resume"),
    )
    projects: list[Project] = Field(
        default=[],
        json_schema_extra=build_description("The projects section of the resume"),
    )
    custom_sections: list[CustomSection] = Field(
        default=[],
        json_schema_extra=build_description("The custom sections of the resume"),
    )
    meta: Meta | None = Field(
        default=None,
        json_schema_extra=build_description(
            "The meta section of the resume. This is optional."
        ),
    )

    @staticmethod
    def get_empty() -> Resume:
        return Resume(
            basics=Basics.get_empty(),
            work=[Work.get_empty()],
            volunteer=[Volunteer.get_empty()],
            education=[Education.get_empty()],
            awards=[Award.get_empty()],
            certificates=[Certificate.get_empty()],
            publications=[Publication.get_empty()],
            skills=[Skill.get_empty()],
            languages=[Language.get_empty()],
            interests=[Interest.get_empty()],
            references=[Reference.get_empty()],
            projects=[Project.get_empty()],
            custom_sections=[CustomSection.get_empty()],
            meta=Meta(
                canonical="",
                version="",
                lastModified=datetime.date.today().isoformat(),
            ),
        )


PaperSize = Literal[
    "a0",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "a8",
    "a9",
    "a10",
    "a11",
    "iso-b1",
    "iso-b2",
    "iso-b3",
    "iso-b4",
    "iso-b5",
    "iso-b6",
    "iso-b7",
    "iso-b8",
    "iso-c3",
    "iso-c4",
    "iso-c5",
    "iso-c6",
    "iso-c7",
    "iso-c8",
    "din-d3",
    "din-d4",
    "din-d5",
    "din-d6",
    "din-d7",
    "din-d8",
    "sis-g5",
    "sis-e5",
    "ansi-a",
    "ansi-b",
    "ansi-c",
    "ansi-d",
    "ansi-e",
    "arch-a",
    "arch-b",
    "arch-c",
    "arch-d",
    "arch-e1",
    "arch-e",
    "jis-b0",
    "jis-b1",
    "jis-b2",
    "jis-b3",
    "jis-b4",
    "jis-b5",
    "jis-b6",
    "jis-b7",
    "jis-b8",
    "jis-b9",
    "jis-b10",
    "jis-b11",
    "sac-d0",
    "sac-d1",
    "sac-d2",
    "sac-d3",
    "sac-d4",
    "sac-d5",
    "sac-d6",
    "iso-id-1",
    "iso-id-2",
    "iso-id-3",
    "asia-f4",
    "jp-shiroku-ban-4",
    "jp-shiroku-ban-5",
    "jp-shiroku-ban-6",
    "jp-kiku-4",
    "jp-kiku-5",
    "jp-business-card",
    "cn-business-card",
    "eu-business-card",
    "fr-tellière",
    "fr-couronne-écriture",
    "fr-couronne-édition",
    "fr-raisin",
    "fr-carré",
    "fr-jésus",
    "uk-brief",
    "uk-draft",
    "uk-foolscap",
    "uk-quarto",
    "uk-crown",
    "uk-book-a",
    "uk-book-b",
    "us-letter",
    "us-legal",
    "us-tabloid",
    "us-executive",
    "us-foolscap-folio",
    "us-statement",
    "us-ledger",
    "us-oficio",
    "us-gov-letter",
    "us-gov-legal",
    "us-business-card",
    "us-digest",
    "us-trade",
    "newspaper-compact",
    "newspaper-berliner",
    "newspaper-broadsheet",
    "presentation-16-9",
    "presentation-4-3",
]


class RenderMargins(BaseModel):
    top: float
    bottom: float
    left: float
    right: float


PageNumbering = Literal["none", "1 / 1", "1"]
FontFamily = Literal[
    "New Computer Modern",
    "Times New Roman",
    "Arial",
]

DefaultSection = Literal[
    "work",
    "volunteer",
    "education",
    "awards",
    "certificates",
    "publications",
    "projects",
]

DEFAULT_SECTIONS = [
    "work",
    "volunteer",
    "education",
    "awards",
    "certificates",
    "publications",
    "projects",
]

COLOR_DESCRIPTION = "Color in hex format. e.g. #000000"


class RenderCtx(BaseModel):
    json_schema: str = Field(
        default=f"https://raw.githubusercontent.com/austinyu/cv-model/refs/heads/main/schemas/{consts.CTX_SCHEMA_NAME}",
        alias="$schema",
    )
    page_size: PaperSize = Field(
        default="a4",
        json_schema_extra=build_description(
            "The paper size to use for the document. "
            + "See https://typst.app/docs/reference/layout/page/#parameters-paper for "
            + "a list of available sizes."
        ),
    )
    page_margin: RenderMargins = Field(
        default=RenderMargins(top=0.5, bottom=0.5, left=0.5, right=0.5),
        json_schema_extra=build_description(
            "The margins in inches in the order (top, bottom, left, right)."
        ),
    )
    page_numbering: PageNumbering = Field(
        default="none",
        json_schema_extra=build_description(
            "The page numbering style to use for the document."
        ),
    )

    font_family: FontFamily = Field(default="New Computer Modern")
    font_size: int = Field(default=12, json_schema_extra=build_description("Font size in pt."))
    text_color: str = Field(
        default="#000000",
        json_schema_extra=build_description(
            "The default color to use for the document. " + COLOR_DESCRIPTION
        ),
    )
    name_color: str = Field(
        default="#000000",
        json_schema_extra=build_description(
            "The color to use for the main name in the document. " + COLOR_DESCRIPTION
        ),
    )
    section_title_color: str = Field(
        default="#26428b",
        json_schema_extra=build_description(
            "The color to use for the section titles in the document. " + COLOR_DESCRIPTION
        ),
    )
    entry_title_color: str = Field(
        default="#26428b",
        json_schema_extra=build_description(
            "The color to use for the entry titles in the document. " + COLOR_DESCRIPTION
        ),
    )
    link_color: str = Field(
        default="#26428b",
        json_schema_extra=build_description(
            "The color to use for the links in the document. " + COLOR_DESCRIPTION
        ),
    )

    highlight_spacing: float = Field(
        default=-0.5,
        json_schema_extra=build_description("The spacing between the highlight items in em."),
    )
    entry_spacing: float = Field(
        default=-0.5,
        json_schema_extra=build_description("The spacing between the entry items in em."),
    )
    section_spacing: float = Field(
        default=-0.5,
        json_schema_extra=build_description("The spacing between the section items in em."),
    )

    section_order: list[DefaultSection | str] = Field(
        default=[
            "education",
            "work",
            "projects",
            "volunteer",
            "awards",
            "certificates",
            "publications",
        ],
        json_schema_extra=build_description(
            "The order of the sections to render in the document."
        ),
    )


DEFAULT_RESUME = Resume(
    basics=Basics(
        name="Austin Yu",
        label="Software Engineer",
        email="yuxm.austin1023@gmail.com",
        phone="+1 (xxx) xxx-xxxx",
        url="https://www.google.com",
        summary="A dedicated software engineer with experience in cloud services, AI, and autonomous systems.",
        location=Basics.Location(
            address="",
            postalCode="",
            city="Bay Area",
            countryCode="US",
            region="CA",
        ),
        profiles=[
            Basics.Profiles(
                network="GitHub",
                username="austinyu",
                url="https://github.com/austinyu",
            ),
            Basics.Profiles(
                network="LinkedIn",
                username="xinmiao-yu-619128174",
                url="https://linkedin.com/in/xinmiao-yu-619128174",
            ),
        ],
    ),
    work=[
        Work(
            name="Microsoft",
            location="Redmond, WA",
            description="Azure Cloud Services Team",
            position="Software Engineer Intern",
            url="https://microsoft.com",
            startDate=datetime.date.fromisoformat("2023-05-15"),
            endDate=datetime.date.fromisoformat("2023-08-15"),
            summary="Developed solutions for Azure cloud services and improved performance metrics.",
            highlights=[
                "Developed a distributed caching solution for Azure Functions, reducing cold start latency by **30%** and improving overall performance for serverless applications.",
                "Implemented a monitoring dashboard using `Power BI` to visualize key performance metrics, enabling proactive issue detection and resolution.",
                "Collaborated with a team of engineers to refactor *legacy code*, improving maintainability and reducing technical debt by 25%.",
                "Contributed to the design and development of a new [API gateway](https://azure.microsoft.com/services/api-management/), enhancing scalability and security for cloud-based applications.",
                "Presented project outcomes to senior engineers and received **commendation** for delivering impactful solutions under tight deadlines.",
            ],
        ),
        Work(
            name="Amazon",
            location="Seattle, WA",
            description="Alexa Smart Home Team",
            position="Software Development Engineer Intern",
            url="https://amazon.com",
            startDate=datetime.date.fromisoformat("2022-06-01"),
            endDate=datetime.date.fromisoformat("2022-09-01"),
            highlights=[
                "Designed and implemented a feature to integrate third-party smart home devices with Alexa, increasing compatibility by 20%.",
                "Optimized voice recognition algorithms, reducing error rates by **15%** and improving *user satisfaction*.",
                "Developed automated ***testing frameworks*** with `pytest` to ensure the reliability of new integrations, achieving 90% test coverage.",
                "Worked closely with product managers to define [feature requirements](https://developer.amazon.com/alexa) and deliver a seamless user experience.",
                "Participated in **code reviews** and contributed to *team-wide best practices* for software development.",
            ],
        ),
        Work(
            name="Tesla",
            location="Palo Alto, CA",
            description="Autopilot Software Team",
            position="Software Engineer Intern",
            url="https://tesla.com",
            startDate=datetime.date.fromisoformat("2021-06-01"),
            endDate=datetime.date.fromisoformat("2021-08-31"),
            highlights=[
                "Developed and tested computer vision algorithms for lane detection, improving accuracy by **25%** in *challenging driving conditions*.",
                "Enhanced the performance of real-time object detection systems using `TensorFlow`, reducing processing latency by 10%.",
                "Collaborated with hardware engineers to optimize sensor data processing pipelines for [autonomous vehicles](https://www.tesla.com/autopilot).",
                "Conducted **extensive simulations** to validate new features, ensuring *compliance with safety standards*.",
                "Documented technical findings and contributed to research papers on advancements in autonomous driving technology.",
            ],
        ),
    ],
    volunteer=[
        Volunteer(
            organization="Bay Area Homeless Shelter",
            position="Volunteer Coordinator",
            url="",
            startDate=datetime.date.fromisoformat("2023-01-01"),
            endDate=datetime.date.fromisoformat("2023-05-01"),
            summary="Coordinated volunteer efforts to support homeless individuals in the Bay Area, providing essential services and resources.",
            location="Bay Area, CA",
            highlights=[
                "Managed a team of 20+ volunteers to organize weekly meal services",
                "Collaborated with a team of volunteers to sort and package food donations, ensuring efficient distribution to partner agencies.",
                "Participated in community education initiatives, promoting awareness of food insecurity and available resources.",
            ],
        ),
        Volunteer(
            organization="Stanford University",
            position="Volunteer Tutor",
            url="stanford.edu",
            startDate=datetime.date.fromisoformat("2023-06-01"),
            endDate=datetime.date.fromisoformat("2023-09-01"),
            location="Stanford, CA",
            summary="Provided tutoring support to high school students in mathematics and science subjects, fostering academic growth and confidence.",
            highlights=[
                "Developed personalized lesson plans and study materials to address individual student needs.",
                "Facilitated group study sessions, encouraging collaboration and peer learning.",
                "Received positive feedback from students and parents for effective teaching methods and dedication to student success.",
            ],
        ),
    ],
    education=[
        Education(
            institution="Stanford University",
            location="Stanford, CA",
            url="https://stanford.edu",
            area="Physics and Computer Science",
            studyType="Bachelor of Science",
            startDate=datetime.date.fromisoformat("2019-09-01"),
            endDate=datetime.date.fromisoformat("2023-06-01"),
            score="3.9/4.0",
            courses=[
                "Data Structures",
                "Algorithms",
                "Operating Systems",
                "Computer Networks",
                "Quantum Mechanics",
                "Linear Algebra",
                "Machine Learning",
                "Multivariable Calculus",
            ],
        ),
        Education(
            institution="University of California, Berkeley",
            location="Berkeley, CA",
            url="https://berkeley.edu",
            area="Computer Science",
            studyType="Master of Science",
            startDate=datetime.date.fromisoformat("2023-08-01"),
            endDate=datetime.date.fromisoformat("2025-05-01"),
            score="4.0/4.0",
            courses=[
                "Advanced Machine Learning",
                "Distributed Systems",
                "Cryptography",
                "Artificial Intelligence",
                "Database Systems",
                "Convex Optimization",
                "Natural Language Processing",
                "Computer Vision",
            ],
        ),
    ],
    awards=[
        Award(
            title="Best Student Award",
            date=datetime.date.fromisoformat("2023-05-01"),
            url="https://stanford.edu",
            awarder="Stanford University",
            summary="",
        ),
        Award(
            title="Dean's List",
            date=datetime.date.fromisoformat("2023-05-01"),
            url="",
            awarder="Stanford University",
            summary="Achieved Dean's List status for maintaining a GPA of 3.9 or higher.",
        ),
        Award(
            title="Outstanding Research Assistant",
            date=datetime.date.fromisoformat("2023-05-01"),
            url="https://stanford.edu",
            awarder="",
            summary="Recognized for exceptional contributions to research projects in the Physics and Computer Science departments.",
        ),
        Award(
            title="Best Paper Award",
            date=datetime.date.fromisoformat("2023-05-01"),
            url="https://berkeley.edu",
            awarder="University of California, Berkeley",
            summary="Received Best Paper Award at the UC Berkeley Graduate Research Symposium.",
        ),
    ],
    certificates=[
        Certificate(
            name="AWS Certified Solutions Architect",
            issuer="",
            url="https://aws.amazon.com/certification/certified-solutions-architect-associate/",
            date=datetime.date.fromisoformat("2023-05-01"),
        ),
        Certificate(
            name="Google Cloud Professional Data Engineer",
            issuer="Google Cloud",
            url="https://cloud.google.com/certification/data-engineer/",
            date=datetime.date.fromisoformat("2023-05-01"),
        ),
        Certificate(
            name="Microsoft Certified: Azure Fundamentals",
            issuer="Microsoft",
            url="https://learn.microsoft.com/en-us/certifications/azure-fundamentals/",
            date=datetime.date.fromisoformat("2023-05-01"),
        ),
        Certificate(
            name="Certified Kubernetes Administrator (CKA)",
            issuer="Linux Foundation",
            url="",
            date=datetime.date.fromisoformat("2023-05-01"),
        ),
        Certificate(
            name="Certified Ethical Hacker (CEH)",
            issuer="",
            url="https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/",
            date=datetime.date.fromisoformat("2023-05-01"),
        ),
    ],
    publications=[
        Publication(
            name="Understanding Quantum Computing",
            publisher="Springer",
            releaseDate=datetime.date.fromisoformat("2023-05-01"),
            url="https://arxiv.org/abs/quantum-computing",
            summary="A comprehensive overview of quantum computing principles and applications.",
        ),
        Publication(
            name="Machine Learning for Beginners",
            publisher="O'Reilly Media",
            releaseDate=datetime.date.fromisoformat("2023-05-01"),
            url="",
            summary="",
        ),
        Publication(
            name="Advanced Algorithms in Python",
            publisher="Packt Publishing",
            releaseDate=datetime.date.fromisoformat("2023-05-01"),
            url="https://packt.com/advanced-algorithms-python",
            summary="A deep dive into advanced algorithms and data structures using Python.",
        ),
        Publication(
            name="Data Science Handbook",
            publisher="Springer",
            releaseDate=datetime.date.fromisoformat("2023-05-01"),
            url="",
            summary="A practical guide to data science methodologies and tools.",
        ),
    ],
    skills=[
        Skill(
            name="Web Development",
            level="Master",
            keywords=[
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Node.js",
                "Express",
                "Django",
                "Flask",
                "Ruby on Rails",
                "RESTful APIs",
            ],
        ),
        Skill(
            name="Machine Learning",
            level="Intermediate",
            keywords=[
                "Python",
                "TensorFlow",
                "Keras",
                "PyTorch",
                "Scikit-learn",
                "Natural Language Processing",
                "Computer Vision",
            ],
        ),
        Skill(
            name="Cloud Computing",
            level="Intermediate",
            keywords=[
                "AWS",
                "Azure",
                "Google Cloud Platform",
                "Docker",
                "Kubernetes",
                "Terraform",
                "CI/CD",
            ],
        ),
    ],
    languages=[
        Language(language="English", fluency="Native speaker"),
        Language(language="Spanish", fluency="Conversational"),
        Language(language="Mandarin", fluency="Basic"),
        Language(language="French", fluency="Basic"),
    ],
    interests=[
        Interest(
            name="Artificial Intelligence",
            keywords=[
                "Machine Learning",
                "Deep Learning",
                "Natural Language Processing",
                "Computer Vision",
                "Reinforcement Learning",
            ],
        ),
        Interest(
            name="Quantum Computing",
            keywords=[
                "Quantum Algorithms",
                "Quantum Cryptography",
                "Quantum Machine Learning",
                "Quantum Information Theory",
            ],
        ),
        Interest(
            name="Software Development",
            keywords=[
                "Agile Methodologies",
                "Version Control (Git)",
                "Continuous Integration/Continuous Deployment (CI/CD)",
                "Test-Driven Development (TDD)",
                "Code Review",
            ],
        ),
    ],
    references=[
        Reference(
            name="Timothy Cook",
            reference="Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.",
        ),
        Reference(
            name="Bill Gates",
            reference="Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.",
        ),
        Reference(
            name="Elon Musk",
            reference="Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.",
        ),
    ],
    projects=[
        Project(
            name="Hyperschedule",
            description="Developed and maintained an open-source scheduling tool used by students across the Claremont Consortium, leveraging TypeScript, React, and MongoDB.",
            highlights=[
                "Implemented new features such as course filtering and schedule sharing, improving user experience and engagement.",
                "Collaborated with a team of contributors to address bugs and optimize performance, reducing load times by 40%.",
                "Coordinated with college administrators to ensure accurate and timely release of course data.",
            ],
            keywords=["React", "TypeScript", "MongoDB", "Git"],
            startDate=datetime.date.fromisoformat("2022-01-01"),
            endDate="Present",
            url="https://hyperschedule.io",
            roles=["Individual Contributor", "Maintainer"],
            entity="Claremont Colleges",
            type="application",
            source_code="https://github.com/hyperschedule",
        ),
        Project(
            name="Claremont Colleges Course Registration",
            description="Contributed to the development of a course registration platform for the Claremont Colleges, streamlining the enrollment process for thousands of students.",
            highlights=[
                "Designed and implemented a user-friendly interface for course selection, increasing adoption rates by 25%.",
                "Optimized backend systems to handle peak traffic during registration periods, ensuring system stability.",
                "Provided technical support and documentation to assist users and administrators with platform usage.",
            ],
            keywords=["React", "Node.js", "PostgreSQL", "Git"],
            startDate=datetime.date.fromisoformat("2021-09-01"),
            endDate=datetime.date.fromisoformat("2022-12-01"),
            url="",
            roles=["Individual Contributor", "Maintainer"],
            entity="Claremont Colleges",
            type="application",
            source_code="https://github.com/claremont-colleges",
        ),
    ],
    custom_sections=[
        CustomSection(
            title="Programming Languages",
            highlights=[
                CustomSection.Highlight(
                    summary="Languages",
                    description="**Python**, *Java*, `C++`, [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), and ***TypeScript***",
                ),
                CustomSection.Highlight(
                    summary="Frameworks",
                    description="*React*, **Node.js**, `Express`, [Flask](https://flask.palletsprojects.com/), and ***Django***",
                ),
                CustomSection.Highlight(
                    summary="Databases",
                    description="**MySQL**, *MongoDB*, and `PostgreSQL` with [advanced indexing](https://www.postgresql.org/docs/current/indexes.html)",
                ),
                CustomSection.Highlight(
                    summary="Tools",
                    description="`Git` for **version control**, *Docker* containers, ***Kubernetes*** orchestration, and [AWS cloud services](https://aws.amazon.com/)",
                ),
            ],
        ),
        CustomSection(
            title="Skills",
            highlights=[
                CustomSection.Highlight(
                    summary="Soft Skills",
                    description="**Teamwork**, *Communication*, `Problem Solving`, and [Time Management](https://en.wikipedia.org/wiki/Time_management) ***techniques***",
                ),
                CustomSection.Highlight(
                    summary="Technical Skills",
                    description="*Data Structures*, **Algorithms**, `Software Development` methodologies, and [Web Development](https://developer.mozilla.org/en-US/docs/Web) ***best practices***",
                ),
                CustomSection.Highlight(
                    summary="Languages",
                    description="**English** (*Fluent*), `Spanish` (Conversational), and [Mandarin](https://en.wikipedia.org/wiki/Mandarin_Chinese) (***Basic***)",
                ),
            ],
        ),
    ],
    meta=Meta(
        canonical="https://example.com/resume.json",
        version="v1.0.0",
        lastModified=datetime.datetime.now().date().isoformat(),
    ),
)


def get_default_resume() -> Resume:
    return DEFAULT_RESUME
