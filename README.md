# studentPairings

This is a script to assign students to topics given a csv file containing the student numbers and their preference rankings for their top 7 topic choices and a second csv file, `student_numbers.csv`, containing the student numbers and names.

The script is run by typing `python3 student_choices.py` into the command line from within the `studentPairings` directory. The program will output two CSV files:
- `student_pairings.csv` will contain the student numbers, names and assigned topic for all students listed in `student_numbers.csv`. Any students that submitted preferences but were not assigned a topic will have a topic number of `*` and topic title of `***` in the resulting csv file. Any students that did not submit preferences will have a blank topic name and title.
- `unnamed_allocations.csv` will contain the student number and assigned topic for any students where the program failed to match their provided student number with that in `student_numbers.csv`. These will need to be matched manually.
