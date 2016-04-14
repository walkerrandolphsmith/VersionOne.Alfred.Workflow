import sys
from workflow import Workflow
from versionone import V1


def main(wf):
    command = wf.args[0]
    query = wf.args[1] if len(wf.args) > 1 else None
    v1 = V1(wf)

    options = {
        'set_url': v1.set_url,
        'view_url': v1.view_url,
        'set_token': v1.set_token,
        'view_token': v1.view_token,
        'open_menu_pages': v1.open_menu_pages,
        'open_lobby': v1.open_lobby,
        'open_page': v1.open_page,
        'open_teamroom': v1.open_teamroom,
        'open': v1.open_by_asset_type,
        'open_by_id': v1.open_by_oid_token
    }

    results = options[command](query)

    for result in results:
        wf.add_item(
            result['title'],
            result['subtitle'],
            arg=result['arg'],
            valid=result['valid'],
            icon=result['icon']
        )
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
