"""This script releases versions of cdf.
It :
- bumps the version,
- tags it
- push the bump commit to github
- push the tag to github
- upload the pip package to pypo
- create a github release

Concerning the version numbers, the script reads the previous release version
from cdf/__init__.py. It increments its micro version and modify
cdf/__init__.py consequently.


Limitations:
This script only increases the micro version,
if you want to increase the major or minor version, you will have to do it
by yourself.

Releases can not be launched by jenkins as
it does not have sufficient rights
"""

import argparse
import subprocess
import os.path
import fileinput
import re
import json
import requests
import getpass

#get the path to the local cdf directory
regex = ".*/botify-cdf"
LOCAL_PACKAGE_PATH = re.search(regex, os.path.abspath(__file__)).group(0)

#modify sys.path so that the local cdf is loaded
import sys
sys.path.insert(0, LOCAL_PACKAGE_PATH)

import cdf


class Level(object):
    micro = 'micro'
    minor = 'minor'
    major = 'major'


def get_last_release_version():
    """Returns the version number of the last release
    as a tuple (major, minor, micro).
    :returns: tuple
    """
    #get current VERSION
    release_version = cdf.__version__
    return [int(i) for i in release_version.split(".")]


def get_release_version(level=Level.micro):
    """Returns the version number of the next release version
    as a tuple (major, minor, micro).
    :param level: version level to be incremented
    :type level: str
    :returns: tuple
    """
    major, minor, micro = get_last_release_version()
    #increment micro version and reset micro version
    if level == Level.micro:
        result = [major, minor, micro + 1]
    elif level == Level.minor:
        result = [major, minor + 1, 0]
    elif level == Level.major:
        result = [major + 1, 0, 0]
    else:
        raise ValueError(
            "Unknown version level: {}, "
            "should be {}, {} or {}".format(
                level, Level.micro,
                Level.minor, Level.major
            )
        )
    result = [int(i) for i in result]
    result = tuple(result)
    return result


def get_init_filepath():
    """Return the path to cdf.__init__.py file
    :returns: str
    """
    filepath = os.path.join(os.path.dirname(cdf.__file__),
                            "__init__.py")
    return filepath


def set_version(version):
    """Change the version of the package.
    This function modifies __init__.py
    :param version: the new version to set as a tuple of integers
                    (major, minor, micro)
    :param version: tuple
    """
    #find file location
    filename = get_init_filepath()
    regex = re.compile("version\s*=\s*\(\d+, \d+, \d+\)")
    version_line_found = False
    #inplace replacement
    #cf http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
    for line in fileinput.input(filename, inplace=True):
        if regex.match(line):
            sys.stdout.write("version = {}\n".format(str(version)))
            version_line_found = True
        else:
            sys.stdout.write(line)
    if not version_line_found:
        raise ValueError("Error line defining version not found in {}".format(filename))


def get_changelog(tag):
    """Generate a changelog from a given tag to HEAD
    :param tag: the reference tag
    :type tag: str
    :returns: str
    """
    #each commit is formatted this way
    #-  Merge pull request #392 from sem-io/feature/foo [John Doe]
    #
    #  Very useful commit message because:
    #  - it lists what the commit does
    #
    #cf man git log for further explanations on the syntax
    #the trickiest part is the %w(...)
    #that configures the commit message indentation
    width = 80
    indent = 4
    log_format = "- %s [%cn]%n%n%w({},{},{})%b".format(width, indent, indent)
    command = ["git", "log", "{}..HEAD".format(tag),
               "--first-parent", '--pretty=format:{}'.format(log_format)]
    changelog = subprocess.check_output(command)
    return changelog


