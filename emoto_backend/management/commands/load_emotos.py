from django.core.management.base import BaseCommand, CommandError
from emoto_backend.models import Emoto
import requests
import yaml
import argparse

class Command(BaseCommand):
    help = "upload images to an instance of emoto backend"

    def add_arguments(self, parser):
        parser.add_argument("base_url", nargs=1, type=str, help="Base URL for target app")
        parser.add_argument("datafile", nargs=1, type=argparse.FileType('r'), help="YAML file containing a list of emotos, each with {'name': string, 'image': file_path}")

    def handle(self, *args, **options):
        uploadUrl = "{}/api/v1/emotos/new".format(options['base_url'][0])
        emotosToUpload = yaml.load(options['datafile'][0].read())
        for emoto in emotosToUpload:
            with open(emoto['image'], 'rb') as imagefile:
                r = requests.post(
                    uploadUrl,
                    data={"name": emoto['name'] },
                    files={"image": imagefile }
                )
                if r.status_code is 200:
                    self.stdout.write(self.style.SUCCESS("Uploaded {} as {}".format(emoto['image'], emoto['name'])))
                else:
                    raise CommandError(r.text)




