# -*- coding: utf-8 -*-
""" Responsible for downloading, saving and loading data. """

import praw
import cPickle as pickle
from submission import Submission

def load_data(filename):
    """
    Load reddit data from a filename.
    
    Returns a dictionary of dictionaries, with keys being the name of the respective sub-reddits.
    """
    with open('data/' + filename, 'rb') as subreddits:
        return dict((sub.strip(), pickle.load(
                open('data/' + sub.strip() + '.p', 'rb'))) for sub in subreddits)


def load_sent():
    """Load sentiment data."""
    return dict(map(lambda (k, v): (k, int(v)),
                    [line.split('\t') for line in open("AFINN/AFINN-111.txt", 'rb')]))


def scrape(username, password):
    """
    Mine data from reddit.
    
    -> username: Login to reddit with this username
    -> password: Password matching the given username
    """
    latest = ''
    try:
        reddit = praw.Reddit('Scraper bot for sentiment analysis v 1.0'
                    'Url: https://github.com/SwestJ/SAofReddit')
        
        reddit.login(username, password)
        
        subreddits = open('data/sub-reddits2.txt', 'rb')
        for sub in subreddits:
            data = dict()
            sub = sub.strip()
            subreddit = reddit.get_subreddit(sub)
            latest = sub
            for submission in subreddit.get_top_from_month(limit=10):
                print submission.title
                submission.replace_more_comments(limit=None, threshold=0)
                comments = [c.body for c in praw.helpers.flatten_tree(submission.comments)]
                sub_data = Submission(submission.url, 
                                      submission.title,
                                      submission.selftext,
                                      comments)
                data[submission.id] = sub_data
            
            pickle.dump(data, open(sub + '.p', 'wb'))
    except Exception as e:
        print e
        print latest

        
def resave_data():
    """Fix classname error."""
    subreddit = load_data()
    for name, posts in subreddit.items():
        data = dict()
        for sub_id, sub in posts.items():
            sub_data = Submission(sub.url,
                                  sub.title,
                                  sub.text,
                                  sub.comments)
            data[sub_id] = sub_data
            
        pickle.dump(data, open('data_new/' + name + '.p', 'wb'))


class UnknownWord:
    
    """Class for words without sentiment valence."""
    
    sub = ''
    value = 0
    
    def __init__(self, sub, value, average):
        """
        Create a new unknown word.
        
        sub = list of sub-reddits in which this word has been used
        
        value = average sentiment value per comment
        
        average = average sentiment value per word
        """
        self.sub = sub,
        self.value = value
        self.average = average