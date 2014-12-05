# -*- coding: utf-8 -*-
""" Contains functions for visualizing data. """

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

import analyser as anl
import scraper as scraper


def analyse_lexical():
    """
    Runner script.
    
    Loads data, retrieves lexical diversity scores and plots them
    """
    try:
        subreddit = scraper.load_data('sub-reddits.txt')
    except IOError as e:
        print e
        return
    
    names, scores, titles = anl.lexical_diversity(subreddit)
    plot_bar_avg(names, scores)
    plot_bar(names, scores)
    
def analyse_sentiment():
    """
    Runner script.
    
    Loads data, retrieves sentiment scores and plots them
    """
    try:
        subreddit = scraper.load_data('sub-reddits.txt')
    except IOError as e:
        print e
        return
        
    try:
        sentiments = scraper.load_sent()
    except IOError as e:
        print e
        return
    
    names, scores, titles = anl.sentiment(subreddit, sentiments)
    
    plot_bar_avg(names, scores)
    plot_bar(names, scores)

    
def compare_freqs():
    """
    Runner script.
    
    Loads data, retrieves word frequency distributions and plots them
    """
    try:
        subreddit = scraper.load_data('sub-reddits.txt')
    except IOError as e:
        print e
        return
    
    names, freq_dists, titles = anl.most_frequent_words(subreddit)    
    
    plot_bar_compare_freqs(names, freq_dists)

def compare_sent_lex():
    """
    Runner script.
    
    Loads data, retrieves sentiment and lexical scores and plots them
    """
    try:
        subreddit = scraper.load_data('sub-reddits.txt')
    except IOError as e:
        print e
        return
        
    try:
        sentiments = scraper.load_sent()
    except IOError as e:
        print e
        return
    
    names, scores1, titles = anl.sentiment(subreddit, sentiments)
    _, scores2, _ = anl.lexical_diversity(subreddit)
    
    plot_bar_compare_avg(names, scores1, scores2)

def plot_bar_compare_freqs(names, freq_dists):  
    """
    Cummulative distribution.
    
    Plots the cummulative distribution of all frequency distributions
    
    -> name: Names of sub-reddits
    -> freq_dists: A list of frequency distributions
    """
    fig, ax = plt.subplots(nrows=2, ncols=5)
    
    ax_list = ax.tolist()
    ax_list = [item for sublist in ax_list for item in sublist]
    
#    width = 0.35
    for freq_dist, name, ax in zip(freq_dists, names, ax_list):
        freq_values = sorted(freq_dist.values(), reverse=True)
        nr_of_words = sum(freq_dist.values())
        
        percents = [value / nr_of_words for value in freq_values]
        cum_dist = []
        s = 0
        for p in percents:
            s = s + p
            cum_dist.append(s)
#        minimum = min(freq_values)
        maximum = max(cum_dist)
#        norm_scores = [(score - minimum) / (maximum - minimum) for score in subscores1]
#        ax.bar(np.arange(len(freq_values)), freq_values, width, color='black')
        ax.plot(np.arange(len(cum_dist)), cum_dist)
        ax.set_title(name)
#        print cum_dist
#        ax.set_xlim(-2 * width, len(freq_values)+2*width)
        ax.set_ylim(0, maximum)
    
    plt.show()


def plot_bar_compare_avg(names, scores1, scores2):
    """
    Bar graph.

    Normalizes the mean of the data for each sub-reddit.
    Plots the results in a bar graph
    
    -> name: Names of sub-reddits
    -> scores1: Nested lists containing data for each post for each sub-reddit
    -> scores2: Nested lists containing data for each post for each sub-reddit
    """   
    averages1 = np.average(scores1, axis=1)
    averages2 = np.average(scores2, axis=1)
    
    minimum = min(averages1)
    maximum = max(averages1)
    norm_averages1 = [(score - minimum) / (maximum - minimum) for score in averages1]
    minimum = min(averages2)
    maximum = max(averages2)
    norm_averages2 = [(score - minimum) / (maximum - minimum) for score in averages2]
    width = 0.35
    indent = np.arange(len(averages1))
    ax = plt.axes()
    rects1 = ax.bar(np.arange(len(scores1)), norm_averages1, width, color='black')
    rects2 = ax.bar(np.arange(len(scores2)) + width, norm_averages2, width, color='red')
    
    ax.set_xlim(-0.5 * width, len(indent) + 0.5 * width)
    ax.set_ylim(0, 1.2)
    
    ax.set_xticks(indent + 0.5 * width)
    ax.set_xticklabels(names, rotation=45)
    ax.legend((rects1[0], rects2[0]), ('Sentiment', 'Lexical diversity'))
    
    
    plt.show()

def plot_bar_avg(names, scores):
    """
    Bar graph.
    
    Plots the mean of scores for each sub-reddit
    
    -> name: Names of sub-reddits
    -> scores: Nested lists containing data for each post for each sub-reddit
    """
    averages = np.average(scores, axis=1)
    indent = np.arange(len(averages))
    width = 0.7
    rects = plt.bar(indent, averages, width=width)
    ax = plt.axes()
    ax.set_xticklabels(names, rotation=45)
    ax.set_xticks(indent + 0.4 * width)
    ax.set_xlim(-0.5 * width, 0.5 * width + len(indent))
    ax.set_ylim(min(averages) - 0.5, max(averages) + 0.5)
    ax.set_ylabel('Average sentiment')
    ax.legend((rects[0],), ('Average sentiment',))
    plt.show()


def plot_bar(names, scores):  
    """
    Bar graph.
    
    Plots data for all posts in a bar graph
    
    -> name: Names of sub-reddits
    -> scores: Nested lists containing data for each post for each sub-reddit
    """
    fig, ax = plt.subplots(nrows=1, ncols=10, sharey='row')
    
    ax_list = ax.tolist()

#    ax_list = [item for sublist in ax_list for item in sublist]
    
    for subscores, name, ax in zip(scores, names, ax_list):
        ax.bar(np.arange(len(subscores)), subscores, 0.35, color='black')
        ax.set_title(name)
        ax.set_xticks([])
    
    plt.show()
    

def plot_bar_compare(names, scores1, scores2):   
    """
    Bar graph.
    
    Plots normalized data for all posts in a bar graph, comparing two sets of data
    
    -> name: Names of sub-reddits
    -> scores1: Nested lists containing data for each post for each sub-reddit
    -> scores2: Nested lists containing data for each post for each sub-reddit
    """
    fig, ax = plt.subplots(nrows=2, ncols=5, sharey='row')
    
    ax_list = ax.tolist()
    ax_list = [item for sublist in ax_list for item in sublist]
    
    width = 0.35
    for subscores1, subscores2, name, ax in zip(scores1, scores2, names, ax_list):
        minimum = min(subscores1)
        maximum = max(subscores1)
        norm_scores1 = [(score - minimum) / (maximum - minimum) for score in subscores1]
        minimum = min(subscores2)
        maximum = max(subscores2)
        norm_scores2 = [(score - minimum) / (maximum - minimum) for score in subscores2]
        
        ax.bar(np.arange(len(subscores1)), norm_scores1, width, color='black')
        ax.bar(np.arange(len(subscores2)) + width, norm_scores2, width, color='red')
        ax.set_title(name)
        ax.set_xticks([])
        ax.set_xlim(-2 * width, len(subscores1) + 2 * width)
    
    plt.show()
    