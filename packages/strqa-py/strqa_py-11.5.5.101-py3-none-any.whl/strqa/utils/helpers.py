import logging
import sys

logger_stream_handler = logging.StreamHandler(stream=sys.stdout)

logger = logging.getLogger("strqa")
logger.propagate = False
logger.addHandler(logger_stream_handler)
logger.setLevel(logging.INFO)


def normalize_lines(sql: str, case_sensitive: bool) -> list[str]:
    """Normalize SQL string into a list of lines.

    Handles escape sequences and applies case conversion if needed.

    Args:
        sql (str): SQL string to normalize
        case_sensitive (bool): Whether to preserve a case (True) or convert
            to lowercase (False)

    Returns:
        List of normalized lines
    """
    if not sql:
        return []

    escape_sequences = {
        "\\n": "\n",
        "\\t": "\t",
        "\\r": "\r",
        "\\\\": "\\",
        "\\'": "'",
        '\\"': '"',
        "\\nn": "\n\n",
    }

    for seq, char in escape_sequences.items():
        sql = sql.replace(seq, char)

    lines = sql.strip().splitlines()
    if not case_sensitive:
        lines = [line.lower() for line in lines]
    return lines
