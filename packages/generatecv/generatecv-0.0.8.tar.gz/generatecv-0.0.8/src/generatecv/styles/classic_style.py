"""Classic style for CVs."""

from reportlab.lib.styles import ParagraphStyle

from .base_style import CVStyle


class ClassicStyle(CVStyle):
    """Classic style for CVs."""

    def _setup_styles(self) -> None:
        """Setup classic style."""
        # Name style
        self.styles.add(
            ParagraphStyle(
                name="Name",
                parent=self.styles["Heading1"],
                fontSize=16,  # Increased font size
                spaceAfter=4,  # Adjusted spacing
                leading=22,  # Added leading
            )
        )

        # Section headings
        self.styles.add(
            ParagraphStyle(
                name="SectionHeading",
                parent=self.styles["Heading2"],
                fontSize=12,  # Increased font size
                spaceAfter=4,  # Adjusted spacing
                fontName="Times-Bold",
                leading=18,  # Added leading
            )
        )

        # Contact info style
        self.styles.add(
            ParagraphStyle(
                name="ContactInfo",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceAfter=4,  # Adjusted spacing
                leading=12,  # Added leading
            )
        )

        # Experience title style
        self.styles.add(
            ParagraphStyle(
                name="ExperienceTitle",
                parent=self.styles["Normal"],
                fontSize=10,
                fontName="Times-Bold",
                spaceAfter=2,  # Adjusted spacing
                leading=14,  # Added leading
            )
        )

        # Role Title style (new)
        self.styles.add(
            ParagraphStyle(
                name="RoleTitle",
                parent=self.styles["Normal"],
                fontSize=12,
                fontName="Times-Bold",
                leftIndent=0,  # Removed indent
                spaceBefore=3,  # Adjusted spacing
                spaceAfter=2,  # Adjusted spacing
                leading=12,  # Added leading
            )
        )

        # Experience details style
        self.styles.add(
            ParagraphStyle(
                name="ExperienceDetails",
                parent=self.styles["Normal"],
                fontSize=10,
                fontName="Times-Italic",
                leftIndent=0,  # Ensure no indent
                spaceAfter=2,  # Adjusted spacing
                leading=12,  # Added leading
            )
        )

        # Normal text style
        normal_style = self.styles["Normal"]
        normal_style.fontSize = 10
        normal_style.spaceAfter = 6
        normal_style.fontName = "Times-Roman"
        normal_style.leading = 12  # Added leading

        # Paragraph style (similar to Normal)
        self.styles.add(
            ParagraphStyle(
                name="Paragraph",
                parent=self.styles["Normal"],
                fontSize=10,
                spaceAfter=4,
                fontName="Times-Roman",
                leading=12,
                firstLineIndent=15,
            )
        )
