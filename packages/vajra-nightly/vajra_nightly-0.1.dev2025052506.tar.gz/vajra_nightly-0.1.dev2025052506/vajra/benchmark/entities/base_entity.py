from abc import ABC, abstractmethod


class BaseEntity(ABC):
    _id = 0

    @classmethod
    def generate_id(cls):
        cls._id += 1
        return cls._id

    @property
    def id(self) -> int:
        return self._id

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def __str__(self) -> str:
        # use to_dict to get a dict representation of the object
        # and convert it to a string
        class_name = self.__class__.__name__
        return f"{class_name}({str(self.to_dict())})"
