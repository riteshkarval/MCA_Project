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
def presence_in(word):
    count=0
    for string in slist:
        string=string.lower()
        if(string.count(word)>0):
            count=count+1
    if (count==0):
        return -1
    else:
        return count
def tfidf(twlist):
    tf_idf=[0]*len(twlist)
    for x in range(0,(len(twlist))):
        #print wlist[x]
        tf=float(wlist.count(twlist[x]))/len(wlist)
        idf=float(len(slist))/presence_in(twlist[x])
        tf_idf[x]=tf*idf
    return tf_idf
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
                    keywordsB[m].append(s.strip())
            elif l>1 and not subwords[len(subwords)-1] in keywords:
                if subwords[len(subwords)-1] not in keywords:
                    keywords.append(subwords[len(subwords)-1])
                    keywordsB[m].append(subwords[len(subwords)-1])
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
                    keywordsA[m].append(s.strip())
            elif l>1 and not subwords[0] in keywords:
                if subwords[0] not in keywords:
                    keywords.append(subwords[0])
                    keywordsA[m].append(subwords[0])
def difficulty(sentence,query,Do):
    No=sentence.count(query)
    Lq=len(query.split())
    sen=sentence.split()
    stop = stopwords.words('english')
    stop=[x.encode('UTF8') for x in stop]
    #Ls=len([w for w in sen if not w in stop])
    Ls=len(sen)
    '''
    print Ls,Lq,No
    Dscore=(1.0/(No*frac))+(1.0/(Ls-No*Lq))-1.0
    '''
    Dscore=(1.0/100)*((50.0/No)+(20.0/Ls)+(30.0/Do))
    return Dscore
def getpos(sen):
    for p in plist:
        #print p,'\n\n'
        temp=sentdec.tokenize(p.strip())
        #print len(temp)
        for t in range(0,len(temp)):
	    if temp[t]==sen:
	        return t+1
    return 100
def myreplace(string, target, replacement):
    no_case = string.lower()
    index = no_case.find(target.lower())
    result = string[:index] + replacement + string[index + len(target):]
    return result
def findblank(string):
    string=string.lower()
    swords=nltk.word_tokenize(string)
    swords=[w for w in swords if not w in stop and len(w)>2]
    for tw in keywords:
        if tw in string and string.count(tw) is 1:# and not tw in answer:
            keywords.remove(tw)
            keywords.append(tw)
	    return tw
    tf_idf=[0]*len(swords)
    for x in range(0,(len(swords))):
        tf=float(wlist.count(swords[x]))/len(wlist)
        idf=float(len(slist))/presence_in(swords[x])
        tf_idf[x]=tf*idf
    for i in range( 0,len(tf_idf) ):
        for k in range(0, len(tf_idf)-1):
            if ( tf_idf[k]<tf_idf[k+1] ):
                temp=tf_idf[k]
                tf_idf[k]=tf_idf[k+1]
                tf_idf[k+1]=temp                         
                temp=swords[k]
                swords[k]=swords[k+1]
                swords[k+1]=temp
    for w in swords:
	if not w in answer:
	    return w
    return ''
def getoptions(word,sent):
    options=[blank]
    for i in range(0,len(keywordsA)):
        if word in keywordsA[i]:
            index=keywords.index(word)
            trow=pmatrix[index]
            twords=keywords
            for j in range( 0,len(trow) ):
                for k in range(0, len(trow)-1):
                    if ( trow[k]<trow[k+1] ):
                        temp=trow[k]
                        trow[k]=trow[k+1]
                        trow[k+1]=temp
                        temp=twords[k]
                        twords[k]=twords[k+1]
                        twords[k+1]=temp
            for w in twords:
	        if not w is word and not w in sent.lower() and not w in options and w in keywordsA[i]:
		    if len(options)<4:
		        options.append(w)
	            '''
            for w in keywordsA[i]:
                if not w is word and not w in sent.lower() and not w in options:
                    if len(options)<4:
                        options.append(w)
                        keywordsA[i].remove(w)
                        keywordsA[i].append(w)
                        '''
            return options
    for i in range(0,len(keywordsB)):
        if word in keywordsB[i]:
	    index=keywords.index(word)
            trow=pmatrix[index]
            twords=keywords
            for j in range( 0,len(trow) ):
                for k in range(0, len(trow)-1):
                    if ( trow[k]<trow[k+1] ):
                        temp=trow[k]
                        trow[k]=trow[k+1]
                        trow[k+1]=temp
                        temp=twords[k]
                        twords[k]=twords[k+1]
                        twords[k+1]=temp
            for w in twords:
	        if not w is word and not w in sent.lower() and not w in options and w in keywordsB[i]:
		    if len(options)<4:
		        options.append(w)
	            '''
            for w in keywordsB[i]:
                if not w is word and not w in sent.lower() and not w in options:
                    if len(options)<4:
                        options.append(w)
                        keywordsB[i].remove(w)
                        keywordsB[i].append(w)
                        '''
            return options
    return options
def getparamatrix():
    length=len(keywords)
    paramatrix=numpy.zeros((length,length),numpy.int32)
    for i in range(0,length):
        for j in range(i+1,length):
            for p in plist:
                if(keywords[i] in p and keywords[j] in p):
                    paramatrix[i,j]=paramatrix[i,j]+1
                    #print '..',
            paramatrix[j,i]=paramatrix[i,j]
    return paramatrix
