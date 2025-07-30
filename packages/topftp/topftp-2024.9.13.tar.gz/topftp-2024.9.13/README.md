# topftp

a package on top of ftplib to use FTP easily

## installation

```bash
pip install topftp
```

## usage

```python
from topftp.ftp import FTP

host = "127.0.0.1"
user ="username"
password = "password"
port = 21
timeout = 5

ftp = FTP(host, user, password, port=port, timeout=timeout)
# set verbose to True to print exceptions
# set silent to True to not raise exceptions
# ftp.silent = True
# ftp.verbose = True

ftp.connect()

# list files in current directory
files, folders = ftp.listdir()

# download file
ftp.download("/file.txt", "local_file.txt")

# download file content to list
lines = ftp.download_to_list("/file.txt")

# upload file
ftp.upload("local_file.txt", "/remote_file.txt")

# upload from string
ftp.upload_from_string("Hello, topftp!", "/remote_file.txt")

# delete file
ftp.delete("/remote_file.txt")

# for missing methods on ftplib.FTP, you can use them directly
# ftp.some_method(*args, **kwargs)
# is same to
# ftp.ftp.some_method(*args, **kwargs)

# close connection
ftp.close()
```
