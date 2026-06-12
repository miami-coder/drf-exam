from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_moderation_notification(manager_email, car_id, reason):

    print(f'[Celery] Sending email to {manager_email} about the announcement #{car_id}')

    subject = f'Announcement #{car_id} deactivated'
    message = (
        f'Announcement #{car_id} was automatically deactivated.\n'
        f'Reason: {reason}\n\n'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[manager_email],
            fail_silently=False,
        )
        print(f'[Celery] Email sent to {manager_email}')
        return {'status': 'sent', 'email': manager_email}
    except Exception as e:
        print(f'[Celery] Error sending email: {e}')
        return {'status': 'error', 'error': str(e)}


@shared_task
def send_listing_flagged_notification(seller_email, car_id, edits_remaining):

    print(f'[Celery] Seller notification {seller_email} about flagged ads #{car_id}')

    subject = f'Your ad #{car_id} needs correction'
    message = (
        f'Your ad #{car_id} contains prohibited content.\n'
        f'You have left {edits_remaining} attempts to correct.\n\n'
        f'Please edit your ad and remove any prohibited words.'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seller_email],
            fail_silently=False,
        )
        return {'status': 'sent'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}