from starlette import status
from pathlib import Path
from shutil import rmtree
import subprocess
import json

nix_stores_path = '../nix_stores'


def run_command(command):
    proc = subprocess.run(
        command,
        capture_output=True,
        text=True)
    return proc.stdout, proc.returncode


def create_store(uname, sname, stores_db):
    try:
        store_path_str = f'{nix_stores_path}/{uname}/{sname}'
        store_path = Path(store_path_str)
        store_path.mkdir(parents=True)
        stores_db.insert(uname, sname, store_path_str)
    except FileExistsError:
        return status.HTTP_400_BAD_REQUEST, 'Store already exists'
    return status.HTTP_200_OK, store_path


def remove_store(uname, sname, stores_db):
    try:
        store_path = Path(f'{nix_stores_path}/{uname}/{sname}')
        rmtree(store_path)
        stores_db.remove(uname, sname)
    except Exception as e:
        return status.HTTP_400_BAD_REQUEST, e
    return status.HTTP_200_OK, store_path


def add_package(uname, sname, pname):
    stdout, returncode = run_command(
        [
            'nix',
            'build',
            '--json',
            '--no-link',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode
    output = json.loads(stdout)
    package_path = output[0]["outputs"]["out"]
    return status.HTTP_200_OK, package_path


def rem_package(uname, sname, pname):
    # Delete package
    stdout, returncode = run_command(
        [
            'nix',
            'store',
            'delete',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode

    # Collect garbage
    stdout, returncode = run_command(
        [
            'nix',
            'store',
            'gc',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode

    return status.HTTP_200_OK, pname


def dif_paths(uname, sname1, sname2):
    store_path1 = Path(f'{nix_stores_path}/{uname}/{sname1}/nix/store')
    store_path2 = Path(f'{nix_stores_path}/{uname}/{sname2}/nix/store')

    if not any(store_path1.iterdir()):
        set1 = set()
    else:
        set1 = set([f'/nix/store/{path}' for path in store_path1.iterdir()])
    if not any(store_path2.iterdir()):
        set2 = set()
    else:
        set2 = set([f'/nix/store/{path}' for path in store_path2.iterdir()])

    return status.HTTP_200_OK, list(set1 - set2)


def dif_package(uname, sname1, pname1, sname2, pname2):
    # Get first closure paths
    stdout, returncode = run_command(
        [
            'nix',
            'path-info',
            '--recursive',
            '--store',
            f'{nix_stores_path}/{uname}/{sname1}',
            f'nixpkgs#{pname1}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode
    set1 = set(stdout.split())
    package_set1 = set()
    for s in set1:
        package_set1.add(s.split('-', 1)[1])

    # Get second closure paths
    stdout, returncode = run_command(
        [
            'nix',
            'path-info',
            '--recursive',
            '--store',
            f'{nix_stores_path}/{uname}/{sname2}',
            f'nixpkgs#{pname2}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode
    set2 = set(stdout.split())
    package_set2 = set()
    for s in set2:
        package_set2.add(s.split('-', 1)[1])

    # Get difference
    return status.HTTP_200_OK, list(package_set1 - package_set2)


def size_package(uname, sname, pname):
    stdout, returncode = run_command(
        [
            'nix',
            'path-info',
            '--json',
            '--recursive',
            '--closure-size',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ])
    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode

    output = json.loads(stdout)
    closure_size = sum(path["closureSize"] for path in output)
    return status.HTTP_200_OK, closure_size


def package_exists(uname, sname, pname):
    stdout, returncode = run_command(
        [
            'nix',
            'path-info',
            '--json',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ])

    if returncode != 0:
        return status.HTTP_400_BAD_REQUEST, returncode

    output = json.loads(stdout)
    valid = output[0]["valid"]
    return status.HTTP_200_OK, valid
