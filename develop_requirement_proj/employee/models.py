from django.db import models


class Employee(models.Model):
    """Wistron EBG + CPBG Employee Information Table"""
    employee_id = models.CharField(db_column='EMPLID', max_length=11, primary_key=True)
    chinese_name = models.CharField(db_column='NAME', max_length=60)
    english_name = models.CharField(db_column='NAME_A', max_length=50)
    department_id = models.CharField(db_column='DEPTID', max_length=10)
    department_name = models.CharField(db_column='DESCR', max_length=30)
    job_title = models.CharField(db_column='DESCR60_A', max_length=60)
    extension = models.CharField(db_column='PHONE_A', max_length=120)
    mail = models.EmailField(db_column='EMAIL_ADDRESS_A', max_length=70)
    supervisor_id = models.CharField(db_column='SUPERVISOR_ID', max_length=11)
    site = models.CharField(db_column='SITE_ID_A', max_length=6)
    location = models.CharField(db_column='LOCATION', max_length=10)

    class Meta:
        ordering = ['employee_id']
        managed = False
        db_table = 'WHQ_HR'
