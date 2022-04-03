from rest_framework.exceptions import ValidationError

from akinator_api import models


def get_object_or_error(model, object_id: int, **kwargs):
    try:
        model.objects.get(id=object_id, **kwargs)
    except model.DoesNotExist:
        raise ValidationError(
            "Object {} with id={} - DoesNotExist".format(
                model._meta.model_name.title(), object_id
            )
        )


def get_list_index_or_error(current_list, value):
    try:
        return current_list.index(value)
    except ValueError:
        raise ValidationError(
            "There is no such element - {} in list {}".format(value, current_list)
        )


def add_new_answers_to_object(new_answers: list, parent_object):
    parent_object_answers_id = [answer['id'] for answer in parent_object.answers]
    for new_answer in new_answers:
        if new_answer['id'] in parent_object_answers_id:
            continue
        get_object_or_error(models.Question, new_answer["id"])
        parent_object.answers.append(new_answer)
    parent_object.save(update_fields=["answers"])
    return parent_object.answers


def delete_answers_from_object(delete_answers: list, parent_object):
    for delete_answer in delete_answers:
        delete_answer_index = get_list_index_or_error(
            parent_object.answers, delete_answer
        )
        get_object_or_error(models.Question, delete_answer["id"])
        del parent_object.answers[delete_answer_index]
    parent_object.save(update_fields=["answers"])
    return parent_object.answers
