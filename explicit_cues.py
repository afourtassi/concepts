'''
Kyra Wilson
12/5/19

How to run: explicit_cues.py followed by ages (<3, <4, <5, or <6) you want to get data for

Ex: "explicit_cues.py 3 4" will get co-occurrences for all utterances for children under 3 and all utterances for children under 4

TODO:
*make total number of occurrences (caculated in utterances_to_txt) a csv instead of just print statement
*make a cleaner file structure
*make it run faster by tacking on ages instead of researching each time

add in code to get broad concepts (if necessary)
test & make sure output is what we actually want...

'''

import csv
import re
import sys

'''-----------------------------------------------------------------------------------------------------'''
'''THIS CODE IS AWFUL AND BAD AND NEEDS TO BE FIXED SOON'''
n = 0
all = True

'''
PARAMETERS: n, the size of the window to search
            all, whether to search for co-occurrence in all categories or only the correct superordinate category.
Find any co-ocurrences of basic terms and superordinate categroies in utterances from childes database.
'''
def concept_and_instance(n, all):
    conceptLists = ["food", "clothes", "animals", "toys", "furniture"]

    if n == 0:
        concept_and_instance_zero(conceptLists, all)

    else:
        n = 2 * n + 1

        curUtterances = [""] * n

        with open('all_utterances_3.csv', newline='') as f:
            reader = csv.reader(f)

            with open('concept_and_instance_all_verbs_n=0_3.csv', 'w') as writeFile:
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
        for concept in conceptsDict.keys():
            if concept in curUtterances[i][0].split():
                temp = []
                temp.append(conceptsDict[concept])
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

    #add something in here to know if utterance was a category utterance or verb utterance?
    else:
        for concept in conceptsDict.keys():
            if concept in curUtterances[i][0].split():
                temp = []
                temp.append(conceptsDict[concept])
                temp.append(" ")
                temp.append((curUtterances[i][0], curUtterances[i][1]))

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

