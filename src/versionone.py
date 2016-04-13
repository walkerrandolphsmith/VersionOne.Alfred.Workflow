from workflow import web, PasswordNotFound, ICON_ACCOUNT, ICON_WEB

class V1(object):
    def __init__(self, workflow):
        super(V1, self).__init__()
        self._workflow = workflow

        pages_exists_in_settings = self._workflow.settings.get('pages', False)
        if not pages_exists_in_settings:
            self._workflow.settings['pages'] = {
            'strategic themes': ['StrategicThemesPage', 'Open strategic themes', 'View strategic themes', ICON_WEB],
            'epic tree': ['EpicsPortfolioPlanningPage', 'Open portfolio tree', 'View portfolio tree', ICON_WEB],
            'epic board': ['EpicBoardPage', 'Open portfolio kanban', 'View portfolio kanban', ICON_WEB],
            'epic timeline': ['EpicTimelinePage', 'Open epic timeline', 'View epic timeline', ICON_WEB],
            'project timeline': ['ProjectTimelinePage', 'Open project timeline', 'View project timeline', ICON_WEB],

            'backlog': ['PrimaryBacklogPage', 'Open backlog', 'View product backlog', ICON_WEB],
            'issues': ['IssuesProductPlanningPage', 'Open blocking issues', 'View blocking issues', ICON_WEB],
            'regression tests': ['RegressionTestPage', 'Open regression tests', 'View regression tests', ICON_WEB],
            'reports': ['ReportOverviewPage', 'Open reports', 'View reports', ICON_WEB],
            'cop': ['Conversations', 'Open reports', 'View reports', ICON_WEB],
            'release scheduling': ['ReleaseSchedulingPage', 'Open release scheduling', 'View release scheduling', ICON_WEB],
            'program board': ['ProgramBoardPage', 'Open program board', 'View program board', ICON_WEB],
        }

    def make_query(self, url, params=dict(sel="Name")):
        base_url = self.get_url()
        token = self.get_token()
        if not token.startswith('Bearer '):
            token = 'Bearer ' + token

        rest_url = '%srest-1.v1/Data/%s' % (base_url, url)
        headers = dict(Authorization=token, Accept="application/json")
        r = web.get(rest_url, params, headers)
        r.raise_for_status()

        return r.json()

    def upper_first(self, x):
        return x[0].upper() + x[1:]

    def set_url(self, url):
        self._workflow.settings['url'] = url
        self._workflow.settings.save()

    def view_url(self, query):
        url = self.get_url()
        info = {
            "title": url,
            "subtitle": 'Current VersionOne instance URL',
            "arg": None,
            "valid": False,
            "icon": ICON_ACCOUNT
        }
        return [info]

    def get_url(self):
        url = self._workflow.settings.get('url')

        if not url:
            self._workflow.add_item("No VersionOne url set, please set using command: 'v1 set url'")
            self._workflow.send_feedback()
        return url

    def set_token(self, token):
        self._workflow.save_password('api_key', token)
        self._workflow.settings.save()

    def view_token(self, query):
        token = self.get_token()
        info = {
            "title": token,
            "subtitle": 'Current VersionOne instance token',
            "arg": None,
            "valid": False,
            "icon": ICON_ACCOUNT
        }
        return [info]

    def get_token(self):
        try:
            token = self._workflow.get_password('api_key')
        except PasswordNotFound:
            self._workflow.add_item("No VersionOne token set, please set using command: 'v1 set token'")
            self._workflow.send_feedback()
        return token

    def open_menu_pages(self, query):
        results = []
        url = self._workflow.settings['url']
        pages = self._workflow.settings['pages']
        for page in pages:
            item, title, subtitle, icon = pages[page]
            link = 'Default.aspx?menu=%s&feat-nav=m1' % item
            info = {
                "title": title,
                "subtitle": subtitle,
                "arg": url + link,
                "valid": True,
                "icon": icon
            }
            results.append(info)
        return results

    def open_lobby(self, query):
        url = self.get_url()
        return [
            {
                "title": 'Open TeamRoom Lobby',
                "subtitle": 'View all TeamRooms',
                "arg": url + "Default.aspx?menu=TeamRoomsPage",
                "valid": True,
                "icon": ICON_WEB
            },
            {
                "title": 'Open PlanningRoom Lobby',
                "subtitle": 'View all PlanningRooms',
                "arg": url + "Default.aspx?menu=PlanningRoomsPage",
                "valid": True,
                "icon": ICON_WEB
            }
        ]

    def open(self, query):
        url = self.get_url()
        page = self._workflow.settings['pages'][query]
        if page:
            link, title, subtitle, icon = page
            return [
                {
                    "title": title,
                    "subtitle": subtitle,
                    "arg": '%sDefault.aspx?menu=%s&feat-nav=m1' % (url, link),
                    "valid": True,
                    "icon": icon

                }
            ]
        else:
            return []

    def open_teamroom(self, name):
        url = self.get_url()
        results = self.make_query('TeamRoom', params=dict(where="Name='" + name + "'"))
        team_room_oid = results['Assets'][0]['id'].split(':')[1]
        return [
            {
                "title": 'Open TeamRoom %s' % name,
                "subtitle": 'View TeamRoom in browser',
                "arg": '%sTeamRoom.mvc/Show/%s' % (url, team_room_oid),
                "valid": True,
                "icon": ICON_WEB
            }
        ]

    def open(self, query):
        if ":" in query:
            return self.open_by_oid_token(query)
        elif query.endswith('s'):
            return self.open_by_asset_type(query)
        else:
            return []

    def open_by_asset_type(self, asset_type):
        url = self.get_url()
        asset_type = self.upper_first(asset_type)[:-1]
        assets = self.make_query(asset_type)["Assets"]
        results = []
        for asset in assets:
            oid = asset['id']
            info = {
                "title": asset['Attributes']['Name']['value'],
                "subtitle": oid,
                "arg": url + asset_type + '.mvc/Summary?oidToken=' + oid,
                "valid": True,
                "icon": ICON_WEB
            }
            results.append(info)
        return results

    def open_by_oid_token(self, oid):
        url = self.get_url()
        asset_type, asset_number = oid.split(':')
        asset_type = self.upper_first(asset_type)
        asset = self.make_query(asset_type + '/' + asset_number)
        oid = asset['id']
        return [
            {
                "title": oid,
                "subtitle": asset['Attributes']['Name']['value'],
                "arg": url + asset_type + '.mvc/Summary?oidToken=' + oid,
                "valid": True,
                "icon": ICON_WEB
            }
        ]

    '''
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
    '''



    '''
    def set(query, url, api_key):
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
    '''


    '''
    def rest_post(query)
        oid, related_oid = query.split(' ')
            asset_type, asset_number = oid.split(':')
            query_url = url + 'rest-1.v1/Data/' + asset_type + '/' + asset_number
            headers = dict({
                "Authorization": api_key,
                "Accept": "application/json",
                "Content-Type": "application/json"
            })
            data = dict({
                "id": 'Story:1185',
                "Attributes": {
                    "Status": {
                        "name": "Status",
                        "value": 'StoryStatus:133',
                        "act": "set"
                    }
                }
            })
    '''
