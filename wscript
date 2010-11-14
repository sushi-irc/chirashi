#!/usr/bin/env python

APPNAME = 'plugins'
VERSION = '1.4.0'

top = '.'
out = 'build'

def configure (ctx):
	ctx.load('gnu_dirs')

def build (ctx):
	ctx.install_files('${DATAROOTDIR}/sushi/plugins', ctx.path.ant_glob('*.py'))
