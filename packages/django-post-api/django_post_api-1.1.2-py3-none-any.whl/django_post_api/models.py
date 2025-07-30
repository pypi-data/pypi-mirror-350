from django.db import models
from django.db.models.manager import BaseManager
from django.utils import timezone


def get_mysql_default_dict():
    return {}


def get_mysql_default_list():
    return []


class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        # 这个方法用来获取未被标记为删除的对象
        return self.exclude(is_deleted=True)

    def deleted(self):
        # 这个方法用来获取已被标记为删除的对象
        return self.filter(is_deleted=True)

    def delete(self):
        return super(SoftDeleteQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()


class PropertyManager(BaseManager.from_queryset(SoftDeleteQuerySet)):
    # django 的Manager就是这样继承的
    pass


# Create your models here.
class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    is_deleted = models.BooleanField(verbose_name="是否删除", default=False)

    objects = PropertyManager()

    class Meta:
        abstract = True
        ordering = ("-id",)

    def delete(self, using=None, keep_parents=False):
        # 这里可以直接调用 SoftDeleteQuerySet 的 delete 方法
        self.__class__.objects.filter(pk=self.pk).update(is_deleted=True)
        # self.is_deleted = True
        # self.save(using=using, update_fields=["is_deleted", ])
