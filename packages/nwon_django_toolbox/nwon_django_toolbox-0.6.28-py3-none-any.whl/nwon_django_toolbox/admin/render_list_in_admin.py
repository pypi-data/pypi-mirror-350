from typing import List

from django.utils.html import format_html


def render_list_in_admin(
    list_to_display: List[str], sort_alphabetically: bool = True
) -> str:
    """Renders a list in a Django admin table"""

    if sort_alphabetically:
        list_to_display = sorted(list_to_display)

    elements = [f"<li>{element}</li>" for element in list_to_display]
    return format_html("<ul>" + "".join(elements) + "</ul>")
