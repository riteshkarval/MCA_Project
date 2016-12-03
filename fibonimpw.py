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
    options=[word]
    for i in range(0,len(keywordsA)):
        if word in keywordsA[i]:
            for w in keywordsA[i]:
                if not w is word and not w in sent.lower() and not w in options:
                    if len(options)<4:
                        options.append(w)
                        keywordsA[i].remove(w)
                        keywordsA[i].append(w)
            return options
    for i in range(0,len(keywordsB)):
        if word in keywordsB[i]:
            for w in keywordsB[i]:
                if not w is word and not w in sent.lower() and not w in options:
                    if len(options)<4:
                        options.append(w)
                        keywordsB[i].remove(w)
                        keywordsB[i].append(w)
            return options
    return options
def getparamatrix():
    length=len(plist)
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
keywords=[]
answer=[]
beforethis=[' is ',' are ',' can ']
afterthis=[' a ','the ',' in ',' on ',' called ',' of ',' like ',' any ',' has ',' have ']
keywordsA=[]
keywordsB=[]
plist=[]
import nltk
import re
import nltk.data
import sys
from nltk.corpus import stopwords
import numpy
import subprocess
for i in range(0,len(afterthis)):
    keywordsA.append([])
for i in range(0,len(beforethis)):
    keywordsB.append([])
sentdec=nltk.data.load('tokenizers/punkt/english.pickle')
stop = stopwords.words('english')
stop=[x.encode('UTF8') for x in stop]
f = open(sys.argv[1],"r")
string=f.read().decode('utf-8','ignore')
f.close()
string=''.join([i for i in string if not i.isdigit() and isascii(i)])
wlist=nltk.word_tokenize(string.lower())
wlist1=[w for w in wlist if not w in stop]
wlist1=[i.encode('UTF8') for i in wlist1 if len(i)>2]
wlist1=list(set(wlist1))
plist=string.split('\n\n')
ld=[]
pos_weight=[]
queries=(raw_input("Enter query: ")).lower().split(",")
for p in plist:
    slist=slist+sentdec.tokenize(p.strip())
slist=[s.encode('UTF8') for s in slist]
plist=[p.encode('UTF8') for p in plist]
for s in slist:
    findkeyword(s)
print keywordsA,keywordsB
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
print pmatrix
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
f=open('output.txt','w')
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
                    diff.append(difficulty(selectedsen[topsen[i]].lower() , query , string.lower().count(query)))
                    options.append(getoptions(query,selectedsen[topsen[i]]))
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
            f.write(query+'\n\n')
            if j>18:
                break
    else:
        #pass
        f.write("No sentence found for "+query+"\n")
f.close()
subprocess.call(['kwrite','output.txt'])

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
 
