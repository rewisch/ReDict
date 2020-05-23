# Content
  ##   ReDict - A Latin Dictionary
  ##   Downloads
  ##   Technical 
  ##   Additional Dictionaries
 


# ReDict - A Latin Dictionary 

There’s no shortage of available Latin dictionaries both off- and online. I came up with this additional dictionary for the existing dictionaries – at least the once I'm aware of – lacked some features I’d like to have. Besides, it was a fun project to write in Python and to explore its main concepts and features. It's my first real "programming project", so please pardon if things might not be done as they should. Feel free to correct though, I'd be more than happy. 

Main Features:
1.    Not a feature but nice to have: ReDict has support for touch gestures. 
  a.    you can zoom the text with pinch-gestures
  b.    you can select single words to look them up in a new window with a tap gesture
  
2.    Searching over declined Latin words (for all words that the ‚cltk‘ was able to decline you can search all form of a word, hence you needn’t to look-up the lemma. You can, for example, search for „dico“ as well as „dixi“ and get the dictionary article for ‘dico’)

3.    ReDict scans your Clipboard and searches for the word if your clipboard value changes. Hence, reading a Latin book on your computer and look-up words comes with great ease. No copy-paste; just copy. ReDict tries to bring itself to the foreground as well. This works fine on Mac. I try to figure out how to do it on Windows too. 

4.    ReDict has a completer function which shows you which word exists in the dictionary according to what you’re typing. In the settings, you can choose whether this function is performed regarding all forms of the verb or just the lemmata. Up to this point the latter is recommended since the former slows down the application too much. It does work though.

5. From the result, you can select a word, tap or right-click to open the context menu and then look the word up in an additional window. 

6. Choose different stylesheets

Ubuntu:
![Ubuntu](https://image.jimcdn.com/app/cms/image/transf/none/path/s042449d1eb1325c4/image/i770fed9960ec8898/version/1589308383/image.png)

Dark: 
![Dark](https://image.jimcdn.com/app/cms/image/transf/none/path/s042449d1eb1325c4/image/i5eebb3521a9f9cd9/version/1589308553/image.png)

Amoled:
![Ubuntu](https://image.jimcdn.com/app/cms/image/transf/none/path/s042449d1eb1325c4/image/i88396d3f35edb278/version/1589308566/image.png)

# Downloads

You can download an executable distribution of the software here:

Mac: https://www.rewisch.ch/dist/ReDict/Mac/ReDict.zip

Windows: https://www.rewisch.ch/dist/ReDict/Windows/ReDict.zip

Linux (64bit): https://rewisch.ch/dist/ReDict/Linux/ReDict.zip

# Technical

Run Redict.py in the src folder. It should, if the database does not yet exist, create the database and import the dictionaries. 

# Additional dictionaries

If you have additional machine-readable dictionaries please send them to me. I'm more than happy to add as many dictionaries as possible. 
