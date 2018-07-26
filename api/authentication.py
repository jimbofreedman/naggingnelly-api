import json
from json.decoder import JSONDecodeError

from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import TokenAuthentication


class BodyTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Note we don't want to throw exceptions if authentication fails, because this isn't the only auth method
        try:
            token = json.loads(request.body)["authentication_token"]
        except JSONDecodeError:
            return self.authenticate_credentials(None)
        except KeyError:
            msg = _('No token in body.')
            return None
        except UnicodeError:
            msg = _('Invalid token in body. Token string should not contain invalid characters.')
            return None

        return self.authenticate_credentials(token)
