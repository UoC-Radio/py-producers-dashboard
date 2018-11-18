from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/ShowsPage.ui")
class ShowsPage(Gtk.Box):
    """Shows page of the application"""

    __gtype_name__ = "ShowsPage"

    def __repr__(self):
        return "<ShowsPage>"

    @log
    def __init__(self):
        super().__init__()

