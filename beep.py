""" beep on highlight """

import sushi
import string

def do_beep():
	""" tries several beep methods for
		different platforms and frameworks
		and returns if one method was
		successful.
	"""
	try:
		import winsound
		return winsound.Beep(30, 1)
	except:
		pass

	try:
		import MacOS
		# not in 64 bit
		return MacOS.SysBeep()
	except:
		pass

	try:
		import gtk
		return gtk.gdk.beep()
	except:
		pass

	try:
		tty = file("/dev/tty", "w")
		tty.write(chr(7))
		tty.close()
		return None
	except:
		pass

plugin_info = ("Let the PC speaker beep on a highlight.",
	"1.0", "Marian Tietz")
plugin_options = ()

class beep (sushi.Plugin):

	def __init__(self):
		sushi.Plugin.__init__(self, "beep")

		self.get_bus().connect_to_signal("message",
			self.message_cb)

	def message_cb(time, server, usr, target, text):

		def has_highlight(text, needle):
			punctuation = string.punctuation + " \n\t"
			ln = len(needle)
			for line in text.split("\n"):
				i = line.find(needle)
				if i >= 0:
					if (line[i-1:i] in punctuation
					and line[ln+i:ln+i+1] in punctuation):
						return True
			return False

		nick = self.get_nick(server).lower()
		target = target.lower()

		if nick == target or has_highlight(text, nick):
			do_beep()
