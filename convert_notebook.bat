@echo off
REM Define the notebook filename and output directory
set NOTEBOOK_FILE=NewStyle_RaceReport.ipynb

REM Run the nbconvert command
jupyter nbconvert --to html --no-input "%NOTEBOOK_FILE%"

echo Conversion completed for %NOTEBOOK_FILE%
