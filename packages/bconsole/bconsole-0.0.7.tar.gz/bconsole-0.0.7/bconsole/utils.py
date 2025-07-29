__all__ = ["surround_with", "halve_at", "replace_last"]


def surround_with(text: str, /, *, wrapper: str) -> str:
    """
    Surrounds the specified text with the specified wrapper.

    ### Args:
        text (str): The text to surround.
        wrapper (str): The wrapper to use.
        title (bool, optional): Whether to make the first character in the text uppercase. Defaults to True.

    ### Returns:
        str: The surrounded text.
    """
    w1, w2 = halve_at(wrapper)
    return f"{w1}{text}{w2}"


def halve_at(text: str, /, *, at: float = 0.5) -> tuple[str, str]:
    """
    Halves the specified text at the specified position.

    ### Args:
        text (str): The text to cut.
        at (float, optional): The position to cut at. Defaults to 0.5.

    ### Returns:
        tuple[str, str]: Each half of the text.
    """
    where = round(len(text) * at)
    return (text[:where], text[where:])


def replace_last(text: str, old: str, new: str, /) -> str:
    """
    Replaces a single occurrence of a substring in a string with another substring, starting from the end of the string.

    ### Args:
        text (str): The text to replace in.
        old (str): The substring to replace.
        new (str): The substring to replace it with.

    ### Returns:
        str: The replaced text.

    ### Example:
        >>> replace_last("apple, banana or cherry", " or ", ", ")
        "apple, banana, cherry"
    """
    return new.join(text.rsplit(old, 1))
