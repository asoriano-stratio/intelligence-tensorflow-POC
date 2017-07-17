from ipykernel.ipkernel import IPythonKernel
from notebook import notebookapp
import requests


def get_running_server():
    servers = list(notebookapp.list_running_servers())
    if len(servers) != 1:
        raise Exception
    return servers[0]["url"]


class TensorflowKernel(IPythonKernel):

    implementation = 'Tensorflow adaptation'

    # ----------------------------------------------------------------------------
    #  Kernel initialization
    # ----------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(TensorflowKernel, self).__init__(*args, **kwargs)
        self.log.error("New tensorflow kernel!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
        # · Request to NotebookApp -> Request to JupyterHub-TensorflowDispatcher
        self.jupyter_singleserver_url = get_running_server()
        self.log.error(self.jupyter_singleserver_url)

        r = requests.get(self.jupyter_singleserver_url+"tensorflow")
        print(r.content.decode("utf-8"))
        self.send_response(self.)
        #raise Exception("Prueba excepcion")

    # ----------------------------------------------------------------------------
    #  Kernel shutdown
    # ----------------------------------------------------------------------------
    def do_shutdown(self, restart):
        requests.delete(self.jupyter_singleserver_url+"tensorflow")


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=TensorflowKernel)
