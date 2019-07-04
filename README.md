# LDA Project
This project is a research-based app to discuss *LDA algorithm* as a Natural Language Process (**NLP**) algorithm. In summary we are running LDA algorithm on an English Lexicon and discuss its result and test it on a different data-set for several labeled tweets from Twitter API. 

## Approach 
Our approach contain making a LDA model using a lexicon and testing it with some other labeled entry. We use *NRC Sentiment and Emotion Lexicon* (described below) to making sentences containing 4 synonym word and corresponding emotion or polarity. The result of combining these words produce sentences with 5 meaningful word that we use as input for our model. 
In next step after creating the model we test it with another labeled lexicon presented in the same collection but containing different words. We use words of this lexicon as a query on the model and compare word's score for the related emotion and the frequently of that emotion in related topic that our model chooses best fit for our query.

### Update - New testing approach
As described in result section our model failed to determine a proper topic for queries that include only a word. Our new approach is to feed queries with auto generated sentences using same lexicon. These sentences randomly include 4 or 5 words associated with a primary emotion and 1 or 2 words associated with a secondary emotion. For both primary and secondary emotion we randomly choose between related words in the lexicon. We assume that any unrelated word will be omitted before feeding our model for testing and also for training.

## NRC Sentiment and Emotion Lexicons 
The Sentiment and Emotion Lexicons is a collection of lexicons that was entirely created by the experts of the National Research Council of Canada. Developed with a wide range of applications, this lexicon collection can be used in a multitude of contexts such as sentiment analysis, product marketing, consumer behavior and even political campaign analysis. 
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

## Result | Queries with one word
For examination we track number of queries that the first and second related topics values for labeled emotion are bigger than some accept threshold. Plus that we track number of failed queries that neither first and second related topic are bigger than threshold. Here are the very first result for our model with 8 and 10 topics:

| Number of Topics | Success on First Topic | Success on Second Topic | Fail Queries |
|--|--|--|--|
| 8 | 1315 | 233 | 1455 |
| 10 | 1003 | 324 | 1676 |
*Number of Queries: 3003 words*

We easily can say our model totally failed to detect a topic relevant to word   queries. Our model failed very often but its not random. To be more precise about our decision over model failure we decide to test our model in different way. **What will happen if we use sentences instead of one word as queries** and then compare the score of emotions included in sentences and frequently score of that in the related topic?

## Generating Sentences
As described above our model failed to find the most related topics for queries that contain only one word. Before considering that our model doesn't totally works we decide to test it with queries that contain more than one words. We make a data-set of sentences with at least 5 and 7 most words that follows these types:

Any sentences has 2 part: primary and secondary
words between these two part will randomly placed anywhere in sentence

words divided into 4 group related to their score
   - words with 0.8 score or above:  **high**
   - words between 0.6 and 0.8:      **semi-high**
   - words between 0.4 and 0.6:      **semi-low**
   - words with 0.4 score or below:  **low**

types of primary part:
   - **4** high emotion words + **1** semi-high emotion word     (5 words)
   - **3** high emotion words + **2** semi-high emotion words    (5 words)
   - **4** high emotion words                                (4 words)
   - **3** high emotion words + **1** semi-high emotion word     (4 words)

type of secondary part:
   - **2** semi-low emotion words                        (2 words)
   - **1** semi-low emotion word + **1** low emotion word    (2 words)
   - **1** semi-low emotion word                         (1 word)
   - **1** low emotion word                              (1 word)

## Result | Sentences Queries
As our sentences, success/fail variables in this section separated in two part: Primary and Secondary. Just like last result there is two variable that count number of successful queries (queries that matched with their labels) in first or second most related topics that our model predict. Here is the result:
| Primary Emotion Query |  |
|--|--|
| Number of success on first topic | 27 |
| Number of success on second topic | 19 |
| Number of fails | 101 |

and for the secondary:

| Secondary Emotion Query |  |
|--|--|
| Number of success on first topic | 27 |
| Number of success on second topic | 22 |
| Number of fails | 98 |

## Conclusion 
Unfortunately our model failed to find related topics even with sentences queries. As far as it may seem there is no connection between the score of the labels in result queries topic and the actual label of test query in a LDA model that trained with synonym words plus their labels.

> This Report Written by Farzin Mohammdi with [StackEdit](https://stackedit.io/).

