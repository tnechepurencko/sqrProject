from fastapi import FastAPI
from starlette import status
from starlette.responses import Response
import uvicorn

app = FastAPI()


def one_param_check(p1):
    return '%s' % p1


def two_param_check(p1, p2):
    return '%s %s' % (p1, p2)


@app.get('/login')
def login(uname, pwd):
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, pwd), media_type='text/plain')


@app.get('/logout')
def logout(uname):
    return Response(status_code=status.HTTP_200_OK, content=one_param_check(uname), media_type='text/plain')


@app.post('/registration')
def registration(uname, pwd):
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, pwd), media_type='text/plain')


@app.post('/create_store')
def create_store(uname, sname):
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, sname), media_type='text/plain')


@app.post('/remove_store')
def remove_store(uname, sname):
    return Response(status_code=status.HTTP_200_OK, content=two_param_check(uname, sname), media_type='text/plain')


@app.post('/track_store')
def track_store(sname):
    return Response(status_code=status.HTTP_200_OK, content=one_param_check(sname), media_type='text/plain')


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
