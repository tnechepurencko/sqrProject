from fastapi import FastAPI
from starlette import status
from starlette.responses import Response

from db import Users

app = FastAPI()
users_db = Users()


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
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, sname), media_type='text/plain')


@app.post('/remove_store')
def remove_store(uname, sname):
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, sname), media_type='text/plain')


@app.post('/track_store')
def track_store(sname):
    return Response(status_code=status.HTTP_200_OK, content=one_param_check(sname), media_type='text/plain')

