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

import math
from enum import Enum
from threading import Lock
from gi.repository import GObject, GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import pympris

class PaginationState:
    def __init__(self, total_items, items_per_page=20):
        self._sensitivities = None
        self._current_page = 1
        self._total_items = total_items
        self._items_per_page = items_per_page
        self._lock = Lock()

        self._n_pages = self._calculate_n_pages()
        self._assign_sensitivities()

    def _assign_sensitivities(self):
        # Single page
        if self._total_items <= self._items_per_page:
            self._sensitivities = (False, False, False, False)
        # First page
        elif self._current_page == 1:
            self._sensitivities = (False, False, True, True)
        # Last page
        elif self._current_page == self._n_pages:
            self._sensitivities = (True, True, False, False)
        # Middle page
        else:
            self._sensitivities = (True, True, True, True)

    def _get_shown_range(self):
        first = (self._current_page - 1) * self._items_per_page + 1
        last = min(self._total_items, first + self._items_per_page - 1)

        return first, last

    def _calculate_n_pages(self):
        return math.ceil(self._total_items / self._items_per_page)

    def goto_next_page(self):
        if self._current_page < self._n_pages:
            self._current_page += 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_previous_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_first_page(self):
        if self._current_page != 1:
            self._current_page = 1
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def goto_last_page(self):
        if self._current_page != self._n_pages:
            self._current_page = self._n_pages
            self._assign_sensitivities()

        return self._current_page, self._sensitivities, self._get_shown_range()

    def update_total_items(self, new_total_items):
        """
        Update the total items encoded by the paginator, e.g. when new messages are received. It's update and not
        increment in case there is a possibility to decrement the total items in the future.

        :param new_total_items: The new value for total_items
        :return: The state of the paginator, as if goto_*_page was selected
        """

        # I don't know if it is the proper way for locking in this case...
        self._lock.acquire()

        # Update appropriate vars
        self._total_items = new_total_items
        self._n_pages = self._calculate_n_pages()
        self._assign_sensitivities()

        self._lock.release()

        return self._current_page, self._sensitivities, self._get_shown_range()

    @property
    def total_items(self):
        return self._total_items

    @property
    def current_page(self):
        return self._current_page


class MetadataSource(Enum):
    EMPTY = 1
    PLAYER = 2
    MANUAL = 3


class MediaPlayersStore:
    def __init__(self):
        self._supported_players = ['org.mpris.MediaPlayer2.{}'.format(id) for id in ['audacious', 'vlc', 'quodlibet']]
        dbus_loop = DBusGMainLoop()
        self._bus = dbus.SessionBus(mainloop=dbus_loop)
        self._media_players = dict()
        self._signal_match = None

        for name in filter(lambda item: item in self._supported_players, self._bus.list_names()):
            mp = pympris.MediaPlayer(str(self._bus.get_name_owner(name)), self._bus)
            print(mp.root.Identity)
            self._media_players[mp.root.Identity] = mp

    def __del__(self):
        # Maybe it is already automatically handled, but I implicitly remove the signal handler to dbus
        if self._signal_match:
            self._signal_match.remove()

    @staticmethod
    def handle_properties_changes(changed_props, invalidated_props):
        for name, value in changed_props.items():
            if name == 'Metadata':
                print('Property %s was change value to %s.' % (name, value))
                title = value['xesam:title'] if 'xesam:title' in value else ''
                artist = value['xesam:artist'] if 'xesam:artist' in value else ''
                album = value['xesam:album'] if 'xesam:album' in value else ''
                cover_url = value['mpris:artUrl'] if 'mpris:artUrl' in value else ''

                # TODO: Create and call a callback to metadata propagator
                print(title, artist, album)

    def switch_to_player(self, player_name):
        return self._media_players[player_name].player.register_properties_handler(MediaPlayersStore.handle_properties_changes)

    def get_players_names(self):
        return list(self._media_players.keys())


class MetadataPropagationState:
    def __init__(self):
        self._source = MetadataSource.EMPTY
        self._current_player = None
        self._players_store = None

    def _find_avalable_players(self):
        self._players_store = MediaPlayersStore()

    def get_players_names(self, rediscover=False):
        if self._players_store is None or rediscover:
            self._find_avalable_players()
        return self._players_store.get_players_names()

    def switch_to_player(self, player_name):
        self._source = MetadataSource.PLAYER
        self._players_store.switch_to_player(player_name)