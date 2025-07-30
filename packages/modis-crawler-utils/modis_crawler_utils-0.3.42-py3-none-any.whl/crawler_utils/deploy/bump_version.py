import semver
import sys
import json


def main():
    gitlab_packages = json.load(sys.stdin)
    version = gitlab_packages[0]["version"]
    commit_msg = sys.argv[1]

    if "#major" in commit_msg:
        version = semver.bump_major(version)
    elif "#minor" in commit_msg:
        version = semver.bump_minor(version)
    else:
        version = semver.bump_patch(version)

    print(version)


if __name__ == '__main__':
    main()
