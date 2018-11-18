from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/WaitPage.ui")
class WaitPage(Gtk.Box):
    """Wait page of the application"""

    __gtype_name__ = "WaitPage"

    def __repr__(self):
        return "<WaitPage>"

    @log
    def __init__(self):
        super().__init__()

