import tensorflow as tf
print("num gpu",len(tf.config.experimental.list_physical_devices('GPU' \
'')))