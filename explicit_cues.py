import csv
import re

'''
TODO:
Add command line interface
add functions to do different kinds of concepts/instances
'''

conceptsDict = {"animal": "animal", "eat": "food", "food": "food", "wear": "clothes", "clothing": "clothes",
                "clothes": "clothes", "play": "toy", "toy": "toy", "play with": "toy", "furniture": "furniture",
                "use": "furniture", "ride": "vehicle", "vehicle": "vehicle", "ride in": "vehicle",
                "ride on": "vehicle"}

broad_concepts = ["animal", "artifact"]
broad_concept_categories = ["toy", "vehicle", "furniture", "animal"]
concepts = ["animal", "toy", "vehicle", "clothes", "furniture", "food"]

verbs = ["ride on", "ride in", "ride", "play", "play with", "use", "eat", "wear"]


def get_instances():
    temp = []

    with open('pydata/wb_nouns_edited.csv', newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            # data[row[1]] = [x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"]

            if row[1] in broad_concept_categories:
                temp.append([x for x in row[2:] if x != "" and x != "animal" and x != "toy" and x != "food"])

        instances = [item for sublist in temp for item in sublist]
        return instances


# row[8] for 3, 6 and row[9] for 4,5
def utterances_to_txt():
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


def get_concepts():
    count = 0
    # animal_furniture = data["animal"] + data["furniture"]
    # other = data["food"] + data["toy"] + data["clothes"]

    with open(readfile, newline='') as f:
        reader = csv.reader(f)

        with open(write_concept_file, 'w') as writeFile:
            writer = csv.writer(writeFile)

            for row in reader:
                utt = row[8].split()

                if count % 10000 == 0:
                    print(count)
                count += 1

                # Get co-occurrence of concepts and instances
                for instance in instances:
                    if instance in utt:
                        for concept in broad_concepts:
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

                # #Get categorization from verb+compl pattern
                # for instance in instances:
                #     if instance in utt:
                #         for verb in verbs:
                #             if verb in row[8]:
                #                 regex = verb + r' ([a-z]* ){0,1}' + instance
                #                 if re.search(regex, row[8]) is not None:
                #                     #print("true")
                #                     temp = []
                #                     temp.append(conceptsDict[verb])
                #                     temp.append(" ")
                #                     temp.append((row[8], row[12]))
                #                     temp.append([0, row[8]])
                #                     temp.append(instance)
                #                     temp.append(row[14])
                #                     temp.append(row[16])
                #                     temp.append(row[25])
                #
                #                     writer.writerow(temp)


readfile = "pydata/adult_utterances_3.csv"
write_txt_file = "rdata/adult_utterances_3.txt"
write_concept_file = "rdata/broad_concepts_and_instances_3.csv"

instances = get_instances()
utterances_to_txt()
get_concepts()
