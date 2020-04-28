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


        @param self         The parent class
        @param directory    The directory in which to search for git repositories
        @param emojis       If you want to enable emojis in the console output or not
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
            if "nothing to commit, working tree clean" in status:
                icon = self.icon("success")
                message = "Everything up to date"
            else:
                if status:
                    errors += 1
                icon = self.icon("error")
                message = "\n{}".format(status)
            self.log_status(
                done=index,
                icon=icon,
                repo=repo,
                message=message
            )
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
            if self.has_remote_tracking(repo):
                try:
                    status = repo.git.pull()
                except git.exc.GitCommandError as error:
                    status = "Error while Pulling Repo:\n{}".format(error)
            else:
                status = "No tracking possible, maybe no remote or no remote branch"
            index += 1
            if not status:
                errors += 1
                status = "Got no status"
            # Match icons to status messages
            if "Already up to date." in status:
                icon = self.icon("success")
                message = "Already up to date"
            elif (
                    ("No tracking possible, maybe no remote or no remote branch" in status) or
                    ("Error while Pulling Repo:" in status) or
                    ("Got no status" in status)
                ):
                icon = self.icon("error")
                message = "{}".format(status)
            else:
                icon = self.icon("download")
                message = "Pulling Repo"
            self.log_status(
                done=index,
                icon=icon,
                repo=repo,
                message=message
            )
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
            if self.has_remote_tracking(repo):
                try:
                    status = repo.git.push()
                except git.exc.GitCommandError as error:
                    status = "Error while Pulling Repo:\n{}".format(error)
            else:
                status = "No tracking possible, maybe no remote or no remote branch"
            index += 1
            if not status:
                icon = self.icon("upload")
                message = "Up to date"
            else:
                icon = self.icon("error")
                message = "{}".format(status)
            self.log_status(
                done=index,
                icon=icon,
                repo=repo,
                message=message
            )
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

    def has_remote_tracking(self, repo):
        """
        Creates tracking information for active branch
        if branch with the same name exists on the remote

        @param self The parent class
        @param repo The repo object to perform the action on
        @return If tracking information is available
        """
        active_branch = str(repo.active_branch)
        active_head = repo.heads[active_branch]
        if repo.remotes:
            # Has a registered Remote
            if active_head.tracking_branch():
                # Already has remote tracking
                return True
            else:
                # Try to set up remote tracking
                # Select First remote (defaults to origin)
                origin = repo.remote(repo.remotes[0])
                if active_branch in origin.refs:
                    # If branch with the same name exists on the remote, set up tracking
                    self.log.info("Setting up remote tracking branch")
                    active_head.set_tracking_branch(origin.refs[active_branch])
                    return True
                # If no branch with the same name exists on the remote, no tracking
                return False
        else:
            # Does not have a remote, thus no tracking information
            return False

    def log_status(self, done, repo, icon, message):
        """
        Print status messages with progress, repo, branch, icon and message

        @param self The parent class
        @param done (int) Current index in the list
        @param repo (str) Current Repo Object
        @param icon (str) Icon to display (Emoji/Text)
        @param message (str) message to display for more information
        """
        repo_name = repo.working_dir.split("/")[-1]
        branch = repo.active_branch
        status = "[{done:02d}/{total:02d}] {repo}:{branch} {icon} -> {message}".format(
            done=int(done),
            total=int(len(self.directories)),
            icon=str(icon),
            repo=str(repo_name),
            branch=str(branch),
            message=str(message)
        )
        self.log.info("%s", status.strip())

    def icon(self, name):
        """
        Matches either Icon or Text to icon name

        @param self The parent class
        @param name The name of the Icon
        @return (str) Icon
        """
        emoji = {
            "success": "✔️ ",
            "error": "❌ ",
            "upload": "📤 ",
            "download": "📥 ",
        }
        text_sub = {
            "success": "OK",
            "error": "ERR",
            "upload": "UP",
            "download": "DWN"
        }
        if self.emojis:
            return emoji[name]
        return text_sub[name]

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
