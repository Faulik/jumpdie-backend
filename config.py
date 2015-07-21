# Config file for pulsar server

# set the datastore for the pubsub
#data_store = 'pulsar://127.0.0.1:6410/1'
data_store = 'redis://0.0.0.0:6379/1'

bind = '0.0.0.0:8060'

reload = True

thread_workers = 10

