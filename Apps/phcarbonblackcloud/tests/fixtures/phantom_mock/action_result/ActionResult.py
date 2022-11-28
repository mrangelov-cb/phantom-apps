"""ActionResult for unit tests"""


class ActionResult:
    """ActionResult class for unit tests"""

    def __init__(self, param=None):
        """Constructor for the mock actionresult class"""
        self.param = param
        self.message = ""
        self.status = False
        self.data = []
        self.summary = {}
        self.logger = None
        return

    def set_status(self, status, message=None, error=None):
        """Status setter stub"""
        self.status = status
        self.message = message
        return status

    def add_data(self, data):
        """Add data stub"""
        self.data.append(data)
        return

    def get_data(self):
        """Data getter stub"""
        return self.data

    def get_message(self):
        """Message getter stub"""
        return self.message

    def update_summary(self, summary):
        """Update summary stub"""
        self.summary = summary
        return self.summary

    def set_summary(self, summary):
        """Summary setter stub"""
        self.update_summary(summary)
        return

    def get_status(self):
        """Status getter stub"""
        return self.status

    def set_logger(self, logger):
        """Logger setter stub"""
        self.logger = logger
