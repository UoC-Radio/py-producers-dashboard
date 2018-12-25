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


@Gtk.Template(resource_path="/gr/uoc/radio/dashboard/Message.ui")
class Message(Gtk.Box):
    """Message item for inbox"""

    __gtype_name__ = "Message"

    def __repr__(self):
        return "<Message>"

    @log
    def __init__(self, message, sender, timesamp):
        super().__init__()
        self._message = utils.get_descendant(self, 'inbox_message_textview', 0)
        self._sender = utils.get_descendant(self, 'sender_label', 0)
        self._timestamp = utils.get_descendant(self, 'timestamp_label', 0)

        self._message.get_buffer().set_text(message)
        self._sender.set_text(sender)
        self._timestamp.set_text(timesamp)
