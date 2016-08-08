import numpy as np
# from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
import matplotlib.pyplot as plt
import matplotlib.font_manager

from mind.param import *
from mind.mind.mind import Mind

class Anomaly(Mind):
    pass

class Outlier(Anomaly):
    name = Alias(['anomaly','outlier','novelty'])
    contamination = Numeric(['where randomness $'])

    def execute(self,data_source):
        header = np.genfromtxt(data_source, dtype=None, delimiter=',', names=True)
        X1 = np.loadtxt(open(data_source,"rb"),delimiter=",",skiprows=1)

        # print(X1)
        # X1 = x[:, np.newaxis]
        # print(X1[:,0])

        conta = self.contamination.get_float()

        # Define "classifiers" to be used
        classifiers = {
            # "Empirical Covariance": EllipticEnvelope(support_fraction=1.,
            #                                          contamination=conta),
            # "Robust Covariance":
            # EllipticEnvelope(contamination=conta),
            "OCSVM": OneClassSVM(nu=conta, gamma=0.9)}
        colors = ['m', 'g', 'b']
        legend1 = {}

        # Learn a frontier for outlier detection with several classifiers
        xx1, yy1 = np.meshgrid(np.linspace(min(X1[:,0])-1, max(X1[:,0])+1, 500), np.linspace(min(X1[:,1])-1, max(X1[:,1])+1, 500))
        plt.clf()
        for i, (clf_name, clf) in enumerate(classifiers.items()):
            plt.figure(1)
            clf.fit(X1)
            Z1 = clf.decision_function(np.c_[xx1.ravel(), yy1.ravel()])
            Z1 = Z1.reshape(xx1.shape)
            legend1[clf_name] = plt.contour(
                xx1, yy1, Z1, levels=[0], linewidths=2, colors=colors[i])
            plt.contourf(xx1, yy1, Z1, levels=np.linspace(Z1.min(), 0, 7), cmap=plt.cm.Greens_r)
            a = plt.contour(xx1, yy1, Z1, levels=[0], linewidths=2, colors='yellow')
            plt.contourf(xx1, yy1, Z1, levels=[0, Z1.max()], colors='red')

        legend1_values_list = list( legend1.values() )
        legend1_keys_list = list( legend1.keys() )

        # Plot the results (= shape of the data points cloud)
        plt.figure(1)  # two clusters
        plt.title("Outlier detection")
        plt.scatter(X1[:, 0], X1[:, 1], color='black')
        plt.xlim((xx1.min(), xx1.max()))
        plt.ylim((yy1.min(), yy1.max()))
        # plt.legend((legend1_values_list[0].collections[0],
        #             # legend1_values_list[1].collections[0],
        #             # legend1_values_list[2].collections[0]),
        #            (legend1_keys_list[0], legend1_keys_list[1], legend1_keys_list[2]),
        #            loc="lower left",
        #            prop=matplotlib.font_manager.FontProperties(size=12))
        plt.xlabel(header.dtype.names[0])
        plt.ylabel(header.dtype.names[1])

        plt.savefig('static/images/last_plot.png')
