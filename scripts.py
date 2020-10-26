import random

from datacenter.models import Schoolkid, Lesson, Commendation


def create_commendation(schoolkid_name, subject_title):
    commendation_texts = ['Молодец!', 'Отлично!', 'Хорошо!', 'Так держать!']

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.MultipleObjectsReturned:
        return 'Найдено несколько учеников с таким именем! Нужен запрос точнее!'
    except Schoolkid.DoesNotExist:
        return 'Такого ученика не существует!'

    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=subject_title,
                                   ).order_by('-date').first()

    if not lesson:
        return 'Урок не найден!'

    commendation = Commendation.objects.create(text=random.choice(commendation_texts),
                                               created=lesson.date,
                                               schoolkid=schoolkid,
                                               subject=lesson.subject,
                                               teacher=lesson.teacher,)

    commendation.save()

    return 'Похвала записана в дневник!'


def remove_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.MultipleObjectsReturned:
        return 'Найдено несколько учеников с таким именем! Нужен запрос точнее!'
    except Schoolkid.DoesNotExist:
        return 'Такого ученика не существует!'

    schoolkid.chastisement_set.all().delete()

    return 'Замечания учителей удалены.'


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.MultipleObjectsReturned:
        return 'Найдено несколько учеников с таким именем! Нужен запрос точнее!'
    except Schoolkid.DoesNotExist:
        return 'Такого ученика не существует!'

    schoolkid.mark_set.filter(points__in=[2, 3]).update(points=5)

    return 'Плохие оценки исправлены на пятерки.'
