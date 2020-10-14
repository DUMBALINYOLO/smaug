from django.db import models

class SoftDeletionModel(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)


    def delete(self):
        self.active = False
        self.save()

    def hard_delete(self):
        super().delete()



class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


