from io import StringIO

import pytest

from dj_angles.caseconverter.boundaries import (
    BoundaryHandler,
    OnDelimeterLowercaseNext,
    OnDelimeterUppercaseNext,
    OnUpperPrecededByLowerAppendLower,
    OnUpperPrecededByLowerAppendUpper,
    OnUpperPrecededByUpperAppendCurrent,
    OnUpperPrecededByUpperAppendJoin,
)


class TestBoundaryHandler:
    def test_not_implemented(self):
        handler = BoundaryHandler()
        with pytest.raises(NotImplementedError):
            handler.is_boundary("a", "b")
        with pytest.raises(NotImplementedError):
            handler.handle("a", "b", StringIO(), StringIO())


class TestOnDelimeterUppercaseNext:
    def test_is_boundary(self):
        handler = OnDelimeterUppercaseNext(delimiters=["-"])
        assert handler.is_boundary("a", "-")
        assert not handler.is_boundary("a", "b")

    def test_handle(self):
        handler = OnDelimeterUppercaseNext(delimiters=["-"], join_char="_")
        input_buffer = StringIO("x")
        output_buffer = StringIO()
        handler.handle("a", "-", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "_X"


class TestOnDelimeterLowercaseNext:
    def test_is_boundary(self):
        handler = OnDelimeterLowercaseNext(delimiters=["-"])
        assert handler.is_boundary("a", "-")
        assert not handler.is_boundary("a", "b")

    def test_handle(self):
        handler = OnDelimeterLowercaseNext(delimiters=["-"], join_char="_")
        input_buffer = StringIO("X")
        output_buffer = StringIO()
        handler.handle("a", "-", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "_x"


class TestOnUpperPrecededByLowerAppendUpper:
    def test_is_boundary(self):
        handler = OnUpperPrecededByLowerAppendUpper()
        assert handler.is_boundary("a", "B")
        assert not handler.is_boundary("A", "B")
        assert not handler.is_boundary("a", "b")
        assert not handler.is_boundary(None, "B")

    def test_handle(self):
        handler = OnUpperPrecededByLowerAppendUpper(join_char="_")
        input_buffer = StringIO()
        output_buffer = StringIO()
        handler.handle("a", "B", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "_B"


class TestOnUpperPrecededByLowerAppendLower:
    def test_is_boundary(self):
        handler = OnUpperPrecededByLowerAppendLower()
        assert handler.is_boundary("a", "B")
        assert not handler.is_boundary("A", "B")
        assert not handler.is_boundary("a", "b")

    def test_handle(self):
        handler = OnUpperPrecededByLowerAppendLower(join_char="_")
        input_buffer = StringIO()
        output_buffer = StringIO()
        handler.handle("a", "B", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "_b"


class TestOnUpperPrecededByUpperAppendJoin:
    def test_is_boundary(self):
        handler = OnUpperPrecededByUpperAppendJoin()
        assert handler.is_boundary("A", "B")
        assert not handler.is_boundary("a", "B")
        assert not handler.is_boundary("A", "b")

    def test_handle(self):
        handler = OnUpperPrecededByUpperAppendJoin(join_char="_")
        input_buffer = StringIO()
        output_buffer = StringIO()
        handler.handle("A", "B", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "_B"


class TestOnUpperPrecededByUpperAppendCurrent:
    def test_is_boundary(self):
        handler = OnUpperPrecededByUpperAppendCurrent()
        assert handler.is_boundary("A", "B")
        assert not handler.is_boundary("a", "B")

    def test_handle(self):
        handler = OnUpperPrecededByUpperAppendCurrent(join_char="_")
        input_buffer = StringIO()
        output_buffer = StringIO()
        handler.handle("A", "B", input_buffer, output_buffer)
        assert output_buffer.getvalue() == "B"
