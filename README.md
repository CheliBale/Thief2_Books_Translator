I was playing through some fan-made missions for Thief 2 again. Previously, I had to manually translate the in-game books one by one using an online translator.
While small missions usually don't contain many books, encountering a mission with around 300 of them becomes quite a chore.
To address this, I decided to create a workflow that allows for the translation of any number of books in under two minutes.
The resulting translation is of high quality. The only minor drawback—which doesn't affect immersion at all—is that while
the original text might have been carefully formatted by the mission author for readability, the translated version will
appear as a continuous block of text. This is rarely an issue, as most books in fan-made missions consist of continuous text anyway.


Preconditions

As a precaution, please keep a backup copy of the books in a backup folder.


Postconditions

1) Once you have downloaded and extracted the fan-made mission, navigate to the "mission folder/books/" directory.
   You may see subfolders for different languages; select the one that matches your game's language
   (If you only see ".str" files, proceed directly to step 2).

2) Place both programs "Program_1", "Program_2" and the "config.ini" file in the same directory as the ".str" files.

3) Read the instructions for "Program_1" and "Program_2" before running them.


Program_1

1) Launch the program.

2) Open the "All.html" (which will appear in the same folder after the program is launched) file in your web browser (Chrome is
   recommended, as it supports in-page translation). Right-click anywhere on the text and select the option to translate it into
   your preferred language (you can adjust the target language in your browser's settings if necessary).

3) Once translated, select all the text CTRL+A and copy it CTRL+C. 
4) In the same folder, alongside the programs, create a file named "All.txt" and paste the copied text into it.


Program_2

Before running the program, you can adjust the number of words per book page in the config.ini file. (Since the game features various
types of books, the translated text—in terms of word or character count—may exceed the original, potentially causing the text
to overflow the page. Therefore, if you notice the text being cut off in-game, you should lower this number.
I have set it to 110 as a reasonably balanced value.)

1) Run the program.

2) A folder named "Result" will be created, containing .str files with the translated text.

3) Copy these .str files and paste them into the original location, overwriting the existing files.
