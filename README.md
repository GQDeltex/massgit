# massgit

Massgit is a simple CLI-Tool to help you manage all of your git repositories.

I wrote it because I have a folder in my home directory containing all of my git repositories. I wanted to be able to pull changes for all my repositories at the same time and then also implemented the push function to move all local changes (maybe of multiple repositories) to git.

## Usage

Make sure the python file is executable

```bash
sudo chmod +x /path/to/massgit/massgit.py
```

The Script uses the Folder it is executed in as the root folder to search for git repos or the folder you specify as an argument.

```bash
$ massgit.py -h
usage: massgit.py [-h] [--status] [--push] [--pull] [--update] [folder]

Git bulk processor

positional arguments:
  folder        Folder in which all the repositories are in (default this
                folder './')

optional arguments:
  -h, --help    show this help message and exit
  --status, -s  Get the Status of all Repositories (default)
  --push, -p    Push all Repositories
  --pull, -g    Pull all Repositories
  --update, -u  Update (Pull then Push) all Repositories
```

## Tips & Tricks

There are multiple ways to make execution a lot easier:

1. .bashrc alias

    Add to `~/.bashrc`

    ```bash
    # Make massgit available as command
    alias massgit=/path/to/massgit/massgit.py
    ```

    Then you have to source the `~/.bashrc` file or log out and in again

    ```bash
    source ~/.bashrc
    ```

2. symbolic link in `/usr/bin/` **or** `/bin/`

    link in `/usr/bin`

    ```bash
    ls -s /path/to/massgit/massgit.py /usr/bin/massgit
    ```

    or link in `/bin`

    ```bash
    ls -s /path/to/massgit/massgit.py /bin/massgit
    ```

After either one of them you should be able to call the script from anywhere using only

```bash
massgit
```
