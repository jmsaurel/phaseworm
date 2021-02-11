import json
#from flask import Flask, jsonify, request
import numpy as np
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from scipy.interpolate import interp1d
#from dataclasses import dataclass
#from collections import namedtuple
#from data_reader import DataReader_mseed
from detect_peaks import detect_peaks
from model import UNet

#app = Flask(__name__)

#@dataclass
#class Config:
class Config:
    seed = 100
    use_seed = False
    n_channel = 3
    n_class = 3
    sampling_rate = 100.0
    dt = 1.0/sampling_rate
    X_shape = (3000, 1, n_channel)
    Y_shape = (3000, 1, n_class)
    min_event_gap = 3 * sampling_rate
    label_width = 6
    dtype="float32"
    depths = 5
    filters_root = 8
    kernel_size = [7, 1]
    pool_size = [4, 1]
    dilation_rate = [1, 1]
    class_weights = [1,1,1]
    batch_size = 20
    loss_type = "cross_entropy"
    weight_decay = 0
    optimizer = "adam"
    learning_rate = 0.001
    decay_step = -1
    decay_rate = 0.9
    momentum = 0.9
#def set_config():
#    config=Config()
#    config.seed = 100
#    config.use_seed = False
#    config.n_channel = 3
#    config.n_class = 3
#    config.sampling_rate = 100.0
#    config.dt = 1.0/sampling_rate
#    config.X_shape = (3000, 1, n_channel)
#    config.Y_shape = (3000, 1, n_class)
#    config.min_event_gap = 3 * sampling_rate
#    config.label_width = 6
#    config.dtype="float32"
#    config.depths = 5
#    config.filters_root = 8
#    config.kernel_size = [7, 1]
#    config.pool_size = [4, 1]
#    config.dilation_rate = [1, 1]
#    config.class_weights = [1,1,1]
#    config.batch_size = 20
#    config.loss_type = "cross_entropy"
#    config.weight_decay = 0
#    config.optimizer = "adam"
#    config.learning_rate = 0.001
#    config.decay_step = -1
#    config.decay_rate = 0.9
#    config.momentum = 0.9
#    return config


## load model
#def laod_model()
#config = Config()

def extact_picks(preds, fnames=None, config=None):
    picks = []
    for i, pred in enumerate(preds):
        if config is None:
            idx_p, prob_p = detect_peaks(pred[:,0,1], mph=0.3, mpd=50, show=False)
            idx_s, prob_s = detect_peaks(pred[:,0,2], mph=0.3, mpd=50, show=False)
        else:
            idx_p, prob_p = detect_peaks(pred[:,0,1], mph=config.prob_p, mpd=0.5/config.dt, show=False)
            idx_s, prob_s = detect_peaks(pred[:,0,2], mph=config.prob_s, mpd=0.5/config.dt, show=False)
        if fnames is None:
            fname = f"{i:04d}"
        else:
            fname = fnames[i].decode()
        picks.append(( list(map(int, idx_p)), list(map(float, prob_p)), list(map(int, idx_s)), list(map(float, prob_s)) ))
    return picks


def normalize(data, window=3000):
    """
    data: nsta, nt, chn
    """
    #shift = window//2
    #nt = data.shape[1]

    datan=np.zeros(shape=np.shape(data))
    for i in range(np.shape(data)[-1]):
        #if sum(datan[:,i])==0:
        #    continue
        #else:
        datan[:,i]=(data[:,i]-np.mean(datan[:,i]))/np.std(data[:,i])

    return datan

def preprocess(data):
    data = normalize(data)
    data = data[np.newaxis,:,np.newaxis,:]
    return data

def init_pred(config, opts):
    # config=Config()
    model = UNet(config, mode="pred")
    sess_config = tf.compat.v1.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    # sess_config.log_device_placement = False

    sess = tf.compat.v1.Session(config=sess_config)
    saver = tf.compat.v1.train.Saver()
    init = tf.compat.v1.global_variables_initializer()
    sess.run(init)
    # latest_check_point = tf.train.latest_checkpoint("./model/190703-214543")
    latest_check_point = tf.train.latest_checkpoint(opts.checkpoint)
    saver.restore(sess, latest_check_point)
    return sess,model

def get_prediction(data,sess,model):

    data = preprocess(data)

    
    feed = {model.X: data,
            model.drop_rate: 0,
            model.is_training: False}
    preds = sess.run(model.preds, feed_dict=feed)
    #print(preds.shape)

    picks = extact_picks(preds)

    return picks
 

#@app.route('/predict', methods=['POST'])
def predict(data,sess,model):
    #if request.method == 'POST':
    #data = np.array(request.json['data'])
    picks = get_prediction(data,sess,model)
    return picks#jsonify({"picks":picks})

#if __name__ == '__main__':
#    predict()
