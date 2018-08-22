import json
from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Friend


class UpdateListForm(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "20", }))

    def update_from_json(self, owner):
        json_data = json.loads(self.cleaned_data['json_data'])
        for friend_data in json_data['friends']:
            # Facebook doesn't encode names properly,
            # c.f. https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded
            # Going to be a nice surprise when they fix this
            name = friend_data['name'].encode('latin1').decode('utf8')
            date = timezone.make_aware(datetime.utcfromtimestamp(friend_data['timestamp']))
            Friend.objects.get_or_create(
                facebook_name=name,
                added_at=date,
                owner=owner
            )
