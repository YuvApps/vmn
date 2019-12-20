import pytest
import time
import sys
import os
import importlib.machinery
import types
import pathlib

sys.path.append('{0}/../version_stamp'.format(os.path.dirname(__file__)))
import ver_stamp


def test_wrong_parameters(mercurial_app_layout):
    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='/tmp/version.py',
            release_mode='debug',
            app_name='xxx',
            main_version_file='xxx',
            main_system_name=None,
        )

    except RuntimeError as exc:
        expected = 'Main system name was not specified but its ' \
                   'main_version file was specified "'
        assert exc.__str__() == expected

    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='something that is not None',
            release_mode='debug',
            app_name='xxx',
            main_version_file=None,
            main_system_name='Name',
        )

    except RuntimeError as exc:
        expected = 'Main system name was specified but main ' \
                   'version file path was not'
        assert exc.__str__() == expected

    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='/tmp/dir/version.py',
            release_mode='debug',
            app_name='xxx',
            main_system_name=None,
            main_version_file=None,
        )

    except RuntimeError as exc:
        expected = 'App version file must be within versions repository'
        assert exc.__str__() == expected

    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='{0}/versions/a/dir/wrong_name.py'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            release_mode='debug',
            app_name='xxx',
            main_system_name=None,
            main_version_file=None,
        )

    except RuntimeError as exc:
        expected = 'App version file must be named "version.py"'
        assert exc.__str__() == expected

    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='{0}/versions/a/dir/version.py'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            release_mode='debug',
            app_name='xxx',
            main_version_file='/tmp/a/dir/main_version.py'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            main_system_name='MainName',
        )
    except RuntimeError as exc:
        expected = 'Main app version file must be within versions repository'
        assert exc.__str__() == expected

    try:
        ver_stamp.run_with_mercurial_versions_be(
            repos_path='{0}/'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            app_version_file='{0}/versions/a/dir/version.py'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            release_mode='debug',
            app_name='xxx',
            main_version_file='{0}/versions/a/dir/wrong_name.py'.format(
                mercurial_app_layout.base_versions_dir_path
            ),
            main_system_name='MainName',
        )

    except RuntimeError as exc:
        expected = 'Main version file must be named "main_version.py"'
        assert exc.__str__() == expected


def test_get_current_changesets(mercurial_app_layout):
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    assert len(changesets) == 0

    current_changesets = {}
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

        current_changesets[repo[0]] = \
            mercurial_app_layout.get_changesets(repo_name=repo[0])

        current_changesets[repo[0]] = \
            mercurial_app_layout.get_changesets(repo_name=repo[0])

    changesets = ver_stamp.HostState.get_current_changeset(
            mercurial_app_layout.base_versions_dir_path
    )

    for k,v in changesets.items():
        assert k in current_changesets
        assert current_changesets[k]['hash'] == v['hash']
        assert current_changesets[k]['vcs_type'] == v['vcs_type']


def test_stamp_version(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    current_version = mbe.stamp_app_version(changesets)
    assert current_version == '0.0.1.0'


def test_stamp_main_version(mercurial_app_layout):
    strings = time.strftime("%y,%m")
    strings = strings.split(',')
    tmp_date_ver = '{0}.{1}'.format(strings[0], strings[1])

    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        app_name='test_app1',
        release_mode='patch',
        main_system_name='MainSystem'
    )

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    current_version = mbe.stamp_app_version(changesets)

    assert current_version == '0.0.1.0'

    formatted_main_ver = mbe.stamp_main_system_version(
        current_version
    )

    assert formatted_main_ver == '{0}.1'.format(tmp_date_ver)

    mbe.publish(current_version, formatted_main_ver)
    mbe.deallocate_backend()

    mercurial_app_layout.write_file(
        repo_name='repo1', file_relative_path='a/b/c.txt', content='hello3'
    )

    params = mercurial_app_layout.create_mercurial_backend_params(
        app_name='test_app2',
        release_mode='patch',
        main_system_name='MainSystem'
    )

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    current_version = mbe.stamp_app_version(changesets)

    assert current_version == '0.0.1.0'

    formatted_main_ver = mbe.stamp_main_system_version(
        current_version
    )

    assert formatted_main_ver == '{0}.2'.format(tmp_date_ver)

    mbe.publish(current_version, formatted_main_ver)
    mbe.deallocate_backend()

    params = mercurial_app_layout.create_mercurial_backend_params(
        app_name='test_app1',
        release_mode='patch',
        main_system_name='MainSystem'
    )

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    current_version = mbe.stamp_app_version(changesets)

    assert current_version == '0.0.2.0'

    formatted_main_ver = mbe.stamp_main_system_version(
        current_version
    )

    assert formatted_main_ver == '{0}.3'.format(tmp_date_ver)

    mbe.publish(current_version, formatted_main_ver)
    mbe.deallocate_backend()


