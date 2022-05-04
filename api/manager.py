
from django.db import models

class MusicManager(models.Manager):
    def get_by_category(self, category):
        return self.filter(category=category)
