import a2s
import socket

from set_constants import (
    ADDRESS,
    PORT,
)

while True:
    query_port = int(PORT) + 1
    try:
        info = a2s.info(ADDRESS, query_port)
        print(info)
        break
    except socket.timeout as timeout:
        print("timeout")
    except Exception as error:
        raise Exception(error)
