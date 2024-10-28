import csv
from random import sample
import re

dictReader = csv.DictReader(open("BI2331 Physiology News & Views Assessment Sign-up Form 2024 (Responses) - Form Responses 1.csv"))

all_responses = list(dictReader)
best_pairings = {}
lowest_leftover = len(all_responses)

topics = dictReader.fieldnames
topics.remove('Timestamp')
topics.remove('Student Number')
topics.remove('I have checked my EIGHT- (or SEVEN-) digit student number and it is correct')

response_students = []

for response in all_responses:
    response_students.append(response['Student Number'])

for i in range(1000000):

    if i%10000 == 0:
        print(i)
        print(lowest_leftover)

    if lowest_leftover == 0:
        break

    responses = all_responses.copy()

    pairings = {}

    for topic in topics:
        pairings[topic] = []

    # Last number should be one more than the number of preferences
    for preference in range(1,8):
        # print(preference)
        for topic in topics:
            topic_students = []

            for response in responses:
                if response[topic] == str(preference):
                    topic_students.append(response['Student Number'])

    # Number should be the number of places available in each topic
            places_remaining = 7-len(pairings[topic])
            topic_students = sample(topic_students, min(places_remaining, len(topic_students)))

            for student in topic_students:
                # Look up their response in the responses list
                student_response = [response for response in responses if response['Student Number']==student][0]

                # Remove their response from the responses list
                responses.remove(student_response)

            pairings[topic].extend(topic_students)

    # print(pairings)
    # print(len(responses))
    if len(responses) < lowest_leftover:
        best_pairings=pairings
        lowest_leftover=len(responses)

# print(best_pairings)

final_allocations = {}

for topic in best_pairings:
    for student in best_pairings[topic]:
        final_allocations[student] = topic

print(final_allocations)
print(lowest_leftover)

with open('student_numbers.csv', 'r') as f:
    reader = csv.reader(f)
    # next(reader)

    with open('student_pairings.csv', 'w') as g:
        writer = csv.writer(g)
        header = next(reader)
        writer.writerow([*header, 'Topic Number', 'Topic Title'])

        for row in reader:
            student_number = row[0][:-2]
            possible_student_number_entries = [student_number, f"c{student_number}", f"C{student_number}", f"{student_number}/1", f"c{student_number}/1", f"C{student_number}/1"]

            topic = ''

            for possible_number in possible_student_number_entries:
                if possible_number in final_allocations.keys():
                    topic = final_allocations[possible_number]
                    del final_allocations[possible_number]
                    break
                elif possible_number in response_students:
                    topic = "*"
                    break

            if topic not in ['', '*']:
                cleaned_topic = re.findall(r'\[.*?\]', topic)[0].replace('[', '').replace(']', '')
                split_topic = cleaned_topic.split(": ")
                topic_number = split_topic[0].replace('Topic ', '')
                if len(split_topic) > 1:
                    topic_title = split_topic[1]
                else:
                    print(cleaned_topic)
                    topic_title = '?'
            elif topic == '*':
                topic_number = '*'
                topic_title = '***'
            else:
                topic_number=''
                topic_title=''
            writer.writerow([*row, topic_number, topic_title])

with open('unnamed_allocations.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Student Number', 'Topic Number', 'Topic Title'])

    for student, topic in final_allocations.items():
        cleaned_topic = re.findall(r'\[.*?\]', topic)[0].replace('[', '').replace(']', '')
        split_topic = cleaned_topic.split(": ")
        topic_number = split_topic[0].replace('Topic ', '')
        if len(split_topic) > 1:
            topic_title = split_topic[1]
        else:
            print(student, cleaned_topic)
            topic_title = '?'
        writer.writerow([student, topic_number, topic_title])
