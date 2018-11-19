from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/WaitPage.ui")
class WaitPage(Gtk.Box):
    """Wait page of the application"""

    __gtype_name__ = "WaitPage"

    __gsignals__ = \
        {
            'wait-page-shown': (GObject.SignalFlags.RUN_FIRST, None, (Gtk.Label, Gtk.TextView, Gtk.Label)),
            'instant-attempted': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'cancel-attempted': (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

    def __repr__(self):
        return "<WaitPage>"

    @log
    def __init__(self):
        super().__init__()
        self._show_title = utils.get_descendant(self, 'showtitle_label', 0)
        self._message = utils.get_descendant(self, 'message_textview', 0)
        self._remaining = utils.get_descendant(self, 'remaining_label', 0)

    @Gtk.Template.Callback()
    @log
    def on_WaitPage_map(self, widget):
        self.emit('wait-page-shown', self._show_title, self._message, self._remaining)

    @Gtk.Template.Callback()
    @log
    def on_instant_button_clicked(self, widget):
        self.emit('instant-attempted')

    @Gtk.Template.Callback()
    @log
    def on_cancel_button_clicked(self, widget):
        self.emit('cancel-attempted')
