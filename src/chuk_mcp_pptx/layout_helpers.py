"""
Layout Helpers for PowerPoint MCP Server

Provides utilities for ensuring proper positioning and sizing of elements
within standard PowerPoint slide dimensions.
"""
from typing import Tuple, Optional, List, Dict
from pptx.util import Inches


# Standard PowerPoint slide dimensions (16:9 aspect ratio)
SLIDE_WIDTH = 10.0  # inches
SLIDE_HEIGHT = 5.625  # inches (16:9 ratio)

# Alternative 4:3 dimensions
SLIDE_WIDTH_4_3 = 10.0  # inches  
SLIDE_HEIGHT_4_3 = 7.5  # inches

# Safe margins from edges
MARGIN_TOP = 1.0  # inches - accounts for typical title area
MARGIN_BOTTOM = 0.5  # inches
MARGIN_LEFT = 0.5  # inches  
MARGIN_RIGHT = 0.5  # inches

# Content area (safe zone)
CONTENT_WIDTH = SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # 9.0 inches
CONTENT_HEIGHT = SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM  # 4.125 inches
CONTENT_LEFT = MARGIN_LEFT
CONTENT_TOP = MARGIN_TOP


def validate_position(
    left: float, 
    top: float, 
    width: float, 
    height: float,
    aspect_ratio: str = "16:9"
) -> Tuple[float, float, float, float]:
    """
    Validate and adjust position to ensure element fits within slide.
    
    Args:
        left: Left position in inches
        top: Top position in inches
        width: Width in inches
        height: Height in inches
        aspect_ratio: Slide aspect ratio ("16:9" or "4:3")
        
    Returns:
        Tuple of adjusted (left, top, width, height)
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3
    
    # Ensure minimum size
    width = max(0.5, width)
    height = max(0.5, height)
    
    # Adjust if element goes beyond right edge
    if left + width > slide_width:
        if width <= slide_width:
            left = slide_width - width
        else:
            width = slide_width - left
            
    # Adjust if element goes beyond bottom edge  
    if top + height > slide_height:
        if height <= slide_height:
            top = slide_height - height
        else:
            height = slide_height - top
            
    # Ensure element starts within slide
    left = max(0, min(left, slide_width - 0.5))
    top = max(0, min(top, slide_height - 0.5))
    
    return left, top, width, height


def calculate_grid_layout(
    num_items: int,
    columns: int = None,
    spacing: float = 0.2,
    container_left: float = CONTENT_LEFT,
    container_top: float = CONTENT_TOP,
    container_width: float = CONTENT_WIDTH,
    container_height: float = CONTENT_HEIGHT
) -> List[Dict[str, float]]:
    """
    Calculate optimal grid layout for multiple items.
    
    Args:
        num_items: Number of items to arrange
        columns: Number of columns (auto-calculated if None)
        spacing: Spacing between items in inches
        container_left: Left position of container area
        container_top: Top position of container area
        container_width: Width of container area
        container_height: Height of container area
        
    Returns:
        List of position dictionaries with 'left', 'top', 'width', 'height'
    """
    if num_items == 0:
        return []
        
    # Auto-calculate columns if not specified
    if columns is None:
        if num_items <= 2:
            columns = num_items
        elif num_items <= 4:
            columns = 2
        elif num_items <= 9:
            columns = 3
        else:
            columns = 4
            
    # Calculate rows
    rows = (num_items + columns - 1) // columns
    
    # Calculate item dimensions
    total_h_spacing = spacing * (columns - 1)
    total_v_spacing = spacing * (rows - 1)
    
    item_width = (container_width - total_h_spacing) / columns
    item_height = (container_height - total_v_spacing) / rows
    
    # Ensure minimum item size
    item_width = max(1.0, item_width)
    item_height = max(0.75, item_height)
    
    positions = []
    for i in range(num_items):
        row = i // columns
        col = i % columns
        
        left = container_left + col * (item_width + spacing)
        top = container_top + row * (item_height + spacing)
        
        # Validate each position
        left, top, width, height = validate_position(left, top, item_width, item_height)
        
        positions.append({
            'left': left,
            'top': top, 
            'width': width,
            'height': height
        })
        
    return positions


def get_logo_position(
    position: str,
    size: float = 1.0,
    margin: float = 0.5,
    aspect_ratio: str = "16:9"
) -> Dict[str, float]:
    """
    Get standard logo position coordinates.
    
    Args:
        position: Position name (e.g., "top-left", "bottom-right")
        size: Logo size in inches
        margin: Margin from edges in inches
        aspect_ratio: Slide aspect ratio
        
    Returns:
        Dictionary with 'left', 'top', 'width', 'height'
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3
    
    positions = {
        "top-left": (margin, margin),
        "top-center": ((slide_width - size) / 2, margin),
        "top-right": (slide_width - size - margin, margin),
        "center-left": (margin, (slide_height - size) / 2),
        "center": ((slide_width - size) / 2, (slide_height - size) / 2),
        "center-right": (slide_width - size - margin, (slide_height - size) / 2),
        "bottom-left": (margin, slide_height - size - margin),
        "bottom-center": ((slide_width - size) / 2, slide_height - size - margin),
        "bottom-right": (slide_width - size - margin, slide_height - size - margin)
    }
    
    left, top = positions.get(position, positions["top-right"])
    
    # Validate position
    left, top, width, height = validate_position(left, top, size, size, aspect_ratio)
    
    return {
        'left': left,
        'top': top,
        'width': width,
        'height': height
    }


