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
from gi.repository import GObject, Gtk
from dashboard.views import  utils
from dashboard import log


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/GolivePage.ui")
class GolivePage(Gtk.Box):
    """Live page of the application"""

    __gtype_name__ = "GolivePage"

    __gsignals__ = \
        {
            'golive-page-shown': (GObject.SignalFlags.RUN_FIRST, None, ()),
            'golive-attempted': (GObject.SignalFlags.RUN_FIRST, None, ()),
        }

    def __repr__(self):
        return "<GolivePage>"

    @log
    def __init__(self):
        super().__init__()
        self._message = utils.get_descendant(self, 'message_textview', 0)

    @Gtk.Template.Callback()
    @log
    def on_GolivePage_map(self, widget):
        self.emit('golive-page-shown')

    @Gtk.Template.Callback()
    @log
    def on_golive_button_clicked(self, widget):
        self.emit('golive-attempted')

    def set_buffer(self, text_buffer: Gtk.TextBuffer):
        self._message.set_buffer(text_buffer)