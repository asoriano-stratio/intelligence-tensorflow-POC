import re
import requests
from notebook.base.handlers import IPythonHandler
from notebook.utils import url_path_join


class TensorflowHandler(IPythonHandler):

    def data_received(self, chunk):
        pass

    def get(self):

        self.log.info("GET - NotebookApp - Tensorflow Handler")
        hub_api_url = self.settings['hub_api_url']
        hub_api_key = self.settings['hub_api_key']
        r = requests.get(url_path_join(
            re.sub('/api', '', hub_api_url), "tensorflow"),
            headers={'Authorization': 'token %s' % hub_api_key},
        )

        self.finish('GET - NotebookApp - Tensorflow Handle')

    def delete(self, *args, **kwargs):

        self.log.info("DELETE - NotebookApp - Tensorflow Handler")
        hub_api_url = self.settings['hub_api_url']
        hub_api_key = self.settings['hub_api_key']
        r = requests.delete(url_path_join(
            re.sub('/api', '', hub_api_url), "tensorflow"),
            headers={'Authorization': 'token %s' % hub_api_key},
        )

        self.finish('DELETE - NotebookApp - Tensorflow Handle')


def load_jupyter_server_extension(nb_app):

    web_app = nb_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/tensorflow')
    web_app.add_handlers(host_pattern, [(route_pattern, TensorflowHandler)])
