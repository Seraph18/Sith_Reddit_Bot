
import praw
import pdb
import re
import os
import sys

from configparser import ConfigParser

config = ConfigParser()
config.read('password.ini')

botPass = config.get('s1', 'pass')
devPass = config.get('s1', 'devPass')

numberOfTopPostsToCheck = 200
phrasesToRecognize = {"absolute", "absolutes", "absolutely", "absolution"}
subredditToSearch = 'pics'
# 'StarWars'
# 'AbsoluteUnits'
# 'PrequelMemes'

reddit = praw.Reddit(
    client_id="tRclfC6esR4Mz3-5B4Axjg",
    client_secret=devPass,
    password=botPass,
    user_agent="testscript by u/SithLord_Bot",
    username="SithLord_Bot",
)

print(reddit.user.me())

subreddit = reddit.subreddit(subredditToSearch)

# Create a list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# Or load the list of posts we have replied to
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


numberPost = 0
absoluteReplies = 0
fatherReplies = 0
# searchResultssubreddit.search()

for submission in subreddit.hot(limit=numberOfTopPostsToCheck):
    # print(submission.title)
    # Make sure you didn't already reply to this post

    numberPost = numberPost + 1
    print("Checked ", numberPost)
    #print("Post Name: ", submission.title)

    if submission.id not in posts_replied_to:
        # Search through comments for keywords

        for currentComment in submission.comments:
            # Not case sensitive

            for keyword in phrasesToRecognize:
                try:
                    if submission.id not in posts_replied_to:

                        if re.search(keyword, currentComment.body, re.IGNORECASE):

                            # Reply

                            currentComment.reply(
                                "Only a Sith deals in absolutes.")

                            print(numberPost, ": Bot replying to : ",
                                  submission.title)

                            # Store id in list
                            posts_replied_to.append(submission.id)
                            absoluteReplies = absoluteReplies + 1
                            break

                    else:
                       # print("I already commented on this post.")
                        break

                except Exception as e:
                    print(e)

            try:
                if re.search("father", currentComment.body, re.IGNORECASE):
                    if submission.id not in posts_replied_to:
                        fatherReply = str(currentComment.author) + ", I am your father."
                        currentComment.reply( fatherReply
                            )

                        posts_replied_to.append(submission.id)
                        fatherReplies = fatherReplies + 1
                        break

            except Exception as e:
                print(e)

# Write updated list to file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")

print("Absolute Sith Comments: ", absoluteReplies)
print("Father Comments: ", fatherReplies)
