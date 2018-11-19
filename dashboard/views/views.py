import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GIRepository', '2.0')
gi.require_version('Gst', '1.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import GIRepository, Gio, Gtk, Gst, Gdk, cairo, Pango, PangoCairo, GObject
from gi.repository.GdkPixbuf import Pixbuf

from dashboard.custom_renderers import *


class ShowsColumns(Enum):
    ICON = 0
    TITLE = 1
    SUBTITLE = 2
    N_COLUMNS = 3


def setup_shows_treeview(tv, shows):
    # Check if already set, e.g. case Cancel button has been clicked
    if len(tv.get_columns()) > 0:
        return

    fallback_icon_name = 'audio-x-generic-symbolic'

    icon_theme = Gtk.IconTheme.get_default()

    # List Store
    tm = Gtk.ListStore(Pixbuf, str, str)

    for s in shows:
        tm.append([icon_theme.load_icon(fallback_icon_name, 48, Gtk.IconLookupFlags.FORCE_SVG), s.title, s.nickname])

    # The TreeView:
    tv.set_model(tm)

    tv.headers_visible = False

    renderer = ProducerShowsCellRenderer()
    col = Gtk.TreeViewColumn("My shows", renderer)

    col.add_attribute(renderer, "icon", ShowsColumns.ICON.value)
    col.add_attribute(renderer, "title", ShowsColumns.TITLE.value)
    col.add_attribute(renderer, "subtitle", ShowsColumns.SUBTITLE.value)
    tv.append_column(col)


class MessageColumns(Enum):
    SENDER = 0
    TIMESTAMP = 1
    MESSAGE = 2
    N_COLUMNS = 3
