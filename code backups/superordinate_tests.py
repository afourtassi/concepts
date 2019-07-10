import csv
import re
from collections import defaultdict

filename = 'child_utterances_age_corpus.csv'

concepts = ["food", "clothes", "animal", "toy", "furniture"]

data = {}

food=[]
clothes=[]
animals=[]
toys=[]
furniture=[]

foodShort = ["banana", "apple", "peas", "corn", "bread"]
clothesShort = ["shirt", "pants", "pajamas", "coat", "jeans"]
animalsShort = ["dog", "bunny", "cat", "cow", "pig"]
toysShort = ["book", "doll", "stick", "ball", "train"]
furnitureShort = ["chair", "table", "bed", "couch", "door"]

foodExt = ["beans", "peas", "corn", "bread", "orange", "turkey", "banana", "chicken", "cake", "raisin", "strawberry", "potato", "apple", "pickle", "pumpkin"]
clothesExt = ["gloves", "pajamas", "pants", "boots", "jeans", "mittens", "coat", "jacket", "shirt", "sweater", "belt"]
animalsExt = ["goose", "moose", "squirrel", "dog", "frog", "cat", "horse", "cow", "giraffe", "pony", "zebra", "owl", "penguin", "donkey", "cow", "lion", "mouse", "duck", "pig", "sheep", "butterfly", "lamb", "bear", "rooster", "ant", "alligator", "turtle", "tiger", "elephant", "deer"]
toysExt = ["sled", "book", "boat", "train", "helicopter", "airplane", "doll", "hammer", "truck", "bus", "motorcycle","tricycle", "crayon", "scissors", "pencil", "stick", "balloon", "ball"]
furnitureExt = ["couch", "table", "lamp", "door", "telephone", "pillow", "chair", "bathtub", "bed", "sink", "broom", "carpet", "closet"]

things = ["bucket", "jar", "fork", "dish", "bowl", "ball", "napkin", "sled", "bottle", "oven", "spoon", "couch", "knife", "stove", "table", "book", "boat", "train", "helicopter", "airplane", "doll", "hammer", "truck", "lamp", "door", "telephone", "radio", "bus", "motorcycle", "table", "pillow", "cup", "chair", "tricycle", "cup", "crayon", "scissors", "bathtub", "bed", "shovel", "balloon", "necklace", "sink", "broom", "carpet", "closet", "bedroom", "pencil", "stick", "garage", "telephone"]


