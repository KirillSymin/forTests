from django.urls import path

from entity.views import EntityImportView, GetNodesView, DeleteNodeView, UpdatesView, HistoryView

app_name = 'entity'
urlpatterns = [
    path('imports', EntityImportView.as_view(), name='imports'),
    path('nodes/<str:entity_id>', GetNodesView.as_view(), name='nodes'),
    path('delete/<str:entity_id>', DeleteNodeView.as_view(), name='delete'),
    path('updates', UpdatesView.as_view(), name='updates'),
    path('node/<str:entity_id>/history', HistoryView.as_view(), name='history'),
]
