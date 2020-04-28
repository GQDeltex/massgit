#!/usr/bin/python3
"""
Python Module to Update all git repositories in a specific Folder (e.g. ./)
"""
import argparse
import os
import logging
import git

class UpdateGit(object):
    """
    Main Class of the Git Updater.
    Houses all the functions, can also be used to import into other projects.

    @author GQDeltex
    """
    def __init__(self, directory="./", emojis=True):
        """
        Initializes the Class and sets up some basic Variables


        @param self The parent class
        @param directory The directory in which to search for git repositories
        """
        # Get the Specified Folder and resolve ~ Paths
        self.base_dir = os.path.abspath(os.path.expanduser(directory))
        self.directories = {}
        self.bad_folders = []
        self.log = logging.getLogger(__name__)
        self.emojis = emojis

    def discover(self):
        """
        Discovers the Repositories in the specified Folder (searches for .git folders)

        @param self The parent class
        """
        self.log.info("Discovering Git Repositories")
        all_available = os.listdir(self.base_dir)
        self.bad_folders = []
        for folder in all_available:
            if os.path.isdir(os.path.join(self.base_dir, folder)):
                if os.path.isdir(os.path.join(self.base_dir, folder, ".git")):
                    repo = git.Repo(os.path.join(self.base_dir, folder))
                    self.directories[folder] = repo
                else:
                    self.bad_folders.append(folder)
        if self.bad_folders:
            self.log.info("Found Folders that are not git Repos:")
            for index in range(len(self.bad_folders)):
                folder = self.bad_folders[index]
                self.log.info(" %02d -> %s", index, str(folder))
        if len(self.directories) < 1:
            self.log.warning("Found 0 Repositories in %s", self.base_dir)
            exit()
        self.log.info("Done. Found %d Repositories", len(self.directories))

    def status(self):
        """
        Runs 'git status' for all the found repositories

        @param self The parent class
        """
        errors = 0
        index = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Checking Status")
        for folder in self.directories:
            repo = self.directories[folder]
            status = repo.git.status()
            index += 1
            if not status:
                errors += 1
            branch = status.split("\n")[0].replace("On branch ", "").strip()
            if "nothing to commit, working tree clean" in status:
                if self.emojis:
                    icon = "✔️ "
                else:
                    icon = "OK"
                message = "Everything up to date"
            else:
                if status:
                    errors += 1
                if self.emojis:
                    icon = "❌ "
                else:
                    icon = "ERR"
                message = "\n{}".format(status)
            status = "[{done:02d}/{all:02d}] {repo}:{branch} {icon} -> {message}".format(
                done=index,
                all=len(self.directories),
                icon=icon,
                repo=folder,
                branch=branch,
                message=message
            )
            self.log.info("%s", status.strip())
        if errors > 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "%d of %d Repositories up to date",
            len(self.directories)-errors,
            len(self.directories)
        )

    def pull(self):
        """
        Runs 'git pull' for all the found repositories

        @param self The parent class
        """
        errors = 0
        index = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Pulling Repositories")
        for folder in self.directories:
            repo = self.directories[folder]
            if repo.remotes:
                if repo.heads[str(repo.active_branch)].tracking_branch():
                    try:
                        status = repo.git.pull()
                    except git.exc.GitCommandError as error:
                        status = "Error while Pulling Repo:\n{}".format(error)
                else:
                    origin = repo.remote(repo.remotes[0])
                    if str(repo.active_branch) in origin.refs:
                        self.log.info("Setting up remote tracking branch")
                        repo.heads[str(repo.active_branch)].set_tracking_branch(origin.refs[str(repo.active_branch)])
                        try:
                            status = repo.git.pull()
                        except git.exc.GitCommandError as error:
                            status = "Error while Pulling Repo:\n{}".format(error)
                    else:
                        status = "No upstream branch"
            else:
                status = "No remote set up"
            index += 1
            if not status:
                errors += 1
                status = "Got no status"
            if "Already up to date." in status:
                if self.emojis:
                    icon = "✔️ "
                else:
                    icon = "OK"
                message = "Already up to date"
            elif (
                    ("No remote set up" in status) or
                    ("Error while Pulling Repo" in status) or
                    ("Got no status" in status) or
                    ("No upstream branch")
                ):
                if self.emojis:
                    icon = "❌ "
                else:
                    icon = "ERR"
                message = "{}".format(status)
            else:
                if self.emojis:
                    icon = "📥 "
                else:
                    icon = "PULL"
                message = "Pulling Repo"
            status = "[{done:02d}/{all:02d}] {repo}:{branch} {icon} -> {message}".format(
                done=index,
                all=len(self.directories),
                icon=icon,
                repo=folder,
                branch=str(repo.active_branch),
                message=message
            )
            self.log.info("%s", status.strip())
        if errors > 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "Pulled %d of %d Repositories in the Folder",
            len(self.directories)-errors,
            len(self.directories)
        )

    def push(self):
        """
        Runs 'git push' for all the found repositories

        @param self The parent class
        """
        errors = 0
        index = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Pushing Repositories")
        for folder in self.directories:
            repo = self.directories[folder]
            if repo.remotes:
                if repo.heads[str(repo.active_branch)].tracking_branch():
                    try:
                        status = repo.git.push()
                    except git.exc.GitCommandError as error:
                        status = "Error while Pulling Repo:\n{}".format(error)
                else:
                    origin = repo.remote(repo.remotes[0])
                    if str(repo.active_branch) in origin.refs:
                        self.log.info("Setting up remote tracking branch")
                        repo.heads[str(repo.active_branch)].set_tracking_branch(origin.refs[str(repo.active_branch)])
                        try:
                            status = repo.git.push()
                        except git.exc.GitCommandError as error:
                            status = "Error while Pulling Repo:\n{}".format(error)
                    else:
                        status = "No upstream branch"
            else:
                status = "No remote set up"
            index += 1
            if not status:
                if self.emojis:
                    icon = "📤 "
                else:
                    icon = "OK"
                message = "Up to date"
            else:
                if self.emojis:
                    icon = "❌ "
                else:
                    icon = "ERR"
                message = "{}".format(status)
            status = "[{done:02d}/{all:02d}] {repo}:{branch} {icon} -> {message}".format(
                done=index,
                all=len(self.directories),
                icon=icon,
                repo=folder,
                branch=str(repo.active_branch),
                message=message
            )
            self.log.info("%s", status.strip())
        if errors > 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "Pushed %d of %d Repositories in the Folder",
            len(self.directories)-errors,
            len(self.directories)
        )

    def update(self):
        """
        Runs 'git pull' and 'git push' for all the found repositories

        @param self The parent class
        """
        self.log.info("Updating all Repositories")
        self.pull()
        self.push()

