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

import gi
from gi.repository import GObject


from collections import namedtuple

Show = namedtuple('Show', ['title', 'users', 'nickname', 'description', 'sites', 'logo_path'])

AsyncResult = namedtuple('AsyncResult', ['self', 'widget', 'actual_result'])


class ShowObject(GObject.Object):
    def __init__(self, title, subtitle, logo_path):
        GObject.GObject.__init__(self)
        self.title = title
        self.subtitle = subtitle
        self.logo_path = logo_path


class MessageObject(GObject.Object):
    def __init__(self, message, sender, timestamp):
        GObject.GObject.__init__(self)
        self.message = message
        self.timestamp = timestamp
        self.sender = sender
