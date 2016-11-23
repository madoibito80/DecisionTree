#	Binary Decision Tree
import numpy as np


def importData(data_type, num):

	if data_type == "mnist":


		fp = open("./train-images-idx3-ubyte","rb")

		magic = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])
		mnist_num = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])
		img_row = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])
		img_col = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])


		dim = img_row * img_col
		data = np.ndarray((num,dim))
		label = np.ndarray(num)


		for i in range(num):
			for y in range(img_row):
				for x in range(img_col):
					data[i,y*img_col+x] = ord(fp.read(1))



		fp = open("./train-labels-idx1-ubyte","rb")

		magic = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])
		mnist_num = sum([ord(fp.read(1)) * pow(256,3-i) for i in range(4)])

		for i in range(num):
			label[i] = ord(fp.read(1))




		return (data/255, label, 10)





def searchThreshold(data, label, cl, dn, branches, code):

	dim = len(data)

	thrs = np.zeros(dim)

	maxg = [-1,-1,float("inf")]

	for d in range(dim):

		thrs_list = np.unique(data[d])

		for i in range(len(thrs_list)-1):

			t1 = np.zeros(cl)
			t2 = np.zeros(cl)

			for n in range(dn):

				if(branches[n] == code):
					if(data[d,n] <= thrs_list[i]):
						t1[int(label[n])] += 1
					else:
						t2[int(label[n])] += 1

			p1 = t1.copy()
			p2 = t2.copy()

			if(np.sum(t1) != 0):
				p1 /= np.sum(t1)
			if(np.sum(t2) != 0):
				p2 /= np.sum(t2)


			e1 = 0.0
			e2 = 0.0

			for c in range(cl):
				if(p1[c] != 0):
					e1 -= p1[c] * np.log2(p1[c])

				if(p2[c] != 0):
					e2 -= p2[c] * np.log2(p2[c])


			e1 *= np.sum(t1)/dn
			e2 *= np.sum(t2)/dn

			entropy = e1 + e2

			if(entropy < maxg[2]):
				maxg[0] = d
				maxg[1] = thrs_list[i]
				maxg[2] = entropy


	print maxg[2]
	return (maxg[0], maxg[1])
			





def main():

	dn = 100

	(data, label, cl) = importData("mnist", dn)

	data = data.T


	branches = [''] * dn


	for l in range(4):

		codes = list(set(branches))
			
		for code in codes:

			(d, thr) = searchThreshold(data, label, cl, dn, branches, code)

			for n in range(dn):

				if(branches[n] == code):
					if(data[d][n] <= thr):
						branches[n] += '1'
					else:
						branches[n] += '0'


	for i in range(dn):
		print branches[i] + ':' + str(label[i])




main()

