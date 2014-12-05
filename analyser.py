# -*- coding: utf-8 -*-
""" Contains functions for analysing output data from reddit. """

from __future__ import division
from collections import defaultdict
from nltk.collocations import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import scraper as scraper
import nltk as nltk
import cPickle as pickle
import copy as copy
import random


def fixer(comment, stop, stem):
    """
    String handling.
    
    Take a comment and removes stopwords and stems based on input, 
    also removes non-alphanumeric characters (except ') 
    and makes the entire comment lowercase.

    comment -> Piece of text to be altered

    stop -> Boolean to determine if stopwords should be removed

    stem -> Boolean to determine if stemming should be applied
    """
    token = nltk.RegexpTokenizer(r'[a-zA-Z]+\'[a-zA-Z]+|[a-zA-Z]+')

    comment = comment.lower()
    comment = ' '.join(token.tokenize(comment))

    if(stop):
        stopwords = set(nltk.corpus.stopwords.words('english'))
        split = filter(lambda word: word not in stopwords, comment.split())
        
        comment = ' '.join(split)
    
    if(stem):
        stemmer = nltk.stem.PorterStemmer()
        split = [stemmer.stem(word) for word in comment.split()]
        
        comment = ' '.join(split)
    
    return comment
        
def sentiment(subreddit, sentiment):
    """
    Sentiment analysis.
    
    Calculate and return the average sentiment for each thread with all comments concatenated
    
    -> subreddit: dictionary containing data from sub-reddits
    
    <- (names, scores_all, titles_all): Tuple of the names of the sub-reddits, 
    sentiment scores and titles of posts in each sub-reddit
    """
    scores_all = []
    names = []
    titles_all = []
    for name, data in subreddit.items():
        scores_subs = []
        titles_subs = []
        names.append(name)
        for sub_id, sub in data.items():
            comment_score = []
            for comment in sub.comments:
                words = comment.lower().split()
                words_in_sent = [word for word in words if word in sentiment]
                comment_score += [sum([sentiment.get(word) for word in words_in_sent])]
                
            score_filter = [score for score in comment_score if score not in range(-2, 3)]    
            total = sum(score_filter)
            length = len(score_filter) if score_filter else 1         
            scores_subs.append(total / length)
            titles_subs.append(sub.title)
            
        scores_all.append(scores_subs)
        titles_all.append(titles_subs)
        
    return names, scores_all, titles_all 

def lexical_diversity(subreddit):
    """
    Lexical diversity.
    
    Calculate and return the lexical diversity for each thread with all comments concatenated
    
    -> subreddit: dictionary containing data from sub-reddits
    
    <- (names, scores_all, titles_all): Tuple of the names of the sub-reddits, 
    lexical diversity scores and titles of posts in each sub-reddit
    """
    scores_all = []
    names = []
    titles_all = []
    for name, data in subreddit.items():
        scores_subs = []
        titles_subs = []
        names.append(name)
        for sub_id, sub in data.items(): 
            words = " ".join([fixer(comment, True, False) for comment in sub.comments]).split()
            lex_div = len(set(words)) / len(words)
            
            scores_subs.append(lex_div)
            titles_subs.append(sub.title)
        
        scores_all.append(scores_subs)
        titles_all.append(titles_subs)
        
    return names, scores_all, titles_all 
      
def most_frequent_words(subreddit):
    """
    Word counting.
    
    Returns the most frequent words for each sub-reddit
    
    -> subreddit: dictionary containing data from sub-reddits
    
    <- (names, freq_dists, titles_all): Tuple of the names of the sub-reddits, 
    frequency distributions and titles of posts in each sub-reddit
    """
    freq_dists = []
    names = []
    titles_all = []
    for name, data in subreddit.items()[-1:]:
        titles_subs = []
        all_words = ['']
        for sub_id, sub in data.items():
            all_words = " ".join([fixer(comment, True, False) 
                        for comment in sub.comments]).split()
            
            titles_subs.append(sub.title)            
            
        freq_dist = nltk.probability.FreqDist(all_words)
        names.append(name)
        titles_all.append(titles_subs)
        freq_dists.append(freq_dist)
    return names, freq_dists, titles_all

        
def collocations_bigram(stop=True, stem=True):
    """
    Topic mining.
    
    Collocations: multi-word expressions that commonly co-occur
    
    Calculate collocations for each thread with all comments concatenated
    """
    subreddit = scraper.load_data()
    
    bigram_measures = nltk.collocations.BigramAssocMeasures()

    for name, data in subreddit.items()[-2:]:
        print name
        for sub_id, sub in data.items(): 
            words = " ".join([fixer(comment, stop, stem) 
                        for comment in sub.comments]).split()
            finder = nltk.collocations.BigramCollocationFinder.from_words(words)
            finder.apply_freq_filter(4)
            collo = finder.nbest(bigram_measures.raw_freq, 5)
            print sub.title
            print collo
            
        print "\n"
        

