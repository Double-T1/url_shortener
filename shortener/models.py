from django.db import models


class ShortenedUrl(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(
        unique=True, blank=True, max_length=100, db_index=True
    )
    published = models.BooleanField(default=True)

    @classmethod
    def has_short_code(cls, short_code):
        return cls.objects.filter(short_code=short_code).exists()

    def __str__(self):
        return f"{self.original_url} => {self.short_code}"
