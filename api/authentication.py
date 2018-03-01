import json
from json.decoder import JSONDecodeError

from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication


class BodyTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            token = json.loads(request.body)["authentication_token"]
        except JSONDecodeError:
            return self.authenticate_credentials("")
        except KeyError:
            msg = _('No token in body.')
            raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = _('Invalid token in body. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword
