import json
import os
from datetime import datetime, timedelta

import click
import requests
from packaging.version import Version

from ..__init__ import __version__

objection_path = os.path.join(os.path.expanduser('~'), '.objection')
version_file = os.path.join(objection_path, 'version_info')

version_data = {
    'remote_version': '0.0.0',
    'last_check': datetime.now() - timedelta(days=7)
}

date_fmt = '%d%m%y %H:%M:%S'


def cached_version_data() -> version_data:
    """
        Reads the local version file and returns the
        version data structure

        :return:version_data
    """

    if not os.path.exists(version_file):
        return version_data

    with open(version_file, 'r') as f:
        data = json.load(f)

    data['last_check'] = datetime.strptime(data['last_check'], date_fmt)

    return data


def update_version_cache(version: str) -> None:
    """
        Store version information.

        :param version:
        :return:
    """

    version_data['remote_version'] = version
    version_data['last_check'] = datetime.now().strftime(date_fmt)

    with open(version_file, 'w') as f:
        json.dump(version_data, f)


def notify_newer_version() -> None:
    """
        Print a notification message about the newer version
        that is available.

        :return:
    """

    cache_version = cached_version_data()['remote_version']

    if Version(cache_version) > Version(__version__):
        click.secho('\n\nA newer version of objection is available!', fg='green')
        click.secho('You have v{0} and v{1} is ready for download.\n'.format(
            __version__, cache_version), fg='green')
        click.secho('Upgrade with: pip3 install objection --upgrade', fg='green', bold=True)
        click.secho('For more information, please see: '
                    'https://github.com/sensepost/objection/wiki/Updating\n', dim=True)


def check_version() -> None:
    pass
