# coding: UTF-8
"""
Copyright (c) 2008 Marian Tietz
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
"""

from gettext import gettext as _
import sushi

plugin_info = (
	_("Writes the current playing song to the channel after typing /np"),
	"1.0",
	"Marian Tietz"
)

plugin_options = (
	("mpd_host", _("MPD host"), sushi.TYPE_STRING, "localhost"),
	("mpd_port", _("MPD port"), sushi.TYPE_NUMBER, 6600),
	("mpd_password", _("MPD password"), sushi.TYPE_PASSWORD, ""),
	("player", _("Player"), sushi.TYPE_CHOICE,
		(("MPD","mpd"),
		("Banshee","banshee"),
		("Decibel Audio Player", "decibel"),
		("Audacious", "audacious")))
)

class np (sushi.Plugin):

	def __init__(self):
		sushi.Plugin.__init__(self, "np")

		self.add_command("np", self.np_command)

	def unload(self):
		self.remove_command("np")

	def np_command(self, server, target, args):
		player = self.get_config("player")

		if player == "mpd":
			try:
				import mpd

				client = mpd.MPDClient()

				mpd_host = self.get_config("mpd_host") or "localhost"
				mpd_port = self.get_config("mpd_port") or 6600
				mpd_port = int(mpd_port)
				mpd_password = self.get_config("mpd_password") or ""

				client.connect(mpd_host, mpd_port)

				if mpd_password:
					client.password(mpd_password)

				data = {"artist":"N/A","title":"N/A","album":"N/A"}
				data.update(client.currentsong())

				fstring = "np: %(artist)s – %(title)s" % data

				self.get_bus().message(
					server,
					target,
					fstring)

				client.disconnect()

			except BaseException as e:
				self.display_error(str(e))

		elif player == "banshee":
			try:
				import dbus

				bus = dbus.SessionBus(
					mainloop = dbus.mainloop.glib.DBusGMainLoop())

				proxy = bus.get_object("org.bansheeproject.Banshee",
					"/org/bansheeproject/Banshee/PlayerEngine")
				banshee = dbus.Interface(proxy,
					"org.bansheeproject.Banshee.PlayerEngine")

				curTrack = banshee.GetCurrentTrack()
				artist = unicode(curTrack["artist"])
				title = unicode(curTrack["name"])

				nowPlaying = "np: %(artist)s – %(title)s" % {
					"artist": artist, "title": title }

				self.get_bus().message(server, target, nowPlaying)

			except Exception as e:
				self.display_error(str(e))

		elif player == "decibel":

			try:
				import os
				from xdg.BaseDirectory import xdg_config_home

				f = open(os.path.join(
					xdg_config_home,
					"decibel-audio-player",
					"now-playing.txt"))
				s = f.read().replace("\n", " ")
				f.close()

				self.get_bus().message(
					server,
					target,
					"np: %s" % (s))

			except BaseException as e:
				self.display_error(str(e))

		elif player == "audacious":
			import dbus

			bus = dbus.SessionBus(
				mainloop=dbus.mainloop.glib.DBusGMainLoop())
			proxy = bus.get_object("org.atheme.audacious",
				"/org/atheme/audacious")

			mdata = {}
			if proxy.Status() == "playing":
				pos = proxy.Position() # in Playlist

				artist = proxy.SongTuple(pos, "artist")
				if artist:
					mdata["artist"] = artist
				title = proxy.SongTuple(pos, "title")
				if title:
					mdata["title"] = title

			data = {"artist":"N/A","title":"N/A"}
			data.update(mdata)

			fstring = "np: %(artist)s – %(title)s" % (data)

			self.get_bus().message(
				server, target, fstring)

		else:
			self.display_error("No player configured.")

