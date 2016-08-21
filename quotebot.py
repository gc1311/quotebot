import os
import time
from slackclient import SlackClient
import time
import logging
import requests
import json
import pypwned
import random


BOT_ID = ('[bot ID]')

AT_BOT = "<@" +BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient('[slack API]')

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Invalid command."
   
    
    if command.startswith('commands'):
	response =" "
	response += header()
	response +="""displaying random quotes.
				
				Comands:
			-------------------------------------------------------------
				sun - Sun Tzo, the Art of War
				seuss - Dr Seuss
				einstein - A Einstein
				random - Random quote from the above and some others
			-------------------------------------------------------------

			*************************************************************
			 hibp - randomly displays one of the first 100 HIBP records
			*************************************************************

				"""
	response +=" "


    if command.startswith('hibp'):
	response = random_breaches()
    if command.startswith('random'):
	response = random_test()
    if command.startswith('sun'):
	response = sun_tzu()
    if command.startswith('seuss'):
	response = seuss()
    if command.startswith('c'):
	responses = hill()
    if command.startswith('einstein'):
	response = einstein()
    if command.startswith('header'):
	response = header()

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def random_breaches():
	json_processed = json_parser(pypwned.getAllBreaches())
	return json_processed

def description_parser(descr):
    if '<' or '>' in descr:
        descr = re.sub('<.*?>', '', descr)

    for tld in pc_config.tld_strip_list:    
        if tld in descr:
            descr = descr.replace(tld,'').strip()

    if '.' in descr:
        descr = descr.replace('.','.\n').strip()
    if '&quot;' in descr:
        descr = descr.replace('&quot;','').strip()
    if "'" in descr:
        descr = descr.replace("'","").strip()
    if '&mdash;' in descr:
        descr = descr.replace('&mdash;','')
    descr = ''.join([x for x in descr if ord(x) < 128])
    return descr.strip()

def output_formatter(title,org,domain,count,data,sys_date,date,verif,descrip):
    #descrip_dedent = textwrap.dedent(descrip).strip()
    #descrip = textwrap.fill(descrip_dedent, width=50)

    breach_template = """
===========================================================
-----------------------------------------------------------
Breach Title       | {0:10}
Organization       | {1:10}
Domain             | {2:10}
Date               | {3:10}
System Storage Date| {4:10}
Accounts Breached  | {5:1}
Breach Verified    | {6:1}
-----------------------------------------------------------
-----------------------------------------------------------
< Breach Details >    
-----------------------------------------------------------
{7:1}
-----------------------------------------------------------
-----------------------------------------------------------
< Data Types Compromised In Breach >
-----------------------------------------------------------
{8:1}
-----------------------------------------------------------
===========================================================
    """.format(title,org,domain,date,sys_date,count,verif,descrip, '| ' + '\n| '.join(data).upper())
    return breach_template

def json_parser(query):
		x = random.randint(0,100)
		title = query[x]['Title']
		organization = query[x]['Name']
		domain = query[x]['Domain']
		breach_date = query[x]['BreachDate']
		pwncount = query[x]['PwnCount']
		verified = query[x]['IsVerified']
		added_date = query[x]['AddedDate']
	    	affected_data_types = query[x]['DataClasses']
		description = query[x]['Description']
	    	stdout_report = output_formatter(title, organization, domain, pwncount, affected_data_types, added_date, breach_date, verified, description)
		
		 	
		return stdout_report



