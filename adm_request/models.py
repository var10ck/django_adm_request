from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from django.urls import reverse
import uuid
from django.utils.text import slugify


# Document model
class Document(models.Model):
    def get_file_path(self, filename):
        extension = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), extension)
        return os.path.join("Documents", filename)

    name = models.CharField(_('Название'),
                            max_length=300,
                            db_index=True,
                            blank=True,
                            default='Документ',
                            help_text='Если '
                            )
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            help_text='Название в url. Может содержать латинские '
                                      'буквы, подчеркивания, тире и цифры',
                            )
    file = models.FileField(upload_to=get_file_path,
                            blank=False,
                            unique=True,
                            max_length=300,
                            )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.file.name)
        if self.name.strip() in ['Документ', '']:
            self.name = '-'.join(self.file.name.split('.')[:-1])
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f'Документ \"{self.file.name}\"'


class ADMRequest(models.Model):
    number = models.IntegerField(_('Номер претензии'),
                                 db_index=True,
                                 blank=False,
                                 unique=True,
                                 )
    date = models.DateField(_('От'),
                            auto_now=False,
                            )
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            help_text='Название в url. Может содержать латинские '
                                      'буквы, подчеркивания, тире и цифры',
                            )
    amount = models.DecimalField(_('Сумма'),
                                 decimal_places=2,
                                 max_digits=15,
                                 )
    file = models.OneToOneField(Document,
                                verbose_name=_('Файл'),
                                on_delete=models.CASCADE,
                                )
    comment = models.TextField(_('Комментарий'))

    class Meta:
        ordering = ('-date',)
        verbose_name = 'ADM запрос'
        verbose_name_plural = 'ADM запросы'

    def __str__(self):
        return f'Запрос №{self.number} от {self.date}'


class Investigation(models.Model):
    adm_request = models.ForeignKey(ADMRequest,
                                    verbose_name=_('ADM-запрос'),
                                    on_delete=models.CASCADE,
                                    )
    description = models.TextField(_('Описание'),
                                   blank=False,
                                   )
    result = models.TextField(_('Результат'),
                              blank=True,
                              null=True
                              )
    documents = models.ManyToManyField(Document,
                                       verbose_name=_('Документы'),
                                       related_name='investigations',
                                       )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')

    def __str__(self):
        return f'Расследование №{self.id} от {self.created.date()}'

    class Meta:
        verbose_name = 'Расследование'
        verbose_name_plural = 'Расследования'
        ordering = ('-id',)


class StoryRecord(models.Model):
    description = models.CharField(_('Описание'),
                                   max_length=228,
                                   help_text='Введите описание',
                                   )
    date = models.DateTimeField(_('Дата и время'),
                                auto_now_add=True,
                                editable=False,
                                )
    investigation = models.ForeignKey(Investigation,
                                      related_name='check_story',
                                      on_delete=models.CASCADE,
                                      )

    def __str__(self):
        return f'Запись №{self.id} ({str(self.date)})'


class ConclusionType(models.Model):
    name = models.CharField(_('Название'),
                            max_length=100,
                            )
    description = models.TextField(_('Описание'),
                                   )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name='Дата обновления')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип заклюяения'
        verbose_name_plural = 'Типы заключений'

    def __str__(self):
        return str(self.name)


class Conclusion(models.Model):
    number = models.IntegerField(_('Номер'),
                                 unique=True,
                                 )
    conclusion_type = models.ForeignKey(ConclusionType,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('Тип заключения')
                                        )
    description = models.TextField(_('Описание'),
                                   help_text='Введите описание сделанного заключения',
                                   )
    created = models.DateTimeField(_('Дата создания'),
                                   auto_now_add=True,
                                   )
    updated = models.DateTimeField(_('Дата обновления'),
                                   auto_now=True,
                                   )
    payoff_required = models.BooleanField()
    document = models.ForeignKey(Document,
                                 related_name='conclusion',
                                 on_delete=models.CASCADE,
                                 )

    class Meta:
        ordering = ('-updated',
                    )
        verbose_name = 'Заключение'
        verbose_name_plural = 'Заключения'

    def __str__(self):
        return f'Заключение №{self.number} от {self.created}'
