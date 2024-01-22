import os
import pytest
import subprocess

from configparser import SafeConfigParser, DuplicateSectionError
from pathlib import Path


@pytest.mark.skip(reason="Temporal para que pase nix")
def test_manage_migrate():
    """
        Run manage migrate with nothing to migrate
        The idea is to catch a broken migration
    """
    if 'POSTGRES_DB' in os.environ:
        # I'm on gitlab ci runner
        # I will overwrite server.ini
        connection_string = 'postgresql+psycopg2://{username}:{password}@postgres/{database}'.format(
            username=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            database=os.environ['POSTGRES_DB'],
        )
        bugcode_config = SafeConfigParser()
        config_path = Path('~/.bugcode/config/server.ini').expanduser()
        bugcode_config.read(config_path)
        try:
            bugcode_config.add_section('database')
        except DuplicateSectionError:
            pass
        bugcode_config.set('database', 'connection_string', connection_string)
        with config_path.open('w') as bugcode_config_file:
            bugcode_config.write(bugcode_config_file)

        command = ['bugcode-manage', 'create-tables']
        subproc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        std, err = subproc.communicate()
        assert subproc.returncode == 0, ('Create tables failed!', std, err)

        command = ['bugcode-manage', 'migrate']
        subproc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subproc.wait()
        std, err = subproc.communicate()
        print(std)
        print(err)
        assert subproc.returncode == 0, ('manage migrate failed!', std, err)
