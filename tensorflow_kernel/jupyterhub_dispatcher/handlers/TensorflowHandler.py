from jupyterhub.handlers.base import BaseHandler
from tornado.web import RequestHandler


class TensorflowHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.log.info("GET /hub/tensorflow")
        print(self.request)

        print(self.get_current_user())
        user = self.get_current_user()
        if user:
            self.write("Hello {} from Tensorflow dispatcher!!!".format(str(user.name)))
        else:
            self.write("Hello UNKNOWN PERSON from Tensorflow dispatcher!!!")

    def delete(self, *args, **kwargs):
        self.log.info("DEL /hub/tensorflow")
        ""

