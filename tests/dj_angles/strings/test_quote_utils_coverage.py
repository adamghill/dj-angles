from dj_angles.quote_utils import QuoteTracker


def test_reset():
    qt = QuoteTracker()
    qt.update("'")
    assert qt.inside_quotes
    qt.reset()
    assert not qt.inside_quotes
