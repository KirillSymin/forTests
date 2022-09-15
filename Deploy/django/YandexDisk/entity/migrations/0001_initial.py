# Generated by Django 4.0.5 on 2022-09-15 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('id', models.CharField(max_length=65535, primary_key=True, serialize=False, verbose_name='id')),
                ('type', models.CharField(choices=[('FILE', 'Файл'), ('FOLDER', 'Папка')], max_length=8, verbose_name='тип сущности')),
            ],
            options={
                'verbose_name': 'сущность файла или папки',
                'verbose_name_plural': 'сущности файлов и папок',
            },
        ),
        migrations.CreateModel(
            name='EntityDataHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_id', models.CharField(blank=True, max_length=65535, null=True, verbose_name='id родителя')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='название')),
                ('size', models.PositiveIntegerField(blank=True, null=True, verbose_name='цена')),
                ('created_date', models.DateTimeField(verbose_name='время создания')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity', to='entity.entity', verbose_name='сущность')),
            ],
            options={
                'verbose_name': 'история данных сущности файла или папки',
                'verbose_name_plural': 'истории данных сущностей файлов и папок',
            },
        ),
        migrations.AddField(
            model_name='entity',
            name='actual_data',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actual_data', to='entity.entitydatahistory', verbose_name='актуальные данные'),
        ),
    ]
