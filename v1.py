import sys
from workflow import Workflow, ICON_WEB, web

API_KEY = "Bearer <token>"

def main(wf):
    url = "<url>"
    params = dict(sel="Name")
    headers = dict(Authorization=API_KEY, Accept="application/json")

    r = web.get(url, params, headers)
    r.raise_for_status()

    result = r.json()
    assets = result['Assets']

    for asset in assets:
        title = asset['id']
        subtitle = asset['Attributes']['Name']['value']
        wf.add_item(title=title, subtitle=subtitle, arg="walker", valid=True, icon=ICON_WEB)
    wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