def random_test():
	answers = ["Two things are infinite the universe and human stupidity and I'm not sure about the universe.", "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.", "I am enough of an artist to draw freely upon my imagination. Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.", "The important thing is not to stop questioning. Curiosity has its own reason for existing.", "The significant problems we have cannot be solved at the same level of thinking with which we created them.", "Anyone who has never made a mistake has never tried anything new.", "Try not to become a man of success, but rather try to become a man of value.", "Great spirits have always encountered violent opposition from mediocre minds.", "Everything should be made as simple as possible, but not simpler.", "The most beautiful thing we can experience is the mysterious. It is the source of all true art and science.", "Success consists of going from failure to failure without loss of enthusiasm.", "If you're going through hell, keep going.", "You have enemies? Good. That means you've stood up for something, sometime in your life.", "Courage is what it takes to stand up and speak. Courage is also what it takes to sit down and listen", "A pessimist sees the difficulty in every opportunity; an optimist sees the opportunity in every difficulty.", "To improve is to change; to be perfect is to change often.", "Success is not final, failure is not fatal: it is the courage to continue that counts.", "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing ever happened.", "The farther backward you can look, the farther forward you are likely to see.", "The price of greatness is responsibility.", "We shall not fail or falter. We shall not weaken or tire. Neither the sudden shock of battle nor the long-drawn trials of vigilance and exertion will wear us down. Give us the tools and we will finish the job.", "The greatest lesson in life is to know that even fools are right sometimes.", "Appear weak when you are strong, and strong when you are weak.","Appear weak when you are strong, and strong when you are weak.", "Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.", "If you know the enemy and know yourself, you need not fear the result of a hundred battles. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle.","Supreme excellence consists of breaking the enemy's resistance without fighting.","Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win", "All warfare is based on deception. Hence, when we are able to attack, we must seem unable; when using our forces, we must appear inactive; when we are near, we must make the enemy believe we are far away; when far away, we must make him believe we are near.", "If your enemy is secure at all points, be prepared for him. If he is in superior strength, evade him. If your opponent is temperamental, seek to irritate him. Pretend to be weak, that he may grow arrogant. If he is taking his ease, give him no rest. If his forces are united, separate them. If sovereign and subject are in accord, put division between them. Attack him where he is unprepared, appear where you are not expected .", "In the midst of chaos, there is also opportunity", "Engage people with what they expect; it is what they are able to discern and confirms their projections. It settles them into predictable patterns of response, occupying their minds while you wait for the extraordinary moment that which they cannot anticipate.", "The greatest victory is that which requires no battle.", "There is no instance of a nation benefitting from prolonged warfare.", "The art of war is of vital importance to the State. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected.", "Don't cry because it's over, smile because it happened.", "You know you're in love when you can't fall asleep because reality is finally better than your dreams.", "I like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.", "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You're on your own. And you know what you know. And YOU are the one who'll decide where to go...", "Sometimes the questions are complicated and the answers are simple.", "Today you are You, that is truer than true. There is no one alive who is Youer than You.", "The more that you read, the more things you will know. The more that you learn, the more places you'll go.", "A person's a person, no matter how small.", "Unless someone like you cares a whole awful lot, Nothing is going to get better. It's not.", "Being crazy isn't enough.", "Fantasy is a necessary ingredient in living, it's a way of looking at life through the wrong end of a telescope.", "Being crazy isn't enough.", "Fantasy is a necessary ingredient in living, it's a way of looking at life through the wrong end of a telescope." , "Why fit in when you were born to stand out?", "I have heard there are troubles of more than one kind. Some come from ahead and some come from behind. But I've bought a big bat. I'm all ready you see. Now my troubles are going to have troubles with me!", "How did it get so late so soon?", "If things start happening, don't worry, don't stew, just go right along and you'll start happening too.", "Today was good. Today was fun. Tomorrow is another one.", "From there to here, from here to there, funny things are everywhere", "All alone! Whether you like it or not, alone is something you'll be quite a lot!", "Then the Grinch thought of something he hadn't before! What if Christmas, he thought, doesn't come from a store. What if Christmas...perhaps...means a little bit more", "I meant what I said and I said what I meant. An elephant's faithful one hundred percent!", "Adults are just obsolete children and the hell with them.", "Remember me and smile, for it's better to forget than to remember me and cry.", "Only you can control your future.", "I'm afraid that sometimes you'll play lonely games too. Games you can't win cause you'll play against you."]
	return random.choice(answers)

def einstein():
	answers = ["Two things are infinite the universe and human stupidity and I'm not sure about the universe.", "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.", "I am enough of an artist to draw freely upon my imagination. Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world.", "The important thing is not to stop questioning. Curiosity has its own reason for existing.", "The significant problems we have cannot be solved at the same level of thinking with which we created them.", "Anyone who has never made a mistake has never tried anything new.", "Try not to become a man of success, but rather try to become a man of value.", "Great spirits have always encountered violent opposition from mediocre minds.", "Everything should be made as simple as possible, but not simpler.", "The most beautiful thing we can experience is the mysterious. It is the source of all true art and science."]
	return random.choice(answers)

def hill():
	answers = ["Success consists of going from failure to failure without loss of enthusiasm.", "If you're going through hell, keep going.", "You have enemies? Good. That means you've stood up for something, sometime in your life.", "Courage is what it takes to stand up and speak. Courage is also what it takes to sit down and listen", "A pessimist sees the difficulty in every opportunity; an optimist sees the opportunity in every difficulty.", "To improve is to change; to be perfect is to change often.", "Success is not final, failure is not fatal: it is the courage to continue that counts.", "Men occasionally stumble over the truth, but most of them pick themselves up and hurry off as if nothing ever happened.", "The farther backward you can look, the farther forward you are likely to see.", "The price of greatness is responsibility.", "We shall not fail or falter. We shall not weaken or tire. Neither the sudden shock of battle nor the long-drawn trials of vigilance and exertion will wear us down. Give us the tools and we will finish the job.", "The greatest lesson in life is to know that even fools are right sometimes."]
	return random.choice(answers)