def collocations_trigram(stop=True, stem=True):
    """
    Topic mining.
    
    Calculate collocations for each thread with all comments concatenated
    """
    subreddit = scraper.load_data()
    
    trigram_measures = nltk.TrigramAssocMeasures()
    
    for name, data in subreddit.items()[-2:]:
        print name
        for sub_id, sub in data.items(): 
            words = " ".join([fixer(comment, stop, stem) for comment in sub.comments]).split()
            finder = nltk.TrigramCollocationFinder.from_words(words)
            finder.apply_freq_filter(4)
            # Add filter function
            finder.apply_ngram_filter(lambda w1, w2, w3: 'the' == w3 or 'and' in (w1, w3))
            collo = finder.nbest(trigram_measures.raw_freq, 5)
            print sub.title
            print collo

        print "\n"
        

def collocations_ngram(n):
    """
    Topic mining.
    
    Calculate collocations for each thread with all comments concatenated.
    """
    subreddit = scraper.load_data()
    
    nltk.metrics.association.NgramAssocMeasures()

    for name, data in subreddit.items():
        print name
        for sub_id, sub in data.items(): 
            words = " ".join([comment for comment in sub.comments]).lower().split()
            ngrams = nltk.util.ngrams(words, n)
            freq_dist = nltk.probability.FreqDist(ngrams)
            print sub.title
            print [key for key, val in freq_dist.items() if val >= 4]

        print "\n"


def get_unknownwords(filename, stem):
    """
    Extended sentiment analysis.
    
    Find all words that do not have a sentiment classification (stopwords excluded).
    """
    subreddit = scraper.load_data('sub-reddits.txt')
    sentiment = scraper.load_sent(stem)
    
    unknowndict = defaultdict(list)
    
    for name, data in subreddit.items():
        print name
        for sub_id, sub in data.items():
            for comment in sub.comments:
                words = fixer(comment, True, stem).split()
                value = sum(map(lambda word: sentiment.get(word, 0), words))
                unknown = [word for word in words if word not in sentiment]
                for word in unknown:
                    unknowndict[word].append(UnknownWord(name, value, value / len(words)))
                    
    pickle.dump(unknowndict, open(filename + '.p', 'wb'))


def unknownsent(filename):
    r"""
    Extended sentiment analysis.
    
    Load words without a sentiment classification from a file 
    and return only a portion of them if, 
    they satisfy that they appear atleast 100 times, 
    and they have a collected sentiment-score higher than 5.
    
    -> filename: name of the file to load
    
    <- [(word, score), \S..]: list of tuples containing an unknown word 
    and its corresponding sentiment score
    """
    words = []

    for word, data in pickle.load(open('data/' + filename + '.p', 'rb')).items():
        if(len(data) > 100 and abs(sum([point.value for point in data]) / len(data)) > 5):
            words.append((word, sum([point.value for point in data]) / len(data)))

    return words


def unknowncoll(filename='unknownwords.p', stem=False):
    """
    Word cloud from sentiment analysis.
    
    Finds the bi-collocation of unknown words (words without sentiment) 
    and displays the 10 most common words based on frequency in a word-cloud, 
    colored green for words seen mostly in positive sentiments and red 
    for the opposite. Comparison is made on all comments concatenated
    
    -> filename: name of the file to load unknown words from
    -> stem: stem the words
    """
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    subreddits = scraper.load_data('sub-reddits.txt')
    fullcomment = []
    
    print 'building comment'
    for name, data in subreddits.items():
        for sub_id, sub in data.items():
            fullcomment += [fixer(comment, True, stem).split() for comment in sub.comments]

    print 'getting unknowns'
    unknownwords = unknownsent(filename)
    
    #flatten the comment structure
    fullcomment = [word for comment in fullcomment for word in comment]
    
    basefinder = BigramCollocationFinder.from_words(fullcomment)
    count = 0
    
    for unknown, unknownscore in unknownwords:
        finder = copy.copy(basefinder)
        
        print '\n' + unknown
        #only bigrams that contain the unknown word
        finder.apply_ngram_filter(lambda w1, w2: unknown != w1 and unknown != w2)
        
        wordcloud = WordCloud()
        wordcloud.font_path = 'C:\Windows\Fonts\comic.ttf'
        #trick the wordcloud to accept custom input
        wordcloud.generate('generate')
        
        colls = finder.score_ngrams(bigram_measures.raw_freq)
        colls = colls[:10]        
        maximum = colls[1][1]
        
        #generate the tuple (word, score) for the wordcloud
        cloudwords = [(word, score) for ((word, _), score) in colls if word != unknown]
        cloudwords += [(word, score) for ((_, word), score) in colls if word != unknown]
        
        #normalize the scores
        cloudwords = [(word, score / maximum) for (word, score) in cloudwords]
        
        #tricking part 2.
        wordcloud.fit_words(cloudwords)
        wordcloud.to_image()
        if(unknownscore > 0):
            wordcloud = wordcloud.recolor(color_func=green_color_func, random_state=3)
        else:
            wordcloud = wordcloud.recolor(color_func=red_color_func, random_state=3)
        
        count += 1
        plt.figure(count)
        plt.title(unknown)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('plots/' + unknown + '.png', bbox_inches='tight')
        plt.close()


def green_color_func(word, font_size, position, orientation, hue=None, random_state=None):
    """ Return a green color map for a wordcloud."""
    return "hsl(120, 100%%, %d%%)" % random.randint(30, 50)

    
def red_color_func(word, font_size, position, orientation, hue=None, random_state=None):
    """Return a red color map for a wordcloud."""
    return "hsl(0, 100%%, %d%%)" % random.randint(30, 50)