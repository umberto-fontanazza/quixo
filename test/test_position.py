from src.position import Position
from src.symmetry import Symmetry

def test_symmetric():
    assert Position(1, 2).symmetric(Symmetry.HORIZONTAL) == Position(1, 2)
    assert Position(1, 2).symmetric(Symmetry.VERTICAL) == Position(3, 2)
    assert Position(1, 2).symmetric(Symmetry.DIAGONAL) == Position(2, 1)
    assert Position(1, 2).symmetric(Symmetry.ANTIDIAGONAL) == Position(2, 3)
    assert Position(3, 3).symmetric(Symmetry.HORIZONTAL) == Position(3, 1)
    assert Position(3, 3).symmetric(Symmetry.VERTICAL) == Position(1, 3)
    assert Position(3, 3).symmetric(Symmetry.DIAGONAL) == Position(3, 3)
    assert Position(3, 3).symmetric(Symmetry.ANTIDIAGONAL) == Position(1, 1)

