import logging
import re
import string
from io import StringIO

logger = logging.getLogger(__name__)


class StringBuffer(StringIO):
    """StringBuffer is a wrapper around StringIO.

    By wrapping StringIO, adding debugging information is easy.
    """

    def write(self, s):
        super().write(s)


DELIMITERS = " -_"


def stripable_punctuation(delimiters):
    """Construct a string of stripable punctuation based on delimiters.

    Stripable punctuation is defined as all punctuation that is not a delimeter.
    """

    return "".join([c for c in string.punctuation if c not in delimiters])


class CaseConverter:
    def __init__(self, s, delimiters=DELIMITERS, strip_punctuation=True):  # noqa: FBT002
        """Initialize a case conversion.

        On initialization, punctuation can be optionally stripped. If
        punctuation is not stripped, it will appear in the output at the
        same position as the input.

        BoundaryHandlers should take into consideration whether or not
        they are evaluating the first character in a string and whether or
        not a character is punctuation.

        Delimeters are taken into consideration when defining stripable
        punctuation.

        Delimeters will be reduced to single instances of a delimeter. This
        includes transforming `   -_-__  `  to `-`.

        During initialization, the raw input string will be passed through
        the prepare_string() method. Child classes should override this
        method if they wish to perform pre-conversion checks and manipulate
        the string accordingly.

        :param s: The raw string to convert.
        :type s: str
        :param delimiters: A set of delimiters used to identify boundaries.
            Defaults to DELIMITERS
        :type delimiters: str
        """

        self._delimiters = delimiters

        s = s.strip(delimiters)

        if strip_punctuation:
            punctuation = stripable_punctuation(delimiters)
            s = re.sub(f"[{re.escape(punctuation)}]+", "", s)

        # Change recurring delimiters into single delimiters.
        s = re.sub(f"[{re.escape(delimiters)}]+", delimiters[0], s)

        self._raw_input = s
        self._input_buffer = StringBuffer(self.prepare_string(s))
        self._output_buffer = StringBuffer()
        self._boundary_handlers = []

        self.define_boundaries()

    def add_boundary_handler(self, handler):
        """Add a boundary handler.

        :type handler: BoundaryHandler
        """

        self._boundary_handlers.append(handler)

    def define_boundaries(self):
        """Define boundary handlers.

        define_boundaries() is called when a CaseConverter is initialized.
        define_boundaries() should be overridden in a child class to add
        boundary handlers.

        A CaseConverter without boundary handlers makes little sense.
        """

        logger.warning("No boundaries defined")

    def delimiters(self):
        """Retrieve the delimiters.

        :rtype: str
        """

        return self._delimiters

    def raw(self):
        """Retrieve the raw string to be converted.

        :rtype: str
        """

        return self._raw_input

    def init(self, input_buffer, output_buffer):  # noqa: ARG002
        """Initialize the output buffer.

        Can be overridden.

        See convert() for call order.
        """

        return

    def mutate(self, c):
        """Mutate a character not on a boundary.

        Can be overridden.

        See convert() for call order.
        """

        return c

    def prepare_string(self, s: str) -> str:
        """Prepare the raw intput string for conversion.

        Executed during CaseConverter initialization providing an opportunity
        for child classes to manipulate the string. By default, the string
        is not manipulated.

        Can be overridden.

        :param s: The raw string supplied to the CaseConverter constructor.
        :type s: str
        :return: A raw string to be used in conversion.
        :rtype: str
        """

        return s

    def _is_boundary(self, pc, c):
        """Determine if we've hit a boundary or not.

        :rtype: BoundaryHandler
        """

        for bh in self._boundary_handlers:
            if bh.is_boundary(pc, c):
                return bh

        return None

    def convert(self) -> str:
        """Convert the raw string.

        convert() follows a series of steps.

            1. Initialize the output buffer using `init()`.
            For every character in the input buffer:
            2. Check if the current position lies on a boundary as defined
               by the BoundaryHandler instances.
            3. If on a boundary, execute the handler.
            4. Else apply a mutation to the character via `mutate()` and add
               the mutated character to the output buffer.

        :return: The converted string.
        :rtype: str
        """

        self.init(self._input_buffer, self._output_buffer)

        logger.debug(f"input_buffer = {self._input_buffer.getvalue()}")

        # Previous character (pc) and current character (cc)
        pc = None
        cc = self._input_buffer.read(1)

        while cc:
            bh = self._is_boundary(pc, cc)
            if bh:
                bh.handle(pc, cc, self._input_buffer, self._output_buffer)
            else:
                self._output_buffer.write(self.mutate(cc))

            pc = cc
            cc = self._input_buffer.read(1)

        return str(self._output_buffer.getvalue())
