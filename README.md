# VersionOne.alfred.workflow
![Alfred Logo](https://cloud.githubusercontent.com/assets/398893/3528722/5b5b30c6-0792-11e4-956d-750ac3a00bd8.png)

[Alfred 2](https://www.alfredapp.com/) Workflow for interacting with a [VersionOne](https://www.versionone.com/) instance. To learn more about the VersionOne API visit [the documentation site](https://community.versionone.com/Developers)

## Workflows

Enter your VersionOne instance's url  
> Triggers: `v1url`  

Enter your VersionOne API token: 
//Example: Bearer XXXXXXXXXXX  
> Triggers: `v1token`

Open lobby:
> Triggers: `v1 open lobby`

<img width="500" alt="colors" src="./screenshots/v1-open-lobby.png">

 Open team room by name:
> Triggers: `v1 open teamroom <team room name>`

<img width="500" alt="colors" src="./screenshots/v1-open-teamroom-x.png">

 Lookup VersionOne assets by type and open asset
> Triggers: `v1 open epics` | `v1 open storys`

<img width="500" alt="colors" src="./screenshots/v1-open-asset-by-asset-type.png">

 Open VersionOne asset by oid
> Triggers: `v1 open story:12345`

<img width="500" alt="colors" src="./screenshots/v1-open-by-asset-oid.png">

 Open VersionOne asset by name
> Triggers: `v1 open <asset-type> <asset-name>`

<img width="500" alt="colors" src="./screenshots/v1-open-asset-by-name.png">

 Set single value relations to assets
 > Triggers: `v1 set <oid> <relation-name>`

 <img width="500" alt="colors" src="./screenshots/v1-set-single-value-relation-by-relation-name.png">