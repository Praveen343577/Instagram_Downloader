def sanitize_link(raw_link: str) -> str:
    """
    Strips query parameters from an Instagram URL.
    Example: https://www.instagram.com/p/DFOEoFftk9u/?utm_source=ig -> https://www.instagram.com/p/DFOEoFftk9u/
    """
    if not raw_link:
        return ""
    return raw_link.split("?")[0].strip()