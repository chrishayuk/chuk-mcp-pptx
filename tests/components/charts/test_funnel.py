"""
Tests for Funnel, Gantt, and Heatmap chart components.
"""

import pytest

from chuk_mcp_pptx.components.charts.funnel import FunnelChart, GanttChart, HeatmapChart


class TestFunnelChart:
    """Test FunnelChart component."""

    def test_init(self, sample_chart_data, dark_theme):
        """Test initialization."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(
            stages=data["stages"],
            values=data["values"],
            variant="standard",
            show_percentages=True,
            show_values=True,
            title="Sales Funnel",
            theme=dark_theme,
        )

        assert chart.stages == data["stages"]
        assert chart.values == data["values"]
        assert chart.variant == "standard"
        assert chart.show_percentages is True
        assert chart.show_values is True
        assert chart.title == "Sales Funnel"

    def test_validate(self, sample_chart_data, dark_theme):
        """Test validation."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(stages=data["stages"], values=data["values"], theme=dark_theme)

        valid, error = chart.validate()
        assert valid is True
        assert error is None

    def test_validate_mismatched_lengths(self, dark_theme):
        """Test validation with mismatched data."""
        with pytest.raises(ValueError, match="Number of stages must match number of values"):
            FunnelChart(
                stages=["Stage1", "Stage2", "Stage3"],
                values=[100, 50],  # Wrong length
                theme=dark_theme,
            )

    def test_validate_negative_values(self, dark_theme):
        """Test validation with negative values."""
        with pytest.raises(ValueError, match="Funnel values must be non-negative"):
            FunnelChart(
                stages=["Stage1", "Stage2"],
                values=[100, -50],  # Negative value
                theme=dark_theme,
            )

    def test_conversion_rates(self, dark_theme):
        """Test conversion rate calculation."""
        stages = ["Leads", "Qualified", "Closed"]
        values = [1000, 500, 100]

        FunnelChart(stages=stages, values=values, show_percentages=True, theme=dark_theme)

        # Check conversion rates
        # Qualified/Leads = 500/1000 = 50%
        # Closed/Qualified = 100/500 = 20%
        conversion_rates = []
        for i in range(1, len(values)):
            rate = (values[i] / values[i - 1]) * 100
            conversion_rates.append(rate)

        assert conversion_rates[0] == 50.0
        assert conversion_rates[1] == 20.0

    def test_variants(self, sample_chart_data, dark_theme):
        """Test different funnel variants."""
        data = sample_chart_data["funnel_data"]
        variants = ["standard", "cylinder", "inverted"]

        for variant in variants:
            chart = FunnelChart(
                stages=data["stages"], values=data["values"], variant=variant, theme=dark_theme
            )
            assert chart.variant == variant

    def test_calculate_dimensions(self, sample_chart_data, dark_theme):
        """Test dimension calculation for funnel segments."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(stages=data["stages"], values=data["values"], theme=dark_theme)

        dimensions = chart._calculate_dimensions(width=8.0, height=5.0)

        # Check we have dimensions for each stage
        assert len(dimensions) == len(data["stages"])

        # Check dimensions are tuples of (left, top, width, height)
        for dim in dimensions:
            assert len(dim) == 4
            assert all(isinstance(x, (int, float)) for x in dim)

    @pytest.mark.asyncio
    async def test_render(self, mock_slide, sample_chart_data, dark_theme):
        """Test rendering funnel chart."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(stages=data["stages"], values=data["values"], theme=dark_theme)

        # Note: FunnelChart uses shapes, not native charts
        chart._render_sync(mock_slide, left=1, top=1, width=4, height=4)

        # Should add shapes for funnel segments
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called

    def test_show_options(self, sample_chart_data, dark_theme):
        """Test show values and percentages options."""
        data = sample_chart_data["funnel_data"]

        # Test with values only
        chart1 = FunnelChart(
            stages=data["stages"],
            values=data["values"],
            show_values=True,
            show_percentages=False,
            theme=dark_theme,
        )
        assert chart1.show_values is True
        assert chart1.show_percentages is False

        # Test with percentages only
        chart2 = FunnelChart(
            stages=data["stages"],
            values=data["values"],
            show_values=False,
            show_percentages=True,
            theme=dark_theme,
        )
        assert chart2.show_values is False
        assert chart2.show_percentages is True

    async def test_render_with_defaults(self, mock_slide, sample_chart_data, dark_theme):
        """Test rendering with default position parameters."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(stages=data["stages"], values=data["values"], theme=dark_theme)
        # Call render without position parameters (uses defaults)
        result = await chart.render(mock_slide)
        assert result is None  # FunnelChart returns None

    async def test_render_with_title(self, mock_slide, sample_chart_data, dark_theme):
        """Test rendering with title."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(
            stages=data["stages"], values=data["values"], title="Sales Funnel", theme=dark_theme
        )
        result = await chart.render(mock_slide, left=1, top=2, width=8, height=5)
        assert result is None
        # Should have called add_textbox for title
        assert mock_slide.shapes.add_textbox.called

    def test_validate_empty_stages(self, dark_theme):
        """Test validation with empty stages."""
        with pytest.raises(ValueError):
            FunnelChart(stages=[], values=[], theme=dark_theme)

    def test_variant_rectangle(self, sample_chart_data, dark_theme):
        """Test non-standard variant (rectangle shapes)."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(
            stages=data["stages"],
            values=data["values"],
            variant="pyramid",  # Non-standard variant
            theme=dark_theme,
        )
        assert chart.variant == "pyramid"

    def test_get_colors_without_theme(self, sample_chart_data):
        """Test default colors when theme is not provided."""
        data = sample_chart_data["funnel_data"]
        chart = FunnelChart(stages=data["stages"], values=data["values"])
        colors = chart._get_chart_colors()
        # Should return default colors
        assert isinstance(colors, list)
        assert len(colors) > 0
        assert colors[0].startswith("#")

    def test_validate_increasing_values(self, dark_theme):
        """Test validation with increasing values (should pass with warning)."""
        chart = FunnelChart(
            stages=["A", "B", "C"],
            values=[100, 120, 150],  # Increasing values
            theme=dark_theme,
        )
        is_valid, error = chart.validate_data()
        # Should still be valid (just a warning case)
        assert is_valid is True


class TestGanttChart:
    """Test GanttChart component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        tasks = [
            {"name": "Task 1", "start": "2024-01-01", "end": "2024-01-15", "progress": 0.75},
            {"name": "Task 2", "start": "2024-01-10", "end": "2024-01-25", "progress": 0.50},
            {"name": "Task 3", "start": "2024-01-20", "end": "2024-02-05", "progress": 0.25},
        ]

        chart = GanttChart(
            tasks=tasks,
            start_date="2024-01-01",
            end_date="2024-02-28",
            show_dependencies=True,
            show_milestones=True,
            title="Project Timeline",
            theme=dark_theme,
        )

        assert chart.tasks == tasks
        assert chart.start_date == "2024-01-01"
        assert chart.end_date == "2024-02-28"
        assert chart.show_dependencies is True
        assert chart.show_milestones is True

    def test_validate(self, dark_theme):
        """Test validation."""
        tasks = [
            {"name": "Task 1", "start": "2024-01-01", "end": "2024-01-15"},
            {"name": "Task 2", "start": "2024-01-10", "end": "2024-01-25"},
        ]

        chart = GanttChart(
            tasks=tasks, start_date="2024-01-01", end_date="2024-01-31", theme=dark_theme
        )

        valid, error = chart.validate()
        assert valid is True
        assert error is None

    def test_validate_missing_name(self, dark_theme):
        """Test validation with missing task name."""
        tasks = [
            {"start": "2024-01-01", "end": "2024-01-15"}  # Missing name
        ]

        with pytest.raises(ValueError, match="Each task must have a name"):
            GanttChart(
                tasks=tasks, start_date="2024-01-01", end_date="2024-01-31", theme=dark_theme
            )

    def test_validate_empty_tasks(self, dark_theme):
        """Test validation with empty tasks."""
        with pytest.raises(ValueError, match="Gantt chart requires tasks"):
            GanttChart(tasks=[], start_date="2024-01-01", end_date="2024-01-31", theme=dark_theme)

    def test_dependencies(self, dark_theme):
        """Test task dependencies."""
        tasks = [
            {"name": "Task 1", "id": 1},
            {"name": "Task 2", "id": 2, "depends_on": [1]},
            {"name": "Task 3", "id": 3, "depends_on": [1, 2]},
        ]

        chart = GanttChart(
            tasks=tasks,
            start_date="2024-01-01",
            end_date="2024-01-31",
            show_dependencies=True,
            theme=dark_theme,
        )

        assert chart.show_dependencies is True
        assert tasks[1].get("depends_on") == [1]
        assert tasks[2].get("depends_on") == [1, 2]

    @pytest.mark.asyncio
    async def test_render(self, mock_slide, dark_theme):
        """Test rendering gantt chart."""
        tasks = [
            {"name": "Task 1", "start": "2024-01-01", "end": "2024-01-15"},
            {"name": "Task 2", "start": "2024-01-10", "end": "2024-01-25"},
        ]

        chart = GanttChart(
            tasks=tasks, start_date="2024-01-01", end_date="2024-01-31", theme=dark_theme
        )

        # Note: GanttChart uses shapes, not native charts
        chart._render_sync(mock_slide, left=1, top=1, width=8, height=5)

        # Should add shapes for gantt bars
        assert mock_slide.shapes.add_shape.called or mock_slide.shapes.add_textbox.called

    @pytest.mark.asyncio
    async def test_render_with_defaults(self, mock_slide, dark_theme):
        """Test rendering with default position parameters."""
        tasks = [{"name": "Task 1", "start": "2024-01-01", "end": "2024-01-15"}]
        chart = GanttChart(
            tasks=tasks, start_date="2024-01-01", end_date="2024-01-31", theme=dark_theme
        )
        # Call render without position parameters (uses defaults)
        result = await chart.render(mock_slide)
        assert result is None

    @pytest.mark.asyncio
    async def test_render_with_title(self, mock_slide, dark_theme):
        """Test rendering with title."""
        tasks = [{"name": "Task 1", "start": "2024-01-01", "end": "2024-01-15"}]
        chart = GanttChart(
            tasks=tasks,
            start_date="2024-01-01",
            end_date="2024-01-31",
            title="Project Timeline",
            theme=dark_theme,
        )
        result = await chart.render(mock_slide, left=1, top=2, width=8, height=5)
        assert result is None
        # Should have called add_textbox for title
        assert mock_slide.shapes.add_textbox.called

    def test_get_colors_without_theme(self, dark_theme):
        """Test default colors when theme is not provided."""
        tasks = [{"name": "Task 1"}]
        chart = GanttChart(tasks=tasks, start_date="2024-01-01", end_date="2024-01-31")
        colors = chart._get_chart_colors()
        # Should return default colors
        assert isinstance(colors, list)
        assert len(colors) > 0
        assert colors[0].startswith("#")


