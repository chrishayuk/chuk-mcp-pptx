"""
Template Manager for PowerPoint MCP Server

Manages built-in templates and provides async template operations.
Similar to ThemeManager, provides access to pre-built templates.
"""

import asyncio
import io
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from pptx import Presentation

logger = logging.getLogger(__name__)


class TemplateMetadata(BaseModel):
    """Metadata for a template."""

    name: str = Field(..., description="Template name/identifier")
    display_name: str = Field(..., description="Human-readable template name")
    description: str = Field(..., description="Template description")
    layout_count: int = Field(..., description="Number of slide layouts", ge=0)
    category: str = Field(default="general", description="Template category")
    tags: list[str] = Field(default_factory=list, description="Search tags")
    is_builtin: bool = Field(default=True, description="Whether this is a built-in template")

    class Config:
        extra = "forbid"


class TemplateManager:
    """
    Manages PowerPoint templates similar to ThemeManager.

    Provides access to built-in templates and custom template management.
    All operations are async and use Pydantic models.
    """

    def __init__(self):
        """Initialize the template manager."""
        # Use multiple path resolution strategies for robustness
        self.templates_dir = self._find_templates_dir()
        self._templates: dict[str, TemplateMetadata] = {}
        self._template_cache: dict[str, bytes] = {}

        # Log template directory for debugging
        logger.info(f"TemplateManager initialized with templates_dir: {self.templates_dir}")
        logger.info(f"Templates directory exists: {self.templates_dir.exists()}")
        logger.info(f"Templates directory absolute path: {self.templates_dir.absolute()}")
        if self.templates_dir.exists():
            template_files = list(self.templates_dir.glob("*.pptx"))
            logger.info(
                f"Found {len(template_files)} template files: {[f.name for f in template_files]}"
            )
        else:
            logger.error("Templates directory does not exist!")
            logger.error(f"__file__ = {__file__}")
            logger.error(f"Parent directory contents: {list(Path(__file__).parent.iterdir())}")

        self._initialize_builtin_templates()

    def _find_templates_dir(self) -> Path:
        """Find templates directory using multiple strategies."""
        # Strategy 1: Relative to this file (works for editable installs)
        templates_dir = Path(__file__).parent / "builtin"
        if templates_dir.exists():
            return templates_dir

        # Strategy 2: Use importlib.resources (works for installed packages)
        try:
            import importlib.resources as resources

            if hasattr(resources, "files"):
                # Python 3.9+
                templates_ref = resources.files("chuk_mcp_pptx") / "templates" / "builtin"
                if hasattr(templates_ref, "as_posix"):
                    templates_dir = Path(str(templates_ref))
                    if templates_dir.exists():
                        return templates_dir
        except Exception as e:
            logger.warning(f"Could not use importlib.resources: {e}")

        # Strategy 3: Fallback to package location
        import chuk_mcp_pptx

        pkg_dir = Path(chuk_mcp_pptx.__file__).parent
        templates_dir = pkg_dir / "templates" / "builtin"
        if templates_dir.exists():
            return templates_dir

        # If all else fails, return the original path (will log error later)
        return Path(__file__).parent / "builtin"

    def _initialize_builtin_templates(self) -> None:
        """Initialize registry of built-in templates."""
        # Define built-in templates
        # These would be actual .pptx files in the builtin/ directory
        builtin_templates = [
            TemplateMetadata(
                name="brand_proposal",
                display_name="Brand Proposal",
                description="Professional brand proposal template with 55 layouts for comprehensive brand presentations",
                layout_count=55,
                category="business",
                tags=["brand", "proposal", "marketing", "business", "professional"],
            ),
            TemplateMetadata(
                name="minimal",
                display_name="Minimal",
                description="Clean minimal template with basic layouts",
                layout_count=5,
                category="basic",
                tags=["minimal", "clean", "simple"],
            ),
            TemplateMetadata(
                name="corporate",
                display_name="Corporate",
                description="Professional corporate template with standard layouts",
                layout_count=8,
                category="business",
                tags=["corporate", "business", "professional"],
            ),
            TemplateMetadata(
                name="modern",
                display_name="Modern",
                description="Modern template with contemporary design",
                layout_count=10,
                category="business",
                tags=["modern", "contemporary", "stylish"],
            ),
            TemplateMetadata(
                name="tech",
                display_name="Technology",
                description="Tech-focused template with data visualization layouts",
                layout_count=12,
                category="technology",
                tags=["tech", "technology", "data", "startup"],
            ),
            TemplateMetadata(
                name="academic",
                display_name="Academic",
                description="Academic template for research presentations",
                layout_count=7,
                category="education",
                tags=["academic", "research", "education", "university"],
            ),
        ]

        for template in builtin_templates:
            self._templates[template.name] = template

    async def get_template_data(self, template_name: str) -> bytes | None:
        """
        Get template data as bytes.

        Args:
            template_name: Name of the template

        Returns:
            Template data as bytes or None if not found
        """
        # Check cache first
        if template_name in self._template_cache:
            return self._template_cache[template_name]

        # Check if template exists in metadata
        if template_name not in self._templates:
            logger.warning(f"Template not found: {template_name}")
            return None

        # Try to load from builtin directory
        template_path = self.templates_dir / f"{template_name}.pptx"
        logger.info(f"Looking for template at: {template_path}")

        if template_path.exists():
            try:
                data = await asyncio.to_thread(template_path.read_bytes)
                self._template_cache[template_name] = data
                logger.info(f"Successfully loaded template {template_name} ({len(data)} bytes)")
                return data
            except Exception as e:
                logger.error(f"Failed to load template {template_name}: {e}")
                return None

        # Template file not found - this is an error condition
        logger.error(f"Template file not found: {template_path}")
        logger.error(f"Templates directory: {self.templates_dir}")
        logger.error(f"Templates directory exists: {self.templates_dir.exists()}")
        if self.templates_dir.exists():
            logger.error(f"Files in templates directory: {list(self.templates_dir.iterdir())}")

        # Return None to indicate error instead of silently creating blank presentation
        return None

    async def _create_placeholder_template(self) -> bytes:
        """Create a blank placeholder template."""
        prs = Presentation()
        buffer = io.BytesIO()
        await asyncio.to_thread(prs.save, buffer)
        buffer.seek(0)
        return buffer.read()

    def list_templates(self) -> list[TemplateMetadata]:
        """
        List all available templates.

        Returns:
            List of TemplateMetadata objects
        """
        return list(self._templates.values())

    def get_template_metadata(self, template_name: str) -> TemplateMetadata | None:
        """
        Get metadata for a specific template.

        Args:
            template_name: Name of the template

        Returns:
            TemplateMetadata or None if not found
        """
        return self._templates.get(template_name)

    def search_templates(self, query: str) -> list[TemplateMetadata]:
        """
        Search templates by name, category, or tags.

        Args:
            query: Search query string

        Returns:
            List of matching TemplateMetadata objects
        """
        query_lower = query.lower()
        results = []

        for template in self._templates.values():
            if (
                query_lower in template.name.lower()
                or query_lower in template.display_name.lower()
                or query_lower in template.description.lower()
                or query_lower in template.category.lower()
                or any(query_lower in tag.lower() for tag in template.tags)
            ):
                results.append(template)

        return results

    def register_custom_template(
        self,
        name: str,
        display_name: str,
        description: str,
        layout_count: int,
        category: str = "custom",
        tags: list[str] | None = None,
    ) -> None:
        """
        Register a custom template.

        Args:
            name: Template identifier
            display_name: Human-readable name
            description: Template description
            layout_count: Number of layouts in template
            category: Template category
            tags: Search tags
        """
        template = TemplateMetadata(
            name=name,
            display_name=display_name,
            description=description,
            layout_count=layout_count,
            category=category,
            tags=tags or [],
            is_builtin=False,
        )
        self._templates[name] = template
        logger.info(f"Registered custom template: {name}")

    def get_categories(self) -> list[str]:
        """
        Get list of all template categories.

        Returns:
            List of unique category names
        """
        return sorted(set(t.category for t in self._templates.values()))
