import pytest
import os
import subprocess
import textwrap

from tests.expected_files import jwt_files
from tests.utils import build_files_list, WIN, WORKING

@pytest.mark.parametrize('template', ['jinja2', 'mako', 'chameleon'])
def test_jwt(cookies, venv, capfd, template):
    result = cookies.bake(extra_context={
        'project_name': 'Test Project',
        'template_language': template,
        'backend': 'none',
        'pyramid_services': 'pyramid-services',
        'authentication': 'jwt',
        'repo_name': 'myapp',
    })

    assert result.exit_code == 0

    out, err = capfd.readouterr()

    if WIN:
        assert 'Scripts\\pserve' in out
        for idx, base_file in enumerate(jwt_files):
            jwt_files[idx] = base_file.replace('/', '\\')
        jwt_files.sort()

    else:
        assert 'bin/pserve' in out

    # Get the file list generated by cookiecutter. Differs based on backend.
    files = build_files_list(str(result.project_path))
    files.sort()

    # Rename files based on template being used
    if template == 'chameleon':
        template = 'pt'

    for idx, base_file in enumerate(jwt_files):
        if 'templates' in base_file:
            jwt_files[idx] = jwt_files[idx].split('.')[0] + '.' + template

    assert jwt_files == files

    cwd = str(result.project_path)

    # this is a hook for executing scaffold tests against a specific
    # version of pyramid (or a local checkout on disk)
    if 'OVERRIDE_PYRAMID' in os.environ:  # pragma: no cover
        venv.install(os.environ['OVERRIDE_PYRAMID'], editable=True)

    # venv.install(cwd, editable=True, upgrade=True)
    subprocess.call([venv.bin + '/pip', 'install', 'poetry'], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'install', ], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'config', 'virtualenvs.create', 'false', '--local'], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'install'], cwd=cwd)
    subprocess.call([venv.bin + '/poetry', 'run', 'pytest'], cwd=cwd)
