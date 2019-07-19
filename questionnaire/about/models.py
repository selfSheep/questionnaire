from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=10, verbose_name='部门名称')
    brief_introduction = models.CharField(max_length=500, verbose_name='部门简介', null=True, blank=True)
    is_delete = models.BooleanField(verbose_name='是否删除')
    def __str__(self):
        return '<Department: {}>'.format(self.name)


class StaffMember(models.Model):
    name = models.CharField(max_length=10, verbose_name='名字')
    work_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True)
    grade = models.CharField(max_length=4, verbose_name='年级')
    school_department = models.CharField(max_length=10, verbose_name='系别')
    major = models.CharField(max_length=20, verbose_name='专业')
    personal_signature = models.CharField(max_length=30, verbose_name='个性签名', null=True, blank=True)
    brief_introduction = models.CharField(max_length=500, verbose_name='个人简介', null=True, blank=True)
    start_entry = models.DateField(verbose_name='起始任职', null=True, blank=True)
    end_quit = models.DateField(verbose_name='结束任职', null=True, blank=True)
    is_incumbent = models.BooleanField(verbose_name='是否在任')
    is_first_generation = models.BooleanField(verbose_name='是否初代')
    is_man = models.BooleanField(verbose_name='性别男')
    is_delisting = models.BooleanField(verbose_name='是否除名')
