from django.forms import ModelForm
from emoto_backend.models import Emoto

class EmotoForm(ModelForm):
    class Meta:
        model = Emoto
        fields = ['name', 'image']
