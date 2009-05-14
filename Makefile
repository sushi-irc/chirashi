include ../Makefile.common

all:

install: all
	$(INSTALL) -d -m 755 '$(DESTDIR)$(sharedir)/sushi/plugins'
	$(INSTALL) -m 644 *.py '$(DESTDIR)$(sharedir)/sushi/plugins'

clean:
	$(RM) -f *.pyc
