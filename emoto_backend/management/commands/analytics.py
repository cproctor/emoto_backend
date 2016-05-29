from django.core.management.base import BaseCommand, CommandError
from emoto_backend.models import Emoto, Message, Profile
import csv
import argparse

class Command(BaseCommand):
    help = "Report analytics"

    def handle(self, *args, **options):
        messages = Message.objects.all()
        with open('messages.csv', 'w', newline='') as csvfile:
            msgWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for m in Message.objects.all():
                msgWriter.writerow([
                    m.author.username,
                    m.author.partner.username if m.author.partner else None,
                    m.text,
                    m.emoto.name if m.emoto else None,
                    m.created_time.isoformat(),
                ])
