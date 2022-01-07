
import praw
import pdb
import re
import os
import sys
import time

from configparser import ConfigParser

config = ConfigParser()
config.read('password.ini')

botPass = config.get('s1', 'pass')
devPass = config.get('s1', 'devPass')

numberOfTopPostsToCheck = 100
phrasesToRecognize = {"absolute", "absolutes", "absolutely", "absolution"}
subredditToSearchList = {'all', 'StarWars', 'starwarsmemes', 'SequelMemes', 'StarWarsBattlefront',
                         'BookofBobaFett', 'TheMandalorianTV', 'TheBadBatch', 'StarWarsKenobi',
                         'StarWarsLando', 'lego', 'AbsoluteUnits', 'PrequelMemes', 'StarWarsMagic',
                         'BinghamtonUniversity', 'whowouldwin', 'Cornell', 'funkopop', 'CrappyDesign'}

reddit = praw.Reddit(
    client_id="tRclfC6esR4Mz3-5B4Axjg",
    client_secret=devPass,
    password=botPass,
    user_agent="testscript by u/SithLord_Bot",
    username="SithLord_Bot",
)

print("Current bot = ", reddit.user.me())

for subredditToSearch in subredditToSearchList:

    print("Searching Subreddit: ", subredditToSearch)
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

    # Handle errors for Absolute response

                    except Exception as e:
                        errorMessage = e
                        print(e)

                        # Handle too many comments
                        if(errorMessage.contains("You're doing that too much. Try again in")):
                            currentWord = ""
                            minutesToWait = minutesToWait = int(
                                re.search(r'\d+', str).group())
                            secondsToWait = minutesToWait * 60
                            print("Sleeping for ", minutesToWait,
                                  " minutes, aka ", secondsToWait, " seconds.")
                            time.sleep(secondsToWait)

                try:
                    if re.search("father", currentComment.body, re.IGNORECASE):
                        if submission.id not in posts_replied_to:
                            fatherReply = str(
                                currentComment.author) + ", I am your father."
                            currentComment.reply(fatherReply
                                                 )

                            posts_replied_to.append(submission.id)
                            fatherReplies = fatherReplies + 1
                            break

    # Handle error for father response

                except Exception as e:
                    errorMessage = e
                    print(errorMessage)

                    if(re.search("You're doing that too much. Try again in", errorMessage, re.IGNORECASE)):
                        currentWord = ""
                        minutesToWait = minutesToWait = int(
                            re.search(r'\d+', str).group())
                        secondsToWait = minutesToWait * 60
                        print("Sleeping for ", minutesToWait,
                              " minutes, aka ", secondsToWait, " seconds.")
                        time.sleep(secondsToWait)

    # Write updated list to file
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

    print("Absolute Sith Comments: ", absoluteReplies)
    print("Father Comments: ", fatherReplies)
