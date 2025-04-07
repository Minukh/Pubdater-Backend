import requests
import re
from packaging.version import Version
from .exceptions import ContentLengthException


class Pubdater:

    def __init__(self, package: str, dart_version: str):
        self.pubspec_updated = ""
        self.message = ""
        deps = self.extract_deps(package)
        if len(lines) > 100:
            raise ContentLengthException(
                "The pubspec.yaml contents are too long to process."
            )
        elif len(lines) == 1 and len(lines[0]) == 0:
            raise ContentLengthException("Contents are empty.")
        elif len(deps[0]) == 0:
            self.pubspec_updated = str
            raise ContentLengthException("Didn't find any dependencies to upgrade.")

        lineCount = 0

        for i in range(len(lines)):
            if str(lines[i]).find(deps[1][lineCount]) != -1:
                try:
                    latest_version = self.fetch_latest_compatible_version(
                        deps[0][lineCount], dart_version
                    )
                except:
                    latest_version = 0
                if latest_version != None:
                    lines[i] = str(lines[i]).replace(
                        deps[1][lineCount],
                        (
                            deps[1][lineCount]
                            if latest_version is None
                            else self.check_latest(deps[1][lineCount], latest_version)
                        ),
                    )
                lineCount += 1

        self.count = lineCount
        self.pubspec_updated = "\n".join(lines)
        if len(deps[1]) != lineCount:
            self.message = "Couldn't resolve versions for one or more packages."
        else:
            self.message = "Upgradable packages have been updated to their latest compatible version."

    def fetch_latest_compatible_version(self, package_name: str, dart_version: str):
        url = f"https://pub.dev/packages/{package_name}/versions"
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to fetch package versions.")
            self.message = "Failed to fetch package versions."
            return None

        html_content = response.text

        version_pattern = re.compile(
            r'data-version="([^"]+)".*?<td class="sdk">([\d\.]+)', re.DOTALL
        )
        matches = version_pattern.findall(html_content)

        compatible_versions = []
        target_dart_version = Version(dart_version)

        for package_version, sdk_version in matches:
            try:
                parsed_sdk_version = Version(sdk_version)
                if parsed_sdk_version <= target_dart_version:
                    compatible_versions.append(
                        (Version(package_version), package_version)
                    )
            except:
                continue

        if not compatible_versions:
            print("No compatible versions found.")
            return None

        return max(compatible_versions, key=lambda x: x[0])[1]

    def is_dependency_line(self, line):
        pattern = r"^\s*([\w\-_]+):\s*\^?\d+\.\d+\.\d+\s*$"
        return bool(re.match(pattern, line))

    def extract_deps(self, pubspec: str):
        dep = []
        ver = []
        count = 0
        global lines
        lines = pubspec.split("\n")
        for i in map(str.strip, lines):
            if self.is_dependency_line(i):
                dep.append(i.split(":")[0].strip(" "))
                ver.append(i.split(":")[1].strip(" "))
                count += 1
        return [dep, ver, count]

    def check_latest(self, version: str, target: str):
        if version.find(str(target)) == -1:
            return (
                ("^" if version.find("^") != -1 else "")
                + max([version.strip("^"), target])
                + f" #updated from {version}"
            )
        return version
