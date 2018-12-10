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
            'wait-page-shown': (GObject.SignalFlags.RUN_FIRST, None, ()),
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
        self._remaining_stack = utils.get_descendant(self, 'remaining_stack', 0)

    @Gtk.Template.Callback()
    @log
    def on_WaitPage_map(self, widget):
        self.emit('wait-page-shown')

    @Gtk.Template.Callback()
    @log
    def on_instant_button_clicked(self, widget):
        self.emit('instant-attempted')

    @Gtk.Template.Callback()
    @log
    def on_cancel_button_clicked(self, widget):
        self.emit('cancel-attempted')

    def set_buffer(self, text_buffer: Gtk.TextBuffer):
        self._message.set_buffer(text_buffer)

    def set_title(self, txt):
        self._show_title.set_text(txt)

    def set_wait(self):
        self._remaining_stack.set_visible_child_name('wait_spinner')

    def set_remaining(self, txt):
        self._remaining.set_text(txt)
        self._remaining_stack.set_visible_child_name('remaining_label')

