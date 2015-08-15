import praw, re, time

def main():
	global GRABBED_REGEX, flair_thread, me, subreddit, r, confirm_thread
	r = praw.Reddit('/u/charredgrass\'s Flair-inator for /r/Gift of Games')
	r.login('CharredBot','',disable_warning=True)

	flair_thread = r.get_submission(submission_id="3dswjr") #submission id of flair request thread
	me = r.get_redditor('CharredBot')
	subreddit = r.get_subreddit("charredgrass")

	confirm_thread = r.get_submission(submission_id="3g7ybp") #thread where mods confirm gifted

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
				if not rip and com.body != "[deleted]":#make sure comment isn't removed, either.
					give_flair(commie)
					time.sleep(2)
		#next, check confirm_thread
		print("I swear I'm still doing something")

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
			if flair_gifted and not is_user_gifted(com.author): #see if user is going from non-gifted to gifted
				print("confirming with mods")
				com.reply("You are upgrading your flair to Gifted, this requires moderator confirmation. Just wait, and your flair will be upgraded when the moderators get to it.")
				#Here it should get the perma of 'com'. Reply with author's name, flair needed, and the perma, on 'confirm_thread'. Then it has to check that to see if the mods have done shit.
				confirm_thread.add_comment(com.permalink + "\n\n" + com.author.name + " wants **" + flair + "** as their flair. Please verify, and update their flair manually. Pls.")
				return True
			if flair_grabbed:
				try:
					amt_grabbed = re.search(GRABBED_REGEX,flair).group(0)
				except:
					amt_grabbed = 1
			else:
				amt_grabbed = 0
			if flair_gifted and not flair_grabbed and not user_has_custom_flair(com.author):
				#check if user has a custom flair.
				r.set_flair(subreddit,com.author,"Gifted","gifted")
				print "Assigning gifted flair to " + com.author.name + "."
				com.reply(get_response(flair))
			elif flair_grabbed and not flair_gifted and not user_has_custom_flair(com.author):
				if amt_grabbed > 1:
					r.set_flair(subreddit,com.author,"Grabbed" + str(amt_grabbed), "grabbed")
				else:
					r.set_flair(subreddit,com.author,"Grabbed", "grabbed")
				print "Assigning grabbed flair to " + com.author.name + "."
				com.reply(get_response(flair))
			elif flair_grabbed and flair_gifted and not user_has_custom_flair(com.author):
				r.set_flair(subreddit,com.author,"Gifted | " + str(amt_grabbed), "giftedgrabbed")
				print "Assigning GiftedGrabbed flair to " + com.author.name + "."
				com.reply(get_response(flair))
			elif user_has_custom_flair(com.author):
				r.set_flair(subreddit,com.author,flair,get_user_cust_flair_class(com.author))
				print "Assigning a custom flair class to " + com.author.name
				com.reply(get_response(flair))
		else:
			if com.body != "[deleted]":
				try:
					com.reply("I think something went wrong. Make sure you've got the format correct, and contact \/u/charredgrass if necessary.")
				except:
					print("Error: unable to post comment. Was the parent deleted, or is reddit down?" + com.body)#will spam if there are removed comments
			return False
	else:
		return False
	#eh
	pass

#TODO finish this
def user_has_custom_flair(person):
	return not r.get_flair(subreddit,person).__getitem__(u'flair_css_class') in ["gifted","giftedgrabbed","grabbed",'',None]

def get_user_cust_flair_class(person):
	return r.get_flair(subreddit,person).__getitem__(u'flair_css_class')

def is_user_gifted(person):
	if r.get_flair(subreddit,person).__getitem__(u'flair_text') == '' or r.get_flair(subreddit,person).__getitem__(u'flair_text') == None:
		return False
	else:
		return u'Gifted' in r.get_flair(subreddit,person).__getitem__(u'flair_text')

def get_response(flair):
	resp = "Setting flair to **" + flair + "**. Hopefully."
	resp = resp + "\n\n" + "Contact \/u/charredgrass with any problems." + "\n\n" + "---\n\nI'm just a poor bot. Please don't hurt me."
	return resp

if __name__ == '__main__':
	main()
