#read in data from text file

import sys
import os

path = sys.argv[1]

# Check if path exits
if os.path.exists(path):
    print ("Input File exists")
else :
    print("File does not exists")


with open(path,"r") as myfile:
   data=myfile.read().replace('\n', ' ')


#with open("C:/Users/Thinkpad T540P/Desktop/NLP HW2/HW2_F17_NLP6320-NLPCorpusTreebank2Parts-CorpusA-Windows.txt","r") as myfile:
#   data=myfile.read().replace('\n', ' ')




unigram_list = data.split()



def unigram_frequency(my_string):
  unigram_dict = {}  
  for item in my_string:
      if item in unigram_dict :
         unigram_dict[item] += 1
      else:
          unigram_dict[item] = 1
  return unigram_dict
  #print(my_dict)

unigram_dict = unigram_frequency(unigram_list)

def bigrams(words):
    bigram_tuple_list = []
    wprev = "None"
    for w in words:
        bigram_tuple_list.append((wprev, w))
        wprev = w
    return bigram_tuple_list

bigram_list = bigrams(unigram_list)
bigram_list = bigram_list[1:]

def bigram_frequency(my_string):
  bigram_dict = {}
  for item in my_string:
      if item in bigram_dict :
         bigram_dict[item] += 1
      else:
          bigram_dict[item] = 1
  return bigram_dict
  #print(bigram_dict)
  
bigram_dictionary = bigram_frequency(bigram_list)
  

bigramProbablity = {}

def bigram_probablities (unigram_dict , bigram_dict) :
    
    for key , value in bigram_dict.items() :
        if str(key[0]) == "None" :
            bigramProbablity[key] = 0
            continue
        bigramProbablity[key] = value/unigram_dict[key[0]]
    #print(bigramProbablity)

bigram_probablities (unigram_dict , bigram_dictionary)



fout = "adj160230_bigram_probablities.txt"
fo = open(fout, "w")

fo.write ("Bigram Probablities" + "\n")
for k, v in bigramProbablity.items():
    fo.write(str(k) + ' : '+ str(v) + '\n')

fo.close()

#################################

#add 1 smoothing

#################################


vocabulary_size = len(unigram_dict)

bigramProbabAddOne = {}

def bigram_prob_addOne_smoothing (unigram_dict , bigram_dict) :
    
    for key , value in bigram_dict.items() :
        if str(key[0]) == "None" :
            bigramProbabAddOne[key] = 1 / vocabulary_size
            continue
        bigramProbabAddOne[key] = (value + 1) / ( unigram_dict[key[0]] + vocabulary_size )
    #print(bigramProbabAddOne)


bigram_prob_addOne_smoothing (unigram_dict , bigram_dictionary)


fout = "adj160230_bigram_probablities_addOne.txt"
fo = open(fout, "w")

fo.write ("Bigram Add - 1 Probablities" + "\n")
for k, v in bigramProbabAddOne.items():
    fo.write(str(k) + ' : '+ str(v) + '\n')

fo.close()


#################################

# good turing

#################################

freqOfFreq={}
for v in bigram_dictionary.values():
    if not v in freqOfFreq :
        freqOfFreq[v]=1
    else :
        freqOfFreq[v] += 1

sorted_freqOfFreq = sorted(freqOfFreq.items())

N = len(bigram_list) #total number of things (bigrams) that actually occur in training
N1 = freqOfFreq[1] #count of things that were seen once in training

#cumulative Good-Turing probability of things that don’t occur even once
P_no_occurance = N1/N

#N0 is the number of bigrams that never occur

bigram_goodTuring = {}

#calculate c*
cstar = {}
pstar = {}
i=1
j=0
endIndex = len(sorted_freqOfFreq)
maxiumOccCount = max(sorted_freqOfFreq)[0]

b = [int(i[0]) for i in sorted_freqOfFreq]

for item in range(1,maxiumOccCount):
    if item not in b:
        sorted_freqOfFreq.append((item,0))
       
sorted_freqOfFreq = sorted(sorted_freqOfFreq)

###handle 0 case!!!!!



#v1 = round (((i+1) * sorted_freqOfFreq[1][1] ) / sorted_freqOfFreq[0][1] , 4)


for i in range(1,maxiumOccCount):
    value = sorted_freqOfFreq[i-1][1]
    if value == 0 :
        v = 0
    else :
        v = round (((i+1) * sorted_freqOfFreq[i][1] ) / (value) , 4)
    if v < value :
        cstar[sorted_freqOfFreq[i-1][0]] = v
        pstar[sorted_freqOfFreq[i-1][0]] = v/N
    else:
        cstar[sorted_freqOfFreq[i-1][0]]=value
        pstar[sorted_freqOfFreq[i-1][0]]=value/N

    
for key,value in bigram_dictionary.items():
    bigram_goodTuring[key]=pstar.get(value)
    



fout = "adj160230_bigram_probablities_goodTurning.txt"
fo = open(fout, "w")

fo.write ("Bigram Good Turing Probablities" + "\n")
for k, v in bigram_goodTuring.items():
    fo.write(str(k) + ' : '+ str(v) + '\n')

fo.close()


response = input("\n\nPlease input test string : ")

unigram_list_test = response.split()
unigram_test_count = {}
bigram_test_count = {}

