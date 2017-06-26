import sys
sys.path.append(
    "/home/asoriano/Stratio/Stratio-Intelligence/Sprints/SP3/Tensorflow refinement/tensorflow_kernel/notebookApp_extension"
)

c.NotebookApp.server_extensions = [
    'nb_tensorflow_ext'
]