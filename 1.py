#Simple document classifier. Uses Naive Bayse classifiers.
import math
import nltk
from pandas import DataFrame
import re


#Naive bayes. Takes a data matrix as input(In this case matrix containing True/False categorical values.
#adds a row at the end containing probability P(True/1) for each attribute. (class 1-Positive Review).
def NaiveBayes(data):
	last_row=[0,0]

	#For each column get the ratio- no of True/No of category 1.
	for j in range(2,len(data[0])):
		count=0
		pos_count=0
		for i in range(len(data)):
			if data[i][0]==1:
				pos_count+=1
				if data[i][j]==True:
					count+=1
		try:
			rat=round(float(count)/pos_count,5)
			last_row.append(rat)
		except:pass
	data.append(last_row)
	#print last_row,'\n\n\n'
	#print data[len(data)-1]
	return data
		

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
	print word_feature

	#print word_feature
	

'''	try:#Remove empty strings(If any) and words such as I,and etc.
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
	'''

	data.insert(0,word_feature[:1000])

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

	data=NaiveBayes(data)

main()
