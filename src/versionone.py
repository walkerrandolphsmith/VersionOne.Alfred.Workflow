from workflow import web, ICON_ACCOUNT, ICON_WEB

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
