class Song(object):

	def __init__(self,lyics):
		self.lyrics = lyrics

	def sing_me_a_song(self):
		for line in self.lyrics:
			print line


happy_bday = Song()