def sun_tzu():
	answers = ["Appear weak when you are strong, and strong when you are weak.","Appear weak when you are strong, and strong when you are weak.", "Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.", "If you know the enemy and know yourself, you need not fear the result of a hundred battles. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle.","Supreme excellence consists of breaking the enemy's resistance without fighting.","Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win", "All warfare is based on deception. Hence, when we are able to attack, we must seem unable; when using our forces, we must appear inactive; when we are near, we must make the enemy believe we are far away; when far away, we must make him believe we are near.", "If your enemy is secure at all points, be prepared for him. If he is in superior strength, evade him. If your opponent is temperamental, seek to irritate him. Pretend to be weak, that he may grow arrogant. If he is taking his ease, give him no rest. If his forces are united, separate them. If sovereign and subject are in accord, put division between them. Attack him where he is unprepared, appear where you are not expected .", "In the midst of chaos, there is also opportunity", "Engage people with what they expect; it is what they are able to discern and confirms their projections. It settles them into predictable patterns of response, occupying their minds while you wait for the extraordinary moment that which they cannot anticipate.", "The greatest victory is that which requires no battle.", "There is no instance of a nation benefitting from prolonged warfare.", "The art of war is of vital importance to the State. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected.", "Move swift as the Wind and closely-formed as the Wood. Attack like the Fire and be still as the Mountain.", "Treat your men as you would your own beloved sons. And they will follow you into the deepest valley.", "When the enemy is relaxed, make them toil. When full, starve them. When settled, make them move.", "When you surround an army, leave an outlet free. Do not press a desperate foe too hard.", "So in war, the way is to avoid what is strong, and strike at what is weak.", "To win one hundred victories in one hundred battles is not the acme of skill. To subdue the enemy without fighting is the acme of skill", "who wishes to fight must first count the cost", "who wishes to fight must first count the cost", "What the ancients called a clever fighter is one who not only wins, but excels in winning with ease.", "Be extremely subtle even to the point of formlessness. Be extremely mysterious even to the point of soundlessness. Thereby you can be the director of the opponent's fate.", "He who is prudent and lies in wait for an enemy who is not, will be victorious.", "Thus the expert in battle moves the enemy, and is not moved by him."]
	return random.choice(answers)	

def seuss():
	answers = ["Don't cry because it's over, smile because it happened.", "You know you're in love when you can't fall asleep because reality is finally better than your dreams.", "I like nonsense, it wakes up the brain cells. Fantasy is a necessary ingredient in living.", "You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose. You're on your own. And you know what you know. And YOU are the one who'll decide where to go...", "Sometimes the questions are complicated and the answers are simple.", "Today you are You, that is truer than true. There is no one alive who is Youer than You.", "The more that you read, the more things you will know. The more that you learn, the more places you'll go.", "A person's a person, no matter how small.", "Unless someone like you cares a whole awful lot, Nothing is going to get better. It's not.", "Being crazy isn't enough.", "Fantasy is a necessary ingredient in living, it's a way of looking at life through the wrong end of a telescope.", "Being crazy isn't enough.", "Fantasy is a necessary ingredient in living, it's a way of looking at life through the wrong end of a telescope." , "Why fit in when you were born to stand out?", "I have heard there are troubles of more than one kind. Some come from ahead and some come from behind. But I've bought a big bat. I'm all ready you see. Now my troubles are going to have troubles with me!", "How did it get so late so soon?", "If things start happening, don't worry, don't stew, just go right along and you'll start happening too.", "Today was good. Today was fun. Tomorrow is another one.", "From there to here, from here to there, funny things are everywhere", "All alone! Whether you like it or not, alone is something you'll be quite a lot!", "Then the Grinch thought of something he hadn't before! What if Christmas, he thought, doesn't come from a store. What if Christmas...perhaps...means a little bit more", "I meant what I said and I said what I meant. An elephant's faithful one hundred percent!", "Adults are just obsolete children and the hell with them.", "Remember me and smile, for it's better to forget than to remember me and cry.", "Only you can control your future.", "I'm afraid that sometimes you'll play lonely games too. Games you can't win cause you'll play against you."]
	return random.choice(answers)

def header():
	return """

+-+-+-+-+-+ +-+ +-+-+-+
|Q|u|o|t|e| |-| |B|o|t|
+-+-+-+-+-+ +-+ +-+-+-+
	                                                                         
	"""



if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")






