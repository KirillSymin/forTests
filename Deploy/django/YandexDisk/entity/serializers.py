from rest_framework import serializers

from entity.models import EntityDataHistory


class EntityCommonSerializer(serializers.ModelSerializer):
    id = serializers.CharField(label='id сущности', max_length=65535)
    parentId = serializers.CharField(label='id родителя', allow_null=True, max_length=65535)
    type = serializers.ChoiceField(label='тип', choices=(('FILE', 'Файл'), ('FOLDER', 'Папка')))

    class Meta:
        model = EntityDataHistory
        fields = ('url', 'size', 'id', 'type', 'parentId')


class EntityImportSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=EntityCommonSerializer()
    )
    updateDate = serializers.DateTimeField(format='iso-8601')
