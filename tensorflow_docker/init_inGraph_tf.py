import argparse
import tensorflow as tf
import os

FLAGS = None


def main(_):

    id = FLAGS.id
    worker_hosts = FLAGS.worker_hosts.split(",")
    ps_hosts = FLAGS.ps_hosts.split(",")

    worker_conn = []
    for worker in worker_hosts:
        if worker == id:
            worker_conn += [worker + ".marathon.l4lb.thisdcos.directory:" + os.getenv("PORT0")]
        else:
            worker_conn += [worker + ".marathon.l4lb.thisdcos.directory:2330"]

    ps_conn = []
    for ps in ps_hosts:
        if ps == id:
            ps_conn += [ps + ".marathon.l4lb.thisdcos.directory:" + os.getenv("PORT0")]
        else:
            ps_conn += [ps + ".marathon.l4lb.thisdcos.directory:2330"]

    cluster = tf.train.ClusterSpec(
        {
            "worker": worker_conn,
            "ps": ps_conn
        },
    )
    server = tf.train.Server(cluster, job_name=FLAGS.job, task_index=FLAGS.task_index)
    while True:
        pass


if __name__ == '__main__':

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

    FLAGS, unparsed = parser.parse_known_args()

    # => Run application
    # ------------------------------------------------------------
    tf.app.run()
