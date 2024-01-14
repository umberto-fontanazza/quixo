from src.position import Position, BORDERS, CORNERS
from src.symmetry import Symmetry

def test_symmetric():
    assert Position(1, 2).symmetric(Symmetry.HORIZONTAL) == Position(3, 2)
    assert Position(1, 2).symmetric(Symmetry.VERTICAL) == Position(1, 2)
    assert Position(1, 2).symmetric(Symmetry.DIAGONAL) == Position(2, 1)
    assert Position(1, 2).symmetric(Symmetry.ANTIDIAGONAL) == Position(2, 3)
    assert Position(3, 3).symmetric(Symmetry.HORIZONTAL) == Position(1, 3)
    assert Position(3, 3).symmetric(Symmetry.VERTICAL) == Position(3, 1)
    assert Position(3, 3).symmetric(Symmetry.DIAGONAL) == Position(3, 3)
    assert Position(3, 3).symmetric(Symmetry.ANTIDIAGONAL) == Position(1, 1)

def test_symmetrics():
    expected = {Position(x,y) for x,y in [(0, 0), (0, 4), (4, 4), (4, 0)]}
    actual = Position(4, 0).symmetrics([axis for axis in Symmetry])
    assert actual == expected

def test_filter_out_symmetrics():
    all_axes = [axis for axis in Symmetry]
    filtered = Position.filter_out_symmetrics(BORDERS, all_axes)
    assert len(filtered) == 6