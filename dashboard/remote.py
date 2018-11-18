from collections import namedtuple

Show = namedtuple('Show', ['title', 'users', 'nickname', 'description', 'sites', 'logo_path'])


class Store:

    sample_descr = \
        """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
        ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in 
        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """

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
