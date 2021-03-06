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

from gi.repository import Gtk

from dashboard import log


@Gtk.Template(resource_path='/gr/uoc/radio/dashboard/AboutDialog.ui')
class AboutDialog(Gtk.AboutDialog):
    """About dialog"""

    __gtype_name__ = 'AboutDialog'

    def __repr__(self):
        return '<AboutDialog>'

    @log
    def __init__(self):
        super().__init__()

        self.connect("response", self._about_response)

        self.show()

    @log
    def _about_response(self, klass, data=None):
        klass.destroy()
