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




