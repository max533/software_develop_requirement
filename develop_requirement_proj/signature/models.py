""" signature database model """


class Account:
    """ OEM Accounts Model """
    def __init__(self, **kwargs):
        fields = [
            'id',
            'name',
            'code',
            'business_unit',
            'project_count'
        ]
        for field in fields:
            setattr(self, field, kwargs.get(field, None))

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} : {self.name}>'

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"("
            f"{self.id}, "
            f"{self.name}, "
            f"{self.code}, "
            f"{self.business_unit}, "
            f"{self.project_count}"
            f")"
        )


class Project:
    """ OEM Project Model """
    def __init__(self, **kwargs):
        fields = [
            'id',
            'wistron_name',
            'customer_name',
            'wistron_code',
            'plm_code_1',
            'plm_code_2',
            'deleted_at',
            'type',
            'name',
            'plm_code',
            'status',
            'product_line',
            'business_model',
            'account'
        ]
        for field in fields:
            setattr(self, field, kwargs.get(field, None))

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} : {self.name}>'

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"("
            f"{self.id}, "
            f"{self.wistron_name}, "
            f"{self.customer_name}, "
            f"{self.wistron_code}, "
            f"{self.plm_code_1}, "
            f"{self.plm_code_2}, "
            f"{self.deleted_at}, "
            f"{self.type}, "
            f"{self.name}, "
            f"{self.plm_code}, "
            f"{self.status}, "
            f"{self.product_line}, "
            f"{self.business_model}, "
            f"{self.account}"
            f")"
        )
