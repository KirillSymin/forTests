from django.db import models

from treebeard.mp_tree import MP_Node


class Entity(MP_Node):
    TYPES = (
        ('FILE', 'Файл'),
        ('FOLDER', 'Папка')
    )
    HUMAN_READABLE_TYPES = {'FILE': 'Файл', 'FOLDER': 'Папка'}

    id = models.CharField('id', max_length=65535, primary_key=True)
    actual_data = models.OneToOneField('EntityDataHistory', verbose_name='актуальные данные',
                                       on_delete=models.SET_NULL, related_name='actual_data', null=True, blank=True)
    type = models.CharField('тип сущности', choices=TYPES, max_length=8)

    class Meta:
        verbose_name = 'сущность файла или папки'
        verbose_name_plural = 'сущности файлов и папок'

    def __str__(self):
        return f'{self.id} #{self.HUMAN_READABLE_TYPES[self.type]}'


class EntityDataHistory(models.Model):
    entity = models.ForeignKey(Entity, verbose_name='сущность',
                               on_delete=models.CASCADE, related_name='entity')
    parent_id = models.CharField('id родителя', max_length=65535, null=True, blank=True)
    url = models.CharField('название', max_length=255, null=True, blank=True)
    size = models.PositiveIntegerField('цена', null=True, blank=True)
    created_date = models.DateTimeField('время создания')

    class Meta:
        verbose_name = 'история данных сущности файла или папки'
        verbose_name_plural = 'истории данных сущностей файлов и папок'

    def __str__(self):
        return f'{self.name} #{self.pk}'
