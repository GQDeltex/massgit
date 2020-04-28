# UpdateGit
Authors: **GQDeltex**

Main Class of the Git Updater. Houses all the functions, can also be used to import into other projects.   


## Methods


### __init__


Initializes the Class and sets up some basic Variables   
  


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 
directory | The directory in which to search for git repositories | "./"
emojis | If you want to enable emojis in the console output or not | True





### discover


Discovers the Repositories in the specified Folder (searches for .git folders)   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 





### status


Runs 'git status' for all the found repositories   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 





### pull


Runs 'git pull' for all the found repositories   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 





### push


Runs 'git push' for all the found repositories   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 





### update


Runs 'git pull' and 'git push' for all the found repositories   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 





### has_remote_tracking


Creates tracking information for active branch if branch with the same name exists on the remote   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 
repo | The repo object to perform the action on | 





### log_status


Print status messages with progress, repo, branch, icon and message   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 
done | (int) Current index in the list | 
total | (int) Total number of Repos | 
repo | (str) Name of current Repo | 
branch | (str) Name of current Branch | 
icon | (str) Icon to display (Emoji/Text) | 
message | (str) message to display for more information | 





### icon


Matches either Icon or Text to icon name   


#### Parameters
name | description | default
--- | --- | ---
self | The parent class | 
name | The name of the Icon | 




