# PowerPoint Templates

This directory contains the template management system for the PowerPoint MCP Server.

## Structure

```
templates/
├── __init__.py           # Template module exports
├── template_manager.py   # TemplateManager class for managing templates
├── builtin/             # Built-in template files (.pptx)
│   ├── minimal.pptx     # (placeholder - not yet added)
│   ├── corporate.pptx   # (placeholder - not yet added)
│   ├── modern.pptx      # (placeholder - not yet added)
│   ├── tech.pptx        # (placeholder - not yet added)
│   └── academic.pptx    # (placeholder - not yet added)
└── README.md            # This file
```

## TemplateManager

The `TemplateManager` class provides:

- **Built-in Template Registry**: Pre-configured templates with metadata
- **Template Discovery**: List and search available templates
- **Async Operations**: All template operations are async-native
- **Pydantic Models**: Type-safe template metadata
- **Caching**: In-memory caching of template data

### Built-in Templates

The following built-in templates are available:

| Template | Category | Layouts | Description |
|----------|----------|---------|-------------|
| `minimal` | basic | 5 | Clean minimal template with basic layouts |
| `corporate` | business | 8 | Professional corporate template |
| `modern` | business | 10 | Modern template with contemporary design |
| `tech` | technology | 12 | Tech-focused with data visualization layouts |
| `academic` | education | 7 | Academic research presentation template |

## MCP Tools

The template system provides the following MCP tools:

### `pptx_list_templates(include_builtin: bool = True)`
Lists all available templates (built-in and custom).

### `pptx_get_builtin_template(template_name: str, save_as: str)`
Import a built-in template into the artifact store for use.

### `pptx_import_template(file_path: str, template_name: str)`
Import a custom PowerPoint file as a template.

### `pptx_analyze_template(template_name: str)`
Analyze a template's layouts, placeholders, and structure.

### `pptx_add_slide_from_template(layout_index: int, ...)`
Add a slide using a specific layout from a template.

## Usage Examples

### List Available Templates

```python
# List all templates
result = await pptx_list_templates()

# List only custom templates
result = await pptx_list_templates(include_builtin=False)
```

### Import Built-in Template

```python
# Import the corporate template
await pptx_get_builtin_template(
    template_name="corporate",
    save_as="my_corporate"
)
```

### Create Presentation from Template

```python
# Create presentation using template
await pptx_create(
    name="quarterly_report",
    template_name="my_corporate"
)

# Analyze template layouts
layouts = await pptx_analyze_template("my_corporate")

# Add slide using specific layout
await pptx_add_slide_from_template(
    layout_index=1,  # Title and Content layout
    template_name="my_corporate"
)
```

### Import Custom Template

```python
# Import your own template file
await pptx_import_template(
    file_path="/path/to/my_template.pptx",
    template_name="custom_brand"
)

# Use it to create presentations
await pptx_create(
    name="branded_deck",
    template_name="custom_brand"
)
```

## Adding New Built-in Templates

To add a new built-in template:

1. Create or obtain a PowerPoint template file (`.pptx`)
2. Save it to `templates/builtin/` with an appropriate name
3. Register it in `template_manager.py`:

```python
TemplateMetadata(
    name="your_template",
    display_name="Your Template",
    description="Description of your template",
    layout_count=8,  # Number of layouts in the template
    category="business",
    tags=["tag1", "tag2", "tag3"],
)
```

## Template Features

When using templates, you automatically get:

- **Consistent Styling**: All slides inherit the template's fonts, colors, and styling
- **Slide Layouts**: Access to all the template's pre-designed layouts
- **Master Slides**: Template's slide masters are preserved
- **Themes**: Custom themes from the template are maintained
- **Placeholders**: Layout placeholders for easy content population

## Integration with PresentationManager

Templates are fully integrated with `chuk-artifacts`:

- Templates stored in artifact store namespace: `presentations/templates/<name>`
- Templates persist across sessions based on storage scope
- Templates can be loaded from artifact store or built-in registry
- All operations are async and use Pydantic models

## Design Philosophy

The template system follows the same design principles as the rest of the MCP server:

- **Async Native**: All operations are async
- **Pydantic Models**: Type-safe data structures
- **Artifact Store Integration**: Uses chuk-artifacts for persistence
- **LLM-Friendly**: Tools designed for easy LLM interaction
- **Modular**: Template system is self-contained and extensible
