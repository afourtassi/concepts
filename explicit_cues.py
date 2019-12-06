'''
Kyra Wilson
12/5/19

How to run: explicit_cues.py followed by ages (<3, <4, <5, or <6) you want to get data for

Ex: "explicit_cues.py 3 4" will get co-occurrences for all utterances for children under 3 and all utterances for children under 4

TODO:
add in code to get broad concepts (if necessary)

'''

import csv
import re
import sys

conceptsDict = {"animal": "animal", "eat": "food", "food": "food", "wear": "clothes", "clothing": "clothes",
                "clothes": "clothes", "play": "toy", "toy": "toy", "play with": "toy", "furniture": "furniture",
                "use": "furniture", "ride": "vehicle", "vehicle": "vehicle", "ride in": "vehicle",
                "ride on": "vehicle"}

broad_concepts = ["animal", "artifact"]
broad_concept_categories = ["toy", "vehicle", "furniture", "animal"]
concepts = ["animal", "toy", "vehicle", "clothes", "furniture", "food"]

verbs = ["ride on", "ride in", "ride", "play", "play with", "use", "eat", "wear"]

fileDict = {"3": ["pydata/adult_utterances_3.csv", "rdata/adult_utterances_3.txt", "rdata/broad_concepts_and_instances_3.csv"], "4": ["pydata/adult_utterances_4.csv", "rdata/adult_utterances_4.txt", "rdata/broad_concepts_and_instances_4.csv"], "5": ["pydata/adult_utterances_5.csv", "rdata/adult_utterances_5.txt", "rdata/broad_concepts_and_instances_5.csv"], "6": ["pydata/adult_utterances_6.csv", "rdata/adult_utterances_6.txt", "rdata/broad_concepts_and_instances_6.csv"] }


def get_instances():
    temp = []

    with open('pydata/wb_nouns_edited.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            # data[row[1]] = [x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"]

            if row[1] in broad_concept_categories:
                temp.append([x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"])

        instances = [item for sublist in temp for item in sublist]
        
        f.close()
        return instances


def utterances_to_txt(readfile, write_txt_file):
    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_txt_file, 'w') as writeFile:

            next(reader)

            for row in reader:
                utt = row[8]
                for word in broad_concept_categories:
                    if word in utt:
                        utt = re.sub(word, "", utt)
                writeFile.write(utt + " ")
                
    f.close()
    writeFile.close()


def get_concepts(instances, readfile, write_concept_file):
    count = 0
    # animal_furniture = data["animal"] + data["furniture"]
    # other = data["food"] + data["toy"] + data["clothes"]

    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_concept_file, 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                utt = row[8].split()

#                if count % 10000 == 0:
#                    print(count)
#                count += 1

#                Get co-occurrence of concepts and instances
#                for instance in instances:
#                    if instance in utt:
#                        for concept in broad_concepts:
#                            if concept in utt:
#                                temp = []
#                                temp.append(concept)
#                                temp.append(" ")
#                                temp.append((row[8], row[12]))
#                                temp.append([0, row[8]])
#                                temp.append(instance)
#                                temp.append(row[14])
#                                temp.append(row[16])
#                                temp.append(row[25])
#
#                                writer.writerow(temp)

#               Get categorization from verb+compl pattern
                for instance in instances:
                     if instance in utt:
                         for verb in verbs:
                             if verb in row[8]:
                                 regex = verb + r' ([a-z]* ){0,1}' + instance
                                 if re.search(regex, row[8]) is not None:
                                     #print("true")
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


def main():
    instances = get_instances()
    
    if len(sys.argv) == 1:
        print("Please include required ages")
        sys.exit(0)
    for age in sys.argv[1:]:
        readfile = fileDict[age][0]
        write_txt_file = fileDict[age][1]
        write_concept_file = fileDict[age][2]
        
        print("Getting text for age < " + age + "...")
        utterances_to_txt(readfile, write_txt_file)
        
        print("Getting co-occurrences for age < " + age + "...")
        get_concepts(instances, readfile, write_concept_file)
        
        print("Done with age < " + age)


if __name__ == '__main__':
    main()

