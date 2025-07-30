"""
Utility functions for converting Markdown to HTML using the Python-Markdown package.
"""

from typing import Dict, Any, Optional, List, Union
import markdown

from splore_sdk.core.logger import sdk_logger


class MarkdownConverter:
    """
    A utility class for converting Markdown text to HTML using the Python-Markdown package.

    This class provides a wrapper around the popular 'markdown' library to make it easy
    to convert Markdown content to HTML within the Splore SDK.
    """

    def __init__(self, logger=None):
        """
        Initialize the Markdown converter.

        Args:
            logger: Optional logger instance. If not provided, the default SDK logger is used.
        """
        self.logger = logger or sdk_logger

    def convert(
        self,
        markdown_text: str,
        extensions: Optional[List[Union[str, Any]]] = None,
        extension_configs: Optional[Dict[str, Dict[str, Any]]] = None,
        safe_mode: bool = True,
    ) -> str:
        """
        Convert Markdown text to HTML.

        Args:
            markdown_text: The Markdown text to convert.
            extensions: List of extensions to use. Default includes 'extra', 'tables'.
            extension_configs: Configuration for extensions.
            safe_mode: If True, use safe mode to prevent potentially dangerous HTML.

        Returns:
            HTML string converted from Markdown.

        Example:
            >>> converter = MarkdownConverter()
            >>> html = converter.convert("# Hello World")
            >>> print(html)
            <h1>Hello World</h1>
        """
        if not markdown_text:
            return ""

        # Default extensions for common Markdown features
        default_extensions = ["extra", "tables"]

        # Use provided extensions or default
        md_extensions = extensions or default_extensions

        # Handle safe_mode separately since it's deprecated in recent versions
        # but we still want to provide safety features
        if safe_mode:
            if "smarty" not in md_extensions:
                md_extensions.append("smarty")

            # Add custom sanitization if needed
            markdown_text = self._sanitize_input(markdown_text)

        self.logger.debug(
            f"Converting Markdown to HTML with extensions: {md_extensions}"
        )

        try:
            # Convert Markdown to HTML
            html = markdown.markdown(
                markdown_text,
                extensions=md_extensions,
                extension_configs=extension_configs or {},
            )
        except ImportError as e:
            self.logger.warning(f"Failed to use some markdown extensions: {e}")
            # Fallback to basic markdown without extensions
            html = markdown.markdown(markdown_text)

        # Additional safety check if safe_mode is enabled
        if safe_mode:
            html = self._sanitize_output(html)

        self.logger.debug("Markdown conversion completed")
        return html

    def _sanitize_input(self, text: str) -> str:
        """
        Perform basic sanitization on the input markdown.
        This helps prevent certain types of injection issues.

        Args:
            text: The input markdown text

        Returns:
            Sanitized markdown text
        """
        # Basic sanitization to replace script tags
        # A more comprehensive solution would use a dedicated HTML sanitizer library
        return text.replace("<script", "&lt;script").replace(
            "</script>", "&lt;/script&gt;"
        )

    def _sanitize_output(self, html: str) -> str:
        """
        Perform basic sanitization on the output HTML.
        For production use, consider using a dedicated HTML sanitizer like bleach.

        Args:
            html: The output HTML

        Returns:
            Sanitized HTML
        """
        # Basic sanitization, focuses only on script tags
        # For more comprehensive sanitization, consider using bleach library
        return html.replace("<script", "&lt;script").replace(
            "</script>", "&lt;/script&gt;"
        )


def md_to_html(
    markdown_text: str,
    extensions: Optional[List[Union[str, Any]]] = None,
    extension_configs: Optional[Dict[str, Dict[str, Any]]] = None,
    safe_mode: bool = True,
) -> str:
    """
    Convert Markdown text to HTML using the Python-Markdown package.
    Args:
        markdown_text: The Markdown text to convert.
        extensions: List of extensions to use. Default includes 'extra' and 'tables'.
        extension_configs: Configuration for extensions.
        safe_mode: If True, use safe mode to prevent potentially dangerous HTML.

    Returns:
        HTML string converted from Markdown.

    Example:
        >>> from splore_sdk.utils.markdown_converter import md_to_html
        >>> html = md_to_html("# Hello World")
        >>> print(html)
        <h1>Hello World</h1>

        # With extensions
        >>> html = md_to_html("```python\\nprint('Hello')\\n```",
        ...                   extensions=['fenced_code', 'codehilite'])
    """
    converter = MarkdownConverter()
    return converter.convert(
        markdown_text,
        extensions=extensions,
        extension_configs=extension_configs,
        safe_mode=safe_mode,
    )
