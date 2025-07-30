import abc

class RefactorOwnership(abc.ABC):
    def __init__(self, property_ownership: dict or None):
        self.ownership = property_ownership
        assert self.ownership is  not None


