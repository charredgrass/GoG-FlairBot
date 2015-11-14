import praw, re, time

def set_config():
	global username, password, thread_id, flair_sub, trigger
	username = "My_Flair_Lady" #/u/charredbot
	password = "" 
	thread_id = "" #redd.it/3o6pya
	flair_sub = "GiftofGames" #/r/charredgrass

def choose_random_giveaway_winner():
	return r.get_redditor('charredgrass')

def get_dank_meme():
	return r.get_subreddit('me_irl')

def get_num_grabbed(flair):
	#flair should be a string
	backwards = flair[::-1]
	output = ""
	for x in range(0, len(backwards)):
		if is_number(backwards[x]):
			#uh yeah
			output += backwards[x]
		else:
			break
	if output == "":
		return differentiate_ones_and_zeroes_because_the_mods_are_stupid(flair)
	return int(output[::-1])
	#ok so this probably works

def flairify(com):
	if r.get_flair(subreddit,com.author).__getitem__(u'flair_text') == None or r.get_flair(subreddit,com.author).__getitem__(u'flair_text') == "":
		r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),"grabbed")
	if "grabbed" in com.body.lower():
		iterations = 1
		if com.body.lower().find('grabbed') == -1:
			iterations = 1
		elif com.body.lower().find('grabbed ') == -1:
			iterations = 1
		else:
			iterations = last_digits(r.get_flair(subreddit,com.author).__getitem__(u'flair_text'))
		for x in range(iterations):	
			if  u'gifted' in r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'):
				r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),"giftedgrabbed")
			elif not u'grabbed' in r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'):
				r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'))
			else:
				r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),"grabbed")
	c = com.reply('Your flair has been updated. \n Problems? Message the moderators. Compliments? Message \\/u/charredgrass or talk with him [here](http://steamcommunity.com/id/charredGrass/)' )
	print('upgraded ' + com.author.name + '\'s flair ' + c.permalink)

def increment_grabbed(text):
	if text == None or text == "":
		return "Grabbed"
	numbar = get_num_grabbed(text)
	backwards = text[::-1]
	new_backwards = ""
	for x in range(0,len(backwards)):
		if not is_number(backwards[x]):
			new_backwards += backwards[x]
	numbar += 1
	#ok heres the stoopid part
	if numbar == 1 and not "Grabbed" in text:
		return new_backwards[::-1] + " | Grabbed"
	else:
		return new_backwards[::-1] + str(numbar)

def differentiate_ones_and_zeroes_because_the_mods_are_stupid(flair):
	if "Grabbed" in flair:
		return 1
	else:
		return 0

def is_number(s):
	#s is a string
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():
	set_config()
	global subreddit, r 
	print("Logging in, nerd")
	r = praw.Reddit('/u/charredgrass\'s Flair-inator for /r/Gift of Games')
	r.login(username,password,disable_warning=True)                                               
	flair_thread = r.get_submission(submission_id=thread_id) #submission id of flair request thread
	me = r.get_redditor(username)                                                                  
	subreddit = r.get_subreddit(flair_sub)
	print("if the bot hasnt blown up at this point its a good sign!")
	print("I just started, I swear")
	keepGoing = True
	comments = flair_thread.comments
	flair_thread.replace_more_comments()
	time.sleep(10)
	while keepGoing:
		for com in comments:
			if com.is_root:
				rip = False
				for comm in com.replies:
					if comm.author == me:
						rip = True
				if not rip and com.body != "[deleted]":
					flairify(com)
					print("taking a 10 second nap so i dont explode")
					flair_thread.replace_more_comments()
					time.sleep(10)
					break
		comments = flair_thread.refresh().comments
		time.sleep(2)

if __name__ == '__main__':
	main()

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
