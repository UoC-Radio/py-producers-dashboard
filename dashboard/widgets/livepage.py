from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/LivePage.ui")
class LivePage(Gtk.Notebook):
    """Live page of the application"""

    __gtype_name__ = "LivePage"

    def __repr__(self):
        return "<LivePage>"

    @log
    def __init__(self):
        super().__init__()

