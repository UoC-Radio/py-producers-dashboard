from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/HeaderBar.ui")
class HeaderBar(Gtk.HeaderBar):
    """Headerbar of the application"""

    __gtype_name__ = "HeaderBar"

    def __repr__(self):
        return "<HeaderBar>"

    @log
    def __init__(self):
        super().__init__()

