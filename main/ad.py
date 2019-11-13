from ldap3 import Connection


def checkUserInAD(login, password):
    AD_HOST = "ldap.x5.ru"
    ldap_url = "ldap://" + AD_HOST
    conn = Connection(ldap_url, user = login, password = password)
    conn.bind()
    conn.unbind()
    if conn.result['result'] != 0:
        return False
    return True