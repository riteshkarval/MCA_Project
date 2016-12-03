def presence_in(word,slist):
    count=0
    for string in slist:
        string=string.lower()
        if(string.count(word)>0):
            count=count+1
    if (count==0):
        return -1
    else:
        return count
def seq_search(query,string):
    sub1='(.*)'
    sub=sub1
    for i in query.split():
        sub=sub+i+sub1
    #print sub
    obj=re.search(sub,string,re.I)
    if obj:
        return True
    else:
        return False
def substr_len(query,string):
    q=query.split()
    if(len(q)==1):
        return 1
    else:
        sub1='(.*)'
        sub=sub1+q[0]+sub1+q[len(q)-1]+sub1
        obj=re.search(sub,string,re.I)
        return (len(obj.group(2).split())+2)
def getoptions(sen,query,sentmatrix):
    tarray=[]
    stop = stopwords.words('english')
    stop=[x.encode('UTF8') for x in stop]
    sen=sen.replace('________',' ',1)
    sen=''.join([i for i in sen if not i.isdigit() and isascii(i)])
    senwords=nltk.word_tokenize(sen.lower())
    senwords=[i for i in senwords if not i in stop and len(i)>2]
    topwords=[]
    toptions=[]
    toptions.append(query)
    wtf_idf=tfidf(senwords)
    for i in range( 0,len(wtf_idf) ):
       for k in range(0, len(wtf_idf)-1):
         if ( wtf_idf[k]<wtf_idf[k+1] ):
             temp=wtf_idf[k]
             wtf_idf[k]=wtf_idf[k+1]
             wtf_idf[k+1]=temp
             temp=senwords[k]
             senwords[k]=senwords[k+1]
             senwords[k+1]=temp
    print senwords
    if len(senwords)>2:
	for s in senwords[:3]:
	    for i in range(0,len(wlist)):
                topwords.append(i)
            print len(topwords)
            if s in wlist:
                for i in sentmatrix[wlist.index(s)]:
                    tarray.append(i)
            for i in range( 0,len(tarray) ):
                for k in range(0, len(tarray)-1):
                     if ( tarray[k]<tarray[k+1] ):
		         print i,k
                         temp=tarray[k]
                         tarray[k]=tarray[k+1]
                         tarray[k+1]=temp
                         temp=topwords[k]
                         topwords[k]=topwords[k+1]
                         topwords[k+1]=temp
            for i in range(0,len(wlist)):
		if (not wlist[topwords[i]] in toptions):
			toptions.append(wlist[topwords[i]])
			break
            topwords=[]
            tarray=[]  
    else:
    #print senwords,sen
        for i in range(0,len(wlist)):
            topwords.append(i)
        for i in sentmatrix[wlist.index(query)]:
                 tarray.append(i)
        for i in range( 0,len(tarray) ):
           for k in range(0, len(tarray)-1):
             if ( tarray[k]<tarray[k+1] ):
                 temp=tarray[k]
                 tarray[k]=tarray[k+1]
                 tarray[k+1]=temp
                 temp=topwords[k]
                 topwords[k]=topwords[k+1]
                 topwords[k+1]=temp
        j=0
        for i in range(0,len(wlist)):
           if (not wlist[topwords[i]] in senwords)and(not wlist[topwords[i]] is query):
               toptions.append(wlist[topwords[i]])
               j=j+1
           if j>2:
              break
    #print 'toptions ',toptions
    return toptions

def difficulty(sen,query,sentmatrix):
    stop = stopwords.words('english')
    stop=[x.encode('UTF8') for x in stop]
    sen=sen.replace('________',' ',1)
    sen=''.join([i for i in sen if not i.isdigit()])
    senwords=nltk.word_tokenize(sen.lower())
    senwords=[i for i in senwords if len(i)>2]
    #print senwords,sen
    #senwords.remove('________')
    senwords=[w for w in senwords if not w in stop]
    wtf_idf=tfidf(senwords)
    for i in range( 0,len(wtf_idf) ):
       for k in range(0, len(wtf_idf)-1):
         if ( wtf_idf[k]<wtf_idf[k+1] ):
             temp=wtf_idf[k]
             wtf_idf[k]=wtf_idf[k+1]
             wtf_idf[k+1]=temp
             temp=senwords[k]
             senwords[k]=senwords[k+1]
             senwords[k+1]=temp
    Dscore=0
    for i in range(0,len(senwords[:2])):
        if senwords[i] in wlist:
            Dscore=Dscore+1.0/(1.0+sentmatrix[wlist.index(query),wlist.index(senwords[i])])
            #print senwords[i],sentmatrix[wlist.index(query)][wlist.index(senwords[i])]
    #print Dscore,sentmatrix[wlist.index(query)][wlist.index(senwords[i])]
    return Dscore/len(senwords)
def tfidf(twlist):
    tf_idf=[0]*len(twlist)
    for x in range(0,(len(twlist))):
        #print wlist[x]
        tf=float(wlist.count(twlist[x]))/len(wlist)
        idf=float(len(slist))/presence_in(twlist[x],slist)
        tf_idf[x]=tf*idf
    return tf_idf
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
slist=[]
wlist=[]
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
sentdec=nltk.data.load('tokenizers/punkt/english.pickle')
stop = stopwords.words('english')
stop=[x.encode('UTF8') for x in stop]
f = open(sys.argv[1],"r")
string=f.read().decode('utf-8','remove')
f.close()
#string=string.encode('UTF8')
plist=string.split('\n\n')
for p in plist:
    slist=slist+sentdec.tokenize(p.strip())
