import subprocess
import sys

import mantarix.version
from mantarix.utils.pip import ensure_mantarix_cli_package_installed


def main():
    ensure_mantarix_cli_package_installed()
    import mantarix_cli.cli

    mantarix_cli.cli.main()


if __name__ == "__main__":
    main()