for item in unigram_list_test :
    if item in unigram_dict :
        unigram_test_count[item] = unigram_dict[item]
    else :
        unigram_test_count[item] = 0

bigram_list_test = bigrams(unigram_list_test)

bigram_list_test = bigram_list_test[1:]

for item in bigram_list_test :
    if item in bigram_dictionary:
        bigram_test_count[item] = bigram_dictionary[item]
    else :    
        bigram_test_count[item] = 0

#without_smoothing_test_prob
dummy = 1
#biagram list for without smooth

biagram_list_test_p1 = []

for item in bigram_list_test:
    num = bigram_test_count[item]
    den = unigram_test_count[item[0]]
    
    if den != 0 :
        temp = (num / den)
        #dummy = prob_unsmooth
        biagram_list_test_p1.append((item,temp))
    else:
        #prob_unsmooth = 0
        #dummy = 0
        biagram_list_test_p1.append((item,0))
###prob of add one

bigram_test_count_1 = {}

for item in bigram_list_test :
    if item in bigram_dictionary:
        bigram_test_count_1[item] = bigramProbabAddOne[item]
    else :    
        bigram_test_count_1[item] = 0
 
#dummy = 1
biagram_list_test_p2 = []
for item in bigram_list_test:
    num = bigram_test_count_1[item]
     
    #print(den)
    if num != 0 :
        #temp = (num + 1 / den + N)
        #dummy = prob_unsmooth
        biagram_list_test_p2.append((item,num))
    else:
        if den not in unigram_dict:
            den = 0
        else : 
            den = unigram_test_count[item[0]]

        #prob_addOne = 0
        #dummy = 0
        temp = (num + 1) / (den + len(unigram_dict))
        biagram_list_test_p2.append((item,temp ))

        
    
####### prob of good turing

bigram_test_goodT = {}

dummy=1

for item in bigram_list_test :
    if item in bigram_list:
        bigram_test_goodT[item] = bigram_goodTuring[item]
    else :    
        bigram_test_goodT[item] = 0

#
#biagram_list_test_p3 = []
#
#for item in bigram_list_test:
#    if item in bigram_list:
#        count = bigram_test_goodT[item]
#    else :
#        count = 0
#    
#    if count != 0 :
#        #prob_goodT = dummy * pstar[count]
#        #dummy = prob_goodT
#        biagram_list_test_p3.append((item,count))
#    else:
#        dummy = P_no_occurance
#        biagram_list_test_p3.append((item,P_no_occurance))



biagram_list_test_p3 = []

for item in bigram_list_test:
    if item in bigram_goodTuring.keys():
        val = bigram_goodTuring[item]
        biagram_list_test_p3.append((item,val))
    else :
        biagram_list_test_p3.append((item,P_no_occurance))


#################output printing

test_bigram_count = len(bigram_list_test)

def product(list):
    p = 1
    for i in list:
        p *= i[1]
    return p

p1= product(biagram_list_test_p1)
p2= product(biagram_list_test_p2)
p3= product(biagram_list_test_p3)

fout = "adj160230_outputPart_1.txt"
fo = open(fout, "w")





fo.write("\n################################")
fo.write("\nPart #1 : without smoothing")
fo.write("\n################################")
fo.write("\nbigram counts : " + str(test_bigram_count) + "\n" )

for item in bigram_list_test:
    if item in bigram_dictionary.keys():
        fo.write(str(item) + ":" +str(bigram_dictionary[item]))
    else :
        fo.write(str(item) + " : " +"0")




fo.write("\nbigram probablilites :\n")



print("################################")
print("Part #1 : without smoothing")
print("################################")
print("\nbigram counts : " + str(test_bigram_count) )

print("\nbigram probablilites :")
for i in biagram_list_test_p1 :
    print(i[0] , " : " , i[1])
    fo.write(str(i[0]) + " : " + str(i[1]) + "\n")


fo.write("\nsentence probablity : " + str(p1) + "\n")
fo.write("\n################################\n")
fo.write("Part #2 : Add One Smoothing\n")
fo.write("\n################################\n")
fo.write("\nbigram counts : " + str(test_bigram_count) + "\n")
fo.write("\nbigram probablilites :\n")




print ("\nsentence probablity : " , p1 , "\n")
print("################################")
print("Part #2 : Add One Smoothing")
print("################################")
print("\nbigram counts : " + str(test_bigram_count) )
print("\nbigram probablilites :\n")


for i in biagram_list_test_p2 :
    print(i[0] , " : " , i[1])
    fo.write(str(i[0]) + " : " + str(i[1]) + "\n")
    

fo.write("\nsentence probablity : " + str(p2) + "\n")


fo.write("\n################################\n")
fo.write("Part #3 : Good Turing Smoothing")
fo.write("\n################################\n")
fo.write("\nbigram counts : " + str(test_bigram_count) + "\n" )
fo.write("\nbigram probablilites :\n")



print ("\nsentence probablity : " , p2, "\n")

print("################################")
print("Part #3 : Good Turing Smoothing")
print("################################")
print("\nbigram counts : " , test_bigram_count )
print("\nbigram probablilites :")

for i in biagram_list_test_p3 :
    print(i[0] , " : " , i[1])
    fo.write(str(i[0]) + " : " + str(i[1]) + "\n")

print ("\nsentence probablity : " , p3)
fo.write ("\nsentence probablity : " + str(p3))

fo.close()



