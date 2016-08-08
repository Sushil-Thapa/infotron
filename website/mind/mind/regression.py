import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from mind.param import *
from mind.mind.mind import Mind

class Regression(Mind):
    pass

class MyPolyMulti(Regression):
    name = Alias(['regression','ridge','fit'])
    degrees = NumArray(['(degree|degrees) $'])

    def execute(self,data_source):
        header = np.genfromtxt(data_source, dtype=None, delimiter=',', names=True)
        x = np.loadtxt(open(data_source,"rb"),delimiter=",",usecols=range(0,1),skiprows=1)
        y = np.loadtxt(open(data_source,"rb"),delimiter=",",usecols=range(1,2),skiprows=1)

        # generate points used to plot
        x_plot = np.linspace(min(x), max(x) + 2, 100)
        y_plot = np.linspace(min(y), max(y)+ 2, 100)

        # create matrix versions of these arrays
        X = x[:, np.newaxis]
        X_plot = x_plot[:, np.newaxis]

        plt.clf()
        # plt.plot(x_plot, y_plot, label="ground truth")
        plt.scatter(x, y, label="training points")

        for degree in self.degrees.get():
            model = make_pipeline(PolynomialFeatures(degree), Ridge())
            model.fit(X, y)
            y_plot = model.predict(X_plot)
            plt.plot(x_plot, y_plot, label="degree " + str(degree))

        plt.xlabel(header.dtype.names[0])
        plt.ylabel(header.dtype.names[1])
        plt.legend(loc='lower right')

        plt.savefig('static/images/last_plot.png')
