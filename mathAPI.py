from flask import Flask, render_template
from flask_cors import CORS,cross_origin
from flask_socketio import SocketIO
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timezone
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on('calcMean')
def calcMean(data):
    print('received message: ',data)

    data_list=json.loads(data)
    array_min=np.array([])
    array_max=np.array([])
    for item in data_list:
        print('pressure',item)
        array_sum_min=np.array([item['pressure_min']])
        array_sum_max=np.array([item['pressure_max']])
        array_min=np.append(array_min,array_sum_min)
        array_max=np.append(array_max,array_sum_max)
    file=saveFigure(array_min,array_max)
    socketio.emit('mean',
                  {
                      'min':array_min.mean(),
                      'max':array_max.mean(),
                      'file':file
                  })

def saveFigure(array_min,array_max):
    time=datetime.now().strftime("%Y%m%d%H%M%S")
    plt.plot(array_min)
    plt.plot(array_max)
    plt.savefig('d://medic/dist/charts/'+time+'chart.jpg',format='jpeg')
    plt.clf()
    return time+'chart.jpg'


if __name__ == '__main__':
    socketio.run(app)