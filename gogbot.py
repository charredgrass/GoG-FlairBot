import praw

r = praw.Reddit('/u/charredgrass\'s Flair Bot for /r/Gift of Games')
r.login('CharredBot','lampert')

flair_thread = get_submission("3dswjr") #submission id of flair request thread
me = get_redditor('CharredBot')

keepGoing = True

while keepGoing:
	#check flair_thread
	comments = flair_thread.comments
	for commie in comments:
		if commie.is_root:
			rip=False
			for com in commie.replies:
				if com.author.user_name = "CharredBot":
					rip = True
			if !rip:
				#do the stuff with the things to register flair
				flairify(commie)

def flairify():
	
	pass
