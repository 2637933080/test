@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Running tests with pytest...
pytest

echo Generating coverage report...
coverage run -m pytest
coverage report
coverage html

echo Running pylint for code quality check...
pylint palindrome.py

echo All tasks completed!
pause