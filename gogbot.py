import praw, re, time

def set_config():
	global username, password, thread_id, flair_sub
	username = "CharredBot" #/u/charredbot
	password = "lampert" 
	thread_id = "3o6pya" #redd.it/3o6pya
	flair_sub = "charredgrass" #/r/charredgrass

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
		com.reply('Something went wrong. Contact the [bot creator](/u/charredgrass) or the [subreddit moderators](https://www.reddit.com/message/compose?to=%2Fr%2FGiftofGames) for help.')
		return
	if "dank memelord" in com.body: #                                                     <<<<<<<<<<        dont forget to change this back
		if  u'gifted' in r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'):
			r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),"giftedgrabbed")
		elif not u'grabbed' in r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'):
			r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'))
		else:
			r.set_flair(subreddit,com.author,increment_grabbed(r.get_flair(subreddit,com.author).__getitem__(u'flair_text')),"grabbed")
	c = com.reply('i upgraded ur flair nerdface')
	print('upgraded ' + com.author.name + '\'s flair ' + c.permalink)

def increment_grabbed(text):
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
	print("I just started, I swear!")
	keepGoing = True
	comments = flair_thread.comments
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
					time.sleep(10)
					break
		comments = flair_thread.refresh().comments
		time.sleep(2)

if __name__ == '__main__':
	main()