queries=(raw_input("Enter query: ")).lower().split(",")

root = Tkinter.Tk()
root.withdraw() 
currdir = os.getcwd()
path = tkFileDialog.askopenfilename(parent=root, initialdir=currdir, title='Select output file',filetypes=[('text files','.txt')])

slist=[s.encode('UTF8') for s in slist]
plist=[p.encode('UTF8') for p in plist]
#print wlist
#wtf_idf=tfidf(wlist,slist)
#print wtf_idf
f = open(sys.argv[2],"r")
string=f.read()
tlist=string.split('\n')
values=[int(i) for i in tlist[1].split()]
length=len(tlist[0].split('  '))
wlist=tlist[0].split('  ')
print len(wlist)
sentmatrix=numpy.zeros((length,length),numpy.int32)
x=0
for i in range(0,length):
    for j in range(0,length):
	sentmatrix[i,j]=values[x]
	x=x+1
f=open(path,'w')
for query in queries:
    query_words=query.split()
    filtered_query = [w for w in query_words if not w in stop]
    selectedsen=[]
    imp=[]
    ld=[]
    pos_weight=[]
    #tf-idf of query
    tf_idf=tfidf(filtered_query)
    #print tf_idf
    sum_tf_idf=sum(tf_idf)
        #selecting sentences from each file
    for x in range(0,(len(slist))):
        tstr=slist[x].lower()
        timp=0
        ls=len(slist[x].split())
        lq=len(query.split())
        if (slist[x] not in selectedsen) and (ls>lq):
            if(query in tstr):
                s2list=nltk.word_tokenize(tstr)
                timp=1+sum_tf_idf
            #if slist[x] not in selectedsen:
                selectedsen.append(slist[x])
                imp.append(timp)
                ld.append(float(len(set(s2list)))/len(s2list))
                index=x+1
                pos_weight.append(getpos(slist[x]))
            elif(seq_search(query,tstr)):
                s2list=nltk.word_tokenize(tstr)
                #Lq/Lss
                Lq=len(query.split())
                Lss=substr_len(query,slist[x])
                timp=(float(Lq)/Lss)+sum_tf_idf
            #if slist[x] not in selectedsen:
                selectedsen.append(slist[x])
                imp.append(timp)
                ld.append(float(len(set(s2list)))/len(s2list))
                index=x+1
                pos_weight.append(getpos(slist[x]))
            else:
                s2list=nltk.word_tokenize(tstr)
                timp=0
                for i in range(0,len(filtered_query)):
                    if filtered_query[i] in tstr:
                        timp=timp+tf_idf[i]
                if (timp>0):
                    selectedsen.append(slist[x])
                    imp.append(timp)
                    ld.append(float(len(set(s2list)))/len(s2list))
                    index=x+1
                    pos_weight.append(getpos(slist[x]))
    score=[0]*len(selectedsen)
    topsen=[0]*len(selectedsen)
    #score calculation
    for i in range(0,len(selectedsen)):
        topsen[i]=i
        #score[i]=(1/len(selectedsen[i]).split())
        l=1.0/len(selectedsen[i].split())
        score[i]=imp[i]+ld[i]+numpy.sin(numpy.radians(360*l))+pos_weight[i]
        #print imp[i],ld[i],(1.0/len(selectedsen[i])),pos_weight[i]
    for i in range( 0,len(score) ):
       for k in range(0, len(score)-1):
         if ( score[k]<score[k+1] ):
             temp=score[k]
             score[k]=score[k+1]
             score[k+1]=temp
             temp=topsen[k]
             topsen[k]=topsen[k+1]
             topsen[k+1]=temp
    if len(selectedsen)>0:
        questions=[]
        diff=[]
        sentnum=[0]
        options=[]
        for i in range(0,len(selectedsen)):
            if query in selectedsen[topsen[i]].lower():
                    s=myreplace(selectedsen[topsen[i]],query,"________",)
                    questions.append(s)
                    diff.append(difficulty(s,query,sentmatrix))
                    options.append(getoptions(s,query,sentmatrix))
            if i>8:
	      break
        #print sentnum
        Dscore=numpy.mean(diff)
        Mscore=numpy.mean(diff)-2*numpy.std(diff)
        print Dscore,Mscore,numpy.mean(diff),numpy.std(diff)
        for j in range(0,len(questions)):
	    if(diff[j]>Dscore):
                d='h'+str(j+1)+'. '
            elif(diff[j]<Dscore and diff[j]>Mscore):
                d='m'+str(j+1)+'. '
            else:
                d='e'+str(j+1)+'. '
            f.write(d+questions[j]+'\n')
            for k in range(0,4):
	        f.write(str(k+1)+options[j][k]+'\n')
	    f.write(query+'\n\n')
            if j>18:
                break
    else:
        #pass
        f.write("No sentence found for "+query+"\n")
f.close()
subprocess.call(['kwrite',path])		