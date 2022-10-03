#VENV_PATH=~/Documents/Studium/Code/python/.venv310/bin/activate
TEST_FILE=$(basename $(wildcard ?.test.py))

all: test checkstyle run

#activate:
#	source $(VENV_PATH)

run:
	python main.py

checkstyle:
	pylint *.py

test:
	python test.py *_test.py

design:
	open /Users/tmueller/Documents/Studium/Code/python/.venv310/lib/python3.10/site-packages/PySide6/Designer.app