import datetime
import json
from copy import deepcopy

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.views.generic import View
from silk.profiling.profiler import silk_profile
import pendulum
from application.settings import DEBUG

from entity.models import Entity, EntityDataHistory
from entity.serializers import EntityImportSerializer

error_400 = JsonResponse({'code': 400, 'message': 'Validation Failed'}, status=400)
error_404 = JsonResponse({'code': 404, 'message': 'Item not found'}, status=404)
error_500 = JsonResponse({'code': 500, 'message': 'Internal Error'}, status=500)


def use_silk_when_debug(name):
    def wrapper(func):
        if DEBUG:
            return silk_profile(name=name)(func)
        else:
            return func
    return wrapper


def recalculate_parents_sizes(entity, entity_size, update_date, sign):
    if not entity_size:
        return
    parents = entity.get_ancestors().select_related('actual_data')
    bulk_parents = []
    bulk_parents_data = []
    for parent in parents:
        prev_size = parent.actual_data.size
        bulk_parents_data.append(EntityDataHistory(entity=parent, parent_id=parent.actual_data.parent_id,
                                                   url=parent.actual_data.url,
                                                   size=(0 if prev_size is None else prev_size) + entity_size * (
                                                       1 if sign == '+' else -1),
                                                   created_date=update_date))
    bulk_parents_data = EntityDataHistory.objects.bulk_create(bulk_parents_data)
    for parent_data in bulk_parents_data:
        cur_entity = parent_data.entity
        cur_entity.actual_data = parent_data
        bulk_parents.append(cur_entity)
    Entity.objects.bulk_update(bulk_parents, ['actual_data'])


def update_parents_data(entity, update_date):
    parents = entity.get_ancestors().select_related('actual_data')
    bulk_parents = []
    bulk_parents_data = []
    for parent in parents:
        prev_data = parent.actual_data
        prev_data.id = None
        prev_data.data = update_date
        bulk_parents_data.append(prev_data)
    bulk_parents_data = EntityDataHistory.objects.bulk_create(bulk_parents_data)
    for parent_data in bulk_parents_data:
        cur_entity = parent_data.entity
        cur_entity.actual_data = parent_data
        bulk_parents.append(cur_entity)
    Entity.objects.bulk_update(bulk_parents, ['actual_data'])


class EntityImportView(View):
    @use_silk_when_debug(name='Import')
    @transaction.atomic
    def post(self, request):
        if request.content_type == 'application/json':
            try:
                valid_ser = EntityImportSerializer(data=json.loads(request.body))
            except json.JSONDecodeError:
                return error_400
            if valid_ser.is_valid():
                valid_data = valid_ser.validated_data
                try:
                    with transaction.atomic():
                        for item in valid_data['items']:
                            try:
                                # TODO изучить вопрос с тем, что обязательно должно прийти, а что нет
                                entity_id = item['id']
                                new_parent_id = item['parentId']
                                new_url = item.get('url', None)
                                new_size = item.get('size', None)
                                new_update_date = valid_data['updateDate']
                                entity_type = item['type']
                            except IndexError:
                                return error_400
                            try:
                                entity = Entity.objects.select_related('actual_data').get(id=entity_id)
                            except ObjectDoesNotExist:
                                entity = None
                            if entity:
                                if new_parent_id != entity.actual_data.parent_id:
                                    recalculate_parents_sizes(entity, entity.actual_data.size, new_update_date, '-')
                                    entity.move(Entity.objects.get(id=new_parent_id), 'first_child')
                                    if entity_type == 'FILE':
                                        recalculate_parents_sizes(entity, new_size, new_update_date, '+')
                                    else:
                                        recalculate_parents_sizes(entity, entity.actual_data.size, new_update_date, '+')
                                else:
                                    prev_size = entity.actual_data.size
                                    diff = (0 if new_size is None else new_size) - \
                                           (0 if prev_size is None else prev_size)
                                    if new_size is not None and diff:
                                        recalculate_parents_sizes(entity, abs(diff), new_update_date,
                                                                  '+' if diff >= 0 else '-')
                                    else:
                                        update_parents_data(entity, new_update_date)
                                if entity_type == 'FOLDER':
                                    new_size = entity.actual_data.size
                                new_history = EntityDataHistory.objects.create(entity_id=entity_id,
                                                                               parent_id=new_parent_id,
                                                                               url=new_url,
                                                                               size=new_size,
                                                                               created_date=new_update_date)
                                entity.actual_data = new_history
                                entity.save()
                            else:
                                if new_parent_id:
                                    try:
                                        entity = Entity.objects.get(id=new_parent_id).add_child(id=entity_id,
                                                                                                type=entity_type)
                                    except ObjectDoesNotExist:
                                        return error_400
                                    if entity_type == 'FILE':
                                        recalculate_parents_sizes(entity, new_size, new_update_date, '+')
                                    else:
                                        update_parents_data(entity, new_update_date)
                                else:
                                    entity = Entity.add_root(id=entity_id, type=entity_type)
                                    update_parents_data(entity, new_update_date)
                                new_history = EntityDataHistory.objects.create(entity_id=entity_id,
                                                                               parent_id=new_parent_id,
                                                                               url=new_url,
                                                                               size=new_size,
                                                                               created_date=new_update_date)
                                entity.actual_data = new_history
                                entity.save()
                    return JsonResponse({})
                except IntegrityError:
                    return error_500
        return error_400


