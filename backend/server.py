import asyncio
import base64
import hashlib
import os
import requests
import sqlite3
import sys
from typing import Annotated
import uuid

import uvicorn
from fastapi import (
    Depends, FastAPI, Header, HTTPException, Query, Request, status
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

bin_path = os.path.abspath("bin")
db_path = os.path.join(bin_path, "db.db")
token_user_map = {}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/ui", StaticFiles(
        directory=os.path.abspath(os.path.join("..", "frontend", "dist")),
        html=True,
    ),
    name="ui"
)


class BaseReq(BaseModel):
    data: str
    page_no: int = 0
    page_size: int = -1


class FileReq(BaseModel):
    path: str
    start: int = 0
    size: int = -1


class PopenReq(BaseModel):
    program: str = "cmd"
    cmd: list
    args: list = ["/k", "@ECHO OFF && chcp"]
    encoding: str = "utf-8"
    skip: int = 1


class UserLoginReq(BaseModel):
    username: str
    password: str


async def auth(token: Annotated[str | None, Header()] = None,
               token_query: str = Query(None, alias="token")):
    if not token:
        token = token_query
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no_token"
        )

    if token in token_user_map:
        return token_user_map[token]

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid_token"
    )


@app.get("/ping")
def api_ping():
    return {"status": "ok", "data": "pong"}


@app.post("/login")
def api_login(user: UserLoginReq):
    try:
        psw_md5 = hashlib.md5(b'ctrl-server')
        psw_md5.update(user.password.encode('utf-8'))

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT `id`,username FROM user WHERE username=? and password=?;',
                    (user.username, psw_md5.hexdigest()))
        user = cur.fetchone()
        if user is None:
            return {"status": "fail", "data": "no_user"}

        token = None
        for _ in range(1000):
            token = str(uuid.uuid4())
            if token not in token_user_map:
                break

        if token in token_user_map:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="gen_token"
            )
        token_user_map[token] = user
        return {
            "status": "ok",
            "data": {
                "id": user[0],
                "token": token
            }
        }
    finally:
        cur.close()
        conn.close()


@app.get("/ls")
def api_ls(
    _: Annotated[str, Depends(auth)],
    req: BaseReq
):
    dir_path = req.data
    if not os.path.exists(dir_path):
        return {"status": "fail", "data": "not_found"}
    if not os.path.isdir(dir_path):
        return {"status": "fail", "data": "not_dir"}
    
    data = []
    fid = -1
    fid_start = req.page_no * req.page_size
    fid_end = fid_start + req.page_size - 1
    page = req.page_size > 0
    with os.scandir(dir_path) as iter:
        for entry in iter:
            fid += 1
            if page:
                if fid < fid_start:
                    continue
                elif fid > fid_end:
                    break
            info = {
                "name": entry.name
            }
            path = os.path.join(dir_path, entry.name)
            if entry.is_dir():
                info["type"] = "dir"
            elif entry.is_file():
                info["type"] = "file"
                info["size"] = os.stat(path).st_size
            elif entry.is_symlink():
                info["type"] = "symlink"
            else:
                info["type"] = "unknown"
            data.append(info)
    return {"status": "ok", "data": data}


@app.post("/system")
def api_system(
    _: Annotated[str, Depends(auth)],
    req: BaseReq
):
    code = os.system(req.data)
    return {"status": "ok", "data": code}


@app.post("/popen")
async def api_popen(
    _: Annotated[str, Depends(auth)],
    req: PopenReq
):
    process = await asyncio.create_subprocess_exec(
        req.program,
        *req.args,
        # shell=False,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    for _ in range(req.skip):
        await process.stdout.readline()
    command = "\n".join(req.cmd) + "\n"
    output, err = await process.communicate(command.encode(req.encoding))
    return {
        "status": "ok",
        "data": output.decode(req.encoding),
        "err": err.decode(req.encoding)
    }


@app.post("/read")
async def api_read(
    _: Annotated[str, Depends(auth)],
    req: FileReq
):
    if not os.path.exists(req.path):
        return {"status": "fail", "data": "not_found"}
    if not os.path.isfile(req.path):
        return {"status": "fail", "data": "not_file"}
    with open(req.path, "rb") as fp:
        fp.seek(req.start)
        data = fp.read(None if req.size < 0 else req.size)
        data_base64 = str(base64.b64encode(data), "utf-8")
    return {
        "status": "ok",
        "data": data_base64
    }


@app.get("/hls/{other_path:path}")
async def api_hls(
    _: Annotated[str, Depends(auth)],
    other_path: str,
    req: Request
):
    url = f"http://localhost:8888/{other_path}"
    body = bytes(await req.body()) or None
    r = requests.request(
        req.method,
        url,
        headers={
            'Cookie': req.headers.get('cookie') or '',
            'Content-Type': req.headers.get('Content-Type')
        },
        params=req.query_params,
        data=body,
        stream=True,
        allow_redirects=False
    )
    h = dict(r.headers)
    h.pop('Content-Length', None)
    return StreamingResponse(r.raw.stream(4096000), headers=h, status_code=r.status_code)


if __name__ == "__main__":
    host = "127.0.0.1"
    if len(sys.argv) > 1:
        host = str(sys.argv[1])
    uvicorn.run(app, host=host, port=13314, log_level="info")
