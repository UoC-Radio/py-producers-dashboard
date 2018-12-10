import gi
from gi.repository import GObject


from collections import namedtuple

Show = namedtuple('Show', ['title', 'users', 'nickname', 'description', 'sites', 'logo_path'])

AsyncResult = namedtuple('AsyncResult', ['self', 'widget', 'actual_result'])


class ShowObject(GObject.Object):
    def __init__(self, title, subtitle, logo_path):
        GObject.GObject.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.logo_path = logo_path


class MessageObject(GObject.Object):
    def __init__(self, message, sender, timestamp):
        GObject.GObject.__init__(self)
        self.message = message
        self.timestamp = timestamp
        self.sender = sender
