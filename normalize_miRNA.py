# Bioinformatics 
# Normalize raw dataset using MEAN or MEDIAN value
# Spike-in control normalization
# 4/7/2018, Bongsoo Park, Johns Hopkins

import operator
import numpy as np

f = open("raw_data_before_normalization.txt","r")
line_cnt = 0
id_list = []
norm_factor_mean = []
norm_factor_median = []
mirna_dataset = {}
for line in f:
	line = line.strip()
	data = line.split("\t")
	#print len(data)

	# treatment of header
	if line_cnt == 0:
		cnt = 0
		for ele in data:
			if cnt > 1:
				id_list.append(ele)
			cnt += 1
	else:
		tmp = []
		cnt = 0
		for ele in data:
			if cnt > 1:
				tmp.append(ele)
			cnt += 1
		mirna_dataset.update({data[0]:tmp})
	# calculate normalization factors (Spike-in control)
	if data[0] == "UniSp6 CP":
		#print data
		x = []
		cnt = 0
		for ele in data:
			if cnt > 1:
				x.append(float(ele))
			cnt += 1
		x = np.array(x)
		y = np.mean(x)
		z = np.median(x)
		print "MEAN:", np.mean(x)
		print "MEDIAN:", np.median(x)

		cnt = 0
		for ele in data:
			if cnt > 1:
				norm_factor_mean.append(float(ele)/y)
				norm_factor_median.append(float(ele)/z)
			cnt += 1	
		print "processing normalized factor for MEAN and MEDIAN..."
	line_cnt += 1
f.close()

#print len(id_list)
#print len(norm_factor_mean)
#print len(norm_factor_median)

normalized_mirna_dataset = {}
for the_key, the_value in sorted(mirna_dataset.items(), key=operator.itemgetter(0)):
	norm_array = ""
	cnt = 0
	for ele in mirna_dataset[the_key]:
		try:
			norm_array += "\t" + str(float(ele)/norm_factor_mean[cnt])
		except:
			norm_array += "\t" + "ND"
		cnt += 1
	print the_key+norm_array