def get_safe_content_area(
    has_title: bool = True,
    aspect_ratio: str = "16:9"
) -> Dict[str, float]:
    """
    Get the safe content area for placing elements.
    
    Args:
        has_title: Whether the slide has a title
        aspect_ratio: Slide aspect ratio
        
    Returns:
        Dictionary with 'left', 'top', 'width', 'height'
    """
    top_margin = MARGIN_TOP if has_title else 0.5
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3
    
    return {
        'left': CONTENT_LEFT,
        'top': top_margin,
        'width': CONTENT_WIDTH,
        'height': slide_height - top_margin - MARGIN_BOTTOM
    }


def distribute_horizontally(
    num_items: int,
    item_width: float,
    item_height: float,
    top: float = CONTENT_TOP,
    container_width: float = CONTENT_WIDTH,
    container_left: float = CONTENT_LEFT,
    min_spacing: float = 0.2
) -> List[Dict[str, float]]:
    """
    Distribute items horizontally with equal spacing.
    
    Args:
        num_items: Number of items
        item_width: Width of each item
        item_height: Height of each item
        top: Top position for all items
        container_width: Width of container area
        container_left: Left position of container
        min_spacing: Minimum spacing between items
        
    Returns:
        List of position dictionaries
    """
    if num_items == 0:
        return []
        
    total_items_width = num_items * item_width
    available_space = container_width - total_items_width
    
    if available_space < 0:
        # Items don't fit - scale them down
        item_width = (container_width - min_spacing * (num_items - 1)) / num_items
        spacing = min_spacing
    else:
        spacing = max(min_spacing, available_space / (num_items + 1))
        
    positions = []
    for i in range(num_items):
        left = container_left + spacing + i * (item_width + spacing)
        
        # Validate position
        left, top_adj, width, height = validate_position(left, top, item_width, item_height)
        
        positions.append({
            'left': left,
            'top': top_adj,
            'width': width,
            'height': height
        })
        
    return positions


def center_element(
    width: float,
    height: float,
    horizontal: bool = True,
    vertical: bool = True,
    aspect_ratio: str = "16:9"
) -> Dict[str, float]:
    """
    Center an element on the slide.
    
    Args:
        width: Element width
        height: Element height
        horizontal: Center horizontally
        vertical: Center vertically
        aspect_ratio: Slide aspect ratio
        
    Returns:
        Dictionary with 'left', 'top', 'width', 'height'
    """
    slide_width = SLIDE_WIDTH
    slide_height = SLIDE_HEIGHT if aspect_ratio == "16:9" else SLIDE_HEIGHT_4_3
    
    left = ((slide_width - width) / 2) if horizontal else CONTENT_LEFT
    top = ((slide_height - height) / 2) if vertical else CONTENT_TOP
    
    # Validate position
    left, top, width, height = validate_position(left, top, width, height, aspect_ratio)
    
    return {
        'left': left,
        'top': top,
        'width': width,
        'height': height
    }