import datetime
import os

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels
import tensorflow as tf


class PredictEOD:              
    def plot_loss(history):
        plt.plot(history.history['loss'], label='loss')
        plt.plot(history.history['val_loss'], label='val_loss')
        plt.ylim([0, 10])
        plt.xlabel('Epoch')
        plt.ylabel('Error [MPG]')
        plt.legend()
        plt.grid(True)
            
    def build_and_compile_model(norm, layers, lr):
        model = tf.keras.Sequential(norm)
        for layer in layers:
            ev = eval(layer)
            model.add(ev)
        model.add(tf.keras.layers.Dense(1))

        model.compile(loss='mean_absolute_error',
                            optimizer=tf.keras.optimizers.Adam(0.01))
        return model     
    
    def layers(info):
        for layers in info:
            if len(layers) != 3:
                return 'Invalid input'
            else:
                continue
        layer_list = ['tf.keras.layers.{}({}, activation="{}")'.format(l[0], l[1], l[2]) for l in info]
        return layer_list
    
    def eod_close(data, lay, ep, vs, lr):
        # Split into x and y
        x = data.drop('Close', axis=1)
        y = data['Close']
        
        # Normalize data
        normalizer = tf.keras.layers.Normalization(axis=-1)
        normalizer.adapt(np.array(x))
        
        # Build and compile model
        model = PredictEOD.build_and_compile_model(normalizer, lay, lr)
        history = model.fit(x, y, epochs=ep, validation_split=vs)
        plh = PredictEOD.plot_loss(history)
        print(plh)

        # Collect results
        test_results = model.evaluate(x, y)
        print(test_results)      
        
        return model
    
    def predict(pred_data, model):
        pred = model.predict(pred_data)
        return pred
    
class MultiDayForecast:
    def forecast_plot(data, title):
        sns.set()
        x = data.index
        x.label('Date')
        y.label('Dollars')
        plt.plot(x, data, label=title)
        plt.title(title)
        return plt.show()
    
    def arma(data, drop_col):
        x = data.drop(drop_col, axis=1)
        y = data[drop_col]
        ARMAmodel = sm.SARIMAX(y, order = (1, 0, 1))
