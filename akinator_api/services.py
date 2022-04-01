from rest_framework.exceptions import ValidationError


def get_object_or_error(model, object_id: int, **kwargs):
    try:
        model.objects.get(id=object_id, **kwargs)
    except model.DoesNotExist:
        raise ValidationError('Object {} with id={} - DoesNotExist'.format(model._meta.model_name.title(), object_id))


def get_list_index_or_error(current_list, value):
    try:
        return current_list.index(value)
    except ValueError:
        raise ValidationError('There is no such element - {} in list {}'.format(value, current_list))
