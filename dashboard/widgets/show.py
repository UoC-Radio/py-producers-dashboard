from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/Show.ui")
class Show(Gtk.Box):
    """Show item for shows"""

    __gtype_name__ = "Show"

    def __repr__(self):
        return "<Show>"

    @log
    def __init__(self, title, subtitle, icon_path):
        super().__init__()
        self._title = utils.get_descendant(self, 'title_label', 0)
        self._subtitle = utils.get_descendant(self, 'subtitle_label', 0)
        self._icon = utils.get_descendant(self, 'icon_image', 0)

        self._title.set_text(title)
        self._subtitle.set_text(subtitle)
