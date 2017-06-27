import signal
import sys
import requests

# ------------------------------------------------------------------
#   KERNEL INITIALIZATION
# ------------------------------------------------------------------

# · Request to NotebookApp -> Request to JupyterHub-TensorflowDispatcher
from notebook import notebookapp
servers = list(notebookapp.list_running_servers())
if len(servers) != 1:
    raise Exception

r = requests.get(servers[0]["url"]+"tensorflow")
print(r.content.decode("utf-8"))


# ------------------------------------------------------------------
#   KERNEL SHUTDOWN
# ------------------------------------------------------------------

def signal_shutdown(signum, frame):
    print("signal_shutdown")
    sys.exit(0)


def normal_shutdown():
    print("normal_shutdown")
    requests.delete("http://127.0.0.1:8000/hub/tensorflow")

signal.signal(signal.SIGALRM, signal_shutdown)
signal.signal(signal.SIGHUP, signal_shutdown)
signal.signal(signal.SIGINT, signal_shutdown)
signal.signal(signal.SIGTERM, signal_shutdown)

import atexit
atexit.register(normal_shutdown)

# Remove the CWD from sys.path while we load stuff.
# This is added back by InteractiveShellApp.init_path()
if sys.path[0] == '':
    del sys.path[0]

from ipykernel import kernelapp as app
app.launch_new_instance()