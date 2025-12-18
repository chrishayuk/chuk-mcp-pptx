# src/chuk_mcp_pptx/components/core/connector.py
"""
Connector and arrow components for PowerPoint presentations.

Provides connector lines with arrows for diagrams and flows.
"""

from typing import Optional, Dict, Any
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

from ..base import Component
from ..registry import component, ComponentCategory, prop, example


CONNECTOR_TYPES = {
    "straight": MSO_CONNECTOR.STRAIGHT,
    "elbow": MSO_CONNECTOR.ELBOW,
    "curved": MSO_CONNECTOR.CURVE,
}


@component(
    name="Connector",
    category=ComponentCategory.UI,
    description="Connector line with optional arrows for diagrams",
    props=[
        prop("start_x", "number", "Starting X position in inches", required=True),
        prop("start_y", "number", "Starting Y position in inches", required=True),
        prop("end_x", "number", "Ending X position in inches", required=True),
        prop("end_y", "number", "Ending Y position in inches", required=True),
        prop(
            "connector_type",
            "string",
            "Connector style",
            options=["straight", "elbow", "curved"],
            default="straight",
        ),
        prop("line_color", "string", "Line color", example="primary.DEFAULT"),
        prop("line_width", "number", "Line width in points", default=2.0),
        prop("arrow_start", "boolean", "Show arrow at start", default=False),
        prop("arrow_end", "boolean", "Show arrow at end", default=True),
    ],
    examples=[
        example(
            "Simple arrow",
            """
connector = Connector(
    start_x=1.0,
    start_y=2.0,
    end_x=5.0,
    end_y=3.0,
    line_color="primary.DEFAULT"
)
connector.render(slide)
            """,
            connector_type="straight",
        ),
        example(
            "Curved bidirectional",
            """
connector = Connector(
    start_x=2.0,
    start_y=2.0,
    end_x=6.0,
    end_y=4.0,
    connector_type="curved",
    arrow_start=True,
    arrow_end=True
)
connector.render(slide)
            """,
            connector_type="curved",
        ),
    ],
    tags=["connector", "arrow", "line", "diagram", "flow"],
)
class Connector(Component):
    """
    Connector line component for connecting shapes and creating flows.

    Features:
    - Three connector types (straight, elbow, curved)
    - Optional arrows at start/end
    - Theme-aware colors
    - Customizable line width

    Usage:
        # Simple arrow
        connector = Connector(
            start_x=1.0, start_y=2.0,
            end_x=5.0, end_y=2.0,
            line_color="primary.DEFAULT"
        )
        connector.render(slide)

        # Bidirectional curved connector
        connector = Connector(
            start_x=2.0, start_y=2.0,
            end_x=6.0, end_y=4.0,
            connector_type="curved",
            arrow_start=True,
            arrow_end=True
        )
        connector.render(slide)
    """

    def __init__(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        connector_type: str = "straight",
        line_color: Optional[str] = None,
        line_width: float = 2.0,
        arrow_start: bool = False,
        arrow_end: bool = True,
        theme: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize connector component.

        Args:
            start_x: Starting X position in inches
            start_y: Starting Y position in inches
            end_x: Ending X position in inches
            end_y: Ending Y position in inches
            connector_type: Type (straight, elbow, curved)
            line_color: Line color (hex or semantic)
            line_width: Line width in points
            arrow_start: Whether to show arrow at start
            arrow_end: Whether to show arrow at end
            theme: Optional theme override
        """
        super().__init__(theme)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.connector_type = connector_type
        self.line_color = line_color
        self.line_width = line_width
        self.arrow_start = arrow_start
        self.arrow_end = arrow_end

    def render(self, slide, placeholder: Optional[Any] = None) -> Any:
        """
        Render connector to slide.

        Args:
            slide: PowerPoint slide object
            placeholder: Optional placeholder to replace

        Returns:
            Connector shape object
        """
        # If placeholder provided, extract bounds and delete it
        bounds = self._extract_placeholder_bounds(placeholder)
        if bounds is not None:
            left, top, width, height = bounds
            # For connectors, use bounds to determine start/end points
            self.start_x = left
            self.start_y = top + height / 2
            self.end_x = left + width
            self.end_y = top + height / 2

        # Delete placeholder after extracting bounds
        self._delete_placeholder_if_needed(placeholder)

        # Get connector type
        mso_connector = CONNECTOR_TYPES.get(self.connector_type.lower(), MSO_CONNECTOR.STRAIGHT)

        # Create connector
        connector = slide.shapes.add_connector(
            mso_connector,
            Inches(self.start_x),
            Inches(self.start_y),
            Inches(self.end_x),
            Inches(self.end_y),
        )

        # Set line color
        if self.line_color:
            color_rgb = self._parse_color(self.line_color)
        else:
            color_rgb = self.get_color("muted.foreground")

        connector.line.color.rgb = color_rgb
        connector.line.width = Pt(self.line_width)

        # Add arrows
        self._add_arrows(connector)

        return connector

    def _parse_color(self, color_str: str) -> RGBColor:
        """Parse color string (hex or semantic path)."""
        if color_str.startswith("#"):
            color_str = color_str[1:]
            return RGBColor(
                int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16)
            )
        else:
            return self.get_color(color_str)

    def _add_arrows(self, connector):
        """Add arrow heads to connector."""
        # Get or create line element
        line_elem = connector._element.spPr.ln if hasattr(connector._element.spPr, "ln") else None
        if line_elem is None:
            line_elem = connector._element.spPr._add_ln()

        # Add arrow at end
        if self.arrow_end:
            headEnd = parse_xml(
                '<a:headEnd type="triangle" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'
            )
            line_elem.append(headEnd)

        # Add arrow at start
        if self.arrow_start:
            tailEnd = parse_xml(
                '<a:tailEnd type="triangle" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'
            )
            line_elem.append(tailEnd)
