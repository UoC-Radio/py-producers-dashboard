from collections import namedtuple
import lorem

Show = namedtuple('Show', ['title', 'users', 'nickname', 'description', 'sites', 'logo_path'])


class Store:

    sample_descr = lorem.paragraph()

    shows = \
    [
        Show('Rastamidnights', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awsome show description', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
        Show('Awkward show description', ['arouraios'], 'Jerry', sample_descr, ['https://radio.uoc.gr'], ''),
    ]

    def get_user_shows(self, username):
        user_shows = []
        for s in self.shows:
            if username in s.users:
                user_shows.append(s)


def validate_login(username, password):
    #return username == 'arouraios' and password == 'papakia'
    return not (username + password)
