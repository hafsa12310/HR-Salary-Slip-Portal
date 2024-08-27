import pickle
from datetime import datetime
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_str
from django.utils.timezone import now
from .models import Session  

class MongoSessionBase(SessionBase):
    """
    Implements MongoDB session base using MongoEngine.
    """

    def load(self):
        try:
            session = Session.objects(session_key=self.session_key, expire_date__gt=now()).first()
            if session:
                return self.decode(session.session_data)
        except Session.DoesNotExist:
            pass
        return self.create()

    def create(self):
        self.modified = True
        self.session_key = self._get_new_session_key()
        return {}

    def save(self, must_create=False):
        session_data = self.encode(self._get_session(no_load=must_create))
        session_key = self.session_key
        expire_date = self.get_expiry_date()

        if must_create:
            if Session.objects(session_key=session_key).first():
                raise CreateError
            session = Session(session_key=session_key, session_data=session_data, expire_date=expire_date)
        else:
            session = Session.objects(session_key=session_key).first()
            if session:
                session.update(set__session_data=session_data, set__expire_date=expire_date)
            else:
                session = Session(session_key=session_key, session_data=session_data, expire_date=expire_date)
        session.save()

    def exists(self, session_key):
        return Session.objects(session_key=session_key).first() is not None

    def delete(self, session_key=None):
        if session_key is None:
            session_key = self.session_key
        Session.objects(session_key=session_key).delete()

    def clear_expired(self):
        Session.objects(expire_date__lt=now()).delete()
