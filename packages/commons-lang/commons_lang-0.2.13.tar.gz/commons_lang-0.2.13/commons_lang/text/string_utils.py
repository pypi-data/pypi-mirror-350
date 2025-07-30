def is_blank(text: str) -> bool:
    return text is None or text.isspace() or text == ""


def is_not_blank(text: str) -> bool:
    return not is_blank(text)
