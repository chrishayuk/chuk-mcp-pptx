#!/usr/bin/env python3
"""
Test the PowerPoint MCP Server tools directly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from chuk_mcp_pptx.server import (
    pptx_create, pptx_add_title_slide, pptx_add_slide, 
    pptx_add_text_slide, pptx_save, pptx_list, pptx_get_info,
    pptx_export_base64, pptx_import_base64, pptx_close
)
import json


def test_powerpoint_tools():
    print("Testing PowerPoint MCP Server Tools")
    print("=" * 40)
    
    # Test creating presentation
    print("\n1. Creating presentation...")
    result = pptx_create(name="test_presentation")
    print(f"   Result: {result}")
    assert "Created presentation" in result
    
    # Test adding title slide
    print("\n2. Adding title slide...")
    result = pptx_add_title_slide(
        title="Test Presentation",
        subtitle="Testing the MCP Server"
    )
    print(f"   Result: {result}")
    assert "Added title slide" in result
    
    # Test adding content slide
    print("\n3. Adding content slide...")
    result = pptx_add_slide(
        title="Features",
        content=[
            "Easy to use",
            "Supports multiple presentations",
            "Export/Import functionality"
        ]
    )
    print(f"   Result: {result}")
    assert "Added content slide" in result
    
    # Test adding text slide
    print("\n4. Adding text slide...")
    result = pptx_add_text_slide(
        title="Description",
        text="This is a comprehensive PowerPoint MCP server."
    )
    print(f"   Result: {result}")
    assert "Added text slide" in result
    
    # Test listing presentations
    print("\n5. Listing presentations...")
    result = pptx_list()
    print(f"   Result:\n{result}")
    assert "test_presentation" in result
    
    # Test getting info
    print("\n6. Getting presentation info...")
    result = pptx_get_info()
    info = json.loads(result)
    print(f"   Slides: {info['slides']}")
    print(f"   First slide title: {info['slide_details'][0]['title']}")
    assert info['slides'] == 3
    
    # Test saving
    print("\n7. Saving presentation...")
    result = pptx_save(path="test_output.pptx")
    print(f"   Result: {result}")
    assert "Saved presentation" in result
    
    # Test export/import
    print("\n8. Testing export/import...")
    export_result = pptx_export_base64()
    export_data = json.loads(export_result)
    print(f"   Exported data size: {len(export_data['data'])} chars")
    
    result = pptx_import_base64(
        data=export_data['data'],
        name="imported_presentation"
    )
    print(f"   Import result: {result}")
    assert "Imported presentation" in result
    
    # Test closing
    print("\n9. Closing presentation...")
    result = pptx_close(presentation="imported_presentation")
    print(f"   Result: {result}")
    assert "Closed presentation" in result
    
    print("\n" + "=" * 40)
    print("All tests passed successfully!")


if __name__ == "__main__":
    test_powerpoint_tools()