#row[8] if 3,6 and row[x+1] if 4,5
def concept_and_instance_zero(conceptLists, all):
    with open('all_utterances_3.csv', newline='') as f:
        reader = csv.reader(f)

        with open('concept_and_instance_all_verbs_n=0_3.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            if all:
                for row in reader:
                    for concept in conceptsDict.keys():
                        if concept in row[8].split():
                            temp = []
                            temp.append(conceptsDict[concept])
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
                        if concept in row[8].split() or concept == "food" and "eat" in row[8].split() \
                            or concept == "clothes" and "wear" in row[8].split() \
                                or concept == "toy" and "play" in row[8].split():
                            temp = []
                            temp.append(concept)
                            temp.append(" ")
                            temp.append((row[8], row[12]))

                            for instance in data[concept]:
                                if instance in row[8].split() and instance != concept:
                                    temp.append([0, row[8]])
                                    temp.append(instance)
                                    temp.append(row[14])
                                    temp.append(row[16])
                                    temp.append(row[25])

                                    writer.writerow(temp)

                                    temp = temp[:3]
'''-----------------------------------------------------------------------------------------------------'''


conceptsDict = {"animal": "animal", "eat": "food", "food": "food", "wear": "clothes", "clothing": "clothes",
                "clothes": "clothes", "play": "toy", "toy": "toy", "play with": "toy", "furniture": "furniture",
                "use": "furniture", "ride": "vehicle", "vehicle": "vehicle", "ride in": "vehicle",
                "ride on": "vehicle"}

broad_concepts = ["animal", "artifact"]
broad_concept_categories = ["toy", "vehicle", "furniture", "animal"]
concepts = ["animal", "toy", "vehicle", "clothes", "furniture", "food"]

verbs = ["ride on", "ride in", "ride", "play", "play with", "use", "eat", "wear"]


#broad_concepts_and_instances_age.csv = verb+compl
#concepts_and_instances_all_age.csv = co-occurrence
#explicit_categorization_age.csv = labeling
files = ["pydata/adult_utterances_age.csv", "rdata/adult_utterances_age.txt", "rdata/broad_concepts_and_instances_age.csv", "rdata/concepts_and_instances_all_age.csv", "rdata/explicit_categorization_age.csv"]

def get_instances():
    temp = []

    with open('pydata/wb_nouns_edited.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            # data[row[1]] = [x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"]

            if row[1] in concepts:
                temp.append([x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"])

        instances = [item for sublist in temp for item in sublist]
        
        f.close()
        return instances


def utterances_to_txt(readfile, write_txt_file):
    total_categories = {"animal": 0, "toy": 0, "vehicle": 0, "clothes": 0, "furniture": 0, "food": 0}
    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_txt_file, 'w') as writeFile:
            next(reader)

            for row in reader:
                utt = row[8]
                for word in concepts:
                    if word in utt:
                        utt = re.sub(word, "", utt)
                        total_categories[word] += 1
                writeFile.write(utt + " ")
    
    print(total_categories)
    f.close()
    writeFile.close()
    
# Get co-occurrence of concepts and instances
# Output = concept_and_instance_all_age.csv
def get_concept_cooccurrence(instances, readfile, write_broad_concept_file):
    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_broad_concept_file, 'w') as writeFile:
            writer = csv.writer(writeFile)
            
            for row in reader:
                utt = row[8].split()
                for instance in instances:
                    if instance in utt:
                        for concept in concepts:
                            if concept in utt:
                                temp = []
                                temp.append(concept)
                                temp.append(" ")
                                temp.append((row[8], row[12]))
                                temp.append([0, row[8]])
                                temp.append(instance)
                                temp.append(row[14])
                                temp.append(row[16])
                                temp.append(row[25])

                                writer.writerow(temp)
    f.close()
    writeFile.close()

#  Get categorization from verb+compl pattern
#  Output = broad_concepts_and_instances_age.csv
def get_concept_verbs(instances, readfile, write_concept_file):
    count = 0
    
    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_concept_file, 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                utt = row[8].split()

                for instance in instances:
                     if instance in utt:
                        for verb in verbs:
                            if verb in row[8]:
                                regex = r'\b' + verb + r'\s([a-z]*\s){0,1}' + instance + r'\b'
                                if re.search(regex, row[8]) is not None:
                                    temp = []
                                    temp.append(conceptsDict[verb])
                                    temp.append(" ")
                                    temp.append((row[8], row[12]))
                                    temp.append([0, row[8]])
                                    temp.append(instance)
                                    temp.append(row[14])
                                    temp.append(row[16])
                                    temp.append(row[25])
                
                                    writer.writerow(temp)
                    
    f.close()
    writeFile.close()
    
def explicit_categorization(instances, readfile, writefile):
    count = 0
    rowNum = 0
    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(writefile, 'w') as writeFile:
            writer = csv.writer(writeFile)
            
            for row in reader:
                rowNum += 1
                utt = row[8].split()
                for concept in concepts:
                    regex = r' ([a-z]|\s)* be a([a-z]|\s)*' + concept
                    regex2 = r' ([a-z]|\s)* kind of ' + concept
                    if re.search(regex, row[8]) or re.search(regex2, row[8])is not None:
                        count += 1
                        temp = []
                        temp.append(concept)
                        temp.append(row[8])
                        temp.append(row[6])
                
                        writer.writerow(temp)
                    
    print(str(count) + " instances found.")

    
def main():
    instances = get_instances()
    
    if len(sys.argv) == 1:
        print("Please include required ages")
        sys.exit(0)
        
    for age in sys.argv[1:]:
        #Add in error for unavailable age?
        readfile = files[0].replace("age", str(age))
        write_txt_file = files[1].replace("age", str(age))
        write_verb_file = files[2].replace("age", str(age))
        write_cooccurrence_file = files[3].replace("age", str(age))
        write_explicit_categorization_file = files[4].replace("age", str(age))
        
        print("Getting explicit categorization for age < " + age + "...")
        explicit_categorization(instances, readfile, write_explicit_categorization_file)
        
        print("Getting text for age < " + age + "...")
        utterances_to_txt(readfile, write_txt_file)
        
        print("Getting verb+compl for age < " + age + "...")
        get_concept_verbs(instances, readfile, write_verb_file)
        
        print("Getting concept co-occurrences for age < " + age + "...")
        get_concept_cooccurrence(instances, readfile, write_cooccurrence_file)
        
        print("Done with age < " + age)


if __name__ == '__main__':
    main()
    

