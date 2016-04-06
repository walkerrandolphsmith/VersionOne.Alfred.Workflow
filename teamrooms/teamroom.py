import webbrowser
from workflow import web


def open_lobby(url):
    webbrowser.open(url + "Default.aspx?menu=TeamRoomsPage")


def open_team_room(url, api_key, name):
    team_room_oid = get_asset_oid_from_name(url, api_key, name)
    webbrowser.open(url + 'TeamRoom.mvc/Show/' + team_room_oid)


def get_asset_oid_from_name(url, api_key, name):
    params = dict(where="Name='" + name + "'")
    headers = dict(Authorization=api_key, Accept="application/json")

    print(params, headers, url)

    r = web.get(url + 'rest-1.v1/Data/TeamRoom', params, headers)
    r.raise_for_status()

    return r.json()['Assets'][0]['id'].split(':')[1]

