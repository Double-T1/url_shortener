from django.db import models


class ShortenedUrl(models.Model):
    original_url = models.URLField(unique=True)
    short_url = models.CharField(unique=True, blank=True, max_length=100)

    @classmethod
    def has_short_url(cls, short_url):
        return cls.objects.filter(short_url=short_url).exists()

    def __str__(self):
        return f"{self.original_url} => {self.short_url}"
