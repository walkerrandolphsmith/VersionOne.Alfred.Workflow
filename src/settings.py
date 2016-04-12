import argparse
import sys

from workflow import Workflow, ICON_WEB, ICON_ACCOUNT, PasswordNotFound

log = None


pages = {
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

def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)

    query = args.query
    if query:
        if query == 'view url':
            url = wf.settings.get('url')
            wf.add_item(url, 'VersionOne url previously set', valid=False, icon=ICON_ACCOUNT)
            wf.send_feedback()
        if query.startswith('update url'):
            new_url = query.split('update url ')[1]
            wf.settings['url'] = new_url
            wf.add_item(new_url, 'VersionOne url updated', valid=False, icon=ICON_ACCOUNT)
            wf.send_feedback()
        if query == 'view token':
            try:
                api_key = wf.get_password('api_key')
                wf.add_item(api_key, 'VersionOne token previously set', valid=False, icon=ICON_ACCOUNT)
                wf.send_feedback()
            except PasswordNotFound:
                return 0
        if query.startswith('update token'):
            new_token = query.split('update token ')[1]
            wf.save_password('api_key', new_token)
            wf.add_item(new_token, 'VersionOne token updated', valid=False, icon=ICON_ACCOUNT)
            wf.send_feedback()
        if query == 'view pages':
            pgs = wf.settings.get('pages')
            for page in pgs:
                wf.add_item(page, 'VersionOne menu links', valid=False, icon=ICON_WEB)
            wf.send_feedback()
        '''
        if query.startswith('update page '):
            request = query.split('update page ')[1]
            page_to_update, new_name = request.split('to ')
            page_to_update = page_to_update[:-1]
            if page_to_update and new_name:
                pgs = wf.settings['pages']
                if pgs[page_to_update]:
                    # Note that since this is run approx each keystroke I would need to delete every intermediate save to dict not just the original key :(
                    #wf.settings['pages'][new_name] = wf.settings['pages'][page_to_update]
                    #del wf.settings['pages'][page_to_update]
                    wf.add_item(page_to_update, new_name, valid=False, icon=ICON_WEB)
                    wf.send_feedback()
            else:
                wf.add_item("Specify and page to udpate and the new name", 'update x to y', valid=False, icon=ICON_WEB)
            wf.send_feedback()
        '''

if __name__ == u"__main__":
    wf = Workflow()
    pages_exists_in_settings = wf.settings.get('pages', False)
    if not pages_exists_in_settings:
       wf.settings['pages'] = pages
    log = wf.logger
    sys.exit(wf.run(main))
