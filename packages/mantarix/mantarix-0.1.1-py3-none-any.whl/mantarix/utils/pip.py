import subprocess
import sys

import mantarix.version


def install_mantarix_package(name: str):
    print(f"Installing {name} {mantarix.version.version} package...", end="")
    retcode = subprocess.call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "--disable-pip-version-check",
            f"{name}=={mantarix.version.version}",
        ]
    )
    if retcode == 0:
        print("OK")
    else:
        print(
            f'Unable to upgrade "{name}" package to version {mantarix.version.version}. Please use "pip install \'mantarix[all]=={mantarix.version.version}\' --upgrade" command to upgrade Mantarix.'
        )
        exit(1)


def ensure_mantarix_desktop_package_installed():
    try:
        import mantarix.version
        import mantarix_desktop.version

        assert (
            not mantarix_desktop.version.version
            or mantarix_desktop.version.version == mantarix.version.version
        )
    except:
        install_mantarix_package("mantarix-desktop")


def ensure_mantarix_web_package_installed():
    try:
        import mantarix.version
        import mantarix_web.version

        assert (
            not mantarix_web.version.version
            or mantarix_web.version.version == mantarix.version.version
        )
    except:
        install_mantarix_package("mantarix-web")


def ensure_mantarix_cli_package_installed():
    try:
        import mantarix.version
        import mantarix_cli.version

        assert (
            not mantarix_cli.version.version
            or mantarix_cli.version.version == mantarix.version.version
        )
    except:
        install_mantarix_package("mantarix-cli")
