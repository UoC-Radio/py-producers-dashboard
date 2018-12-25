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
