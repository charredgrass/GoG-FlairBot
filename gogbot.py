import praw, re

def main():
	global GRABBED_REGEX, flair_thread, me, subreddit, r
	r = praw.Reddit('/u/charredgrass\'s Flair-inator for /r/Gift of Games')
	r.login('CharredBot','',disable_warning=True)

	flair_thread = r.get_submission(submission_id="3dswjr") #submission id of flair request thread
	me = r.get_redditor('CharredBot')
	subreddit = r.get_subreddit("charredgrass")

	GRABBED_REGEX = re.compile("Grabbed ([0-9]*)")


	keepGoing = True

	while keepGoing:
		#check flair_thread
		comments = flair_thread.comments
		for commie in comments:
			if commie.is_root:
				rip=False
				for com in commie.replies:
					if com.author == me:
						rip = True
				if not rip:
					give_flair(commie)

#Comment Format

# **Flair Needed**
# 
# [Single Gifted Thanks]
#
# [All Grabbed Thankses]

def give_flair(com):
	text = com.body
	flair_gifted = None
	flair_grabbed = None
	thankses = []
	flairneeded = ""
	lines = text.split('\n\n')
	if len(lines[0]) > 4:
		if lines[0][:2] == "**" and lines[0][-2:] == "**":
			#This means that it did something good
			flair = lines[0][2:-2]
			#ok check if the flair is legit
			flair_gifted = "Gifted" in flair
			flair_grabbed = "Grabbed" in flair
			amt_grabbed = None
			if flair_gifted and False: #something to check if user doesn't already have flair_gifted
				pass
				#verify with mods
			if flair_grabbed:
				amt_grabbed = re.search(GRABBED_REGEX,flair).group(0)
			if flair_gifted and not flair_grabbed and not user_has_custom_flair(com.author):
				#check if user has a custom flair. no praw method to do it, check json maybe
				r.set_flair(subreddit,com.author,"Gifted","gifted")
				print "gifted"
				com.reply("flair set")
			if flair_grabbed and not flair_gifted and not user_has_custom_flair(com.author):
				r.set_flair(subreddit,com.author,"" + amt_grabbed, "grabbed")
				print "grabbed"
				com.reply("flair set")
			if flair_grabbed and flair_gifted and not user_has_custom_flair(com.author):
				r.set_flair(subreddit,com.author,"Gifted | " + amt_grabbed, "giftedgrabbed")
				print "giftedgrabbed"
				com.reply("flair set")
			if user_has_custom_flair(com.author):
				r.set_flair(subreddit,com.author,flair,get_user_cust_flair_class(com.author))
				print "custom"
				com.reply("flair set")
		else:
			return False
	else:
		return False
	#eh
	pass

#TODO finish this
def user_has_custom_flair(person):
	return not r.get_flair(subreddit,person).__getitem__(u'flair_css_class') in ["gifted","giftedgrabbed","grabbed"]

def get_user_cust_flair_class(person):
	return r.get_flair(subreddit,person).__getitem__(u'flair_css_class')

if __name__ == '__main__':
	main()
