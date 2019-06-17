PREFIX ?= $(HOME)/.local
INSTALL_PATH = $(DESTDIR)$(PREFIX)/share/albert/org.albert.extension.python/modules

all:
	@echo "Run make install to install this Albert extension."

install:
	@cp -v translate.py "$(INSTALL_PATH)/translate.py"
