from django.contrib import admin

from entity.models import Entity, EntityDataHistory


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('id', 'actual_data', 'type')
    list_filter = ('type',)


@admin.register(EntityDataHistory)
class EntityDataHistoryAdmin(admin.ModelAdmin):
    list_display = ('url', 'size', 'entity', 'parent_id', 'created_date')
    list_filter = ('entity', 'parent_id', 'created_date',)
