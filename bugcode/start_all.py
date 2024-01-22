import os
import sys

import sh


def start_systemctl_all():
    # TODO: Check if units are installed
    if os.name == 'posix':
        if sys.platform != 'darwin':
            from sh import systemctl  # pylint: disable=import-outside-toplevel
            try:
                systemctl.start('bugcode-server')
                try:
                    systemctl.start('bugcode-worker')
                except sh.ErrorReturnCode as e:
                    systemctl.stop('bugcode-server')
                    print(f"Could not start bugcode worker. {str(e.stderr)}")
            except sh.ErrorReturnCode as e:
                print(f"Could not start bugcode-server. {str(e.stderr)}")
        else:
            print("Sorry, this script will not work with macos.")
    else:
        print("Sorry, this script will not work with non posix os.")


def main():
    start_systemctl_all()
