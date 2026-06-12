from celery import shared_task

from .services import fetch_rates_from_privatbank


@shared_task
def update_exchange_rates():
    print('[Celery] Currency exchange rate updates...')
    rates = fetch_rates_from_privatbank()

    if rates:
        print(f'[Celery] Courses have been updated: {rates}')
        return {'status': 'success', 'rates': {k: str(v) for k, v in rates.items()}}
    else:
        print('[Celery] Error updating courses')
        return {'status': 'error'}