from fastapi import FastAPI
from starlette import status
from starlette.responses import Response
from pathlib import Path
from shutil import rmtree
import subprocess
import json

from db import Users

app = FastAPI()
users_db = Users()

nix_stores_path = './nix_stores'


def one_param_check(p1):
    return '%s' % p1


def two_param_check(p1, p2):
    return '%s %s' % (p1, p2)


def get_response(code, content):
    return Response(status_code=code, content=content, media_type='text/plain')


@app.get('/login')
def login(uname, pwd):
    if users_db.contains_by_uname_pwd(uname, pwd):
        return get_response(status.HTTP_200_OK, two_param_check(uname, pwd))
    return get_response(status.HTTP_401_UNAUTHORIZED, 'No such user')


@app.get('/logout')
def logout(uname):
    if users_db.contains_by_uname(uname):
        return get_response(status.HTTP_200_OK, one_param_check(uname))
    return get_response(status.HTTP_401_UNAUTHORIZED, 'No such user')


@app.post('/registration')
def registration(uname, pwd):
    if users_db.contains_by_uname(uname):
        return get_response(status.HTTP_409_CONFLICT, 'Username already exists')
    users_db.insert(uname, pwd)
    return get_response(status.HTTP_200_OK, two_param_check(uname, pwd))


@app.post('/create_store')
def create_store(uname, sname):
    try:
        store_path = Path(f'{nix_stores_path}/{uname}/{sname}')
        store_path.mkdir(parents=True)
        # TODO : Add store to database
    except FileExistsError:
        return get_response(status.HTTP_400_BAD_REQUEST, 'Store already exists')
    return get_response(status.HTTP_200_OK, one_param_check(store_path))


@app.post('/get_stores')
def get_stores(uname):
    # TODO: get all stores for thus uname from database
    pass


@app.post('/remove_store')
def remove_store(uname, sname):
    try:
        store_path = Path(f'{nix_stores_path}/{uname}/{sname}')
        rmtree(store_path)
        # TODO : Remove store from database
    except Exception as e:
        return get_response(status.HTTP_400_BAD_REQUEST, e)
    return get_response(status.HTTP_200_OK, one_param_check(store_path))


@app.post('/add_package')
def add_package(uname, sname, pname):
    proc = subprocess.run(
        [
            'nix',
            'build',
            '--json',
            '--no-link',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)
    output = json.loads(proc.stdout)
    package_path = output[0]["outputs"]["out"]
    return get_response(status.HTTP_200_OK, one_param_check(package_path))


@app.post('/rem_package')
def rem_package(uname, sname, pname):
    # Delete package
    proc = subprocess.run(
        [
            'nix',
            'store',
            'delete',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)

    # Collect garbage
    proc = subprocess.run(
        [
            'nix',
            'store',
            'gc',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)

    return get_response(status.HTTP_200_OK, pname)


@app.get('/dif_paths')
def dif_paths(uname, sname1, sname2):
    store_path1 = Path(f'{nix_stores_path}/{uname}/{sname1}/nix/store')
    store_path2 = Path(f'{nix_stores_path}/{uname}/{sname2}/nix/store')

    set1 = set([f'/nix/store/{path}' for path in store_path1.iterdir()])
    set2 = set([f'/nix/store/{path}' for path in store_path2.iterdir()])

    return get_response(status.HTTP_200_OK, list(set1 - set2))


@app.get('/dif_package')
def dif_package(uname, sname1, pname1, sname2, pname2):
    # Get first closure paths
    proc = subprocess.run(
        [
            'nix',
            'path-info',
            '--recursive',
            '--store',
            f'{nix_stores_path}/{uname}/{sname1}',
            f'nixpkgs#{pname1}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)
    set1 = set(proc.stdout.split())

    # Get second closure paths
    proc = subprocess.run(
        [
            'nix',
            'path-info',
            '--recursive',
            '--store',
            f'{nix_stores_path}/{uname}/{sname2}',
            f'nixpkgs#{pname2}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)
    set2 = set(proc.stdout.split())

    # Get difference
    return get_response(status.HTTP_200_OK, list(set1 - set2))


@app.get('/size_package')
def size_package(uname, sname, pname):
    proc = subprocess.run(
        [
            'nix',
            'path-info',
            '--json',
            '--recursive',
            '--closure-size',
            '--store',
            f'{nix_stores_path}/{uname}/{sname}',
            f'nixpkgs#{pname}',
        ],
        capture_output=True,
        text=True)
    if proc.returncode != 0:
        return get_response(status.HTTP_400_BAD_REQUEST, proc.returncode)

    output = json.loads(proc.stdout)
    closure_size = sum(path["closureSize"] for path in output)
    return get_response(status.HTTP_200_OK, closure_size)


@app.get('/package_exists')
def package_exists(uname, sname, pname):
    store_path1 = Path(f'{nix_stores_path}/{uname}/{sname}/nix/store')
    for path in store_path1.iterdir():
        if pname in path:
            return get_response(status.HTTP_400_BAD_REQUEST, True)
    return get_response(status.HTTP_400_BAD_REQUEST, False)