def test_starting_version(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch', '1.9.5.0')

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    assert mbe._starting_version == '1.9.5.0'

    ver = mbe.find_version(changesets)
    assert ver is None

    current_version = mbe.stamp_app_version(changesets)

    assert current_version == '1.9.6.0'


def test_find_version(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')
    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    ver = mbe.find_version(changesets)
    assert ver is None

    current_version = mbe.stamp_app_version(changesets)
    assert current_version == '0.0.1.0'

    mbe.publish(current_version)
    mbe.deallocate_backend()

    release_modes = ('patch', 'minor', 'major', 'micro')
    for release_mode in release_modes:
        params = mercurial_app_layout.create_mercurial_backend_params(
            'test_app1', release_mode)
        mbe = ver_stamp.MercurialVersionsBackend(params)
        mbe.allocate_backend()
        changesets = ver_stamp.HostState.get_current_changeset(
            mercurial_app_layout.base_versions_dir_path
        )

        ver = mbe.find_version(changesets)
        assert ver == '0.0.1.0'

        mbe.deallocate_backend()

    # Add a change
    mercurial_app_layout.write_file(
        repo_name='repo1', file_relative_path='a/b/c.txt', content='xxx'
    )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')
    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    ver = mbe.find_version(changesets)
    assert ver is None

    current_version = mbe.stamp_app_version(changesets)
    assert current_version == '0.0.2.0'


def test_output(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt',
            content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt',
            content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')
    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    output = ver_stamp.get_version(mbe, changesets)
    assert output == '0.0.1'

    output = ver_stamp.get_version(mbe, changesets)
    assert output == '0.0.1'


def test_find_recurring_version(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    assert mbe._starting_version == '0.0.0.0'

    current_version = mbe.stamp_app_version(changesets)
    mbe.publish(current_version)
    mbe.deallocate_backend()

    mercurial_app_layout.remove_app_version_file(params['app_version_file'])

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    ver = mbe.find_version(changesets)
    assert ver is None
    assert mbe._starting_version == '0.0.1.0'

    current_version = mbe.stamp_app_version(changesets)
    assert current_version == '0.0.2.0'


def test_version_info(mercurial_app_layout):
    for repo in (('repo1', 'mercurial'), ('repo2', 'git')):
        mercurial_app_layout.create_repo(
            repo_name=repo[0], repo_type=repo[1]
        )

        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello'
        )
        mercurial_app_layout.write_file(
            repo_name=repo[0], file_relative_path='a/b/c.txt', content='hello2'
        )

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')
    dir_path = os.path.dirname(params['app_version_file'])
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    mercurial_app_layout.add_version_info_file(
        '{0}/version_info.py'.format(dir_path).encode(),
        custom_repos=('repo1',)
    )

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    changesets = ver_stamp.HostState.get_current_changeset(
        mercurial_app_layout.base_versions_dir_path
    )

    current_version = mbe.stamp_app_version(changesets)
    loader = importlib.machinery.SourceFileLoader(
        'version', params['app_version_file'])
    ver = types.ModuleType(loader.name)
    loader.exec_module(ver)

    repo_changeset = None
    for k,v in changesets.items():
        if k != 'repo1':
            continue

        repo_changeset = v['hash']
        break

    assert 'repo1' in ver.changesets
    assert len(ver.changesets.keys()) == 1
    assert ver.changesets['repo1']['hash'] == repo_changeset
    assert ver._version == current_version

    mbe.publish(current_version)
    mbe.deallocate_backend()


def test_version_template(mercurial_app_layout):
    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch')

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    ver = mbe.get_be_formatted_version('1.0.3.6')
    assert ver == '1.0.3'

    params = mercurial_app_layout.create_mercurial_backend_params(
        'test_app1', 'patch', version_template='ap{0}xx{0}XX{1}AC@{0}{2}{3}C')

    mbe = ver_stamp.MercurialVersionsBackend(params)
    mbe.allocate_backend()
    ver = mbe.get_be_formatted_version('1.0.3.6')
    assert ver == 'ap1xxXX0AC@36C'
