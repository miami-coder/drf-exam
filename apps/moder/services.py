from apps.cars.models import Car
from apps.notifi.tasks import send_listing_flagged_notification, send_moderation_notification
from apps.users.models import CustomUser

from .models import ModerationLog

FORBIDDEN_WORDS = [
    'badword1',
    'badword2',
    'badword3',
    'badword4',
]


def check_text_for_profanity(text):
    text_lower = text.lower()
    found_words = []
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            found_words.append(word)
    return found_words


def moderate_car(car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        return {'error': 'No ads found.'}

    text_to_check = f'{car.description}'
    found_words = check_text_for_profanity(text_to_check)

    if not found_words:
        car.status = Car.ACTIVE
        car.save()
        ModerationLog.objects.create(
            car=car,
            status=ModerationLog.APPROVED,
            flagged_words='',
        )
        return {'status': 'approved', 'car_id': car_id}
    else:
        if car.edit_count >= 3:
            car.status = Car.INACTIVE
            car.save()
            ModerationLog.objects.create(
                car=car,
                status=ModerationLog.REJECTED,
                flagged_words=', '.join(found_words),
                comment='Edit limit exceeded. Ad deactivated.'
            )
            notify_managers(car)
            return {
                'status': 'deactivated',
                'car_id': car_id,
                'reason': 'Edit limit exceeded'
            }
        else:
            car.status = Car.FLAGGED
            car.save()
            ModerationLog.objects.create(
                car=car,
                status=ModerationLog.REJECTED,
                flagged_words=', '.join(found_words),
                comment=f'Forbidden words found. Remaining attempts: {3 - car.edit_count}'
            )
            notify_seller(car, 3 - car.edit_count)
            return {
                'status': 'flagged',
                'car_id': car_id,
                'found_words': found_words,
                'edits_remaining': 3 - car.edit_count
            }


def notify_managers(car):

    managers = CustomUser.objects.filter(role='manager')
    for manager in managers:
        if manager.email:
            send_moderation_notification.delay(
                manager_email=manager.email,
                car_id=car.id,
                reason='Edit limit exceeded'
            )


def notify_seller(car, edits_remaining):

    if car.owner.email:
        send_listing_flagged_notification.delay(
            seller_email=car.owner.email,
            car_id=car.id,
            edits_remaining=edits_remaining
        )