"""
Tests for components/tracking.py

Comprehensive tests for component tracking registry for >90% coverage.
"""

import pytest
from chuk_mcp_pptx.components.tracking import (
    ComponentInstance,
    ComponentTracker,
    component_tracker,
)


class TestComponentInstance:
    """Tests for ComponentInstance dataclass."""

    def test_basic_creation(self):
        """Test creating a basic component instance."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Badge",
            slide_index=0,
        )
        assert instance.component_id == "test_id"
        assert instance.component_type == "Badge"
        assert instance.slide_index == 0

    def test_creation_with_position(self):
        """Test creating instance with position."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Card",
            slide_index=1,
            left=1.0,
            top=2.0,
            width=3.0,
            height=4.0,
        )
        assert instance.left == 1.0
        assert instance.top == 2.0
        assert instance.width == 3.0
        assert instance.height == 4.0

    def test_creation_with_relationships(self):
        """Test creating instance with parent/children."""
        instance = ComponentInstance(
            component_id="child_id",
            component_type="Badge",
            slide_index=0,
            parent_id="parent_id",
            children_ids=["grandchild1", "grandchild2"],
        )
        assert instance.parent_id == "parent_id"
        assert instance.children_ids == ["grandchild1", "grandchild2"]

    def test_creation_with_target_info(self):
        """Test creating instance with target information."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Text",
            slide_index=0,
            target_type="placeholder",
            target_id=1,
        )
        assert instance.target_type == "placeholder"
        assert instance.target_id == 1

    def test_creation_with_params(self):
        """Test creating instance with params."""
        params = {"text": "Hello", "color": "blue"}
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Text",
            slide_index=0,
            params=params,
        )
        assert instance.params == params

    def test_creation_with_theme(self):
        """Test creating instance with theme."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Badge",
            slide_index=0,
            theme="dark-violet",
        )
        assert instance.theme == "dark-violet"

    def test_creation_with_shape_index(self):
        """Test creating instance with shape index."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Shape",
            slide_index=0,
            shape_index=5,
        )
        assert instance.shape_index == 5

    def test_creation_with_instance_object(self):
        """Test creating with component instance object."""

        class MockComponent:
            pass

        mock_comp = MockComponent()
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Stack",
            slide_index=0,
            instance=mock_comp,
        )
        assert instance.instance is mock_comp

    def test_default_values(self):
        """Test default values for optional fields."""
        instance = ComponentInstance(
            component_id="test_id",
            component_type="Badge",
            slide_index=0,
        )
        assert instance.left is None
        assert instance.top is None
        assert instance.width is None
        assert instance.height is None
        assert instance.parent_id is None
        assert instance.children_ids == []
        assert instance.target_type is None
        assert instance.target_id is None
        assert instance.params == {}
        assert instance.theme is None
        assert instance.shape_index is None
        assert instance.instance is None


class TestComponentTracker:
    """Tests for ComponentTracker class."""

    @pytest.fixture
    def tracker(self):
        """Create a fresh tracker for each test."""
        return ComponentTracker()

    def test_init(self, tracker):
        """Test tracker initialization."""
        assert tracker._instances == {}

    def test_register_basic(self, tracker):
        """Test basic component registration."""
        instance = tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=2.0,
            width=3.0,
            height=4.0,
        )

        assert instance.component_id == "comp1"
        assert instance.component_type == "Badge"
        assert instance.left == 1.0
        assert instance.top == 2.0

    def test_register_creates_nested_dicts(self, tracker):
        """Test that register creates nested dicts for new presentation/slide."""
        tracker.register(
            presentation="new_pres",
            slide_index=5,
            component_id="comp1",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=2.0,
            height=2.0,
        )

        assert "new_pres" in tracker._instances
        assert 5 in tracker._instances["new_pres"]
        assert "comp1" in tracker._instances["new_pres"][5]

    def test_register_with_parent(self, tracker):
        """Test registering component with parent."""
        # Register parent first
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=4.0,
            height=3.0,
        )

        # Register child with parent
        child = tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child",
            component_type="Badge",
            left=1.5,
            top=1.5,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )

        # Child should have parent_id set
        assert child.parent_id == "parent"

        # Parent should have child in children_ids
        parent = tracker.get("test_pres", 0, "parent")
        assert "child" in parent.children_ids

    def test_register_with_all_optional_params(self, tracker):
        """Test registration with all optional parameters."""
        mock_instance = object()
        instance = tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="full_comp",
            component_type="Stack",
            left=1.0,
            top=2.0,
            width=3.0,
            height=4.0,
            target_type="placeholder",
            target_id=1,
            parent_id=None,
            params={"direction": "vertical"},
            theme="dark-blue",
            shape_index=10,
            instance=mock_instance,
        )

        assert instance.target_type == "placeholder"
        assert instance.target_id == 1
        assert instance.params == {"direction": "vertical"}
        assert instance.theme == "dark-blue"
        assert instance.shape_index == 10
        assert instance.instance is mock_instance

    def test_get_existing(self, tracker):
        """Test getting an existing component."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.get("test_pres", 0, "comp1")
        assert result is not None
        assert result.component_id == "comp1"

    def test_get_nonexistent_presentation(self, tracker):
        """Test getting from nonexistent presentation."""
        result = tracker.get("nonexistent", 0, "comp1")
        assert result is None

    def test_get_nonexistent_slide(self, tracker):
        """Test getting from nonexistent slide."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.get("test_pres", 99, "comp1")
        assert result is None

    def test_get_nonexistent_component(self, tracker):
        """Test getting nonexistent component."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.get("test_pres", 0, "nonexistent")
        assert result is None

    def test_get_children(self, tracker):
        """Test getting children of a component."""
        # Register parent
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=4.0,
            height=3.0,
        )

        # Register children
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child1",
            component_type="Badge",
            left=1.2,
            top=1.2,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child2",
            component_type="Text",
            left=1.2,
            top=2.0,
            width=2.0,
            height=0.5,
            parent_id="parent",
        )

        children = tracker.get_children("test_pres", 0, "parent")
        assert len(children) == 2
        assert any(c.component_id == "child1" for c in children)
        assert any(c.component_id == "child2" for c in children)

    def test_get_children_empty(self, tracker):
        """Test getting children when there are none."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="lonely",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        children = tracker.get_children("test_pres", 0, "lonely")
        assert children == []

    def test_get_children_nonexistent_parent(self, tracker):
        """Test getting children of nonexistent component."""
        children = tracker.get_children("test_pres", 0, "nonexistent")
        assert children == []

    def test_get_parent(self, tracker):
        """Test getting parent of a component."""
        # Register parent
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=4.0,
            height=3.0,
        )

        # Register child
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child",
            component_type="Badge",
            left=1.2,
            top=1.2,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )

        parent = tracker.get_parent("test_pres", 0, "child")
        assert parent is not None
        assert parent.component_id == "parent"

    def test_get_parent_no_parent(self, tracker):
        """Test getting parent when component has no parent."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="orphan",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        parent = tracker.get_parent("test_pres", 0, "orphan")
        assert parent is None

    def test_get_parent_nonexistent_component(self, tracker):
        """Test getting parent of nonexistent component."""
        parent = tracker.get_parent("test_pres", 0, "nonexistent")
        assert parent is None

    def test_list_on_slide(self, tracker):
        """Test listing all components on a slide."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp2",
            component_type="Text",
            left=2.0,
            top=1.0,
            width=2.0,
            height=0.5,
        )
        tracker.register(
            presentation="test_pres",
            slide_index=1,  # Different slide
            component_id="comp3",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=3.0,
            height=2.0,
        )

        components = tracker.list_on_slide("test_pres", 0)
        assert len(components) == 2
        assert all(c.slide_index == 0 for c in components)

    def test_list_on_slide_empty(self, tracker):
        """Test listing components on empty slide."""
        components = tracker.list_on_slide("test_pres", 0)
        assert components == []

    def test_list_on_slide_nonexistent_presentation(self, tracker):
        """Test listing components from nonexistent presentation."""
        components = tracker.list_on_slide("nonexistent", 0)
        assert components == []

    def test_compute_absolute_position_no_parent(self, tracker):
        """Test absolute position for component without parent."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=2.0,
            top=3.0,
            width=1.0,
            height=0.5,
        )

        pos = tracker.compute_absolute_position("test_pres", 0, "comp1")
        assert pos == (2.0, 3.0, 1.0, 0.5)

    def test_compute_absolute_position_with_parent(self, tracker):
        """Test absolute position for nested component."""
        # Parent at (1, 1)
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=4.0,
            height=3.0,
        )

        # Child at relative (0.5, 0.5) from parent
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child",
            component_type="Badge",
            left=0.5,
            top=0.5,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )

        pos = tracker.compute_absolute_position("test_pres", 0, "child")
        # Absolute: (1 + 0.5, 1 + 0.5, 1, 0.5)
        assert pos == (1.5, 1.5, 1.0, 0.5)

    def test_compute_absolute_position_deeply_nested(self, tracker):
        """Test absolute position for deeply nested component."""
        # Grandparent at (1, 1)
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="grandparent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=6.0,
            height=5.0,
        )

        # Parent at relative (0.5, 0.5)
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=0.5,
            top=0.5,
            width=4.0,
            height=3.0,
            parent_id="grandparent",
        )

        # Child at relative (0.2, 0.2)
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child",
            component_type="Badge",
            left=0.2,
            top=0.2,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )

        pos = tracker.compute_absolute_position("test_pres", 0, "child")
        # Absolute: (1 + 0.5 + 0.2, 1 + 0.5 + 0.2, 1, 0.5)
        assert pos == (1.7, 1.7, 1.0, 0.5)

    def test_compute_absolute_position_nonexistent(self, tracker):
        """Test absolute position for nonexistent component."""
        pos = tracker.compute_absolute_position("test_pres", 0, "nonexistent")
        assert pos is None

    def test_get_bounds(self, tracker):
        """Test getting component bounds."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=2.0,
            width=3.0,
            height=4.0,
        )

        bounds = tracker.get_bounds("test_pres", 0, "comp1")
        assert bounds == (1.0, 2.0, 3.0, 4.0)

    def test_get_bounds_nonexistent(self, tracker):
        """Test getting bounds for nonexistent component."""
        bounds = tracker.get_bounds("test_pres", 0, "nonexistent")
        assert bounds is None

    def test_update_position(self, tracker):
        """Test updating component position."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            left=2.0,
            top=2.0,
        )

        assert result is True
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp.left == 2.0
        assert comp.top == 2.0

    def test_update_size(self, tracker):
        """Test updating component size."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            width=2.0,
            height=1.0,
        )

        assert result is True
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp.width == 2.0
        assert comp.height == 1.0

    def test_update_params(self, tracker):
        """Test updating component params."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
            params={"text": "Original"},
        )

        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            params={"text": "Updated"},
        )

        assert result is True
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp.params == {"text": "Updated"}

    def test_update_theme(self, tracker):
        """Test updating component theme."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
            theme="dark",
        )

        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            theme="light",
        )

        assert result is True
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp.theme == "light"

    def test_update_shape_index(self, tracker):
        """Test updating shape index."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
            shape_index=5,
        )

        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            shape_index=10,
        )

        assert result is True
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp.shape_index == 10

    def test_update_nonexistent(self, tracker):
        """Test updating nonexistent component."""
        result = tracker.update(
            presentation="test_pres",
            slide_index=0,
            component_id="nonexistent",
            left=1.0,
        )

        assert result is False

    def test_remove_basic(self, tracker):
        """Test removing a component."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        result = tracker.remove("test_pres", 0, "comp1")
        assert result is True

        # Should no longer exist
        comp = tracker.get("test_pres", 0, "comp1")
        assert comp is None

    def test_remove_updates_parent_children(self, tracker):
        """Test removing child updates parent's children_ids."""
        # Register parent
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="parent",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=4.0,
            height=3.0,
        )

        # Register child
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="child",
            component_type="Badge",
            left=1.2,
            top=1.2,
            width=1.0,
            height=0.5,
            parent_id="parent",
        )

        # Remove child
        tracker.remove("test_pres", 0, "child")

        # Parent's children_ids should not contain child
        parent = tracker.get("test_pres", 0, "parent")
        assert "child" not in parent.children_ids

    def test_remove_nonexistent(self, tracker):
        """Test removing nonexistent component."""
        result = tracker.remove("test_pres", 0, "nonexistent")
        assert result is False

    def test_clear_slide(self, tracker):
        """Test clearing all components from a slide."""
        # Register multiple components
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp2",
            component_type="Text",
            left=2.0,
            top=1.0,
            width=2.0,
            height=0.5,
        )
        tracker.register(
            presentation="test_pres",
            slide_index=1,  # Different slide
            component_id="comp3",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=3.0,
            height=2.0,
        )

        tracker.clear_slide("test_pres", 0)

        # Slide 0 should be empty
        assert tracker.list_on_slide("test_pres", 0) == []

        # Slide 1 should still have components
        assert len(tracker.list_on_slide("test_pres", 1)) == 1

    def test_clear_slide_nonexistent_presentation(self, tracker):
        """Test clearing slide from nonexistent presentation (no error)."""
        tracker.clear_slide("nonexistent", 0)
        # Should not raise error

    def test_clear_slide_nonexistent_slide(self, tracker):
        """Test clearing nonexistent slide (no error)."""
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )

        tracker.clear_slide("test_pres", 99)
        # Should not raise error, and slide 0 should still have components
        assert len(tracker.list_on_slide("test_pres", 0)) == 1

    def test_clear_presentation(self, tracker):
        """Test clearing all components from a presentation."""
        # Register components on multiple slides
        tracker.register(
            presentation="test_pres",
            slide_index=0,
            component_id="comp1",
            component_type="Badge",
            left=1.0,
            top=1.0,
            width=1.0,
            height=0.5,
        )
        tracker.register(
            presentation="test_pres",
            slide_index=1,
            component_id="comp2",
            component_type="Text",
            left=1.0,
            top=1.0,
            width=2.0,
            height=0.5,
        )
        tracker.register(
            presentation="other_pres",
            slide_index=0,
            component_id="comp3",
            component_type="Card",
            left=1.0,
            top=1.0,
            width=3.0,
            height=2.0,
        )

        tracker.clear_presentation("test_pres")

        # test_pres should have no components
        assert tracker.list_on_slide("test_pres", 0) == []
        assert tracker.list_on_slide("test_pres", 1) == []

        # other_pres should still have components
        assert len(tracker.list_on_slide("other_pres", 0)) == 1

    def test_clear_presentation_nonexistent(self, tracker):
        """Test clearing nonexistent presentation (no error)."""
        tracker.clear_presentation("nonexistent")
        # Should not raise error


class TestGlobalComponentTracker:
    """Test the global component_tracker instance."""

    def test_global_tracker_exists(self):
        """Test that global tracker exists."""
        assert component_tracker is not None
        assert isinstance(component_tracker, ComponentTracker)

    def test_global_tracker_is_shared(self):
        """Test that global tracker is the same instance across imports."""
        from chuk_mcp_pptx.components.tracking import (
            component_tracker as tracker2,
        )

        assert component_tracker is tracker2
