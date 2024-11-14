class BoundaryHandler:
    """Detect and handle boundaries in a string.

    The BoundaryHandler is an interface for a CaseConverter instance. It provides
    methods for detecting a boundary in a string as well as how to handle
    the boundary.
    """

    def is_boundary(self, pc, c):
        """Determine if we're on a boundary.

        :param pc: Previous character
        :param cc: Current character
        :return: True if a boundary is found, else false.
        :rtype: boolean
        """

        raise NotImplementedError()

    def handle(self, pc, cc, input_buffer, output_buffer):
        """Handle a detected boundary.

        :param pc: Previous character
        :type pc: str
        :param cc: Current character
        :type cc: str
        :param input_buffer: The raw string wrapped in a buffer.
        :type input_buffer: StringBuffer
        :param output_buffer: The output buffer that stores the new string as
            it's constructed.
        :type output_buffer: StringBuffer
        """

        raise NotImplementedError()


class OnDelimeterUppercaseNext(BoundaryHandler):
    def __init__(self, delimiters, join_char=""):
        self._delimiters = delimiters
        self._join_char = join_char

    def is_boundary(self, pc, c):  # noqa: ARG002
        return c in self._delimiters

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).upper())


class OnDelimeterLowercaseNext(BoundaryHandler):
    def __init__(self, delimiters, join_char=""):
        self._delimiters = delimiters
        self._join_char = join_char

    def is_boundary(self, pc, c):  # noqa: ARG002
        return c in self._delimiters

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(self._join_char)
        output_buffer.write(input_buffer.read(1).lower())


class OnUpperPrecededByLowerAppendUpper(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc is not None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(self._join_char)
        output_buffer.write(cc)


class OnUpperPrecededByLowerAppendLower(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc is not None and pc.isalpha() and pc.islower() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(self._join_char)
        output_buffer.write(cc.lower())


class OnUpperPrecededByUpperAppendJoin(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc is not None and pc.isalpha() and pc.isupper() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(self._join_char)
        output_buffer.write(cc)


class OnUpperPrecededByUpperAppendCurrent(BoundaryHandler):
    def __init__(self, join_char=""):
        self._join_char = join_char

    def is_boundary(self, pc, c):
        return pc is not None and pc.isalpha() and pc.isupper() and c.isupper()

    def handle(self, pc, cc, input_buffer, output_buffer):  # noqa: ARG002
        output_buffer.write(cc)
