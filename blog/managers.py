from django.db import models

STATUS_PUBLISHED = 0
STATUS_DRAFT = 1


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=STATUS_PUBLISHED)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()
