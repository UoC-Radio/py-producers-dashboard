from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/Message.ui")
class Message(Gtk.Box):
    """Message item for inbox"""

    __gtype_name__ = "Message"

    def __repr__(self):
        return "<Message>"

    @log
    def __init__(self, message, sender, timesamp):
        super().__init__()
        self._message = utils.get_descendant(self, 'inbox_message_textview', 0)
        self._sender = utils.get_descendant(self, 'sender_label', 0)
        self._timestamp = utils.get_descendant(self, 'timestamp_label', 0)

        self._message.get_buffer().set_text(message)
        self._sender.set_text(sender)
        self._timestamp.set_text(timesamp)
