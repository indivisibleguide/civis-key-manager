import os
import civis
from datetime import date, datetime

class CivisApiKey():
    """This class stores the data about a Civis API key."""

    @staticmethod
    def from_civis(data):
        """Create a CivisApiKey instance from a Civis API response."""
        return CivisApiKey(
            id=data.get('id'),
            name=data.get('name'),
            expires_at=data.get('expires_at'),
            created_at=data.get('created_at'),
            revoked_at=data.get('revoked_at'),
            last_used_at=data.get('last_used_at'),
            scopes=data.get('scopes'),
            use_count=data.get('use_count'),
            expired=data.get('expired'),
            active=data.get('active'),
            constraints=data.get('constraints'),
            token=data.get('token')
        )

    @staticmethod
    def from_env():
        """Create an API key from the os.environ['CIVIS_API_KEY'] varible.

        Returns: None if CIVIS_API_KEY is not present.
        """
        api_key = os.getenv('CIVIS_API_KEY')
        if api_key is None:
            return None

        return CivisApiKey(token=api_key)


    def __init__(
            self,
            id=None,
            name=None,
            expires_at=None,
            created_at=None,
            revoked_at=None,
            last_used_at=None,
            scopes=None,
            use_count=None,
            expired=None,
            active=None,
            constraints=None,
            token=None
    ):
        """ Create a new Civis API key with the given data.

        Note: Unlike the Civis API client, will not try to load the token
              from environmental variables.
        """
        self.id = id
        self.name = name
        self.expires_at = expires_at
        self.created_at = created_at
        self.revoked_at = revoked_at
        self.last_used_at = last_used_at
        self.scopes = scopes
        self.use_count = use_count
        self.expired = expired
        self.active = active
        self.constraints = constraints
        self.token = token


    def days_remaining(self):
        """Return the number of days remaining until this key expires.

        Returns (int):
          0 if no expiration data. 0 if already expired.
        """
        # Uses the Civis date format ex: 2021-07-16T20:45:46.000Z
        if self.expires_at is None:
            return 0

        expires_date = datetime.strptime(
            self.expires_at,
            "%Y-%m-%dT%H:%M:%S.000Z"
        ).date()
        return max((expires_date - date.today()).days, 0)


    def client(self):
        """Create a Civis APIClient that uses this token.

        Returns: None if token is None.
        """
        if self.token is None:
            return None

        return civis.APIClient(api_key=self.token)