if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    PARSER = argparse.ArgumentParser(description='Git bulk processor')
    PARSER.add_argument(
        '--status',
        '-s',
        action='store_true',
        help='Get the Status of all Repositories (default)'
    )
    PARSER.add_argument(
        '--push',
        '-p',
        action='store_true',
        help='Push all Repositories'
    )
    PARSER.add_argument(
        '--pull',
        '-g',
        action='store_true',
        help='Pull all Repositories'
    )
    PARSER.add_argument(
        '--update',
        '-u',
        action='store_true',
        help='Update (Pull then Push) all Repositories'
    )
    PARSER.add_argument(
        'folder',
        nargs='?',
        default='./',
        metavar='folder',
        type=str,
        help='Folder in which all the repositories are in (default this folder \'./\')'
    )
    PARSED_DATA = PARSER.parse_args()

    UPDATER = UpdateGit(PARSED_DATA.folder)
    UPDATER.discover()
    if not PARSED_DATA.status and \
       not PARSED_DATA.pull and \
       not PARSED_DATA.push and \
       not PARSED_DATA.update:
        UPDATER.status()
    if PARSED_DATA.status:
        UPDATER.status()
    if PARSED_DATA.pull:
        UPDATER.pull()
    if PARSED_DATA.push:
        UPDATER.push()
    if PARSED_DATA.update:
        UPDATER.update()
