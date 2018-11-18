from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk

from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/LoginPage.ui")
class LoginPage(Gtk.Box):
    """Login page of the application"""

    __gtype_name__ = "LoginPage"

    __gsignals__ = \
        {
            'login-attempted': (GObject.SignalFlags.RUN_FIRST, None, (str, str)),
        }

    def __repr__(self):
        return "<LoginPage>"

    @log
    def __init__(self):
        super().__init__()
        for c in self.get_children():
            if Gtk.Buildable.get_name(c) == 'username_entry':
                self._username_entry = c
            elif Gtk.Buildable.get_name(c) == 'password_entry':
                self._password_entry = c

    @Gtk.Template.Callback()
    @log
    def on_login_button_clicked(self, widget):
        username = self._username_entry.get_text()
        password = self._password_entry.get_text()

        self.emit('login-attempted', username, password)