#Count number of utterances with category words
def count_concepts():
    counts = [0, 0, 0, 0, 0]

    with open(filename, newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            for concept in concepts:
                if concept in row[8]:
                    counts[concepts.index(concept)] += 1

    print(counts)

#Get utterances that have concepts mentioned
def concept_utterances():
    conceptDict = {}

    with open(filename, newline='') as f:
        reader = csv.reader(f)

        with open('child_concepts_3_ClarkBrown.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                for concept in concepts:
                    if concept in row[8] and row[8] not in conceptDict:
                        conceptDict[row[8]] = [concept, 1, [row[0]]]
                    elif concept in row[8] and row[8] in conceptDict:
                        conceptDict[row[8]][1] += 1
                        conceptDict[row[8]][2].append(row[0])
            for key, value in conceptDict.items():
                writer.writerow([value[0], key, value[1], value[2]])

    f.close()
    writeFile.close()

#Get book lines that have concepts mentioned
def concept_utterances_books():
    conceptDict = {}

    with open('100books.txt', newline='') as f:

        with open('concept_utterance_books.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for line in f:
                for concept in concepts:
                    if concept in line and line not in conceptDict:
                        conceptDict[line] = [concept, 1]
                    elif concept in line and line in conceptDict:
                        conceptDict[line][1] += 1
            for key, value in conceptDict.items():
                writer.writerow([value[0], key, value[1]])

    f.close()
    writeFile.close()

'''
PRELIMINARY FINDINGS
(Arbitrarily looking at any utterances with more than 4 occurrences)
In every case (except "thing"), the bare noun is the most (or second most common utterance.
There seems to be at least some explicit evidence for the "animal" category. There are 
many (100-200?) occurrences of utterances like "What animal is that?" Additional utterances
that may give children evidence that "animal" is a superordinate category are things like
"all these animals", "kind of/sort of animal", "all the animals", "what your favorite animal",
and "other animal".
"Clothes" has less explicit evidence. Also see things like "kind of clothes" and "all those 
clothes", but mostly things like "[POSS] clothes" and "clothes on."
For the "food" category, there are also utterances like "favorite food", "kind of food",
"all the food", and "eat food". There are also many utterances like "[ADJ] food", 
which perhaps suggests to children that there is more than one kind of food, aka it is 
a superordinate category.
"Thing" has (perhaps) least amount of explicit evidence. Examples like "what is this thing?", 
"nothing/something in there", "I want to show you something", "all the things", "what sort of thing?",
"favorite thing", "lot of things", "these things", "something else", but also see perhaps 
contradictory evidence like "something to eat", "do you hear anything?"
For books, we see phrases like "all the animals", "each animal", etc. Again, the referent is likely
some group of animals that have (perhaps?) been named earlier. 
Similar story for "clothes". Nothing explicit in the discourse about instances of "clothes", but perhaps
referent had been mentioned earlier or is pictured.
"Food" also follows this pattern--nothing explicit in the given utterance.
"Thing" also didn't have any explicit information, and probably even less outside reference as
well. Ex: "Do you want anything?", "Did you hear anything?"
For further investigation into this, should try additional concept names, especially 
for "thing." Could also ue "clothing." Analysis could be more quantitative as well. 
'''

#Get utterances that have concept and suggest a relation based on Hearst rules
def hearst_extraction():
    regEx = '([a-zA-Z]*( is a | or other | such as | including | especially )[a-zA-Z]*)|( such [a-zA-Z]* as [a-zA-Z]*)'

    with open('adult_utterances.csv', newline='') as f:
        reader = csv.reader(f)

        with open('hearst_extraction.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                for concept in concepts:
                    if concept in row[8] and (re.search(regEx, row[8])):
                        writer.writerow([concept, row[8]])

    f.close()
    writeFile.close()

#Get book lines that have concept and suggest a relation based on Hearst rules
def hearst_extraction_books():
    regEx = '([a-zA-Z]*( is a | or other | such as | including | especially )[a-zA-Z]*)|( such [a-zA-Z]* as [a-zA-Z]*)'

    with open('100books.txt', newline='') as f:

        with open('hearst_extraction_books.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for line in f:
                for concept in concepts:
                    if concept in line and (re.search(regEx, line)):
                        writer.writerow([concept, line])

    f.close()
    writeFile.close()

'''
PRELIMINARY FINDINGS
There are very few instances of explicit relationships. Most examples are "no such thing as X." 
There is one example that lists examples of "everyday food."
The only explicit example was "This thing is a Thneed." Perhaps it is explicit because kids
would have never encountered a Thneed before. Still no strong evidence for explicit learning.
For further work, could add more examples of strings that suggest relationships, especially 
dialectically specific ones like "X be Y," in addition to ones mentioned in the literature 
like "kind of/sort of X."
'''

#Fix this to align with updated concepts list
#Get other words that frequently occur with instances of a superordinate class in utterances
def extract_concepts():
    contexts = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]

    conceptLists = [food, clothes, animals, things]

    with open('adult_utterances.csv', newline='') as f:
        reader = csv.reader(f)

        with open('extract_concepts.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                for concept in conceptLists:
                    if any(a in row[8] for a in concept):
                        temp = row[8].split()
                        for word in temp:
                            contexts[conceptLists.index(concept)][word] += 1

            for context in contexts:
                for key, value in context.items():
                    writer.writerow([concepts[contexts.index(context)], key, value])

    f.close()
    writeFile.close()

#Get other words that frequently occur with instances of a superordinate class in book lines
def extract_concepts_books():
    contexts = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]

    conceptLists = [food, clothes, animals, things]

    with open('100books.txt', newline='') as f:

        with open('extract_concepts_books.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for line in f:
                for concept in conceptLists:
                    if any(a in line for a in concept):
                        temp = line.split()
                        for word in temp:
                            contexts[conceptLists.index(concept)][word] += 1

            for context in contexts:
                for key, value in context.items():
                    writer.writerow([concepts[contexts.index(context)], key, value])

    f.close()
    writeFile.close()
    
'''
PRELIMINARY FINDINGS
Arbitrarily looked at words that have more than 200 occurrences with the target concept.
Additionally, disregard any words that are functional or "light."
For "animals", the most frequent words were "want", "put", "see", "little", "play", "catch", 
"baby", etc. None of these words seem to give explicit cues about what words might be an 
instance of "animal".
Words associated with "clothes" include "on", "put" (theoretically "put on"), "off". Again, 
there is nothing inherently clothes-related in the words, and they do not occur frequently 
enough to be a reliable cue. 
Words associated with "food" include "eat", "want", "make", "piece", "slice". These words 
seem to be slightly more related to the "food" concept, but even so, they don't appear in every 
utterance that contain an instance of the "food" category.
Words associated with "things" include "get", "have", "put", "look", "think", "read", etc. 
Not surprisingly, these words are very disparate and have little to do necessarily with the 
"thing" concept. 
In books, arbitrarily looked for words with more than 10 occurrences bc of smaller corpus.
For books, "want", "little", "catch", "big", and "see" were most frequent context words related
to the "animal" category.
For "clothes" and "food", none of the words passed the "contentful" criteria. 
For "things", little", "said", "climbed", "looked" were most frequent words. 
Perhaps books lacked very explicit dialogue because there was strong visual evidence? What age
of reader were these books geared towards?
For further work, expand/refine list of instances.
'''

'''
def extraction_with_rules():
    with open('100books.txt', newline='') as rules:

        with open('adult_utterances.csv', newline='') as utterances:
            reader = csv.reader(f)

            with open('extract_concepts_books.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)

'''

#If there is a mention of a concept, look at surrounding utterances for mention of instance

n = 3
all = True

def concept_and_instance(n, all):
    conceptLists = ["food", "clothes", "animals", "toys", "furniture"]

    if n == 0:
        concept_and_instance_zero(conceptLists, all)

    else:
        n = 2 * n + 1

        curUtterances = [""] * n

        with open('all_utterances_3.csv', newline='') as f:
            reader = csv.reader(f)

            with open('concept_and_instance_all_n=3.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)

                for i in range(n):
                    row = next(reader)
                    curUtterances[i] = [row[8], row[12], row[14], row[16], row[25]]

                for i in range(0, n//2):
                    concept_and_instance_helper(i, curUtterances, conceptLists, writer, all)

                for row in reader:
                    i = 2
                    concept_and_instance_helper(i, curUtterances, conceptLists, writer, all)
                    curUtterances.pop(0)
                    curUtterances.append([row[8], row[12], row[14], row[16], row[25]])

                for i in range(n // 2 + 1, n):
                    concept_and_instance_helper(i, curUtterances, conceptLists, writer, all)


def concept_and_instance_helper(i, curUtterances, conceptLists, writer, all):
    if all:
        for concept in concepts:
            if concept in curUtterances[i][0].split():
                temp = []
                temp.append(concept)
                temp.append(" ")
                temp.append((curUtterances[i][0], curUtterances[i][1]))

                for utt in curUtterances:
                    for group in conceptLists:
                        for instance in data[group]:
                            if instance in utt[0].split() and instance != concept:
                                temp.append([curUtterances.index(utt), utt])
                                temp.append(instance)
                                temp.append(curUtterances[i][2])
                                temp.append(curUtterances[i][3])
                                temp.append(curUtterances[i][4])
                                if "Child" in curUtterances[i][1] and "Child" in utt[1]:
                                    temp[1] = "C -> C"
                                elif "Child" not in curUtterances[i][1] and "Child" not in utt[1]:
                                    temp[1] = "A -> A"
                                elif "Child" in curUtterances[i][1]:
                                    temp[1] = "C -> A"
                                elif "Child" in utt[1]:
                                    temp[1] = "A -> C"
                                writer.writerow(temp)
                                temp = temp[:3]

    else:
        for concept in concepts:
            if concept in curUtterances[i][0].split():
                temp = []
                temp.append(concept)
                temp.append(" ")
                temp.append((curUtterances[i][0], curUtterances[i][1]))

                #topicIndex = concepts.index(concept)

                for utt in curUtterances:
                    for instance in data[concept]:
                        if instance in utt[0].split() and instance != concept:
                            temp.append([curUtterances.index(utt), utt])
                            temp.append(instance)
                            temp.append(curUtterances[i][2])
                            temp.append(curUtterances[i][3])
                            temp.append(curUtterances[i][4])
                            if "Child" in curUtterances[i][1] and "Child" in utt[1]:
                                temp[1] = "C -> C"
                            elif "Child" not in curUtterances[i][1] and "Child" not in utt[1]:
                                temp[1] = "A -> A"
                            elif "Child" in curUtterances[i][1]:
                                temp[1] = "C -> A"
                            elif "Child" in utt[1]:
                                temp[1] = "A -> C"
                            writer.writerow(temp)
                            temp = temp[:3]


def concept_and_instance_zero(conceptLists, all):
    with open('all_utterances_3.csv', newline='') as f:
        reader = csv.reader(f)

        with open('concept_and_instance_all_n=0.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            if all:
                for row in reader:
                    for concept in concepts:
                        if concept in row[8].split():
                            temp = []
                            temp.append(concept)
                            temp.append(" ")
                            temp.append((row[8], row[12]))

                            for group in conceptLists:
                                for instance in data[group]:
                                    if instance in row[8].split() and instance != concept:
                                        temp.append([0, row[8]])
                                        temp.append(instance)
                                        temp.append(row[14])
                                        temp.append(row[16])
                                        temp.append(row[25])

                                        writer.writerow(temp)

                                        temp = temp[:3]
            else:
                for row in reader:
                    for concept in concepts:
                        if concept in row[8].split():
                            temp = []
                            temp.append(concept)
                            temp.append(" ")
                            temp.append((row[8], row[12]))

                            #topicIndex = concepts.index(concept)

                            for instance in data[concept]:
                                if instance in row[8].split() and instance != concept:
                                    temp.append([0, row[8]])
                                    temp.append(instance)
                                    temp.append(row[14])
                                    temp.append(row[16])
                                    temp.append(row[25])

                                    writer.writerow(temp)

                                    temp = temp[:3]

def get_instances():

    with open('wb_nouns.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            data[row[1]] = [x for x in row[2:] if x != ""]


#count_concepts()
#concept_utterances()
#hearst_extraction()
#extract_concepts()
#concept_utterances_books()
#hearst_extraction_books()
#extract_concepts_books()
get_instances()
concept_and_instance(n, all)


#More things to do:
#How are children using these superordinate words?
#Comparing children's books for spontaneous speech

#put a duplicate marker in
#Add headers
#Clean code?

#add verbs for toys, clothes, food to co-occurrences
#find number of unique words for up to 3 year olds
#take a sample from each window to make sure co-occurrences are valid

#make vectors for each of the basic terms
#then make the network

#Ask isaac about network construction, ask about input matrix etc.
#igraph library in r
#for now just keep nouns in matrices
#then add in verbs (play, eat, wear)

#Things to think about later: what to do with zero vectors
#Backup code

#if you refactor code, might be smart to include things in dictionaries instead of lists

#possibly change if instance is concept to if instance is any of the concepts
