from typing import NamedTuple


# Type aliases
type MyAliases = list[dict[tuple[int, str], set[int]]] | tuple[str, list[str]]

# Named tuples
Point1 = NamedTuple('Point', [('x', int), ('y', int)])
class Point2(NamedTuple):
    x: int
    y: int
