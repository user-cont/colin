class AbstractCheck(object):

    def __init__(self, name, message, description, reference_url, tags):
        super().__init__()
        self.name = name
        self.message = message
        self.desription = description
        self.reference_url = reference_url
        self.tags = tags

    def check(self):
        pass
