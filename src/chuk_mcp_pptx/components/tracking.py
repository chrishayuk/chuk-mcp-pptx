"""
Component Tracking Registry

Tracks component instances on slides for composition, targeting, and relationships.
Enables component-in-component nesting and querying.
"""

import logging
from typing import Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ComponentInstance:
    """
    Instance of a component on a slide.

    Tracks position, relationships, and metadata for composition.
    """

    component_id: str
    component_type: str
    slide_index: int

    # Position and bounds
    left: float | None = None  # inches
    top: float | None = None  # inches
    width: float | None = None  # inches
    height: float | None = None  # inches

    # Relationships
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)

    # Target information
    target_type: str | None = None  # "placeholder", "component", "layout", "free-form"
    target_id: Any | None = None  # placeholder_idx, component_id, layout_name

    # Component metadata
    params: dict = field(default_factory=dict)
    theme: str | None = None

    # Shape reference (for updates/removal)
    shape_index: int | None = None

    # Component instance (for layout components like Stack)
    instance: Any | None = None


class ComponentTracker:
    """
    Tracks component instances across presentations for composition.

    Enables:
    - Component-in-component nesting
    - Query by ID
    - Relationship tracking (parent/child)
    - Position management
    """

    def __init__(self):
        # presentation_name -> slide_index -> component_id -> ComponentInstance
        self._instances: dict[str, dict[int, dict[str, ComponentInstance]]] = {}

    def register(
        self,
        presentation: str,
        slide_index: int,
        component_id: str,
        component_type: str,
        left: float | None,
        top: float | None,
        width: float | None,
        height: float | None,
        target_type: str | None = None,
        target_id: Any | None = None,
        parent_id: str | None = None,
        params: dict | None = None,
        theme: str | None = None,
        shape_index: int | None = None,
        instance: Any | None = None,
    ) -> ComponentInstance:
        """
        Register a component instance.

        Args:
            presentation: Presentation name
            slide_index: Slide index
            component_id: Unique component ID
            component_type: Component type (e.g., "metric_card")
            left, top, width, height: Position and size in inches
            target_type: Target type ("placeholder", "component", "layout", "free-form")
            target_id: Target identifier
            parent_id: Parent component ID (for nesting)
            params: Component parameters
            theme: Theme override
            shape_index: Shape index in slide.shapes

        Returns:
            ComponentInstance
        """
        if presentation not in self._instances:
            self._instances[presentation] = {}

        if slide_index not in self._instances[presentation]:
            self._instances[presentation][slide_index] = {}

        comp_instance = ComponentInstance(
            component_id=component_id,
            component_type=component_type,
            slide_index=slide_index,
            left=left,
            top=top,
            width=width,
            height=height,
            parent_id=parent_id,
            target_type=target_type,
            target_id=target_id,
            params=params or {},
            theme=theme,
            shape_index=shape_index,
            instance=instance,
        )

        self._instances[presentation][slide_index][component_id] = comp_instance

        # Update parent's children list
        if parent_id:
            parent = self.get(presentation, slide_index, parent_id)
            if parent:
                parent.children_ids.append(component_id)
                logger.debug(f"Registered {component_id} as child of {parent_id}")

        logger.info(
            f"Registered component: {component_id} ({component_type}) on slide {slide_index}"
        )
        return comp_instance

    def get(
        self, presentation: str, slide_index: int, component_id: str
    ) -> ComponentInstance | None:
        """Get component instance by ID."""
        return self._instances.get(presentation, {}).get(slide_index, {}).get(component_id)

    def get_children(
        self, presentation: str, slide_index: int, component_id: str
    ) -> list[ComponentInstance]:
        """Get all children of a component."""
        instance = self.get(presentation, slide_index, component_id)
        if not instance:
            return []

        children = []
        for child_id in instance.children_ids:
            child = self.get(presentation, slide_index, child_id)
            if child:
                children.append(child)

        return children

    def get_parent(
        self, presentation: str, slide_index: int, component_id: str
    ) -> ComponentInstance | None:
        """Get parent of a component."""
        instance = self.get(presentation, slide_index, component_id)
        if not instance or not instance.parent_id:
            return None

        return self.get(presentation, slide_index, instance.parent_id)

    def list_on_slide(self, presentation: str, slide_index: int) -> list[ComponentInstance]:
        """List all components on a slide."""
        return list(self._instances.get(presentation, {}).get(slide_index, {}).values())

    def compute_absolute_position(
        self, presentation: str, slide_index: int, component_id: str
    ) -> tuple[float, float, float, float] | None:
        """
        Compute absolute position of a component considering parent offsets.

        If component is nested, adds parent's position to compute absolute position.

        Returns:
            (left, top, width, height) in inches, or None if not found
        """
        instance = self.get(presentation, slide_index, component_id)
        if not instance:
            return None

        left, top = instance.left, instance.top
        width, height = instance.width, instance.height

        # Walk up parent chain to compute absolute position
        current = instance
        while current.parent_id:
            parent = self.get(presentation, slide_index, current.parent_id)
            if not parent:
                break

            # Add parent's position
            left += parent.left
            top += parent.top
            current = parent

        return (left, top, width, height)

    def get_bounds(
        self, presentation: str, slide_index: int, component_id: str
    ) -> tuple[float, float, float, float] | None:
        """
        Get component bounds (position + size).

        Returns:
            (left, top, width, height) in inches
        """
        instance = self.get(presentation, slide_index, component_id)
        if not instance:
            return None

        return (instance.left, instance.top, instance.width, instance.height)

    def update(
        self,
        presentation: str,
        slide_index: int,
        component_id: str,
        left: float | None = None,
        top: float | None = None,
        width: float | None = None,
        height: float | None = None,
        params: dict | None = None,
        theme: str | None = None,
        shape_index: int | None = None,
    ) -> bool:
        """
        Update a component's properties.

        Args:
            presentation: Presentation name
            slide_index: Slide index
            component_id: Component ID to update
            left, top, width, height: New position/size (optional)
            params: New params (optional)
            theme: New theme (optional)
            shape_index: New shape index (optional)

        Returns:
            True if updated, False if not found
        """
        instance = self.get(presentation, slide_index, component_id)
        if not instance:
            return False

        # Update properties if provided
        if left is not None:
            instance.left = left
        if top is not None:
            instance.top = top
        if width is not None:
            instance.width = width
        if height is not None:
            instance.height = height
        if params is not None:
            instance.params = params
        if theme is not None:
            instance.theme = theme
        if shape_index is not None:
            instance.shape_index = shape_index

        logger.info(f"Updated component: {component_id}")
        return True

    def remove(self, presentation: str, slide_index: int, component_id: str) -> bool:
        """Remove a component from tracking."""
        instance = self.get(presentation, slide_index, component_id)
        if not instance:
            return False

        # Remove from parent's children list
        if instance.parent_id:
            parent = self.get(presentation, slide_index, instance.parent_id)
            if parent and component_id in parent.children_ids:
                parent.children_ids.remove(component_id)

        # Remove from tracking
        del self._instances[presentation][slide_index][component_id]
        logger.info(f"Removed component: {component_id}")
        return True

    def clear_slide(self, presentation: str, slide_index: int):
        """Clear all components from a slide."""
        if presentation in self._instances and slide_index in self._instances[presentation]:
            count = len(self._instances[presentation][slide_index])
            self._instances[presentation][slide_index].clear()
            logger.info(f"Cleared {count} components from slide {slide_index}")

    def clear_presentation(self, presentation: str):
        """Clear all components from a presentation."""
        if presentation in self._instances:
            total = sum(len(slides) for slides in self._instances[presentation].values())
            del self._instances[presentation]
            logger.info(f"Cleared {total} components from presentation '{presentation}'")


# Global component tracker instance
component_tracker = ComponentTracker()
