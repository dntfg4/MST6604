class Token(object):
    def __init__(self):
        super(Token, self).__init__()
        self.__counter = 0

    def increment_counter(self):
        self.__counter += 1

    def get_counter(self):
        return self.__counter