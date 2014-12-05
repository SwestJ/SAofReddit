# -*- coding: utf-8 -*-
""" Contains the class used to store reddit data. """


class Submission:
    
    """Class for a reddit submission."""
    
    url = ''
    title = ''
    text = ''
    comments = []
    
    def __init__(self, url, title, text, comments):
        """
        Create a new submission.
        
        url = the exact address of this submission
        
        text = the content of this submission
        
        title = the title of this submission
        
        comments = list of all comments made on this submission
        """
        self.url = url
        self.text = text
        self.title = title
        self.comments = comments