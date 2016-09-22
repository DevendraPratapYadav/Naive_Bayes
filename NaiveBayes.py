
"""
Devendra Pratap Yadav
Naive Bayes implemented in Python

"""
# NAIVE BAYES Classifier
from numpy import *
from pylab import *
import numpy as np
import math
import operator


# read data from file
def readData(dataset="test"):
	
	if dataset == "train":
		fileName = 'nbctrain';
	elif dataset == "test":
		fileName = 'nbctest';
		
	"""fil = open(fileName, 'rb')
	lbl = pyarray("b", fil.read())
	fil.close()
	"""
	
	with open(fileName) as f:
		content = f.read().splitlines()
	
	#for c in xrange(len(content)/100):
	#	print content[c],"\n\n"
	
	return content;

print "reading file"

emails = readData("train");
#emails=emails[0:10];

print "Training with ",len(emails)," emails"


hwords={};
swords={};


totalSpam=0
totalHam=0


# read email and split into words.
for e in emails:
	#print e,"\n\n"
	
	words=( e.split() );
	label=words[1];
	dict=hwords;
	
	if (label=="spam"):
		dict = swords;
		totalSpam+=1
	else:
		totalHam+=1
	#print label, len(dict)
	
	# store frequency of word
	for w in xrange(2,len(words)-1,2):
		if (words[w] in dict):
			dict[words[w]]+=int(words[w+1]);
			#print "adding ",int(words[w+1])," to ",words[w]," : ",label
		else:
			dict[words[w]]=int(words[w+1]);


			
#for k,v in hwords.items():
#	print k," -> ",v



Hvocab=0.0;
Svocab=0.0;

Hcount=0.0;
Scount=0.0;

# find vocabulary
for k,v in hwords.items():
	Hvocab+=1;
	Hcount+=v;

for k,v in swords.items():
	Svocab+=1;
	Scount+=v;

print "Ham Vocabulary: ",Hvocab, " | Total Words", Hcount,"\n", "Spam Vocabulary: ",Svocab, " | Total Words", Scount,"\n\n"


# sort to find 5 most frequent words
fHam = sorted(hwords.items(), key=operator.itemgetter(1),reverse=True)

fSpam = sorted(swords.items(), key=operator.itemgetter(1),reverse=True)

print "5 most common Ham words"
for i in xrange(5):
	print fHam[i]
	
print "\n5 most common Spam words"
for i in xrange(5):
	print fSpam[i]
	
	# load test data
tmails = readData("test");


priorHam=totalHam/float(totalHam+totalSpam)
priorSpam=totalSpam/float(totalHam+totalSpam)
print "\n"
print "Total Ham emails : ",totalHam, "\nTotal Spam emails : ",totalSpam
print "Prior Probability P(Ham)=",priorHam,"\nPrior Probability P(Spam)=", priorSpam
print "\n"
m=0.1;


print "Testing with ",len(tmails)," emails"

while(m<=1000000):

	correct=0
	#print "m-estimate : ",m,"  ->   ",
	print m," ",
	for e in tmails:
		#print e,"\n\n"
		
		words=( e.split() );
		trueLabel=words[1];
		dict=hwords;
		
		#print label, len(dict)
		Pham=0.0
		Pspam=0.0
		
		for w in xrange(2,len(words)-1,2):
			
			mm=m*1.0;
			wc=0.0;
			#bias=1.0; bl=2;
			if (words[w] in hwords):
				wc=hwords[words[w]];
#				if (words[w] in swords):
#					if (hwords[words[w]]/swords[words[w]] > bl):
#						bias=1.1;
					
			# Ham probability		
			Pham += (float(words[w+1])) * log( (wc+(mm/Hvocab)) /float(Hcount+mm) );
			
			wc=0.0;
#			bias=1.0
			if (words[w] in swords):
				wc=swords[words[w]];
#				if (words[w] in hwords):
#					if (swords[words[w]]/hwords[words[w]] > bl):
#						bias=1.1;			
			
			mm=m*1.0;
			
			# Spam probability
			Pspam += (float(words[w+1])) * log( (wc+(mm/Svocab)) /float(Scount+mm) );
			
		label="spam";
		
		if ( (priorHam+Pham) >(priorSpam+Pspam)):
			label="ham"
			
		if (label==trueLabel):
			correct+=1
#		else:
#			print (priorHam+Pham),(priorSpam+Pspam),"True: ",trueLabel
				
	accuracy=float(correct)/len(tmails);

	#print "Accuracy : ", accuracy*100.0, "%"
	print accuracy*100
	m*=2
	
	




