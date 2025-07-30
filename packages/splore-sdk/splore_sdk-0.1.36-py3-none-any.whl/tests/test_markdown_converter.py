"""
Tests for the Markdown to HTML converter utility.
"""

import pytest
from splore_sdk.utils import md_to_html, MarkdownConverter


class TestMarkdownConverter:
    """Test cases for the Markdown to HTML converter."""

    def test_md_to_html_basic_conversion(self):
        """Test basic conversion with the simple function."""
        markdown_text = "# Hello World"
        html = md_to_html(markdown_text)
        assert "<h1>Hello World</h1>" in html

    def test_md_to_html_empty_input(self):
        """Test conversion with empty input."""
        assert md_to_html("") == ""
        assert md_to_html(None) == ""

    def test_md_to_html_complex_input(self):
        """Test conversion with more complex markdown."""
        markdown_text = """
# Heading 1
## Heading 2

This is a paragraph with **bold** and *italic* text.

- List item 1
- List item 2

```
Code block
```

[Link](https://example.com)
"""
        html = md_to_html(markdown_text)
        # Check for converted elements
        assert "<h1>Heading 1</h1>" in html
        assert "<h2>Heading 2</h2>" in html
        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html
        assert "<li>List item 1</li>" in html
        assert "<pre>" in html  # Code block
        assert '<a href="https://example.com">Link</a>' in html

    def test_markdown_converter_class(self):
        """Test the MarkdownConverter class."""
        converter = MarkdownConverter()
        markdown_text = "# Test Heading"
        html = converter.convert(markdown_text)
        assert "<h1>Test Heading</h1>" in html

    def test_markdown_converter_with_extensions(self):
        """Test conversion with extensions."""
        converter = MarkdownConverter()
        markdown_text = """
```python
def hello():
    print("Hello")
```
"""
        # With codehilite extension
        html = converter.convert(markdown_text, extensions=["extra", "codehilite"])
        # The codehilite extension adds CSS classes
        assert "codehilite" in html or "highlight" in html

    def test_markdown_converter_safety(self):
        """Test that potentially dangerous HTML is handled safely."""
        converter = MarkdownConverter()
        # Try to inject script tag
        markdown_text = "<script>alert('XSS');</script>"
        html = converter.convert(markdown_text, safe_mode=True)
        # The script tag should be escaped
        assert "<script>" not in html
        # Should be escaped as &lt;script&gt; or similar
        assert "&lt;" in html or "<" not in html

    def test_markdown_sanitization(self):
        """Test the sanitization methods."""
        converter = MarkdownConverter()
        # Test input sanitization
        sanitized = converter._sanitize_input("<script>alert('test');</script>")
        assert "<script>" not in sanitized

        # Test output sanitization
        sanitized = converter._sanitize_output("<script>alert('test');</script>")
        assert "<script>" not in sanitized