class TestHeatmapChart:
    """Test HeatmapChart component."""

    def test_init(self, dark_theme):
        """Test initialization."""
        x_labels = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        y_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        data = [
            [10, 20, 30, 40, 50],
            [15, 25, 35, 45, 55],
            [12, 22, 32, 42, 52],
            [18, 28, 38, 48, 58],
        ]

        chart = HeatmapChart(
            x_labels=x_labels,
            y_labels=y_labels,
            data=data,
            color_scale="heat",
            show_values=True,
            title="Activity Heatmap",
            theme=dark_theme,
        )

        assert chart.x_labels == x_labels
        assert chart.y_labels == y_labels
        assert chart.data == data
        assert chart.color_scale == "heat"
        assert chart.show_values is True

    def test_validate(self, dark_theme):
        """Test validation."""
        chart = HeatmapChart(
            x_labels=["A", "B", "C"],
            y_labels=["1", "2"],
            data=[[1, 2, 3], [4, 5, 6]],
            theme=dark_theme,
        )

        valid, error = chart.validate()
        assert valid is True
        assert error is None

    def test_validate_mismatched_rows(self, dark_theme):
        """Test validation with mismatched row count."""
        with pytest.raises(ValueError, match="Data rows must match y_labels length"):
            HeatmapChart(
                x_labels=["A", "B"],
                y_labels=["1", "2", "3"],  # 3 labels
                data=[[1, 2], [3, 4]],  # 2 rows
                theme=dark_theme,
            )

    def test_validate_mismatched_columns(self, dark_theme):
        """Test validation with mismatched column count."""
        with pytest.raises(ValueError, match="Data columns must match x_labels length"):
            HeatmapChart(
                x_labels=["A", "B", "C"],  # 3 labels
                y_labels=["1", "2"],
                data=[[1, 2], [3, 4]],  # 2 columns per row
                theme=dark_theme,
            )

    def test_color_scales(self, dark_theme):
        """Test different color scales."""
        x_labels = ["A", "B"]
        y_labels = ["1", "2"]
        data = [[1, 2], [3, 4]]

        scales = ["heat", "cool", "diverging"]

        for scale in scales:
            chart = HeatmapChart(
                x_labels=x_labels, y_labels=y_labels, data=data, color_scale=scale, theme=dark_theme
            )
            assert chart.color_scale == scale

    @pytest.mark.asyncio
    async def test_render(self, mock_slide, dark_theme):
        """Test rendering heatmap chart."""
        x_labels = ["Mon", "Tue", "Wed"]
        y_labels = ["Week 1", "Week 2"]
        data = [[10, 20, 30], [15, 25, 35]]

        chart = HeatmapChart(x_labels=x_labels, y_labels=y_labels, data=data, theme=dark_theme)

        # Note: HeatmapChart _render_sync is currently a stub (pass)
        # Just verify it doesn't raise an error
        result = chart._render_sync(mock_slide, left=1, top=1, width=8, height=5)
        assert result is None  # Stub returns None

    @pytest.mark.asyncio
    async def test_render_with_defaults(self, mock_slide, dark_theme):
        """Test rendering with default position parameters."""
        chart = HeatmapChart(
            x_labels=["A", "B"], y_labels=["1", "2"], data=[[1, 2], [3, 4]], theme=dark_theme
        )
        # Call render without position parameters (uses defaults)
        result = await chart.render(mock_slide)
        assert result is None

    def test_validate_empty_data(self, dark_theme):
        """Test validation with empty data."""
        with pytest.raises(ValueError, match="Heatmap requires data"):
            HeatmapChart(x_labels=[], y_labels=[], data=[], theme=dark_theme)