wlist=[]
slist=[]
keywords=['']
answer=[]
plist=[]
beforethis=[' is ',' are ',' can ']
afterthis=['the ',' in ',' on ',' called ',' of ',' like ',' any ',' has ',' have ']
keywordsA=[]
keywordsB=[]
import nltk
import re
import nltk.data
import sys
from nltk.corpus import stopwords
import numpy
import subprocess
import Tkinter
import tkFileDialog
import os
for i in range(0,len(afterthis)):
    keywordsA.append([])
for i in range(0,len(beforethis)):
    keywordsB.append([])
sentdec=nltk.data.load('tokenizers/punkt/english.pickle')
stop = stopwords.words('english')
stop=[x.encode('UTF8') for x in stop]

root = Tkinter.Tk()
root.withdraw() 
currdir = os.getcwd()
path = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Select output file',filetypes=[('text files','.txt')])

f = open(sys.argv[1],"r")
string=f.read().decode('utf-8','ignore')
string=''.join([i for i in string if not i.isdigit() and isascii(i)])
wlist=nltk.word_tokenize(string.lower())
wlist1=[w for w in wlist if not w in stop]
wlist1=[i.encode('UTF8') for i in wlist1 if len(i)>2]
wlist1=list(set(wlist1))
plist=string.split('\n\n')
ld=[]
pos_weight=[]
for p in plist:
    slist=slist+sentdec.tokenize(p.strip())
slist=[s.encode('UTF8') for s in slist]
plist=[p.encode('UTF8') for p in plist]
for s in slist:
    findkeyword(s)
print keywords
wtf_idf=tfidf(keywords)
for i in range( 0,len(wtf_idf) ):
       for k in range(0, len(wtf_idf)-1):
         if ( wtf_idf[k]<wtf_idf[k+1] ):
             temp=wtf_idf[k]
             wtf_idf[k]=wtf_idf[k+1]
             wtf_idf[k+1]=temp
             temp=keywords[k]
             keywords[k]=keywords[k+1]
             keywords[k+1]=temp
for tw in keywords:
    if ' ' in tw:
      keywords.insert(0, keywords.pop(keywords.index(tw)))
    if len(tw)<3:
        keywords.remove(tw)
print 'Keywords Fetched, total keywords found ',len(keywords)#,keywords
pmatrix=getparamatrix()
print pmatrix,len(pmatrix)
for s in slist:
    s2list=nltk.word_tokenize(s.lower())
    ld.append(float(len(set(s)))/len(s))
    pos_weight.append(getpos(s))
score=[0]*len(slist)
topsen=[0]*len(slist)
for i in range(0,len(slist)):
    topsen[i]=i
    #score[i]=(1/len(slist[i]).split())
    l=1.0/len(slist[i].split())
    score[i]=ld[i]+pos_weight[i]+numpy.sin(numpy.radians(360*l))
    #print imp[i],ld[i],(1.0/len(slist[i])),pos_weight[i]
for i in range( 0,len(score) ):
   for k in range(0, len(score)-1):
     if ( score[k]<score[k+1] ):
         temp=score[k]
         score[k]=score[k+1]
         score[k+1]=temp                         
         temp=topsen[k]
         topsen[k]=topsen[k+1]
         topsen[k+1]=temp
questions=[]
diff=[]
sentnum=[0]
option=[]
print 'Making Questions'
for i in range(0,len(slist)):
    blank=findblank(slist[topsen[i]])
    answer.append(blank)
    questions.append(myreplace(slist[topsen[i]],blank,"_______"))
    diff.append(difficulty(slist[topsen[i]].lower() , blank , string.lower().count(blank)))
    sentnum.append(len(diff))
    option.append(getoptions(blank,slist[topsen[i]]))
    if(i>18):
      break
print 'Questions Created'
Dscore=numpy.mean(diff)+numpy.std(diff)/2
Mscore=numpy.mean(diff)-2*numpy.std(diff)
f=open(path,'w')
print Dscore,Mscore,numpy.mean(diff),numpy.std(diff)
if len(questions)>0:
    for j in range(0,len(questions)):
            if(diff[j]>Dscore):
                d='h'+str(j+1)+'. '
            elif(diff[j]<Dscore and diff[j]>Mscore):
                d='m'+str(j+1)+'. '
            else:
                d='e'+str(j+1)+'. '
            f.write(d+questions[j]+'\n')
            for k in range(0,len(option[j])):
	        f.write(str(k+1)+option[j][k]+'\n')
            f.write(answer[j]+'\n\n')
            if j>18:
                break
else:
    #pass
    f.write("No sentence found for "+query+"\n")
f.close()
subprocess.call(['kwrite',path])

'''
wfreq=[]
for i in wlist1:
    wfreq.append(wlist.count(i))

print wfreq
bound=numpy.mean(wfreq)-numpy.std(wfreq)
print numpy.mean(wfreq),numpy.std(wfreq)
print bound,numpy.mean(wfreq),numpy.std(wfreq)
for i in wlist1:
    if wfreq[wlist1.index(i)]<bound:
      print i,'\t',
'''
