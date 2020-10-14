import uuid
from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants import COURSES_STATUS_CHOICES


class Author(SoftDeletionModel):
    name = models.CharField(max_length=300)
    author_number = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.author_number:
            self.author_number = str(uuid.uuid4()).replace("-", '').upper()[:10]
        super(Author, self).save(*args, **kwargs)


    @property
    def publications(self):
        return self.publications.all()


class PublisherCity(SoftDeletionModel):
    name = models.CharField(max_length=300)
    number = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.number:
            self.number = str(uuid.uuid4()).replace("-", '').upper()[:10]
        super(PublisherCity, self).save(*args, **kwargs)


    @property
    def publishers(self):
        return self.publishers.all()
    


class Publisher(SoftDeletionModel):
    name = models.CharField(max_length=300)
    city = models.ForeignKey(
                        'PublisherCity',
                        null = True,
                        on_delete = models.SET_NULL,
                        related_name='publishers'
                    )
    number = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.number:
            self.number = str(uuid.uuid4()).replace("-", '').upper()[:10]
        super(Publisher, self).save(*args, **kwargs)


    @property
    def refferences(self):
        return self.refferences.all()
    



class ReferrenceSource(SoftDeletionModel):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(
    					'Author', 
    					on_delete=models.CASCADE, 
    					related_name='publications'
    				)
    publisher  = models.ForeignKey(
                            'Publisher',
                            blank=True,
                            null=True,
                            related_name = 'refferences'
                        )
    date_published = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title





        