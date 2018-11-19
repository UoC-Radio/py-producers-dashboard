from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/GolivePage.ui")
class GolivePage(Gtk.Box):
    """Live page of the application"""

    __gtype_name__ = "GolivePage"

    __gsignals__ = \
        {
            'live-page-shown': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'golive-attempted': (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

    def __repr__(self):
        return "<GolivePage>"

    @log
    def __init__(self):
        super().__init__()

    @Gtk.Template.Callback()
    @log
    def on_GolivePage_map(self, widget):
        self.emit('live-page-shown')

    @Gtk.Template.Callback()
    @log
    def on_golive_button_clicked(self, widget):
        self.emit('golive-attempted')
