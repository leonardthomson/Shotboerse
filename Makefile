TEST_FILE=$(wildcard *test.py)
UI_FILES=$(wildcard *.ui)
UI_TO_PY=$(UI_FILES:%.ui=%.py)
PYTHON_FILE=$(filter-out $(UI_TO_PY), $(wildcard *.py))

all: test checkstyle run

run:
	python main.py

checkstyle:
	pylint $(PYTHON_FILE)

test:
ifneq (,$(TEST_FILE))
	python $(TEST_FILE)
endif

compile: UI_TO_PY

%.py: %.ui
	pyside6-uic $^ > $@

designer:
	open /Users/tmueller/Documents/Studium/Code/python/.venv310/lib/python3.10/site-packages/PySide6/Designer.app

design:
	open $(UI_FILES)