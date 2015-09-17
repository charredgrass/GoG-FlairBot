from pprint import pprint
import praw
import re
import time

class NeedsConfirmation(object):
	#2 constructors - 1 is creating when someone requests Gifted, one is importing from thread
	#TODO this
	def __init__(self, arg):
		self.arg = arg
		

class Flair(object):
	def __init__(self, is_gifted, is_grabbed, num_grabbed):
		self.is_gifted = is_gifted
		self.is_grabbed = is_grabbed
		self.num_grabbed = num_grabbed
	def is_gifted(self):
		return self.is_gifted
	def is_grabbed(self):
		return self.is_grabbed
	def num_grabbed(self):
		return self.num_grabbed
	def gen_flair_text(self):
		if self.is_gifted and self.is_grabbed:
			return "Gifted | " + self.gen_just_grabbed_num()
		if self.is_gifted and not self.is_grabbed:
			return "Gifted"
		if self.is_grabbed and not self.is_gifted:
			return self.gen_just_grabbed_num()
	def gen_just_grabbed_num(self):
		if not self.is_grabbed:
			return ""
		if self.num_grabbed == 0:
			return "Grabbed"
		else:
			return "Grabbed " + str(num_grabbed)
	def gen_flair_class(self):
		if self.is_grabbed and self.is_gifted:
			return "giftedgrabbed"
		if self.is_grabbed and not self.is_gifted:
			return "grabbed"
		if self.is_gifted and not self.is_grabbed:
			return "gifted"
	def can_upgrade_to(self, higher_flair):
		#where higher_flair is another Flair object that is supposed to be higher
		if isinstance(higher_flair,EmptyFlair):
			return False
		if self.is_gifted and not higher_flair.is_gifted:
			return False
		if self.is_grabbed and not higher_flair.is_grabbed:
			return False
		if self.num_grabbed > higher_flair.num_grabbed:
			return False
		return True

class EmptyFlair(Flair):
	def __init__(self):
		super(EmptyFlair, self).__init__(False,False,0)
	def gen_flair_text(self):
		return ""
	def can_upgrade_to(self, higher_flair):
		return True

class CustomFlair(Flair):
	def __init__(self, is_gifted, is_grabbed, num_grabbed, custom_text, custom_class):
		super(CustomFlair, self).__init__(is_gifted, is_grabbed, num_grabbed)
		self.custom_text = custom_text
		self.custom_class = custom_class #the CSS flair class the user flair will use. should obtain from current flair class.
	#def gen_flair_text(self):
	#an augmented version of the Flair class's gen_flair_text function
	def gen_flair_text(self):
		return self.custom_text + " | " + super.gen_flair_text()
	def gen_flair_class(self):
		return self.custom_class

def get_numbers(text):
	i = True
	ret = ""
	n=1
	while i and n < len(text):
		try:
			x = int(text[-(n+1):-n])
		except ValueError:
			i = False
			return 0
		ret += str(x)
	return ret[::-1] #returns number as a STRING

def text_to_Flair(text):
	return Flair("Gifted" in text, "Grabbed" in text, int(get_numbers(text)))

def text_to_custom_Flair(text,com):
	return CustomFlair("Gifted" in text, "Grabbed" in text, int(get_numbers(text)), r.get_flair(subreddit,com.author).__getitem__(u'flair_text').split(' |')[0],r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class'))

def parse_comment_text_into_Flair(com):
	text = com.body
	lines = text.split('\n\n')
	if len(lines[0]) > 4:
		if lines[0][:2] == "**" and lines[0][-2:] == "**":
			flair_text = lines[0][2:-2]
			#convert to a flair class
			wanted_flair = Flair('Gifted' in flair_text,'Grabbed' in flair_text, int(get_numbers(flair_text)))
			current_flair = EmptyFlair()
			try:
				if not r.get_flair(subreddit,com.author).__getitem__(u'flair_css_class') in ["gifted","giftedgrabbed","grabbed",'']:
					current_flair = text_to_Flair(r.get_flair(subreddit,com.author).__getitem__(u'flair_text'))
				else:
					current_flair = text_to_custom_Flair(r.get_flair(subreddit,com.author).__getitem__(u'flair_text'),com)
			except Exception:
				pass
			listerino = [wanted_flair,current_flair]
			return listerino
		else:
			#do some stuff to say it failed or whatever
			pass
	
def reply_to_comment(com,stuff):
	com.reply(stuff + "\n\n --- \n\n *I am a bot, and this message is automated. Please contact [charredgrass](https://www.reddit.com/user/charredgrass/) with any concerns, or the [moderators of the subreddit](https://www.reddit.com/message/compose?to=%%2Fr%%2FGiftofGames)")

def yell_about_error(com,error):
	poop = "Unknown error! Something went wrong."
	if error == 'cheating_bastard':
		poop = "Uh oh. Are you trying to change your flair to something it can't upgrade to? If so, contact the moderators. If not, contact the moderators."
	reply_to_comment(com,poop)

def main():
	global subreddit, me
	check_for_confirmation = [] #list of NeedsConfirmations
	system_admin = ['charredgrass','charredbot']
	system_moderator = ['Ai-Sama','TheAzureDragon','AakashMasani','Cyali']
	#TODO import current checks for confirmation by reading comments on a post
	keep_going = True
	r = praw.Reddit('/u/charredgrass\'s Flair-inator for /r/Gift of Games')
	r.login('CharredBot','lampert',disable_warning=True)
	flair_thread = r.get_submission(submission_id="3l861d") #submission id of flair request thread
	me = r.get_redditor('CharredBot')
	subreddit = r.get_subreddit("charredgrass")
	confirm_thread = r.get_submission(submission_id="3g7ybp")
	while (keep_going):
		comments = flair_thread.comments
		for commie in comments:
			if commie.is_root:
				rip=False
				for com in commie.replies:
					if com.author == me:
						rip = True
				if not rip and not commie.body == u'[deleted]':
					lol = parse_comment_text_into_Flair(commie)
					if lol != None:
						wanted_flair = lol[0]
						current_flair = lol[1]
						if not current_flair.can_upgrade_to(wanted_flair):
							yell_about_error(commie, 'cheating_bastard')
						else:
							#this means it worked, do more stuff here
							r.set_flair(subreddit,commie.author,wanted_flair.gen_flair_text(), wanted_flair.gen_flair_class())
							commie.reply('setting flair...')
							comments = flair_thread.comments
							time.sleep(3)
							print("doin stuff")
							#TODO check for moderator approval
							pass
					else:
						commie.reply('hey stop it nerd, this is for cool kids requesting flair only')
						comments = flair_thread.comments
					time.sleep(4)

if __name__ == '__main__':
	main()

