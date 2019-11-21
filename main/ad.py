from ldap3 import Connection, ALL_ATTRIBUTES, SUBTREE


def checkUserInAD(login, password):
    AD_HOST = "ldap.x5.ru"
    ldap_url = "ldap://" + AD_HOST
    conn = Connection(ldap_url, user = login, password = password)
    conn.bind()
    conn.unbind()
    if conn.result['result'] == 0:
        return True
    return False

def checkUserGroup(login, password):
    AD_HOST = "ldap.x5.ru"
    ldap_url = "ldap://" + AD_HOST
    conn = Connection(ldap_url, user = login, password = password)
    conn.bind()
    response = conn.extend.standard.paged_search(
        search_base='OU=Main,DC=X5,DC=ru',
        search_filter='(mail={})'.format(login),
        search_scope=SUBTREE,
        attributes=ALL_ATTRIBUTES,
        generator=False)[0]['attributes']
    groups = response._store['memberOf']
    target = 0
    for group in groups:
        if group == 'CN=Operational_DB_DM_TSX,OU=Security,OU=Groups,OU=Central,OU=Main,DC=X5,DC=ru':
            target = 1
            break
    conn.unbind()
    if target == 1:
        return True
    return False
