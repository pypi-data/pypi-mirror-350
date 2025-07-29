

class BaseModel:
    def to_dict(self):
        return vars(self)