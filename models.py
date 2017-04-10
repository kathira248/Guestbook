from google.appengine.ext import ndb

class Message(ndb.Model):
    message_text = ndb.StringProperty()
    author_name = ndb.StringProperty()
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)