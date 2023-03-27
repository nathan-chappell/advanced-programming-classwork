from typing import Protocol

class P(Protocol):
    x: int
    y: int

class Point2D:
    x: int
    y: int

class PointZ2:
    x: int
    y: int

p2d: Point2D = Point2D()
pz2 = PointZ2()

def erase(p: P) -> P: return p

p: P = erase(p2d)
q: P = erase(pz2)

# NOTE:
# mypy does this differently than pyright!

p2d = q
pz2 = p
