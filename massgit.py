#!/usr/bin/python3
"""
Python Module to Update all git repositories in a specific Folder (e.g. ./)
"""
from subprocess import call
import argparse
import os
import logging

class UpdateGit(object):
    """
    Class to update all git repositories in a specific Folder.
    """
    def __init__(self, directory="./"):
        """
        Initializes the base_dir (defaults to \'./\' ) and sets up logging
        """
        # Get the Specified Folder and resolve ~ Paths
        self.base_dir = os.path.abspath(os.path.expanduser(directory))
        self.directories = []
        self.log = logging.getLogger(__name__)

    def discover(self):
        """
        Discovers the Repositories in the specified Folder (searches for .git folders)
        """
        if not self.base_dir:
            self.log.error('No Path specified at startup')
            exit()
        self.log.info("Discovering Git Repositories")
        all_available = os.listdir(self.base_dir)
        self.bad_folders = []
        for folder in all_available:
            if os.path.isdir(os.path.join(self.base_dir, folder)):
                if os.path.isdir(os.path.join(self.base_dir, folder, ".git")):
                    self.directories.append(folder)
                else:
                    self.bad_folders.append(folder)
        if self.bad_folders:
            self.log.warning("Found Folders that are not git Repos: %s", str(self.bad_folders))
        if len(self.directories) < 1:
            self.log.warning("Found 0 Repositories in %s", self.base_dir)
            exit()
        self.log.info("Done. Found %d Repositories", len(self.directories))

    def status(self):
        """
        Runs 'git status' for all the found repositories
        """
        errors = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Checking Status")
        for i in range(len(self.directories)):
            folder = self.directories[i]
            self.log.info(
                "[%d/%d] Checking dir: %s",
                (i+1),
                len(self.directories),
                os.path.join(self.base_dir, folder)
            )
            status = call(["git", "status"], cwd=os.path.join(self.base_dir, folder))
            if status != 0:
                self.log.error("Error while checking status. Please check console output")
                errors += 1
        if errors != 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "Checked [%d/%d] Repositories",
            len(self.directories)-errors,
            len(self.directories)
        )

    def pull(self):
        """
        Runs 'git pull' for all the found repositories
        """
        errors = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Pulling Repositories")
        for i in range(len(self.directories)):
            folder = self.directories[i]
            self.log.info(
                "[%d/%d] Pulling dir: %s",
                (i+1),
                len(self.directories),
                os.path.join(self.base_dir, folder)
            )
            status = call(["git", "pull"], cwd=os.path.join(self.base_dir, folder))
            if status != 0:
                self.log.error("Error while pulling. Please check console output")
                errors += 1
        if errors != 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "Pulled [%d/%d] Repositories in the Folder",
            len(self.directories)-errors,
            len(self.directories)
        )

    def push(self):
        """
        Runs 'git push' for all the found repositories
        """
        errors = 0
        if not self.directories:
            self.log.error("Please Discover the Repositories first using the discover function")
            return
        self.log.info("Pushing Repositories")
        for i in range(len(self.directories)):
            folder = self.directories[i]
            self.log.info(
                "[%d/%d] Pushing dir: %s",
                (i+1),
                len(self.directories),
                os.path.join(self.base_dir, folder)
            )
            status = call(["git", "push"], cwd=os.path.join(self.base_dir, folder))
            if status != 0:
                self.log.error("Error while pushing. Please check console output")
                errors += 1
        if errors != 0:
            self.log.warning("Encountered %d errors while performing task", errors)
        self.log.info(
            "Pushed [%d/%d] Repositories in the Folder",
            len(self.directories)-errors,
            len(self.directories)
        )

    def update(self):
        """
        Runs 'git pull' and 'git push' for all the found repositories
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
