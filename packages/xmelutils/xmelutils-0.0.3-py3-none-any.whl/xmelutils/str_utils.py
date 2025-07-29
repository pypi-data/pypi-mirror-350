from typing import Union

STR_METHODS = ["many_count"]

def many_count(
    text: str,
    patterns: Union[str, list[str]],
    *,
    case_insensitive: bool = False,
    as_substrings: bool = False
) -> int:
    """
    Counts characters or substrings in a string.

    Args:
        text: type: str -> String to search in.
        patterns: type: Union[str, list[str]] -> Characters/substrings to count (string or list).
        case_insensitive: type: bool = False -> Ignore case if True.
        as_substrings: type: bool = False -> Treat patterns as full substrings if True.

    Returns:
        Total count of occurrences.
    """
    if case_insensitive:
        text = text.lower()
        if isinstance(patterns, str):
            patterns = patterns.lower()

    if as_substrings:
        if isinstance(patterns, str):
            return text.count(patterns)
        return sum(text.count(p) for p in patterns)
    else:
        unique_chars = set(patterns) if isinstance(patterns, str) else set().union(*patterns)
        return sum(text.count(c) for c in unique_chars)
    