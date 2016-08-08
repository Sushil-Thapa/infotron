import time

import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn import datasets
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

from mind.param import *
from mind.mind.mind import Mind

class Cluster(Mind):
	pass

class MyKMeans(Cluster):
    # specify aliases
    name = Alias(['kmeans','cluster'])
    # EASY.... now declare fields and specify related keywords
    n_clusters = Numeric(['to $ (clusters|types)'])
    # std_dev = Numeric(['standard deviation $','sd $','std dev $'])

    # write execute function, everything happens here
    def execute(self,data_source):
        X = np.loadtxt(open(data_source,"rb"),delimiter=",",skiprows=1)

        if len(X[0]) == 2:
            _n_clusters = self.n_clusters.get()
            k_means = KMeans(init='k-means++', n_clusters=_n_clusters, n_init=10)
            t0 = time.time()
            k_means.fit(X)
            t_batch = time.time() - t0
            k_means_labels = k_means.labels_
            k_means_cluster_centers = k_means.cluster_centers_
            k_means_labels_unique = np.unique(k_means_labels)

            ##############################################################################
            # Plot result

            plt.clf()

            a = np.arange(_n_clusters)
            ys = [i+a+(i*a)**2 for i in range(_n_clusters)]
            colors = cm.rainbow(np.linspace(0, 1, len(ys)))

            # KMeans
            for k, col in zip(range(_n_clusters), colors):
                my_members = k_means_labels == k
                cluster_center = k_means_cluster_centers[k]
                plt.plot(X[my_members, 0], X[my_members, 1], 'w',
                        markerfacecolor=col, marker='.')
                plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                        markeredgecolor='k', markersize=6)
            plt.title('KMeans')
            plt.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
                t_batch, k_means.inertia_))

            plt.savefig('static/images/last_plot.png')
            return "Done..."
            # plt.show()

        if len(X[0]) > 2:
            estimators = {'k_means_iris': KMeans(n_clusters=self.n_clusters.get())}

            fignum = 1
            for name, est in estimators.items():
                fig = plt.figure(fignum)
                plt.clf()
                ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

                plt.cla()
                est.fit(X)
                labels = est.labels_

                ax.scatter(X[:, 2], X[:, 0], X[:, 1], c=labels.astype(np.float))

                ax.w_xaxis.set_ticklabels([])
                ax.w_yaxis.set_ticklabels([])
                ax.w_zaxis.set_ticklabels([])
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                fignum = fignum + 1

            plt.savefig('static/images/last_plot.png')
            return "Done..."

class MyDBSCAN(Cluster):
    name = Alias(['cluster','dbscan'])

    def execute(self,data_source):

        X = np.loadtxt(open(data_source,"rb"),delimiter=",",skiprows=1)


        # X = StandardScaler().fit_transform(X)
        # Compute DBSCAN
        db = DBSCAN(eps=0.095).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        print('Estimated number of clusters: %d' % n_clusters_)
        # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
        # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
        # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
        # print("Adjusted Rand Index: %0.3f"
        #       % metrics.adjusted_rand_score(labels_true, labels))
        # print("Adjusted Mutual Information: %0.3f"
        #       % metrics.adjusted_mutual_info_score(labels_true, labels))
        # print("Silhouette Coefficient: %0.3f"
        #       % metrics.silhouette_score(X, labels))

        ##############################################################################
        # Plot result
        import matplotlib.pyplot as plt
        plt.clf()
        # Black removed and is used for noise instead.
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'

            class_member_mask = (labels == k)

            xy = X[class_member_mask & core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=14)

            xy = X[class_member_mask & ~core_samples_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=6)

        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.savefig('static/images/last_plot.png')
        return "Done..."
        # plt.show()