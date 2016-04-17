class ControlIndex(object):
    def __init__(self):
        self.__lower_bound = None
        self.__lower_bound_next = None
        self.__upper_bound = None
        self.__upper_bound_next = None

    def get_lower_bound(self):
        return self.__lower_bound

    def get_lower_bound_next(self):
        return self.__lower_bound_next

    def get_upper_bound(self):
        return self.__upper_bound

    def get_upper_bound_next(self):
        return self.__upper_bound_next

    def set_lower_bound(self, lower_bound):
        self.__lower_bound = lower_bound

    def set_lower_bound_next(self, lower_bound_next):
        self.__lower_bound_next = lower_bound_next

    def set_upper_bound(self, upper_bound):
        self.__upper_bound = upper_bound

    def set_upper_bound_next(self, upper_bound_next):
        self.__upper_bound_next = upper_bound_next