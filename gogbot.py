import praw, re, time
from pprint import pprint

def set_config():
	global username, password, thread_id, flair_sub
	username = "charredbot" #/u/charredbot
	password = "lampert" 
	thread_id = "3su2kk" #redd.it/3o6pya
	flair_sub = "charredgrass" #/r/charredgrass

def get_flair(person):
	time.sleep(2)
	return r.get_flair(subreddit,person).__getitem__(u'flair_text')

def set_flair(person, text, cssclass):
	time.sleep(2)
	return r.set_flair(subreddit,person,text,cssclass)

def log(text,urgency=None):
	if urgency == None:
		print("[INFO] " + text)
	else:
		print("[" +  urgency + "] " + text)

def is_number(s):
	#s is a string
    try:
        int(s)
        return True
    except ValueError:
        return False

def last_digits(words):
	backwords = words[::-1] #play on words
	die = False
	ret = ""
	index = 0
	while not die:
		if (backwords[index] == " "):
			die = True
		else:
			try:
				poop = int(backwords[index])
				ret += str(poop)
			except ValueError:
				die = True
		index += 1
	if (ret == ""):
		return 0
	return int(ret[::-1])

def increfy(num, flair, fclass):
	num = int(num)
	if not "Grabbed" in flair:
		return flair + " | Grabbed" + ("" if num ==1 else (" " + str(num)))
	if last_digits(flair) == 0:
		return flair + " " + str(num)
	return flair[0:(len(flair) - len(str(last_digits(flair))))] + str((last_digits(flair) + num))

def classify(flair, currclass):
	if not currclass in ["grabbed","gifted","giftedgrabbed"]:
		return currclass
	if "Gifted" in flair and "Grabbed" in flair:
		return "giftedgrabbed"
	else:
		return "grabbed"

def main():
	set_config()
	global r, subreddit
	r = praw.Reddit('/u/charredgrass\'s Flair-inator for /r/Gift of Games')
	r.login(username,password,disable_warning=True)                                               
	flair_thread = r.get_submission(submission_id=thread_id) #submission id of flair request thread
	me = r.get_redditor(username)                                                                  
	subreddit = r.get_subreddit(flair_sub)
	time.sleep(4)
	log("Initializing My Flair Lady. Logged in as " + username)
	while True:
		inbox = r.get_unread(unset_has_mail=True, update_user=True)
		for i in inbox:
			if (type(i) is praw.objects.Message):
				body = i.__dict__.__getitem__('body')
				if (is_number(body) and body > 0):
					f = get_flair(i.__dict__.__getitem__('author'))
					fc = r.get_flair(subreddit,i.__dict__.__getitem__('author')).__getitem__('flair_css_class')
					set_flair(i.__dict__.__getitem__('author'), increfy(body,f,fc), classify(increfy(body,f,fc),fc))
					i.reply("Flair updated! It may take a second for this change to show up in comments. \n --- \n Problems? Message /u/charredgrass.")
					log("Updated a flair.")
				else:
					i.reply("You are supposed to send a message with only a positive number corresponding to the number of Grabbed you are getting, and I don't think you did so. \n --- \n Problems? Message /u/charredgrass.")
			i.mark_as_read()

if __name__ == '__main__':
	main()