def authenticate(url, auth_msg=None, retry=True):
    """Interactive authenticate for a webservice

    :param url: url of the webservice endpoint
    :param auth_msg: message to show the user
    :param retry: if retry is needed
    :return: (success, auth)
    :rtype: (bool, `requests.auth.HTTPBasicAuth`)
    """
    def _auth():
        if auth_msg:
            print auth_msg
        username = raw_input("username: ")
        password = getpass.getpass()
        auth = requests.auth.HTTPBasicAuth(username, password)
        ok = requests.get(url, auth=auth).ok
        return ok, auth

    ok, auth = _auth()

    while retry and not ok:
        ok, auth = _auth()

    return ok, auth


def create_github_release(tag, changelog, dry_run):
    """Create a github release
    :param tag: the tag corresponding to the release
    :type tag: str
    :param changelog: the release changelog
    :type changelog: str
    :param dry_run: if True, nothing is actually done.
                    the function just prints what it would do
    :type dry_run: bool
    """

    release_parameters = {
        "tag_name": tag,
        "name": tag,
        "body": changelog,
        "draft": False,
        "prerelease": False
    }
    auth_msg = "\n{} Github authentication {}".format("*" * 20, "*" * 20)
    url = "https://api.github.com/repos/sem-io/botify-cdf/releases"

    if not dry_run:
        _, auth = authenticate(url, auth_msg, retry=True)
        response = requests.post(url, json.dumps(release_parameters), auth=auth)
        if not response.ok:
            print "Could not create github version [{}]: {}".format(response.status_code,
                                                                    response.text)
    else:
        username = "user"
        password = "password"
        print "POST {} ({}, {})".format(url, username, password)


def upload_package(dry_run):
    """Create the python package
    and upload it to pypi
    :param dry_run: if True, nothing is actually done.
                    the function just prints what it would do
    :type dry_run: bool"""
    command = ["python", "setup.py", "sdist", "upload", "-r", "botify"]
    if not dry_run:
        print subprocess.check_output(command)
    else:
        print " ".join(command)


def release_official_version(dry_run, level=Level.micro):
    """Release an official version of cdf
    :param dry_run: if True, nothing is actually done.
                    the function just prints what it would do
    :type dry_run: bool
    :param level: release level to increment, see `get_release_version`
    :type level: str
    """
    #bump version
    version = get_release_version(level)
    tag = ".".join([str(i) for i in version])
    print "Creating cdf {}".format(tag)

    last_tag = ".".join([str(i) for i in get_last_release_version()])
    changelog = get_changelog(last_tag)
    #in case of dry run, we do not want to modify the files
    if not dry_run:
        set_version(version)
    init_filepath = get_init_filepath()
    commit_message = "bump version to {}".format(tag)
    tag_message = ("{}\n\n"
                   "Changelog:\n"
                   "{}").format(tag, changelog)

    commands = [
        #commit version bump
        ["git", "add", init_filepath],
        ["git", "commit", "-m", commit_message],
        #tag current commit
        ["git", "tag", "-a", tag, "-m", tag_message],
        #push commits
        ["git", "push", "origin", "devel"],
        #upload package
        ["git", "push", "origin", tag]
    ]
    if not dry_run:
        for command in commands:
            subprocess.check_output(command)
    else:
        for command in commands:
            print " ".join(command)

    #upload package
    upload_package(dry_run)

    create_github_release(tag, changelog, dry_run)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Release version of cdf.'
    )

    parser.add_argument('-f',
                        dest="force",
                        default=False,
                        action="store_true",
                        help='Force release')

    parser.add_argument('-n',
                        dest="dry_run",
                        default=False,
                        action="store_true",
                        help='Dry run')

    parser.add_argument('-l',
                        dest="level",
                        default=Level.micro,
                        action="store",
                        help='Version level: {}, {} or {}. '
                             'Defaults to micro level.'.format(
                             Level.major, Level.minor, Level.micro))

    args = parser.parse_args()

    if not args.force and not args.dry_run:
        raise ValueError("You must choose option '-f' or '-n'")

    if args.force and args.dry_run:
        raise ValueError("You cannot choose both options '-f' and '-n'")

    release_official_version(args.dry_run, args.level)