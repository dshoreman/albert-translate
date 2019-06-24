ICON ?= light
PREFIX ?= $(HOME)/.local
INSTALL_PATH = $(DESTDIR)$(PREFIX)/share/albert/org.albert.extension.python/modules

all:
	@echo "Run make install to install this Albert extension."

clean:
	@rm -rf "$(INSTALL_PATH)/translate"

install:
	@mkdir -p "$(INSTALL_PATH)/translate"
	@cp -v icons/$(ICON).png "$(INSTALL_PATH)/translate/icon.png"
	@cp -v src/* "$(INSTALL_PATH)/translate/"
