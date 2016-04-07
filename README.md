# VersionOne.alfred.workflow
![Alfred Logo](https://cloud.githubusercontent.com/assets/398893/3528722/5b5b30c6-0792-11e4-956d-750ac3a00bd8.png)

[Alfred 2](https://www.alfredapp.com/) Workflow for interacting with a [VersionOne](https://www.versionone.com/) instance. To learn more about the VersionOne API visit [the documentation site](https://community.versionone.com/Developers)

## Workflows

Enter your VersionOne instance's url  
> Triggers: `v1url`  

Enter your VersionOne API token: 
//Example: Bearer XXXXXXXXXXX  
> Triggers: `v1token`

Open team room lobby:
> Triggers: `v1 open teamroom lobby`

 Open team room by name:
> Triggers: `v1 open teamroom <team room name>`

 Lookup VersionOne assets by type and open asset
> Triggers: `v1 get epics` | `v1 get storys`

 Open VersionOne asset by oid
> Triggers: `v1 open story:12345`

 Open VersionOne asset by name
> Triggers: `v1 open <asset-type> <asset-name>`