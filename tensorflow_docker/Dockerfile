# --------------------------------------------------------------------
#  Stratio Intelligence - Custom tensorflow image
#
#  Integration with Tensorflow v1.1.0 for Python 3
# --------------------------------------------------------------------

FROM tensorflow/tensorflow:1.1.0-py3

# => Init Script

ADD init_inGraph_tf.py /tmp
RUN chmod +x /tmp/init_inGraph_tf.py


# => Docker entrypoint
#       Uses three input arguments '--worker_hosts', '--ps_hosts' and '--task_index'

ENTRYPOINT ["python3.5", "/tmp/init_inGraph_tf.py"]
CMD ["$1 $2 $2"]
