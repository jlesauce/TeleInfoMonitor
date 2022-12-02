class DatabaseError(Exception):

    def __init__(self, error: Exception):
        self.error = error
        super().__init__(self.error)
