from datetime import datetime

from django.db import models
from django.utils.dateformat import format

from app.main.models import Profile


class Quest(models.Model):
    level = models.IntegerField(unique=True)

    img1 = models.URLField(help_text='Imgur direct JPG url, 250x250 px')
    img2 = models.URLField(help_text='Imgur direct JPG url, 250x250 px')

    class Meta:
        ordering = ['level']

    answer = models.CharField(
        max_length=50,
        help_text='Answer is case insensitive'
    )


class QuestScore(models.Model):
    profile = models.OneToOneField(Profile, related_name='quest_score')
    max_level = models.IntegerField(default=1)
    max_time = models.DateTimeField()

    sort_key = models.CharField(max_length=20, blank=True, null=True)

    def next_level(self):
        self.max_level += 1
        self.max_time = datetime.now()

    def save(self, *args, **kwargs):
        if self.max_level > 0:
            if not self.max_time:
                self.max_time = datetime.now()

                self.sort_key = str(self.max_level) + format(self.max_time, 'U')

        super(QuestScore, self).save(*args, **kwargs)

    class Meta:
        ordering = ['sort_key']