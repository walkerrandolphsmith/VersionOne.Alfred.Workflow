import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

log = None


def main(wf):
    print('here')
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
        print(query)
        oid, related_oid = query.split(' ')
        asset_type, asset_number = oid.split(':')
        query_url = url + 'rest-1.v1/Data/' + asset_type + '/' + asset_number
        headers = dict(Authorization=api_key, Accept="application/json")
        params = dict()
        data = dict()
        #params = json({
        # "id": "Story:1185",
        # "Attributes": {
        #   "Status": {
        #   "name": "Status",
        #   "value": "StoryStatus:135",
        #   "act": "set"
        #  }
        # }
        #})
        web.request(method='POST',url=query_url,params=params,data=data,headers=headers)


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))