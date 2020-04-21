""" signature database model """


class Account:
    """ OEM Accounts Model """
    def __init__(self, **kwargs):
        fields = ['id', 'name', 'code', 'business_unit', 'project_count']
        for field in fields:
            setattr(self, field, kwargs.get(field, None))

    def __str__(self):
        return f'{self.id} : {self.name}'

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(" +
            f"{self.id}, {self.name}, {self.code}, {self.business_unit}, {self.project_count})"
        )
