from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/LivePage.ui")
class LivePage(Gtk.Notebook):
    """Live page of the application"""

    __gtype_name__ = "LivePage"

    __gsignals__ = \
        {
            'live-page-shown': (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

    def __repr__(self):
        return "<LivePage>"

    @log
    def __init__(self):
        super().__init__()
        self._message = utils.get_descendant(self, 'message_textview', 0)

    @Gtk.Template.Callback()
    @log
    def on_LivePage_map(self, widget):
        self.emit('live-page-shown')

    def set_buffer(self, text_buffer: Gtk.TextBuffer):
        self._message.set_buffer(text_buffer)
