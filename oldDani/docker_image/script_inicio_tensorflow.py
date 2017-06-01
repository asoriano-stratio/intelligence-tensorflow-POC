import argparse
import sys

import tensorflow as tf

FLAGS = None

def main(_):

  worker_hosts = FLAGS.worker_hosts.split(",") 
  cluster = tf.train.ClusterSpec({"worker": worker_hosts }) 
  server = tf.train.Server(cluster, job_name="worker", task_index=FLAGS.task_index)
  input("Press enter to exit Server")
 
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.register("type", "bool", lambda v: v.lower() == "true")

  # Flags for defining the tf.train.ClusterSpec
  parser.add_argument("--worker_hosts", type=str, default="", help="Comma-separated list of hostname:port pairs")
 
  # Flags for defining the tf.train.Server
  parser.add_argument("--task_index", type=int, default=0, help="Index of task within the job")

  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
