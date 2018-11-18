from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/GolivePage.ui")
class GolivePage(Gtk.Box):
    """Live page of the application"""

    __gtype_name__ = "GolivePage"

    def __repr__(self):
        return "<GolivePage>"

    @log
    def __init__(self):
        super().__init__()

