# Copyright © 2018 George Galanakis <ggalan87@gmail.com>
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from gettext import gettext as _, ngettext
from gi.repository import GObject, Gtk, Gdk

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

    @Gtk.Template.Callback()
    @log
    def on_LoginPage_key_release_event(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            self.on_login_button_clicked(widget)
