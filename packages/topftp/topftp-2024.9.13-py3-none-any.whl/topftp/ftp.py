#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import ftplib
import traceback
from io import BytesIO
from pathlib import Path
from ssl import SSLSocket
from typing import Any


class ReusedSSLSocket(SSLSocket):
    def unwrap(self):
        pass


class MyFTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""

    def ntransfercmd(self, cmd: str, rest: Any = None) -> tuple:
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(
                conn, server_hostname=self.host, session=self.sock.session
            )  # this is the fix
            conn.__class__ = ReusedSSLSocket

        return conn, size


class FTP:
    def __init__(self, host: str = "", user: str = "", password: str = "", **kwargs: Any):
        self.ftp = None
        self.host = host
        self.user = user
        self.password = password
        self.port = kwargs.get("port", 0)
        self.pasv = kwargs.get("pasv", True)
        self.timeout = kwargs.get("timeout", 5)
        self.silent = kwargs.get("silent", False)
        self.use_tls = kwargs.get("use_tls", False)
        self.verbose = kwargs.get("verbose", False)

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass

    def __getattr__(self, name: str) -> Any:
        """
        Delegate all unknown attributes to the ftp object.
        """
        return getattr(self.ftp, name)

    @classmethod
    def get_remote_path(cls, path: str) -> str:
        return f"/{path}".replace("//", "/").replace("//", "/")

    def connect(self, **kwargs: Any) -> Any:
        use_tls = kwargs.get("use_tls", self.use_tls)
        if use_tls:
            ftp = MyFTP_TLS()
        else:
            ftp = ftplib.FTP()

        host = kwargs.get("host", self.host)
        user = kwargs.get("user", self.user)
        port = kwargs.get("port", self.port)
        pasv = kwargs.get("pasv", self.pasv)
        password = kwargs.get("password", self.password)
        timeout = kwargs.get("timeout", self.timeout)
        try:
            ftp.connect(host, port, timeout)
            ftp.set_pasv(pasv)
            ftp.login(user, password)
            if use_tls:
                ftp.prot_p()

            self.ftp = ftp
            return ftp
        except Exception:
            if kwargs.get("silent", self.silent):
                traceback.print_exc()
            else:
                raise

    def close(self) -> None:
        if self.ftp:
            self.ftp.close()

    def run(self, method: str, cmd: str, *args: Any, **kwargs: Any) -> tuple:
        silent = kwargs.pop("silent", self.silent)
        verbose = kwargs.pop("verbose", self.verbose)
        try:
            ftp = self.ftp
            if not ftp:
                ftp = self.connect(silent=silent)

            if ftp:
                return True, getattr(self.ftp, method)(cmd, *args, **kwargs)

        except Exception:
            if silent:
                if verbose:
                    traceback.print_exc()

            else:
                raise

        return False, None

    def upload(self, local: Any, remote: str, **kwargs: Any) -> Any:
        resp = None
        is_ok = False
        fp = Path(local)
        return_all = kwargs.pop("return_all", False)
        filename = kwargs.pop("filename", "")
        blocksize = kwargs.pop("blocksize", 8192)
        remote_path = self.get_remote_path(f"{remote}/{filename or fp.name}")
        if fp.exists():
            with open(str(local), "rb") as fo:
                is_ok, resp = self.run("storbinary", f"STOR {remote_path}", fo, blocksize, **kwargs)

        return is_ok, resp if return_all else is_ok

    def upload_from_string(self, text: Any, remote: str, **kwargs: Any) -> Any:
        remote = self.get_remote_path(remote)
        bio = BytesIO(bytes(str(text), encoding="utf-8"))
        return_all = kwargs.pop("return_all", False)
        is_ok, resp = self.run("storbinary", f"STOR {remote}", bio, **kwargs)
        return is_ok, resp if return_all else is_ok

    def download(self, remote: str, local: Any, blocksize: int = 8192) -> tuple:
        resp = None
        local_path = Path(local)
        remote_path = self.get_remote_path(remote)
        if local_path.is_dir():
            local_path = local_path / Path(remote_path).name

        with open(str(local_path), "wb") as fo:
            is_ok, resp = self.run("retrbinary", f"RETR {remote_path}", fo.write, blocksize)

        return is_ok, resp

    def download_to_list(self, remote: str, blocksize: int = 8192) -> list:
        lines = []
        remote_path = self.get_remote_path(remote)
        self.run("retrbinary", f"RETR {remote_path}", lines.append, blocksize)
        rows = [line.decode("utf-8") for line in lines]
        return "".join(rows).splitlines()

    def listdir(self, remote: str) -> tuple:
        files = []
        folders = []
        for path in self.ftp.nlst(self.get_remote_path(remote)):
            if self.get_size(path) == -1:
                folders.append(path)
            else:
                files.append(path)

        return files, folders

    def delete(self, remote: str) -> tuple:
        return self.run("delete", self.get_remote_path(remote))

    def get_size(self, remote: str) -> int:
        try:
            return self.ftp.size(self.get_remote_path(remote))
        except Exception:
            return -1
