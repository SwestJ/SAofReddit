from visualizer import *
from scraper import *
from analyser import *
import pytest as pytest

    
def test_sentiment():
    """Used to tes sentiment function"""
    sub_data = Submission('url', 
                      'title',
                      'selftext',
                      ['commment 1', 'comment 2'])
    data = {'a': {1: sub_data}, 'b': {1: sub_data}}
    names, scores, titles = sentiment(data, ['sentiment'])
    assert names
    assert scores
    assert titles
    assert len(names) == len(scores) and len(scores) == len(titles)

    
def test_lexical_diversity():
    """Used to test lexical diversity function"""
    sub_data = Submission('url', 
                          'title',
                          'selftext',
                          ['commment 1', 'comment 2'])
    data = {'a': {1: sub_data}, 'b': {1: sub_data}}
    names, scores, titles = lexical_diversity(data)
    assert names
    assert scores
    assert titles
    assert len(names) == len(scores) and len(scores) == len(titles)
    
def test_most_frequent_words():
    """Used to test most_frequent_words function"""
    sub_data = Submission('url', 
                          'title',
                          'selftext',
                          ['commment 1', 'comment 2'])
    data = {'a': {1: sub_data}, 'b': {1: sub_data}}
    names, freq_dists, titles = most_frequent_words(data)
    assert names
    assert freq_dists
    assert titles
    assert len(names) == len(freq_dists) and len(freq_dists) == len(titles)

    
def test_load_data():
    """Used to test load_data function"""
    data = load_data('sub-reddits.txt')
    assert data
    with pytest.raises(IOError):
        data = load_data('wrong_path')
