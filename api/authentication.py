import json
from json.decoder import JSONDecodeError

from rest_framework.authentication import TokenAuthentication


class BodyTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Note we don't want to throw exceptions if authentication fails, because this isn't the only auth method
        try:
            token = json.loads(request.body)["authentication_token"]
        except JSONDecodeError:
            return self.authenticate_credentials(None)
        except KeyError:
            return None
        except UnicodeError:
            return None

        return self.authenticate_credentials(token)
