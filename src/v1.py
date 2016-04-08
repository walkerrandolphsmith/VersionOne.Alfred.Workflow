import argparse
import sys

from workflow import Workflow, ICON_WEB, ICON_WARNING, web, PasswordNotFound

log = None


def upper_first(x):
    return x[0].upper() + x[1:]


def make_query(url, api_key, params=dict(sel="Name")):
    headers = dict(Authorization=api_key, Accept="application/json")
    r = web.get(url, params, headers)
    r.raise_for_status()

    return r.json()


def get_by_asset_type(url, api_key, asset_type):
    asset_type = upper_first(asset_type)[:-1]
    query_url = url + 'rest-1.v1/Data/' + asset_type
    assets = make_query(query_url, api_key)["Assets"]
    for asset in assets:
        oid = asset['id']
        name = asset['Attributes']['Name']['value']
        arg_to_pass_on_enter_click = url + asset_type + '.mvc/Summary?oidToken=' + oid
        wf.add_item(title=name, subtitle=oid, arg=arg_to_pass_on_enter_click, valid=True, icon=ICON_WEB)
    wf.send_feedback()
    return 0


def get_by_oid(url, api_key, oid):
    asset_type = upper_first(oid.split(':')[0])
    asset_number = oid.split(':')[1]
    query_url = url + 'rest-1.v1/Data/' + asset_type + '/' + asset_number
    asset = make_query(query_url, api_key)
    oid = asset['id']
    name = asset['Attributes']['Name']['value']
    arg_to_pass_on_enter_click = url + asset_type + '.mvc/Summary?oidToken=' + oid
    wf.add_item(title=name, subtitle=oid, arg=arg_to_pass_on_enter_click, valid=True, icon=ICON_WEB)
    wf.send_feedback()
    return 0


def get_by_name(url, api_key, query):
    asset_type = upper_first(query.split(' ', 1)[0])
    name = query.split(' ', 1)[1]
    params = dict(where="Name='" + name + "'")
    query_url = url + 'rest-1.v1/Data/' + asset_type
    assets = make_query(query_url, api_key, params)["Assets"]
    for asset in assets:
        oid = asset['id']
        name = asset['Attributes']['Name']['value']
        arg_to_pass_on_enter_click = url + asset_type + '.mvc/Summary?oidToken=' + oid
        wf.add_item(title=name, subtitle=oid, arg=arg_to_pass_on_enter_click, valid=True, icon=ICON_WEB)
    wf.send_feedback()
    return 0


def open_lobby(url):
    team_room_link = url + "Default.aspx?menu=TeamRoomsPage"
    planning_room_link = url + "Default.aspx?menu=TeamRoomsPage"
    wf.add_item('Open TeamRoom lobby', 'View all the TeamRooms', arg=team_room_link, valid=True, icon=ICON_WEB)
    wf.add_item('Open PlanningRoom lobby', 'View all the PlanningRooms', arg=planning_room_link, valid=True, icon=ICON_WEB)
    wf.send_feedback()


def open_team_room_by_name(url, api_key, query):
    name = query.split('teamroom ')[1]
    query_url = url + 'rest-1.v1/Data/TeamRoom'
    team_room_oid = make_query(query_url, api_key, params=dict(where="Name='" + name + "'"))['Assets'][0]['id'].split(':')[1]
    link = url + 'TeamRoom.mvc/Show/' + team_room_oid
    wf.add_item('Open TeamRoom ' + name, 'View this TeamRoom in browser', arg=link, valid=True, icon=ICON_WEB)
    wf.send_feedback()


def open_menu_item(url, item, title, subtitle, icon):
    link = 'Default.aspx?menu=%s&feat-nav=m1' % item
    wf.add_item(title, subtitle, arg=url + link, valid=True, icon=icon)
    wf.send_feedback()


def open_menu_pages():
    return 0

def act_according_to(query, url, api_key):
    if query == 'lobby':
        open_lobby(url)
    elif query.startswith('teamroom'):
        open_team_room_by_name(url, api_key, query)
    elif query == 'pages':
        open_menu_pages()
    elif query == 'backlog':
        open_menu_item(url, 'PrimaryBacklogPage', 'Open backlog', 'View product backlog', ICON_WEB)
    elif query == 'portfolio tree':
        open_menu_item(url, 'EpicsPortfolioPlanningPage', 'Open portfolio tree', 'View portfolio tree', ICON_WEB)
    elif query == 'reports':
        open_menu_item(url, 'ReportOverviewPage', 'Open reports', 'View all reports', ICON_WEB)
    elif query == 'community of practice':
        open_menu_item(url, 'Conversations', 'Open Community of Practice', 'View all communities of practice', ICON_WEB)
    elif query == 'release scheduling':
        open_menu_item(url, 'ReleaseSchedulingPage', 'Open release scheduling', 'View release scheduling', ICON_WEB)
    elif query == 'program board':
        open_menu_item(url, 'ProgramBoardPage', 'Open program board', 'View program board', ICON_WEB)
    elif query == 'iteration scheduling':
        open_menu_item(url, 'IterationSchedulingPage', 'Open iteration scheduling page', 'View iteration scheduling', ICON_WEB)
    elif ":" in query:
        get_by_oid(url, api_key, query)
    elif query.endswith('s'):
        get_by_asset_type(url, api_key, query)
    else:
        get_by_name(url, api_key, query)


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
