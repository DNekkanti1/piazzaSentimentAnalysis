from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
import numpy as np
import pandas as pd
from datetime import datetime


stringo = """To our disappointment, we have discovered a number of instances of academic dishonesty so far this semester (around 50). Here are some examples of cheating that are represented in the instances that we have found. Keep in mind that we have concrete evidence for specific instances of each of the examples below:



- Evidence that students have copied HW solutions from sources available online

- Evidence that students have copied each other's HW solutions (this includes the ones who copied and the ones who gave out solutions)

- Evidence that project teams have colluded while making inputs and solvers.

- Evidence that students have copied from their neighbors during an exam.

- Evidence of students who brought in extra physical materials during an exam (like small notebooks and extra sheets of paper), which they referred to.

- Evidence of students who referred to their mobile devices during an exam.



However, we understand that decisions about cheating are usually made in high-pressure situations (like the day of the deadline), when students are not always thinking rationally. So, we'd like to give you all the chance to self-report instances of academic dishonesty, in return for more leniency from us when deciding what to do with your situation. This includes the students who we already have on our list. We haven't sent out emails to any suspects yet, so it is in your best interest to report yourself. If someone on our list does not report themselves, the consequences will be especially severe.



Please fill out this form if you would like to confess to any instances of academic dishonesty.



You can see what is classified as academic dishonesty on the course policies page of our website. If you think you may have been academically dishonest, but are not sure, please describe the situation to us in the form, and let us decide. You can use the form to report cheating on any aspect of the course (e.g. homework, project, exams). If you have multiple instances to report, please submit the form multiple times.



If you have cheated at some point in the semester before this Piazza post, you have until midnight on Sunday (4/15) to report these instances. You must submit it by then in order to receive leniency. Going forward, you must report an instance of cheating within 48 hours of the incident in order to receive leniency in your decision.



Keep in mind that if we catch any more instances of cheating this semester, and the perpetrators do not report themselves within 48 hours, we will pursue the highest punishment possible.





___________________________________________________________________





Please take a moment to understand the effect cheaters have on this class. Every time someone cheats, that directly corresponds to extra time that your course staff has to spend dealing with the consequences of that cheating. We have to scour through your HW, code, and exams to find these instances of cheating. We have to spend hours looking through each of these submissions individually in order to determine if it really is cheating, or just incidental similarity. And then we have to spend hours deciding appropriate punishments, meeting with suspected cheaters, sending names and evidence to the Center for Student Conduct, etc. The effects of each and every cheater is felt across the teaching stack: by readers, TAs, and professors.



Instead of spending this time improving our teaching materials and serving students better, we instead have to spend that time mindlessly poring over cheating cases in order to make sure that the marks we award are fair. In light of this, this policy of accepting cheating confessions is a privilege and a courtesy we are providing to you. If you have cheated, the least you can do is to be smart and use this escape route we are giving you. You will be saving yourself a harsh punishment, and saving us time that we can instead use to serve students better."""

print(stringo)
def containos(s, word_list):
    rtn = {}
    for keyword in word_list:
        rtn[keyword] = 0
    for w in s.split():
        if w in word_list:
            rtn[w] += 1
    for key,value in sorted(rtn.items(), key=lambda x:-x[1]):
        print("{}: {}".format(key, value))
    return rtn

def post_range(course, post_ID, year, month, day):
    assert len(year)==4
    assert len(month)==2
    assert len(day)==2
    try:
        range_beginning = datetime.strptime("{} {} {}".format(year,month,day), '%Y %m %d')
        print(range_beginning)
    except:
        print("enter a proper date!!!")
    latest_date = datetime.MAXYEAR
    while(range_beginning<latest_date):
        try:
            curr_post = course.get_post(post_ID)
            latest_date_string = curr_post['change_log']['when']
            latest_date = datetime.strptime(latest_date_string,"%Y-%m-%dT%H:%M:%S")
            process(curr_post)
            post_ID -= 1
        except:
            print("something is fucked up")
    return

def process(post):
    print("processed")
    return

    # while date <:
    #     course.get_post(post_ID)

print(post_range(1,1,"2018","13","02"))


d = containos(stringo, ["butts", "moment", "sing", "teaching"])
d
