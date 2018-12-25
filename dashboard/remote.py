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

import lorem
import sqlite3
from dashboard.models import Show

import requests
import math
import json
from abc import ABC, abstractmethod

from gi.repository import Gtk, Gdk, Gio, GLib, GObject


class Store:

    sample_descr = lorem.paragraph()

    shows = \
    [
        Show('Rastamidnights', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awsome show title', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awkward show title', ['ggalan'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
    ]

    def get_user_shows(self, username):
        user_shows = []
        for s in self.shows:
            if username in s.users:
                user_shows.append(s)
        return user_shows


def validate_login(username, password):
    return username == 'arouraios' and password == 'papakia'
    #return not (username + password)


def get_metadata():
    try:
        r = requests.get('http://prod.radio.uoc.gr:9670/')
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        # Awkward way to get the errno from the error message, because it is not stored in the object, unlike older
        # version of the library as reported in:
        # https://stackoverflow.com/questions/19370436/get-errno-from-python-requests-connectionerror
        # msg = e.args[0].reason.args[0]
        # errno = int(re.search(r"\[Errno\ ([0-9]+)\]", msg).group(1))
        # exit(errno)
        return None, 15

    try:
        data = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        print(r.text)
        raise Exception("Strange JSON {}".format(r.text))

    duration = int(data['current_song']['Duration'])
    elapsed = int(data['current_song']['Elapsed'])

    return data, (duration - elapsed)


def query_autopilot_remaining():
    data, next = get_metadata()
    print(data)
    return next


def fetch_sample_messages(page_length, page_number):
    conn = sqlite3.connect('../data/sample_db/radioShows.db')
    c = conn.cursor()
    c.execute('SELECT * FROM messages WHERE recepient is null')
    all = c.fetchall()

    len_all = len(all)
    data_slice = slice(max(0, len_all - page_length * page_number), len_all - page_length * (page_number - 1))
    return all[data_slice][::-1], len_all


class MessagesFetcher(GObject.GObject):
    """
    A class for handling messages fetching from the database
    """

    __gsignals__ = \
        {
            'new_messages_received': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
         }

    def __init__(self, page_length):
        super().__init__()
        self._page_length = page_length
        self._current_messages = None
        self._update_timestamp = None

    @property
    def update_timestamp(self):
        return self._update_timestamp

    @abstractmethod
    def _fetch_messages(self):
        pass

    @abstractmethod
    def fetch_first_time_messages(self):
        pass


class MockMessagesFetcher(MessagesFetcher):
    def __init__(self, page_length):
        super().__init__(page_length)

        # Keep a set of hypothetical future messages, in order to imitate the functionality that some messages are
        # coming later on
        self._future_messages = None
        self._timer_id = None

    def _fetch_messages(self):
        pass

    def fetch_first_time_messages(self):
        # Imitate message fetching by doing the following
        # 0. Fetch all messages from mock database
        # 1. Set the  timer to an arbitrary later message timestamp
        # 2. Schedule a timer to obtain some messages gradually
        self._init_sample_messages()

        # Fetch a new message every 2 seconds
        GLib.timeout_add(2000, self._timer_callback)

        return self.get_page_messages(1)

    def _timer_callback(self):
        if len(self._future_messages) == 0:
            self._invalidate_timer()
            return False
        else:
            self._current_messages.append(self._future_messages.pop())
            # It is by design that new messages are not passed as param to the signal. That is to have common,
            # functionality for every case of pagination. E.g. if someone is at page 2, new messages should not appear
            # but only if the user selects the 1st page. If the user is already at the first page, then a fetch of all
            # 1st-page messages will be issued for fetching, including the new and excluding last of the old. I think it
            # is lightweight enough, to not implement a more sophisticated functionality
            self.emit('new-messages-received', 1)
            return True

    def _invalidate_timer(self):
        if self._timer_id:
            GLib.source_remove(self._timer_id)

    def get_page_messages(self, page_number):
        len_current = len(self._current_messages)
        data_slice = slice(max(0, len_current - self._page_length * page_number), len_current - self._page_length * (page_number - 1))
        return self._current_messages[data_slice][::-1], len_current

    def _init_sample_messages(self):
        conn = sqlite3.connect('../data/sample_db/radioShows.db')
        c = conn.cursor()
        c.execute('SELECT * FROM messages WHERE recepient is null')
        all = c.fetchall()

        self._future_messages = all[-20:][::-1]
        self._current_messages = all[:-20]
