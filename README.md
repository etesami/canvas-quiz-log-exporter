# Canvas Quiz Log Exporter
Export logs of quizzes in Canvas

This script is used to query all quizzes submission from Canvas and save the log of each user attempt to take the quiz. Based on the behaviour of ithe user, someone may take advantage of the logs to ensure no one cheated.

## Getting Started
You will need to initialize the **URL** and **TOKEN** the _URL_ variables in the script with your Canvas _URL_ and the _Token_ taken from the Canvas system. Then run the script by giving course id and quiz id:
```
python quiz-log-export.py <course-id> <quiz-id>
```

The script iterates through all submission of the given quiz in the given course, and save all submission logs into the current folder. The script also looks for those who have at least one behaviour of **Stopped viewing the Canvas page** and save their user id and submission id into a file called `possible-cheating.html` as a list.