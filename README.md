# LDA Project
This project is a research-based app to discuss *LDA algorithm* as a Natural Language Process (**NLP**) algorithm. In summary we are running LDA algorithm on an English Lexicon and discuss its result and test it on a different data-set for several labeled tweets from Twitter API. 

## Approach 
Our approach is to first discuss the result topics from LDA algorithm on our lexicon. 

## NRC Sentiment and Emotion Lexicons 
The Sentiment and Emotion Lexicons is a collection of lexicons that was entirely created by the experts of the National Research Council of Canada. Developed with a wide range of applications, this lexicon collection can be used in a multitude of contexts such as sentiment analysis, product marketing, consumer behaviour and even political campaign analysis. 
NRC Emotion Lexicon: association of words with eight emotions (anger, fear, anticipation, trust, surprise, sadness, joy, and disgust) and two sentiments (negative and positive) manually annotated on Amazon's Mechanical Turk. Available in 105 different languages.
- Version: 0.92
- Number of terms: 14,182 unigrams (words), ~25,000 word senses
- Association scores: binary (associated or not)
- Creators: Saif M. Mohammad and Peter D. Turney
	
Related Papers:

1. Crowdsourcing a Word-Emotion Association Lexicon, Saif Mohammad and Peter Turney, Computational Intelligence, 29 (3), 436-465, 2013.

2. Emotions Evoked by Common Words and Phrases: Using Mechanical Turk to Create an Emotion Lexicon, Saif Mohammad and Peter Turney, In Proceedings of the NAACL-HLT 2010 Workshop on Computational Approaches to Analysis and Generation of Emotion in Text, June 2010, LA, California.

## LDA Arguments
We feed our LDA algorithm with a list of tokenized queries on our lexicon. Each tokenized list contain some synonym words and corresponding emotion or polarity for it. Here is a example of a entry list for LDA:

    ["connective", "connection", "link", "hyphen", "trust"]

> The last word is the emotion (or polarity) corresponding to entry.

Here is the topics with different number of topics given to LDA function (with num_passes=20) Each topic presented with 10 most related words.

| 8-Topics | 10 most related words |
|--|--|
| 0 | joy, anger, amusement, cheerfulness, bad, celebration, man, demon, badness,, love |
| 1 | disgust, anger, uncleanness, deterioration, ugliness, disrepute, danger, adversity, pain,, improbity |
| 2 | sadness, anger, pain, killing, physical, painfulness, punishment, badness, death, lawsuit |
| 3 | negative, positive, violence, poverty, difficulty, courtesy, pitfall, greatness, discord,, prohibition |
| 4 | anticip, surprise, trust, vice, master, chance, ambush, of, excitation, wonder |
| 5 | fear, disease, evil, destruction, malevolence, bane, hindrance, warfare, neglect, arms |
| 6 | positive, trust, remedy, love, resentment, restraint, good, food, repute, clergy |
| 7 | negative, anger, insanity, deception, hate, falsehood, attack, disobedience, disease, badness |
 
 ------------------------------------------------------

| 10-Topics | 10 most related words |
|--|--|
| 0 | disgust, joy, uncleanness, evil, cheerfulness, dislike, hate, badness,, neglect, badness |
| 1 | lawsuit, demon, hindrance, severity, discord, goodness,, discord,, violence,, enmity, oppressive |
| 2 | negative, fear, pain, physical, bad, man, bane, resentment, pain,, deterioration, |
| 3 | positive, fear, deterioration, remedy, danger, master, impotence, food, repute, beauty |
| 4 | sadness, disease, killing, love, violence, painfulness, death, dejection, poverty, lamentation |
| 5 | negative, insanity, deception, falsehood, attack, evil, badness, impurity, wrong, taking |
| 6 | anticip, surprise, amusement, vice, celebration, excitability, money, chance, cry, probity |
| 7 | negative, ugliness, failure, weakness, warning, up,, greatness, uncertainty, restraint,, deception, |
| 8 | trust, positive, joy, pleasurableness, pleasure, clergy, marriage, rejoicing, worship, hope |
| 9 | anger, malevolence, destruction, stealing, punishment, disobedience, accusation, adversity, ejection, improbity |



> This Report Written by Farzin Mohammdi with [StackEdit](https://stackedit.io/).

