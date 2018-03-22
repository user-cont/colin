class AbstractCheck(object):

    def __init__(self, name, message, description, reference_url, tags):
        super().__init__()
        self.name = name
        self.message = message
        self.description = description
        self.reference_url = reference_url
        self.tags = tags
        self.severity = None

    def check(self, target):
        pass
