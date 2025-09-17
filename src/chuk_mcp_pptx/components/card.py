"""
Card component for PowerPoint presentations.
Provides container components with various styles.
"""

from typing import Optional, Dict, Any, List
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from .base import Component


class Card(Component):
    """
    Card component for containing content.
    
    Features:
    - Header, body, and footer sections
    - Multiple variants (default, bordered, elevated)
    - Theme-aware styling
    """
    
    def __init__(self,
                 title: Optional[str] = None,
                 description: Optional[str] = None,
                 variant: str = "default",
                 theme: Optional[Dict[str, Any]] = None):
        """
        Initialize card component.
        
        Args:
            title: Card title
            description: Card description
            variant: Card variant (default, bordered, elevated)
            theme: Theme configuration
        """
        super().__init__(theme)
        self.title = title
        self.description = description
        self.variant = variant
    
    def render(self, slide, left: float, top: float,
               width: float = 3.0, height: float = 2.0) -> Any:
        """
        Render card to slide.
        
        Args:
            slide: PowerPoint slide object
            left: Left position in inches
            top: Top position in inches
            width: Card width in inches
            height: Card height in inches
        
        Returns:
            Shape object representing the card
        """
        # Create card container
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left),
            Inches(top),
            Inches(width),
            Inches(height)
        )
        
        # Apply variant styling
        if self.variant == "elevated":
            # Add shadow effect (PowerPoint limitation: basic shadow)
            card.shadow.visible = True
            card.shadow.blur_radius = Pt(10)
            card.shadow.distance = Pt(4)
            card.shadow.angle = 90
        
        # Apply theme colors
        card.fill.solid()
        card.fill.fore_color.rgb = self.get_color("card.DEFAULT")
        
        if self.variant == "bordered":
            card.line.color.rgb = self.get_color("border.DEFAULT")
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        
        # Add content
        text_frame = card.text_frame
        text_frame.clear()
        text_frame.margin_left = Inches(self.get_padding("md"))
        text_frame.margin_right = Inches(self.get_padding("md"))
        text_frame.margin_top = Inches(self.get_padding("md"))
        text_frame.margin_bottom = Inches(self.get_padding("md"))
        
        # Add title
        if self.title:
            p = text_frame.paragraphs[0]
            p.text = self.title
            style = self.get_text_style("h4")
            p.font.name = style["font_family"]
            p.font.size = Pt(style["font_size"])
            p.font.bold = True
            p.font.color.rgb = self.get_color("card.foreground")
        
        # Add description
        if self.description:
            p = text_frame.add_paragraph()
            p.text = self.description
            p.space_before = Pt(6)
            style = self.get_text_style("body")
            p.font.name = style["font_family"]
            p.font.size = Pt(style["font_size"])
            p.font.color.rgb = self.get_color("muted.foreground")
        
        return card


class MetricCard(Card):
    """
    Specialized card for displaying metrics/KPIs.
    """
    
    def __init__(self,
                 label: str,
                 value: str,
                 change: Optional[str] = None,
                 trend: Optional[str] = None,  # "up", "down", "neutral"
                 theme: Optional[Dict[str, Any]] = None):
        """
        Initialize metric card.
        
        Args:
            label: Metric label
            value: Metric value
            change: Change percentage/value
            trend: Trend direction
            theme: Theme configuration
        """
        super().__init__(theme=theme)
        self.label = label
        self.value = value
        self.change = change
        self.trend = trend
    
    def get_trend_color(self) -> Any:
        """Get color based on trend."""
        if self.trend == "up":
            return self.get_color("success.DEFAULT")
        elif self.trend == "down":
            return self.get_color("destructive.DEFAULT")
        else:
            return self.get_color("muted.foreground")
    
    def get_trend_symbol(self) -> str:
        """Get trend symbol."""
        if self.trend == "up":
            return "↑"
        elif self.trend == "down":
            return "↓"
        else:
            return "→"
    
    def render(self, slide, left: float, top: float,
               width: float = 2.0, height: float = 1.5) -> Any:
        """
        Render metric card to slide.
        """
        # Create card container
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left),
            Inches(top),
            Inches(width),
            Inches(height)
        )
        
        # Apply styling
        card.fill.solid()
        card.fill.fore_color.rgb = self.get_color("card.DEFAULT")
        card.line.color.rgb = self.get_color("border.DEFAULT")
        card.line.width = Pt(1)
        
        # Add content
        text_frame = card.text_frame
        text_frame.clear()
        padding = self.get_padding("md")
        text_frame.margin_left = Inches(padding)
        text_frame.margin_right = Inches(padding)
        text_frame.margin_top = Inches(padding)
        text_frame.margin_bottom = Inches(padding)
        
        # Add label
        p = text_frame.paragraphs[0]
        p.text = self.label
        p.font.size = Pt(12)
        p.font.color.rgb = self.get_color("muted.foreground")
        p.font.name = self.theme.get("font_family", "Inter")
        
        # Add value
        p = text_frame.add_paragraph()
        p.text = self.value
        p.space_before = Pt(4)
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = self.get_color("card.foreground")
        p.font.name = self.theme.get("font_family", "Inter")
        
        # Add change with trend
        if self.change:
            p = text_frame.add_paragraph()
            p.text = f"{self.get_trend_symbol()} {self.change}"
            p.space_before = Pt(2)
            p.font.size = Pt(11)
            p.font.color.rgb = self.get_trend_color()
            p.font.name = self.theme.get("font_family", "Inter")
        
        return card


class FeatureCard(Card):
    """
    Card for displaying features or capabilities.
    """
    
    def __init__(self,
                 icon: Optional[str] = None,
                 title: str = "",
                 features: List[str] = None,
                 theme: Optional[Dict[str, Any]] = None):
        """
        Initialize feature card.
        
        Args:
            icon: Optional icon character
            title: Feature title
            features: List of feature points
            theme: Theme configuration
        """
        super().__init__(title=title, theme=theme)
        self.icon = icon
        self.features = features or []
    
    def render(self, slide, left: float, top: float,
               width: float = 3.0, height: float = 3.5) -> Any:
        """
        Render feature card to slide.
        """
        # Create card
        card = super().render(slide, left, top, width, height)
        
        # Clear default content and rebuild
        text_frame = card.text_frame
        text_frame.clear()
        padding = self.get_padding("md")
        text_frame.margin_left = Inches(padding)
        text_frame.margin_right = Inches(padding)
        text_frame.margin_top = Inches(padding)
        text_frame.margin_bottom = Inches(padding)
        
        # Add icon if provided
        if self.icon:
            p = text_frame.paragraphs[0]
            p.text = self.icon
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(32)
            p.font.color.rgb = self.get_color("primary.DEFAULT")
            
            # Add title after icon
            if self.title:
                p = text_frame.add_paragraph()
                p.text = self.title
                p.alignment = PP_ALIGN.CENTER
                p.space_before = Pt(8)
                p.font.size = Pt(16)
                p.font.bold = True
                p.font.color.rgb = self.get_color("card.foreground")
                p.font.name = self.theme.get("font_family", "Inter")
        elif self.title:
            # Just title, no icon
            p = text_frame.paragraphs[0]
            p.text = self.title
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = self.get_color("card.foreground")
            p.font.name = self.theme.get("font_family", "Inter")
        
        # Add features
        for feature in self.features:
            p = text_frame.add_paragraph()
            p.text = f"• {feature}"
            p.space_before = Pt(6)
            p.font.size = Pt(12)
            p.font.color.rgb = self.get_color("muted.foreground")
            p.font.name = self.theme.get("font_family", "Inter")
            p.level = 0
        
        return card