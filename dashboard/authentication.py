import ldap3


def _ldap_auth(uri, base, username, password):
    ldap_username = 'CN={0},OU=Users,{1}'.format(username, base)

    server = ldap3.Server(uri)

    try:
        with ldap3.Connection(server, user=ldap_username, password=password, auto_bind=True) as conn:
            pass
        return True
    except ldap3.core.exceptions.LDAPBindError:
        print('Wrong username/password')
        return False
    except ldap3.core.exceptions.LDAPExceptionError:
        print('LDAP Exception')
        return False


def _parse_nss_ldap_conf(filepath='/etc/ldap.conf'):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    keys = ['base', 'uri']
    props = dict()
    for l in lines:
        l = l[:-1]
        if len(l) == 0 or l[0] == '#':
            continue
        prop, rest = l.split(' ', 1)
        if prop in keys:
            props[prop] = rest.replace('\"', '')

    if len(keys) != len(props):
        raise ValueError('nss ldap config file {} does not contain required information.'.format(filepath))

    return props


def authenticate(username, password):
    info = _parse_nss_ldap_conf()
    return _ldap_auth(info['uri'], info['base'], username, password)
