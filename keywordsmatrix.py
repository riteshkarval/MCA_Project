def writefile(fname,matrix,wlist,size):
    f = open(fname,"w")
    #f.write(str(size)+'\n')
    for i in range(0,size):
      if i<size-1:
          f.write(wlist[i]+'  ')
      else:
	  f.write(wlist[i])
    f.write('\n')
    for i in range(0,size):
	for j in range(0,size):
        #line = f.next()
	    f.write(str(matrix[i,j])+' ')
def isascii(c, printable = False):
    if 0x00 <= ord(c) <= 0x7f:
        if printable:
            if 0x20 <= ord(c) <= 0x7e:
                return True
            else:
                return False
	else:
            return True
    else:
        return False
def findkeyword(sent):
    senwords=nltk.word_tokenize(sent.lower())
    stop = stopwords.words('english')
    stop=[x.encode('UTF8') for x in stop]
    #print sent
    for m in range(0,len(beforethis)):
      if beforethis[m] in sent:
        obj=re.search('(.*)'+beforethis[m]+'(.*)',sent,re.I)
        #print obj.group(1)
        if not obj.group(1) is '':
            subwords=nltk.word_tokenize(obj.group(1).lower())
            subwords=[w for w in subwords if not w in stop and len(w)>2]
            l=len(subwords)
            if l<3:
	        s=''
                for i in subwords:
                    s=s+' '+i
                if s.strip() not in keywords:
                    keywords.append(s.strip())
            elif l>1 and not subwords[len(subwords)-1] in keywords:
                if subwords[len(subwords)-1] not in keywords:
                    keywords.append(subwords[len(subwords)-1])
    for m in range(0,len(afterthis)):
      if afterthis[m] in sent:
        obj=re.search('(.*)'+afterthis[m]+'(.*)',sent,re.I)
        #print obj.group(1)
        if not obj.group(2) is '':
            subwords=nltk.word_tokenize(obj.group(2).lower())
            subwords=[w for w in subwords if not w in stop and len(w)>2]
            l=len(subwords)
            if l<3:
	        s=''
                for i in subwords:
                    s=s+' '+i
                if s.strip() not in keywords:
                    keywords.append(s.strip())
            elif l>1 and not subwords[0] in keywords:
                if subwords[0] not in keywords:
                    keywords.append(subwords[0])
slist=[]
keywords=[]
plist=[]
beforethis=[' is ',' are ',' can ']
afterthis=['the ',' in ',' on ',' called ',' of ',' like ',' any ',' has ',' have ']
import nltk
import re
import nltk.data
import sys
from nltk.corpus import stopwords
import numpy
sentdec=nltk.data.load('tokenizers/punkt/english.pickle')
stop = stopwords.words('english')
stop=[x.encode('UTF8') for x in stop]
f = open(sys.argv[1],"r")
string=f.read().decode('utf-8','remove')
f.close()
string=''.join([i for i in string if not i.isdigit() and isascii(i)])
#string=''.join([i for i in string if not i.isalnum()])
plist=string.lower().split('\n\n')
slist=[]
for p in plist:
    slist=slist+sentdec.tokenize(p.strip())
slist=[s.encode('UTF8') for s in slist]
plist=[p.encode('UTF8') for p in plist]
print string
for s in slist:
    findkeyword(s)
length=len(keywords)
senmatrix=numpy.zeros((length,length),numpy.int32)
print 'Calculating Pragraph matrix'
for i in range(0,length):
    for j in range(i+1,length):
        for p in plist:
            if(keywords[i] in p and keywords[j] in p):
                senmatrix[i,j]=senmatrix[i,j]+1
                #print '..',
        senmatrix[j,i]=senmatrix[i,j]
print "Pragraph matrix Calculated"
fname=sys.argv[1].split('.')[:1]
print fname
writefile(fname[0]+'.para',senmatrix,keywords,length)
print "Pragraph file written"
print keywords, length

 