def dump_entity_children(cls, parent):
    entities = cls.objects.all().filter(path__startswith=parent.path).select_related('actual_data')
    res, lnk = [], {}
    for entity in entities:
        entity_res = {'id': entity.id, 'type': entity.type, 'size': entity.actual_data.size,
                      'url': entity.actual_data.url,
                      'parentId': entity.actual_data.parent_id,
                      'date': f'{entity.actual_data.created_date.strftime("%Y-%m-%dT%H:%M:%S")}Z', 'children': None}

        path = entity.path
        depth = int(len(path) / cls.steplen)

        if len(path) == len(parent.path):
            res.append(entity_res)
        else:
            parent_path = cls._get_basepath(path, depth - 1)
            parent_obj = lnk[parent_path]
            if not parent_obj['children']:
                parent_obj['children'] = []
            parent_obj['children'].append(entity_res)
        lnk[path] = entity_res
    return res[0]


class GetNodesView(View):
    @use_silk_when_debug(name='GetNode')
    def get(self, request, entity_id=None):
        if entity_id is None:
            return error_400

        try:
            entity = Entity.objects.get(id=entity_id)
        except ObjectDoesNotExist:
            return error_404

        response = dump_entity_children(Entity, parent=entity)

        print(json.dumps(response, indent=4))  # TODO убрать

        return JsonResponse(response, safe=False)


class DeleteNodeView(View):
    @use_silk_when_debug(name='Delete')
    def delete(self, request, entity_id=None):
        date_str = request.GET.get('date')
        if date_str:
            if entity_id is None:
                return error_400

            try:
                entity = Entity.objects.select_related('actual_data').get(id=entity_id)
            except ObjectDoesNotExist:
                return error_404

            recalculate_parents_sizes(entity, entity.actual_data.size, date_str, '-')

            entity.delete()
            return JsonResponse({})
        return 400


class UpdatesView(View):
    @use_silk_when_debug(name='Updates')
    def get(self, request):
        date_str = request.GET.get('date')
        if date_str:
            data = pendulum.parse(date_str)
            print(data)
            entities = Entity.objects.select_related('actual_data') \
                .filter(actual_data__created_date__gte=data - datetime.timedelta(days=1),
                        actual_data__created_date__lte=data, type='FILE')
            response = dict()
            response['items'] = []
            for entity in entities:
                entity_response_obj = dict()
                entity_response_obj['id'] = entity.id
                entity_response_obj['url'] = entity.actual_data.url
                entity_response_obj['parentId'] = entity.actual_data.parent_id
                entity_response_obj['size'] = entity.actual_data.size
                entity_response_obj['type'] = entity.type
                entity_response_obj['date'] = entity.actual_data.created_date
                response['items'].append(entity_response_obj)

            response_with_parsed_data = deepcopy(response)  # TODO убрать
            for i in response_with_parsed_data['items']:
                i['date'] = str(i['date'])
            print(json.dumps(response_with_parsed_data, indent=4))

            return JsonResponse(response, safe=False)
        return error_400


class HistoryView(View):
    @use_silk_when_debug(name='History')
    def get(self, request, entity_id=None):
        if entity_id is None:
            return error_400

        date_start_str = request.GET.get('dateStart')
        date_end_str = request.GET.get('dateEnd')
        if date_start_str and date_end_str:
            date_start = pendulum.parse(date_start_str)
            date_end = pendulum.parse(date_end_str)
            entity_history = EntityDataHistory.objects.filter(entity_id=entity_id,
                                                              created_date__gte=date_start,
                                                              created_date__lt=date_end).select_related('entity')
            if not entity_history:
                return error_404
            entity = entity_history[0].entity
            response = dict()
            response['items'] = []
            for entity_data in entity_history:
                entity_response_obj = dict()
                entity_response_obj['id'] = entity.id
                entity_response_obj['url'] = entity_data.url
                entity_response_obj['parentId'] = entity_data.parent_id
                entity_response_obj['size'] = entity_data.size
                entity_response_obj['type'] = entity.type
                entity_response_obj['date'] = entity_data.created_date
                response['items'].append(entity_response_obj)

            response_with_parsed_data = deepcopy(response)  # TODO убрать
            for i in response_with_parsed_data['items']:
                i['date'] = str(i['date'])
            print(json.dumps(response_with_parsed_data, indent=4))

            return JsonResponse(response, safe=False)
        return error_400
