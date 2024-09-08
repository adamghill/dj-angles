class InvalidEndTagError(Exception):
    def __init__(self, tag, last_tag):
        super().__init__()

        self.tag = tag
        self.last_tag = last_tag
