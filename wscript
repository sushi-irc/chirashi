#!/usr/bin/env python

APPNAME = 'chirashi'
VERSION = '1.4.0'

top = '.'
out = 'build'

def configure (ctx):
	ctx.load('gnu_dirs')

def build (ctx):
	ctx.install_files('${DATAROOTDIR}/chirashi', ctx.path.ant_glob('*.py'))
