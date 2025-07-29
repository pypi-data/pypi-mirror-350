import io
import re
from typing import Optional

from lxml import etree, html
from lxml.html import tostring


def parse_partial_html(input_html: str) -> Optional[etree.Element]:  # noqa
    """Parse string with HTML fragment into an lxml tree.

    Supports partial HTML content.
    Removes comments and CDATA.
    """
    # Simple heuristic to detect unclosed comments
    open_count = input_html.count("<!--")
    close_count = input_html.count("-->")

    # If counts don't match, escape all opening comment tags
    if open_count != close_count:
        input_html = input_html.replace("<!--", "&lt;!--")

    # Normalize new lines to spaces for consistent handling
    input_html = re.sub(r"[\n\r]+", " ", input_html)

    # Remove CDATA sections
    input_html = re.sub(r"<!\[CDATA\[.*?]]>", "", input_html, flags=re.DOTALL)

    parser = etree.HTMLParser(recover=True, remove_comments=True, remove_pis=True)
    tree = html.parse(io.StringIO(input_html), parser=parser)
    return tree.getroot()


def etree_to_str(root: etree.Element) -> str:
    if root.tag in ["root", "html", "body"]:
        # For artificial root, return only content without the root tag
        # todo: check if this is really artificial root and not from input
        result = root.text or ""
        for child in root:
            result += tostring(child, encoding="unicode", method="html")
        return result
    return tostring(root, encoding="unicode", method="html")  # type: ignore[no-any-return]
