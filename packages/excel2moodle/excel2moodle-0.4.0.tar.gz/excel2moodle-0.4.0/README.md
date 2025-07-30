# excel 2 Moodle
[Deutsche README](https://gitlab.com/jbosse3/excel2moodle/-/blob/master/README.de.md)

![Logo](excel2moodleLogo.png "Logo excel2moodle"){width=50%}

This Python program helps to create Moodle questions in less time.
The aim is to put alle the information for the questions into a spreadsheet file, and then parse it, to generate Moodle compliant XML-Files.

Furthermore this program lets you create a single XML-File with a selection of questions, that then can be imported to a Moodle-Test.

## Concept
The concept is, to store the different questions into categories of similar types and difficulties of questions, for each of which, a separated sheet in the Spreadsheet document should be created.

There Should be a sheet called "Kategorien", where an overview over the different categories is stored.
This sheet stores The names and descriptions, for all categories. The name have to be the same as the actual sheet names with the questions.
Furthermore the points used for grading, are set in the "Kategorien" sheet


## Development State
This program is still quite rough, with very litte robustness against faulty user input inside the Spreadsheet.

## Functionality
* Parse multiple Choice Questions, each into one XML file
* Parse Numeric Questions, each into one XML file
* create single XML File from a selection of questions

## Development Goals
* [X] creating an example spreadsheet
* [X] Export function, to create numerical Question version from a matrix of variables and corresponding correct Answers:
  * similar to the calculated question Type, but with the benefit, of serving all students the same exact question
* [.] making it more robust:
  * [X] Adding Error Messages when exporting
  * [X] Creating logging
  * [ ] Logging Errors to File
  * [ ] making it Image File-Type agnostic
* [ ] Creating a Settings Menu
  * [ ] Making keys in spreadsheet selectable in the Settings
  * [ ] Setting image folder

## Licensing and authorship
excel2moodle is lincensed under the latest [GNU GPL license](https://gitlab.com/jbosse3/excel2moodle/-/blob/master/LICENSE)
Initial development was made by Richard Lorenz, and later taken over by Jakob Bosse
