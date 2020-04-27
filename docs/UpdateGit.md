# UpdateGit


Class to update all git repositories in a specific Folder. 

## Methods


### __init__


Initializes the base_dir (defaults to './' ) and sets up logging 

#### Parameters
name | description | default
--- | --- | ---
self |  | 
directory |  | "./"





### discover


Discovers the Repositories in the specified Folder (searches for .git folders) 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### status


Runs 'git status' for all the found repositories 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### pull


Runs 'git pull' for all the found repositories 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### push


Runs 'git push' for all the found repositories 

#### Parameters
name | description | default
--- | --- | ---
self |  | 





### update


Runs 'git pull' and 'git push' for all the found repositories 

#### Parameters
name | description | default
--- | --- | ---
self |  | 




