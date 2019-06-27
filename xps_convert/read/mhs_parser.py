import re
from typing import Iterator, Optional

from xps_convert.read.mhs import MhsRoot, MhsComponent


class ParseError(BaseException):
    def __init__(self, message: str, filename: str, line: Optional[int] = None) -> None:
        location = f"{filename}:{line + 1}" if line is not None else filename
        super().__init__(f"{location}: {message}")


COMMENT_RE = re.compile(r"#.*")
ASSIGNMENT_RE = re.compile(r"(\w+)\s+(\w+)\s*=\s*(.*)")
BLOCK_START_RE = re.compile(r"BEGIN\s+(\w+)")
BLOCK_END_RE = re.compile(r"END")


def parse_mhs(filename: str, lines: Iterator[str]) -> MhsRoot:
    root = MhsRoot()
    current = root
    # Strip leading/trailing whitespace and remove comments from lines
    lines = [COMMENT_RE.sub("", line.strip()) for line in lines]
    # Enumerate lines (line numbers are needed for errors)
    for n, line in enumerate(lines):
        # Skip blank lines
        if not line:
            continue
        # Find the first pattern that matches
        patterns = (ASSIGNMENT_RE, BLOCK_START_RE, BLOCK_END_RE)
        match = next(filter(None, (pattern.match(line) for pattern in patterns)), None)
        # Check whether there is match
        if match is None:
            raise ParseError("unable to parse line", filename, n)
        # Check whether match was assignment
        if match.re == ASSIGNMENT_RE:
            command, name, value = match.groups()
            assignments = current.assignments
            if command == "PARAMETER":
                assignments.parameters[name] = value
            elif command == "BUS_INTERFACE":
                assignments.bus_interfaces[name] = value
            elif command == "PORT":
                assignments.ports[name] = value
            else:
                raise ParseError(f"unknown assignment command ‘{command}’", filename, n)
        # Check whether match was block start
        elif match.re == BLOCK_START_RE:
            if current != root:
                # Already in a component
                raise ParseError("unexpected BEGIN", filename, n)
            current = MhsComponent(match.groups()[0])
        # Check whether match was block end
        elif match.re == BLOCK_END_RE:
            if current == root:
                # Not in a component
                raise ParseError("unexpected END", filename, n)
            # Verify that component has an INSTANCE parameter
            if "INSTANCE" not in current.assignments.parameters:
                raise ParseError("missing required parameter ‘INSTANCE’", filename, n)
            root.components[current.instance_name] = current
            current = root
        # Unreachable
        else:
            raise RuntimeError
    # Check whether currently in a component
    if current != root:
        raise ParseError("unexpected EOF", filename, len(lines))
    # Verify that root has a VERSION parameter
    if "VERSION" not in root.assignments.parameters:
        raise ParseError("missing required parameter ‘VERSION’", filename)
    return root
