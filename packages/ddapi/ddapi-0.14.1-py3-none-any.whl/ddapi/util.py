__all__ = ("slugify2",)

slugify2_symbols = "[\t !\"#$%&'()*-/<=>?@[\\]^_`{|},.:]+"
NON_ASCII_CHARACTER_THRESHOLD = 128


def slugify2(_nickname: str) -> str:
    """Needed for a link generator."""
    string = ""
    for symbol in _nickname:
        string += (
            f"-{ord(symbol)}-"
            if symbol in slugify2_symbols
            or ord(symbol) >= NON_ASCII_CHARACTER_THRESHOLD
            else symbol
        )

    return string
