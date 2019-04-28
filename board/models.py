from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatechars

UserModel = get_user_model()


class Ad(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    author = models.ForeignKey(UserModel, related_name='author', on_delete=models.DO_NOTHING, verbose_name='Автор')
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    ad_text = models.TextField(verbose_name='Содержание')
    deleted = models.BooleanField(default=False, verbose_name='Удалён')
    view_count = models.SmallIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return '{}. {}'.format(self.title, self.ad_text[0:20])

    def short_text(self):
        return truncatechars(self.ad_text, 100)
    short_text.short_description = 'Содержание'
