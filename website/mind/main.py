from mapper import Mapper

mapper = Mapper()
mapper.mapRE("Cluster","datasets/data_cluster2d.csv","cluster into 7 clusters")


# mapper.map("Cluster","datasets/data_cluster3d.csv",['into clusters',7],['sd',2])
# mapper.map("Cluster","datasets/data_cluster2d.csv")


#MyDBSCAN("data_cluster2d.csv")
#MyKMeans("data_cluster3d.csv",7)
