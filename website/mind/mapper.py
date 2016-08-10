from mind.mind.cluster import *
from mind.mind.regression import *
from mind.mind.anomaly import *
from mind.mind.assoc import *
from mind.param import *

import inspect
import re
import sys

#write mapper train function to pickle(module) mapper model
#load pickle model in mapper map function, then process

class Mapper:
    def mapRE(self,action,data_source,command):
        #eval(class_name) returns class
        classes = [cls for cls in eval("Cluster").__subclasses__()] #from cluster class, all inherited classes
        classes.extend([cls for cls in eval("Regression").__subclasses__()])
        classes.extend([cls for cls in eval("Anomaly").__subclasses__()])
        classes.extend([cls for cls in eval("Association").__subclasses__()])
        #print(classes)
        #sys.exit()

        for cls in classes:
        	# get all parameters
        	my_params = [item[0] for item in cls.__dict__.items() if isinstance(item[1], Param)]# and type(item[1]) != Alias] ?? item only?
        	my_keywords = [item.keywords for item in cls.__dict__.values() if isinstance(item, Param)]# and type(item) != Alias]
        	# print(my_keywords)
        	count = len(my_keywords)
        	indexes = []
        	for idx, kw in enumerate(my_keywords):  #key and value of my_keywords
        		# print(kw)
        		for regex in kw:
        			if regex.search(command):
        				match = regex.search(command)
        				count = count - 1 #zero if all checked
        				indexes.append(match.groupdict().get("value"))

        	if(count == 0):
        		exe = cls()
        		for i in range(len(indexes)):
        			x = getattr(exe, my_params[i]) #exe.my_params
        			x.value = indexes[i]
        			# print(my_params[indexes[i]])
        			# print(params[i][1])
        			# print(x)
        		return exe.execute(data_source)
        		break
