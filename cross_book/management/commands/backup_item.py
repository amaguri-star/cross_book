import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Item


class Command(BaseCommand):
    help = 'Backup Item data'

    def handle(self, *args, **options):
        date = datetime.date.today().strftime("%Y%m%d")

        file_path = settings.BACKUP_PATH + 'item_' + date + '.csv'
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            header = [field.name for field in Item._meta.fields]
            writer.writerow(header)

            items = Item.objects.all()

            for item in items:
                writer.writerow([
                    str(item.id),
                    str(item.user),
                    item.name,
                    item.explanation,
                    item.get_state_display(),
                    item.category.name,
                    item.get_shipping_area_display(),
                    item.get_shipping_day_display(),
                    str(item.at_created)
                ])

        files = os.listdir(settings.BACKUP_PATH)
        if len(files) >= settings.NUM_SAVED_BACKUP:
            files.sort()
            os.remove(settings.BACKUP_PATH + files[0])
