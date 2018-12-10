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
            'goto-next-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'goto-previous-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'goto-first-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'goto-last-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

    def __repr__(self):
        return "<LivePage>"

    @log
    def __init__(self):
        super().__init__()
        self._message = utils.get_descendant(self, 'message_textview', 0)

        self._pagination_info = utils.get_descendant(self, 'pagination_info', 0)
        self._goto_first_button = utils.get_descendant(self, 'goto_first_button', 0)
        self._goto_previous_button = utils.get_descendant(self, 'goto_previous_button', 0)
        self._goto_next_button = utils.get_descendant(self, 'goto_next_button', 0)
        self._goto_last_button = utils.get_descendant(self, 'goto_last_button', 0)

    @Gtk.Template.Callback()
    @log
    def on_LivePage_map(self, widget):
        self.emit('live-page-shown')

    @Gtk.Template.Callback()
    @log
    def on_goto_first_button_clicked(self, widget):
        self.emit('goto-first-clicked')

    @Gtk.Template.Callback()
    @log
    def on_goto_previous_button_clicked(self, widget):
        self.emit('goto-previous-clicked')

    @Gtk.Template.Callback()
    @log
    def on_goto_next_button_clicked(self, widget):
        self.emit('goto-next-clicked')

    @Gtk.Template.Callback()
    @log
    def on_goto_last_button_clicked(self, widget):
        self.emit('goto-last-clicked')

    def set_buffer(self, text_buffer: Gtk.TextBuffer):
        self._message.set_buffer(text_buffer)

    def update_pagination(self, info, sensitivities):
        self._pagination_info.set_text(info)

        self._goto_first_button.set_sensitive(sensitivities[0])
        self._goto_previous_button.set_sensitive(sensitivities[1])
        self._goto_next_button.set_sensitive(sensitivities[2])
        self._goto_last_button.set_sensitive(sensitivities[3])
