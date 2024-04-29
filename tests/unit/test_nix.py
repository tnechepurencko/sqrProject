from starlette import status
from pathlib import Path
import pytest

from app import nix
from app.db import Stores

stores_db = Stores()


def test_create_store():
    code, content = nix.create_store('user001', 'store001', stores_db)
    if code == status.HTTP_200_OK:
        assert content == Path('../nix_stores/user001/store001')


def test_remove_store():
    code, content = nix.remove_store('user001', 'store001', stores_db)
    if code == status.HTTP_200_OK:
        assert content == Path('../nix_stores/user001/store001')


def test_add_package():
    package_name = 'bash'
    code, content = nix.add_package('user001', 'store001', package_name)
    if code == status.HTTP_200_OK:
        assert package_name in content


def test_remove_package():
    package_name = 'bash'
    code, content = nix.rem_package('user001', 'store001', package_name)
    if code == status.HTTP_200_OK:
        assert content == package_name


def test_dif_paths():
    nix.create_store('user001', 'store002', stores_db)
    code, content = nix.dif_paths('user001', 'store001', 'store002')

    store_path1 = Path(f'../nix_stores/user001/store001/nix/store')
    set1 = set([f'/nix/store/{path}' for path in store_path1.iterdir()])

    if code == status.HTTP_200_OK:
        assert content == list(set1)


def test_dif_package():
    nix.add_package('user001', 'store001', 'bash')
    nix.add_package('user001', 'store002', 'hello')
    code, content = nix.dif_package('user001', 'store001', 'bash', 'store002', 'hello')

    if code == status.HTTP_200_OK:
        assert set(content) == {'bash-5.2p26-man', 'bash-5.2p26'}


def test_size_package():
    code, content = nix.size_package('user001', 'store002', 'hello')

    if code == status.HTTP_200_OK:
        assert content == 69344456


def test_package_exists():
    code, content = nix.package_exists('user001', 'store002', 'hello')

    if code == status.HTTP_200_OK:
        assert content is True

    code, content = nix.package_exists('user001', 'store002', 'glibc')

    if code == status.HTTP_200_OK:
        assert content is False
