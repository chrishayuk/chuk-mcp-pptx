#!/usr/bin/env python3
"""
Check XML content of PowerPoint files for issues
"""

import zipfile
import xml.etree.ElementTree as ET
import os


def check_xml_in_pptx(filename):
    """Check XML files inside PPTX for issues"""
    print(f"\nChecking XML in {filename}...")

    try:
        with zipfile.ZipFile(filename, "r") as z:
            # Check main presentation.xml
            with z.open("ppt/presentation.xml") as f:
                content = f.read()
                try:
                    # Try to parse XML
                    ET.fromstring(content)
                    print("  ✅ presentation.xml is valid XML")

                    # Check encoding
                    if content.startswith(b"<?xml"):
                        header = content[:100]
                        print(f"  XML header: {header[:50]}...")
                        if b'encoding="UTF-8"' in header:
                            print("  ✅ UTF-8 encoding declared")
                        else:
                            print("  ⚠️  Non-UTF-8 encoding")

                except ET.ParseError as e:
                    print(f"  ❌ Invalid XML: {e}")

            # Check Content_Types.xml
            with z.open("[Content_Types].xml") as f:
                content = f.read()
                try:
                    ET.fromstring(content)
                    print("  ✅ [Content_Types].xml is valid")
                except ET.ParseError as e:
                    print(f"  ❌ Invalid Content_Types: {e}")

    except Exception as e:
        print(f"  ❌ Error: {e}")


def extract_and_compare(file1, file2, xml_path):
    """Extract and compare specific XML file from two PPTX files"""
    print(f"\nComparing {xml_path}:")

    try:
        with zipfile.ZipFile(file1, "r") as z1, zipfile.ZipFile(file2, "r") as z2:
            content1 = z1.read(xml_path)
            content2 = z2.read(xml_path)

            if content1 == content2:
                print("  ✅ Identical content")
            else:
                print("  ❌ Different content")
                print(f"    File 1 size: {len(content1)} bytes")
                print(f"    File 2 size: {len(content2)} bytes")

                # Show first difference
                for i, (b1, b2) in enumerate(zip(content1, content2)):
                    if b1 != b2:
                        print(f"    First difference at byte {i}")
                        print(f"    Context: ...{content1[max(0, i - 20) : i + 20]}...")
                        break

    except Exception as e:
        print(f"  Error: {e}")


if __name__ == "__main__":
    print("XML Content Checker for PowerPoint Files")
    print("=" * 60)

    files = ["test_direct.pptx", "test_server.pptx", "test_manager.pptx"]

    # Check XML validity
    for filename in files:
        if os.path.exists(filename):
            check_xml_in_pptx(filename)

    # Compare critical files
    print("\n" + "=" * 60)
    print("Comparing critical XML files between direct and server versions:")

    if os.path.exists("test_direct.pptx") and os.path.exists("test_server.pptx"):
        extract_and_compare("test_direct.pptx", "test_server.pptx", "ppt/presentation.xml")
        extract_and_compare("test_direct.pptx", "test_server.pptx", "[Content_Types].xml")
        extract_and_compare("test_direct.pptx", "test_server.pptx", "_rels/.rels")

if not os.path.exists("test_direct.pptx"):
    print("\n⚠️  Test files not found. Run test_minimal_issue.py first.")
