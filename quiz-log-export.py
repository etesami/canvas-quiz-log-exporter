# This script is used to query all quizzes submission from Canvas
# and save the log of each user attempt to take the quiz.
# Based on the behaviour of ithe user, someone may take advantage of
# the logs to ensure no one cheated.
#
# Author: Ehsan Etesami <eh.etesami[at]gmail.com>
#

import requests
import sys

def get_event_text(event_title):
   if event_title == "page_blurred":
      return "Stopped viewing the Canvas quiz-taking page..."
   elif event_title == "page_focused":
      return "Resumed"
   else:
      return event_title

if len(sys.argv) != 3:
   print("USAGE: python3 %s <course_id> <quiz_id>" % __file__)
   sys.exit(1)

COURSE_ID = sys.argv[1]
QUIZ_ID = sys.argv[2]

# Initialize the TOKEN variable by your token
TOKEN = ""
# URL = "https://q.utoronto.ca"
URL = ""

if TOKEN == "":
   print('Please ensure you have initialized the TOKEN variable by your token.')
   print('The token is issued using Canvas using web interface.')
   print()
   sys.exit(1)

if URL == "":
   print('Please ensure you have initialized the URL variable by the canvas URL.')
   print()
   sys.exit(1)

req = requests.get( URL+'/api/v1/courses/' + COURSE_ID + '/quizzes/' + \
                    QUIZ_ID + '/submissions?per_page=150' , \
                    headers = {'Authorization': 'Bearer ' + TOKEN})

if(req.status_code != 200):
   print("GET status code: " +req.status_code)
   sys.exit(1)

req_json = req.json()
submissions = []

for submission in req_json["quiz_submissions"]:
   user_id = submission.get('user_id')
   sub_id = submission.get('id')
   entry = [user_id, sub_id]
   submissions.append(entry)

print("Retrive "+str(len(submissions))+" submissions")

if len(submissions) == 0:
   print("Oops! No submission retrived!")
   sys.exit(1)

possible_cheating = []
for entry in submissions:
   user_id = str(entry[0])
   sub_id = str(entry[1])
   req_events = requests.get( URL+'/api/v1/courses/' + COURSE_ID + '/quizzes/' + \
                             QUIZ_ID + '/submissions/' + sub_id + '/events?per_page=200' , \
                             headers = {'Authorization': 'Bearer ' + TOKEN })

   if req_events.status_code != 200 :
      print("Could not retrived events for this submission: "+str(sub_id))
      continue

   req_events_json = req_events.json()
   f = open( user_id + "-events", 'w')
   f.write("Logs for user id: " + user_id + "\n")
   f.write("---------------------------------\n")

   user_has_cheated = False
   events_log = []
   for ev in req_events_json['quiz_submission_events']:
      events_log.append(ev.get('created_at')+": "+ get_event_text(ev.get("event_type")))
      if not user_has_cheated and "Stopped" in get_event_text(ev.get('event_type')):
         print('------> Possible cheating by user: '+str(user_id))
         possible_cheating.append([user_id, sub_id])
         user_has_cheated = True

   for ee in events_log:
      f.write(ee+"\n")
   f.close()

print('---------------------------------------------------')
print("Finish checking all submission for the Quiz/Exam id: " + QUIZ_ID)
if len(possible_cheating) > 0:
   print("Number of possible cheating for the ECE361 final: " + str(len(possible_cheating)))
   f = open('possible_cheating.html', 'w')
   f.write('<html><h1>List of users who possibly cheated:</h1>\n  <ul>\n')
   for cheat in possible_cheating:
      f.write('<li><a href="https://q.utoronto.ca/courses/' + COURSE_ID + '/quizzes/' + \
               QUIZ_ID + '/submissions/' + str(cheat[1]) + '/log" target="_blank">Possible cheating by user: '+ str(cheat[0]) +"</a></li>\n")
   f.write("</ul></html>")
   f.close()
else:
   print("No cheating was detected.")


