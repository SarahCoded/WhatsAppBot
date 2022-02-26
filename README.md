# WhatsApp Crossword Bot

This bot has two uses. It can give the dictionary definition of a word, or a list of matching words from a specified sequence with unknown letters, such that st?d? would return stade, studs, and study. These two features can be useful when nearing the end of finishing a crossword.

## Contents
- [Example Usage](#Example-Usage)
- [Technologies Used](#Technologies-Used)
- [Web Scraping](#Web-Scraping)
- [Word Matches](#Word-Matches)
- [Word Definitions](#Definitions)

## <a name="Example-Usage"></a>Example Usage

You may want to find out all the possible words that could fit the pattern st??d

![Alt text](media/st__d.png?raw=true "Lookup Screenshot")

If you think Stond might be the correct answer to a crossword clue but are unsure of the definition, you can send just that word and the response would be

![Alt text](media/stond.png?raw=true "Lookup Screenshot")

## <a name="Technologies-Used"></a>Technologies Used

This project was created using Flask and deployed with Heroku. It uses the [Twilio API](https://www.twilio.com/) in order to send out WhatsApp messages. The incoming data is taken from this popular crossword solver [site](https://www.crosswordsolver.org/) using web scraping with [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/).

## <a name="Web-Scraping"></a>Web Scraping

I decided to use web scraping to create this programme, because I couldn't find an API that would manage to do something similar to what [this](https://www.crosswordsolver.org/) website can do. I've used it in the past to help with crosswords, but found the keyboard input to be fiddly and often only wanted to get the words, not their definitions as well.

It was quite simple to implement because searching for words can be done with appending the necessary suffix to the web's URL address, with _ symbolising blank letters. 

Each search comes with the word and the definition. I used Beautiful Soup to parse through the html and select the necessary data depending on the query the user has requested.

One issue I came across was that only 10 matches were being displayed per page. In order to access all of the words, in  cases where there were more than 10 results, I had to make multiple requests to the website, adding in a multiple of 10 into the URL to access the next page etc. This was achieved using a while loop with a counter. 

## <a name="Word-Matches"></a>Word Matches

I found it intuitive to have a user enter ? to represent blank spaces when searching for a term. The ?'s can then be converted to _ with the replace() function for the web scraping. 

The site has an unusual way of handling phrases with a space, such as 'Robin Hood', in that the user is expected to express it as a 10 letter search. In my implementation, I have allowed spaces to become an _, so that multi-phrase words will appear in the results.

If the user sent a string which does not comply with the characters I would expect, the programme returns a generic welcome message which explains what the bot can do. I didn't want to implement any help or info commands, as this could clash with genuine querying i.e. to look up the definition of 'help', or find words such as 'info????'.

## <a name="Definitions"></a>Word Definitions

Definitions of words were gathered from the same page that matches were found, because if you enter in a word with no blanks, the word and definition will still appear as the sole matching result. 

Some words might have multiple definitions, so I chose to display each new definition on a new line with a number counter to make it look neater.

![Alt text](media/comic.png?raw=true "Lookup Screenshot")
