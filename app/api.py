from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

from db import Users, Stores
import nix

app = FastAPI()
users_db = Users()
stores_db = Stores()

nix_stores_path = '../nix_stores'


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
    code, content = nix.create_store(uname, sname, stores_db)
    return get_response(code, one_param_check(content))


@app.post('/get_stores')
def get_stores(uname):
    return stores_db.get_by_uname(uname)


@app.post('/remove_store')
def remove_store(uname, sname):
    code, content = nix.remove_store(uname, sname, stores_db)
    return get_response(code, one_param_check(content))


@app.post('/add_package')
def add_package(uname, sname, pname):
    code, content = nix.add_package(uname, sname, pname)
    return get_response(code, one_param_check(content))


@app.post('/rem_package')
def rem_package(uname, sname, pname):
    code, content = nix.rem_package(uname, sname, pname)
    return get_response(code, one_param_check(content))


@app.get('/dif_paths')
def dif_paths(uname, sname1, sname2):
    code, content = nix.rem_package(uname, sname1, sname2)
    return get_response(code, one_param_check(content))


@app.get('/dif_package')
def dif_package(uname, sname1, pname1, sname2, pname2):
    code, content = nix.dif_package(uname, sname1, pname1, sname2, pname2)
    return get_response(code, one_param_check(content))


@app.get('/size_package')
def size_package(uname, sname, pname):
    code, content = nix.size_package(uname, sname, pname)
    return get_response(code, one_param_check(content))


@app.get('/package_exists')
def package_exists(uname, sname, pname):
    code, content = nix.package_exists(uname, sname, pname)
    return get_response(code, one_param_check(content))
