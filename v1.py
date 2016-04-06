import sys
import argparse
import webbrowser
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

log = None


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


def make_query(url, api_key):
    params = dict(sel="Name")
    headers = dict(Authorization=api_key, Accept="application/json")

    print(params, headers, url)

    r = web.get(url + 'rest-1.v1/Data/Team', params, headers)
    r.raise_for_status()

    result = r.json()
    return result['Assets']


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--seturl', dest='url', nargs='?', default=None)
    parser.add_argument('--setkey', dest='apikey', nargs='?', default=None)
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    if args.url:
        wf.settings['url'] = args.url
        return 0

    url = wf.settings.get('url', None)
    if not url:
        wf.add_item('Set VersionOne Url', 'Please use v1url to set your instace url', valid=False, icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    if args.apikey:
        wf.save_password('api_key', args.apikey)
        return 0

    try:
        api_key = wf.get_password('api_key')
    except PasswordNotFound:
        wf.add_item('Set API Token', 'Please use v1token to set your API token', valid=False, icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    query = args.query
    if query:
        open_team_room(url, api_key, query)
    else:
        assets = make_query(url, api_key)
        for asset in assets:
            title = asset['id']
            subtitle = asset['Attributes']['Name']['value']
            wf.add_item(title=title, subtitle=subtitle, arg="walker", valid=True, icon=ICON_WEB)
        wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
