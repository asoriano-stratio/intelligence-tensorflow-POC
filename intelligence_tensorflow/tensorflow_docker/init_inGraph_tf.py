import argparse
import tensorflow as tf
import os

FLAGS = None


def get_cluster_conn():
    """ Composes the cluster connection urls using VIP for service discovery between workers and ps """

    # Marathon Id of the current Tensorflow worker/ps
    id = FLAGS.id
    # VIP port
    vip_port = str(FLAGS.vip_port)
    # Comma-separated list of workers' Marathon Ids
    worker_hosts = FLAGS.worker_hosts.split(",")
    # Comma-separated list of parameter servers' Marathon Ids
    ps_hosts = FLAGS.ps_hosts.split(",")

    # => Composing Workers' connection urls
    worker_conn = []
    for worker in worker_hosts:
        # · Set the random port assigned in DCOS if the current deployment is assigned to a worker
        #     When the tf server is initialized, it will set automatically this port
        if worker == id:
            worker_conn += [worker + ".marathon.l4lb.thisdcos.directory:" + os.getenv("PORT0")]

        # · For the other Tf cluster components urls the VIP port is used
        else:
            worker_conn += [worker + ".marathon.l4lb.thisdcos.directory:" + vip_port]

    # => Composing parameter servers' connection urls
    ps_conn = []
    for ps in ps_hosts:
        # · Set the random port assigned in DCOS if the current deployment is assigned to a ps
        #     When the tf server is initialized, it will set automatically this port
        if ps == id:
            ps_conn += [ps + ".marathon.l4lb.thisdcos.directory:" + os.getenv("PORT0")]

        # · For the other Tf cluster components urls the VIP port is used
        else:
            ps_conn += [ps + ".marathon.l4lb.thisdcos.directory:" + vip_port]

    return worker_conn, ps_conn


def main(_):

    # Getting cluster connection urls for workers and parameter servers
    worker_conn, ps_conn = get_cluster_conn()

    # Creating TF cluster specification
    cluster = tf.train.ClusterSpec({"worker": worker_conn, "ps": ps_conn})

    # Starting the server for the assigned job and task in this deployment
    server = tf.train.Server(cluster, job_name=FLAGS.job, task_index=FLAGS.task_index)
    # Blocks until the server has shut down.
    server.join()

    # if FLAGS.job == "ps":
    # while True:
    #     pass


if __name__ == '__main__':

    print("Hello from Tensorflow")

    # => Parsing input arguments
    # ------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")

    # · Flags for defining the tf.train.ClusterSpec
    parser.add_argument("--worker_hosts", type=str, default="", help="Comma-separated list of hostname:port pairs")

    # · Flags for defining
    parser.add_argument("--task_index", type=int, default=0, help="Index of task within the job")

    # · Flags for defining
    parser.add_argument("--ps_hosts", type=str, default=0, help="Comma-separated list of hostname:port pairs")

    # · Flags for defining
    parser.add_argument("--job", type=str, default=0, help="'worker' or 'ps'")

    # · Flags for defining
    parser.add_argument("--id", type=str, default=0, help="")

    # · Flags for defining
    parser.add_argument("--vip_port", type=str, default=0, help="")

    FLAGS, unparsed = parser.parse_known_args()

    # => Run application
    # ------------------------------------------------------------
    tf.app.run()
