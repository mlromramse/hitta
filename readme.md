




# hitta.py

This is a very simple tool, written in python, that uses the native hitta.se http request to find the owner to a phone number.
It is also possible to search for a name but it has to be a perfect match to work.




## Installation

Clone the repo and then run:

    pip install -r requirements.txt

After that a phone number lookup can be made with:

    ./hitta.py 555123123

The result would be written in your terminal window:

    Title: The hitta.se title field
    Type: Mobil
    Tel: 555123123

In case of an unknown number the result would be:

    Title: The hitta.se title field
    Unknown: 5 55 12 31 23
    Searches: 231




## Usage tip

Write a simple alias in your .bash_rc, .bash_completion or similar like this:

    alias hitta='/home/your/path/to/hitta.py'

After that you can lookup a number anywhere in your terminal window by typing:

    hitta the_number_of_interest


