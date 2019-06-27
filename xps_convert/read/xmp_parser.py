import re
from typing import Iterator

from xps_convert.read.errors import ParseError
from xps_convert.read.xmp import Xmp

FIELD_RE = re.compile(r"([\w\s]+):\s(.*)")


def parse_xmp(filename: str, lines: Iterator[str]) -> Xmp:
    xmp = Xmp()
    # First line is always a comment, skip it
    next(lines)
    # Match each line and enumerate (line numbers are needed for errors)
    for n, match in enumerate((FIELD_RE.match(line) for line in lines)):
        if match is not None:
            xmp.values[match.group(1)] = match.group(2)
        else:
            raise ParseError("unable to parse line", filename, n)
    # Verify that required fields are present
    for field in ("MHS File", "Device", "Package", "SpeedGrade"):
        if field not in xmp.values:
            raise ParseError(f"missing required field ‘{field}’", filename)
    return xmp
