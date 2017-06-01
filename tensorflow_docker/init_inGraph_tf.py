import argparse
import tensorflow as tf

FLAGS = None


def main(_):
    worker_hosts = FLAGS.worker_hosts.split(",")
    ps_hosts = FLAGS.ps_hosts.split(",")
    cluster = tf.train.ClusterSpec(
        {
            "worker": worker_hosts,
            "ps": ps_hosts
        },
    )
    server = tf.train.Server(cluster, job_name="worker", task_index=FLAGS.task_index)
    while True:
        pass


if __name__ == '__main__':

    # => Parsing input arguments
    # ------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")

    # · Flags for defining the tf.train.ClusterSpec
    parser.add_argument("--worker_hosts", type=str, default="", help="Comma-separated list of hostname:port pairs")

    # · Flags for defining the tf.train.Server
    parser.add_argument("--task_index", type=int, default=0, help="Index of task within the job")

    parser.add_argument("--ps_hosts", type=str, default=0, help="Comma-separated list of hostname:port pairs")

    FLAGS, unparsed = parser.parse_known_args()

    # => Run application
    # ------------------------------------------------------------
    tf.app.run()
