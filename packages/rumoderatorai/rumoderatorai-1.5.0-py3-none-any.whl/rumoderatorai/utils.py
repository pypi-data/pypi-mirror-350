def urljoin(base: str, *paths: str) -> str:
    """
    Join paths to the base URL

    Args:
        base (str): Base URL
        *paths (str): Paths to join to the base URL

    Returns:
        str: Joined URL
    """
    for path in paths:
        if not base.endswith("/"):
            base += "/"
        if path.startswith("/"):
            path = path[1:]
        base += path
    return base
