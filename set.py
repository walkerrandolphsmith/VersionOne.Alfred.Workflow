import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

log = None


def upper_first(x):
    return x[0].upper() + x[1:]


def make_query(url, api_key, params=dict(sel="Name")):
    headers = dict(Authorization=api_key, Accept="application/json")
    r = web.get(url, params, headers)
    r.raise_for_status()

    return r.json()


def act_according_to(query, url, api_key):
    parts = query.split(' ', 3)

    oid, attribute = parts
    asset_type, asset_number = oid.split(':')
    # get all the attribute values

    query_url = url + 'rest-1.v1/Data/' + upper_first(asset_type) + upper_first(attribute)
    assets = make_query(query_url, api_key)['Assets']
    for asset in assets:
        asset_oid = asset['id']
        asset_name = asset['Attributes']['Name']['value']
        title = asset_name
        subtitle = 'Set ' + oid + ', ' \
            + upper_first(asset_type) + upper_first(attribute) \
            + ' to ' + asset_oid + ' ' + asset_name
        link = oid + " " + asset_oid
        wf.add_item(title, subtitle, arg=link, valid=True, icon=ICON_WEB)
    wf.send_feedback()


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
        act_according_to(query, url, api_key)

if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
