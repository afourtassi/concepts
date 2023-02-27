import csv
import re

conceptsDict = {"animal": "animal", "eat": "food", "food": "food", "wear": "clothes", "clothing": "clothes",
                "clothes": "clothes", "play": "toy", "toy": "toy", "play with": "toy", "furniture": "furniture",
                "use": "furniture", "ride": "vehicle", "vehicle": "vehicle", "ride in": "vehicle",
                "ride on": "vehicle"}

concepts = ["animal", "toy", "vehicle", "clothes", "furniture", "food"]

verbs = ["ride on", "ride in", "ride", "play", "play with", "use", "eat", "wear"]

def get_instances():
    temp = []

    with open('wb_nouns_edited.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            #data[row[1]] = [x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"]

            if row[1] in concepts:
                temp.append([x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"])

        instances = [item for sublist in temp for item in sublist]
        return instances

#row[8] for 3, 6 and row[9] for 4,5
def utterances_to_txt():
    with open('all_utterances_3.csv', newline='') as f:
        reader = csv.reader(f)

        with open('all_utterances_3.txt', 'w') as writeFile:

            next(reader)

            for row in reader:
                utt = row[8]
                for word in conceptsDict.keys():
                    if word in utt:
                        utt = re.sub(word, "", utt)
                writeFile.write(utt + " ")


def get_concepts():
    count = 0
    #animal_furniture = data["animal"] + data["furniture"]
    #other = data["food"] + data["toy"] + data["clothes"]

    with open('all_utterances_3.csv', newline='') as f:
        reader = csv.reader(f)

        with open('concepts_and_instances_3.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                utt = row[8].split()

                if count % 10000 == 0:
                    print(count)
                count += 1

                #Get co-occurrence of concepts and instances
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

                 #Get categorization from verb+compl pattern
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

instances = get_instances()
utterances_to_txt()
get_concepts()