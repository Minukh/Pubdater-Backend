import requests
import re
from packaging.version import Version
from rich.progress import Progress, BarColumn, TextColumn

# Not used in project, only for testing

class pubdater:
    def fetch_latest_compatible_version(self, package_name: str, dart_version: str):
        url = f"https://pub.dev/packages/{package_name}/versions"
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to fetch package versions.")
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

        latest_version = max(compatible_versions, key=lambda x: x[0])

        return latest_version[1]

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
        if version.find(target) == -1:
            return (
                ("^" if version.find("^") != -1 else "")
                + max([version.strip("^"), target])
                + f" #updated from {version}"
            )
        return version


if __name__ == "__main__":
    package_name = """
dependencies:
flutter:
    sdk: flutter
    
mask_text_input_formatter: ^2.4.0
dotted_border: ^2.0.0+2
auto_route: ^5.0.2
cached_network_image: ^3.2.2
currency_text_input_formatter: ^2.1.8
theme_tailor_annotation: ^1.2.0
just_the_tooltip: ^0.0.12
flutter_svg: ^1.1.6
flutter_gen_runner: 5.1.0+1
google_fonts: ^4.0.4


dev_dependencies:
flutter_test:
    sdk: flutter
flutter_lints: ^2.0.1
auto_exporter: ^1.4.2
build_runner: ^2.2.0
build_test: ^2.1.5
theme_tailor: ^1.0.8
"""
    pub = pubdater()
    dart_version = input("Enter Dart version (e.g., 3.2.6): ")
    deps = pub.extract_deps(package_name)
    lineCount = 0
    with Progress(
        TextColumn("[white]{task.description}"),
        TextColumn("[white]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[green]{task.completed}/{task.total}"),
        BarColumn(pulse_style="black", style="black"),
    ) as progress:
        task = progress.add_task("[white]Processing...", total=len(deps[1]))
        for i in range(len(lines) - 1):
            if str(lines[i]).find(deps[1][lineCount]) != -1:
                latest_version = pub.fetch_latest_compatible_version(
                    deps[0][lineCount], dart_version
                )
                if latest_version:
                    lines[i] = str(lines[i]).replace(
                        deps[1][lineCount],
                        (
                            deps[1][lineCount]
                            if latest_version is None
                            else pub.check_latest(deps[1][lineCount], latest_version)
                        ),
                    )
                    lineCount += 1
                progress.update(task, advance=1)

print("\n".join(lines))
if deps[2] != lineCount:
    print("Couldn't resolve versions for one or more packages.")
