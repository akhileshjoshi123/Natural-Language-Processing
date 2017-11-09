from collections import Counter
import random
import time
import sys
import os


start_time = time.clock()
ran = random.randint(11,15)



#fileName = 'C:/Users/Thinkpad T540P/Desktop/NLP HW2/HW2_F17_NLP6320_POSTaggedTrainingSet-Windows.txt'


#read in data from text file


path = sys.argv[1]

# Check if path exits
if os.path.exists(path):
    print ("Input file exists")
else :
    print("Input file does not exists")


with open(path,"r") as myfile:
   data=myfile.read()


print("Learning Rules : Please stand by :)")


tokens = []
tags = []


for sentence in data.split('\n'):
	for word in sentence.split():
		tokens.append(word.split('_')[0])
		tags.append(word.split('_')[1])


unigrams = {}
uniqueTags = set(tags)

for i in range(len(tokens)):
	if not tokens[i] in unigrams:
		unigrams[tokens[i]] = [tags[i]]
	else:
		unigrams[tokens[i]].append(tags[i])



def mostProbablePOS(dictionary):

	for key, value in dictionary.items():

		counter = Counter(value)
		maxValue = counter.most_common()[0]
		dictionary[key] = maxValue[0]

	return dictionary



mostProbablePOS = mostProbablePOS(unigrams)


def mostProbableErrors(tokens, tags, dictionary):
	modTags = []
	error = 0

	for word in tokens:
		modTags.append(dictionary[word])

	for i in range(len(modTags)):

		if modTags[i] != tags[i]:
			error += 1

	return modTags

modTags = mostProbableErrors(tokens, tags, mostProbablePOS)


def brills(tags, mostProbableTags, uniqueTags):
	

	brillsTemplate = {}

	modTags = mostProbableTags[:]

	index = 0
  
	while index < ran:
		threshold = 0
		index+=1
		print ("Iteration : " , index)
		for fromTag in uniqueTags:
			for toTag in uniqueTags:

				brills_dictionary = {}

				if fromTag == toTag:
					continue

				for pos in range(1,len(modTags)):
					if tags[pos] == toTag and modTags[pos] == fromTag:

						
						rule = (modTags[pos-1], fromTag, toTag)
						if rule in brills_dictionary:
							brills_dictionary[rule] += 1
						else:
							brills_dictionary[rule] = 1

					elif tags[pos] == fromTag and modTags[pos] == fromTag:

						rule = (modTags[pos-1], fromTag, toTag)
						if rule in brills_dictionary:
							brills_dictionary[rule] -= 1
						else:
							brills_dictionary[rule] = -1

				if brills_dictionary:
					maxValueKey = max(brills_dictionary, key=brills_dictionary.get)
					maxValue = brills_dictionary.get(maxValueKey)


					if maxValue > threshold:
						threshold = maxValue
						tupel = maxValueKey


		for i in range(len(modTags)-1):
			if modTags[i] == tupel[0] and modTags[i+1] == tupel[1]:
				modTags[i+1] = tupel[2]

		brillsTemplate[tupel] = threshold
        

	best_brills_template = sorted(brillsTemplate.items(), key=lambda x: x[1], reverse=True)

	print ("Brill Template List : " , best_brills_template)
   
	return best_brills_template



best_templates = brills(tags, modTags, uniqueTags)

print ("\n----------------------------------")
print ("Time required to learn :" , round (time.clock() - start_time,2), "seconds")
print ("\n----------------------------------")

# testing part

#input = "The_DT president_NN wants_VBZ to_TO control_VB the_DT board_NN 's_POS control_NN"

input = input("Enter test string : ")

most_prob_error = 0
input_tokens = []
input_tags = []
inputMostProbable = []


for i in input.split():
    input_token,input_tag = i.split("_")
    input_tokens.append(input_token)
    input_tags.append(input_tag)



for i in range(len(input_tokens)):
	inputMostProbable.append(mostProbablePOS[input_tokens[i]])

inputBrills = inputMostProbable[:]


for i in range(len(inputMostProbable)-1):
	for k, v in best_templates:
		prev = k[0]
		frm = k[1]
		to = k[2]

		if inputBrills[i] == prev and inputBrills[i+1] == frm:
			inputBrills[i+1] = to
			most_prob_error +=1
			break

a =[i for i, item in enumerate(input_tags) if item in inputBrills]

error = len(input_tags) - len(a)

error_rate = error/100 

print ("\n\n----------------------------------")
print("Most Probable Error : ", most_prob_error )
print("Most Probable Error Percentage : ", most_prob_error/100 , "%" )
print("Brills Error : " , error)
print("Brills Error Percentage : " , error_rate , "%")
print ("\n----------------------------------")


fout = "adj160230_brills_output.txt"
fo = open(fout, "w+")

fo.write ("Brills Output : " + "\n")
fo.write("Most Probable Error : " +  str(most_prob_error) )
fo.write("Most Probable Error Percentage : " + str(most_prob_error/100) + "%" )
fo.write("Brills Error : " + str(error))
fo.write("Brills Error Percentage : " + str(error_rate) + "%")

fo.close()