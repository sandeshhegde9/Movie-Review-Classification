#Simple document classifier. Uses Naive Bayse classifiers.
import math
import nltk
from pandas import DataFrame
import re


#Naive bayes. Takes a data matrix as input(In this case matrix containing True/False categorical values.
#adds a row at the end containing probability P(True/1) for each attribute. (class 1-Positive Review).
def NaiveBayes(data):
	last_row=[0,0]
	last_row1=[0,0]

	#For each column get the ratio- no of True/No of category 1.
	for j in range(2,len(data[0])):
		count=0
		pos_count=0
		count1=0
		neg_count=0
		for i in range(len(data)):
			if data[i][0]==1:
				pos_count+=1
				if data[i][j]==True:
					count+=1
			else:
				neg_count+=1
				if data[i][j]==True:
					count1+=1
		try:
			rat=round(float(count)/pos_count,5)
			last_row.append(rat)
		except:pass
		try:
			rat=round(float(count1)/neg_count,5)
			last_row1.append(rat)
		except:pass
	data1=[]
	data1.append(data[0])
	data1.append(last_row)
	data1.append(last_row1)
	rat=round(float(pos_count)/(len(data)-1),5)
	#print last_row,'\n\n\n'
	#print data[len(data)-1]
	return data1,rat


def predict(model,data,p):
	prob=1
	prob1=1
	for i in range(2,len(data)):
		if data[i]==True:
			prob=prob*model[1][i]
		else:
			prob=prob*(1-model[1][i])
	prob=prob*p

	for i in range(2,len(data)):
		if data[i]==True:
			prob1=prob1*model[2][i]
		else:
			prob1=prob1*model[2][i]
	prob1=prob1*p
	if prob>prob1:return 1
	else:return 0

def main():
	data=[]
	words=[]
	f1=open('train1.txt','r')

	#Read each line and make a list of all words.
	for line in f1:
		line=line.strip()
		line=line.split('\t')
		data.append([int(line[0]),line[1]]+[False for i in range(1000)])
		zzz=re.split('[ \t.]',line[1])
		
		try:zzz.remove('')
		except:pass
		words=words+zzz
	f1.close()
	
	#Get the frequency Distribution of the words present and retain only 1000 most frequest words.

	all_words=nltk.FreqDist(words)
	word_feature=all_words.keys()[:1050]
	l=len(word_feature)
	#print word_feature

	


	#Remove empty strings(If any) and words such as I,and etc.
	try:
		word_feature.remove('')
		word_feature.remove('i')
		word_feature.remove('and')
		word_feature.remove('is')
		word_feature.remove('it')
		word_feature.remove('the')
		word_feature.remove('of')
		word_feature.remove('a')
		word_feature.remove('an')
		word_feature.insert(0,"Category")
		word_feature.insert(1,"Text")
	except:pass 


	data.insert(0,word_feature[:1002])

	#Now build the data matrix.
	
	for i in range(1,len(data)):
		line=data[i]
		words=re.split('[ ,.]',line[1])
		try:words.remove('')
		except:pass
		for j in range(2,len(data[0])):
			if data[0][j] in words:
				data[i][j]=True
	

	#Get the probabilities using Naive Bayes method.

	model,pr=NaiveBayes(data)
	#print len(model[0]),len(model[1]),len(model[2]),len(data[0])
	#for a in model:
	#	print a
	count=0
	for i in range(1,len(data)):
		#print data[i][0]
		if predict(model,data[i],pr)==data[i][0]:
			count+=1
	print (float(count)/len(data))

main()
