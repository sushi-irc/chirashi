#!/usr/bin/env python

APPNAME = 'plugins'
VERSION = '1.1.0'

srcdir = '.'
blddir = 'build'

def configure (conf):
	conf.check_tool('gnu_dirs')

def build (bld):
	# FIXME Waf 1.5.9 bug
	bld.new_task_gen()

	bld.install_files('${DATAROOTDIR}/sushi/plugins', bld.glob('*.py'))