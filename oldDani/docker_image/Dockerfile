FROM tensorflow/tensorflow:latest
ADD script_inicio_tensorflow.py /tmp
RUN chmod +x /tmp/script_inicio_tensorflow.py
ENTRYPOINT ["/usr/bin/python", "/tmp/script_inicio_tensorflow.py"]
CMD ["$1 $2"]
