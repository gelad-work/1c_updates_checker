from requests import Session
from bs4 import BeautifulSoup
from configparser import ConfigParser
from collections import namedtuple
# TODO: handle import errors and/or make setup.py file to download dependencies

# data type for product group
ProductGroup = namedtuple('ProductGroup', ['id', 'name'])
# data type for a product
Product = namedtuple('Product', ['id', 'name'])


def get_releases():
    # Function that is called externally, returns formatted info about releases or an error
    config = ConfigParser()
    try:
        config.read('releases_eu_downloader.ini')
    except (FileNotFoundError, IOError):
        exit('Oops, something wrong with INI file.')
    # TODO: if INI file doesn't exist, create one from the default one
    try:
        html = get_html(config['AUTH']['Login'], config['AUTH']['Password'])
    except KeyError:
        exit('Oops, username and/or password for 1C site not specified.')
    if config['GENERAL'].getboolean('Debug'):
        open('releases_eu.html', 'wb').write(html)
    releases = parse_html(html)
    return releases


def get_html(username, password):
    # Function that gets HTML from 1C site
    with Session() as session:
        post_url = 'https://login.1c.eu/login'
        get_url = 'https://releases.1c.eu/'
        response1 = session.get(get_url)
        soup1 = BeautifulSoup(response1.content, features='html.parser')
        exec_obj = soup1.find('input', {'name': 'execution'})
        payload = {'inviteCode': '', 'inviteType': '', 'username': username, 'password': password,
                   'rememberMe': 'on',
                   'execution': exec_obj['value'], '_eventId': 'submit', 'geolocation': '', 'submit': 'Увійти'}
        response2 = session.post(post_url, data=payload)
        # TODO: check if content is a valid HTML with releases
        return response2.content


def parse_html(html):
    soup = BeautifulSoup(html, features='html.parser')
    table = soup.find('table', {'class': 'customTable'}).tbody
    groups = []
    products = []
    for row in table.findAll('tr'):
        if row.find('td', {'class': 'groupColumn'}):
            groups.append(ProductGroup(id=row.attrs['group'].strip(), name=row.text.strip()))

    result = html  # do some shit
    return result
