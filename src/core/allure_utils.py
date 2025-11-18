from typing import Optional

try:
    import allure
except ImportError:
    allure = None


def attach_text(
    name: str,
    content: str,
    attachment_type: Optional["allure.attachment_type"] = None
) -> None:
    """
    Safely attaches text content to Allure report.
    If Allure is not available (e.g., local run without plugin),
    the function silently returns without raising errors.

    Args:
        name: Human-readable label for the attachment.
        content: Text or JSON string that should appear in the report.
        attachment_type: Optional allure attachment type. Defaults to TEXT.
    """
    if allure is None:
        return

    try:
        if attachment_type is None:
            attachment_type = allure.attachment_type.TEXT

        allure.attach(content, name=name, attachment_type=attachment_type)
    except Exception:
        # Never interrupt test execution due to reporting issues
        pass
