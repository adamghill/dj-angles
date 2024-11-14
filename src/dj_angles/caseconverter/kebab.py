from dj_angles.caseconverter.boundaries import OnDelimeterLowercaseNext, OnUpperPrecededByLowerAppendLower
from dj_angles.caseconverter.caseconverter import CaseConverter


class Kebab(CaseConverter):
    JOIN_CHAR = "-"

    def define_boundaries(self):
        self.add_boundary_handler(OnDelimeterLowercaseNext(self.delimiters(), self.JOIN_CHAR))
        self.add_boundary_handler(OnUpperPrecededByLowerAppendLower(self.JOIN_CHAR))

    def prepare_string(self, s):
        if s.isupper():
            return s.lower()

        return s

    def mutate(self, c):
        return c.lower()


def kebabify(s, **kwargs):
    """Convert a string to kebab case

    Example

        Hello World => hello-world

    """
    return Kebab(s, **kwargs).convert()
