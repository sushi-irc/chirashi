#!/usr/bin/env python

APPNAME = 'plugins'
VERSION = '1.1.2'

srcdir = '.'
blddir = 'build'

def configure (conf):
	conf.check_tool('gnu_dirs')

def build (bld):
	bld.install_files('${DATAROOTDIR}/sushi/plugins', bld.glob('*.py'))
