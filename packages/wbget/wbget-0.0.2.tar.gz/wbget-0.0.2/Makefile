#
# Copyright (C) 2025 The Authors
# All rights reserved.
#
# This file is part of wbget.
#
# wbget is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation.
#
# wbget is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with wbget. If not, see http://www.gnu.org/licenses/
#

wbget:
	python3 -m pip install --no-dependencies .

install:
	python3 -m pip install .
	python3 -m pip install dotenv

uninstall:
	python3 -m pip uninstall -y wbget

clean:
	find -name "*~" -delete

distclean:clean
	rm -Rf dist

venv:
	python3 -m venv ~/.venvs/wbget

tools:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine

build:distclean
	python3 -m build

upload:
	python3 -m twine upload --verbose --repository pypi dist/*
