from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2018 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_dataset.

sourcenet_dataset is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_dataset is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet_dataset. If not, see http://www.gnu.org/licenses/.
'''

#===============================================================================
# ! ==> Imports
#===============================================================================

# django imports
from django.contrib.auth.models import User
from django.db import models

# django encoding imports (for supporting 2 and 3).
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible

# taggit tagging APIs
from taggit.managers import TaggableManager

# import six for Python 2 and 3 compatibility.
import six

# python_utilties
from python_utilities.strings.string_helper import StringHelper

# context imports
from context.models import Work_Log

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Abstract_Selected_Text
from sourcenet.models import AbstractSelectedArticleText


#===============================================================================
# ! ==> Shared variables and functions
#===============================================================================


#===============================================================================
# ! ==> Models
#===============================================================================


# AbstractScoredTeamTextData model
@python_2_unicode_compatible
class AbstractScoredTeamTextData( AbstractSelectedArticleText ):

    #---------------------------------------------------------------------------
    # model fields and meta
    #---------------------------------------------------------------------------

    # inherits from sourcenet.models.AbstractSelectedText:
    # basics - value, text before and after the value, length and index of value.
    #value = models.TextField( blank = True, null = True )
    #value_in_context = models.TextField( blank = True, null = True )
    #value_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_length = models.IntegerField( blank = True, null = True, default = 0 )
    #canonical_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_start = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_end = models.IntegerField( blank = True, null = True, default = 0 )
    #paragraph_number = models.IntegerField( blank = True, null = True, default = 0 )
    #context_before = models.TextField( blank = True, null = True )
    #context_after = models.TextField( blank = True, null = True )

    # score of match
    score = models.FloatField( blank = True, null = True )
    
    # team name
    team_name = models.CharField( max_length = 255, null = True, blank = True )

    # Meta-data for this class.
    class Meta:

        abstract = True
        
    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( AbstractScoredTeamTextData, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End WorkResearchMethod Model ================================================


# Data Set model
@python_2_unicode_compatible
class DataSet( models.Model ):

    #----------------------------------------------------------------------
    # ! --> model fields
    #----------------------------------------------------------------------

    name = models.CharField( max_length = 255 )
    unique_identifier = models.CharField( max_length = 255, blank = True, null = True )
    title = models.TextField( blank = True, null = True )
    description = models.TextField( blank = True, null = True )
    date = models.DateTimeField( blank = True, null = True )
    coverages = models.TextField( blank = True, null = True )
    subjects = models.TextField( blank = True, null = True )
    methodology = models.TextField( blank = True, null = True )
    citation = models.TextField( blank = True, null = True )
    additional_keywords = models.TextField( blank = True, null = True )
    family_identifier = models.CharField( max_length = 255, blank = True, null = True )
    parent_data_set = models.ForeignKey( 'DataSet', blank = True, null = True, on_delete = models.SET_NULL )

    # tags!
    tags = TaggableManager( blank = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __str__( self ):
        
        # return reference
        string_OUT = "";

        # declare variables
        prefix_string = ""
        
        if ( self.id ):
        
            # yes. output.
            string_OUT += str( self.id )
            prefix_string = " - "

        #-- END check to see if ID --#

        if ( self.title ):
        
            string_OUT += prefix_string + self.title
            prefix_string = " - "
            
        #-- END check to see if title. --#
            
        if ( self.unique_identifier ):
        
            string_OUT += prefix_string + " ( " + self.unique_identifier + " )"
            prefix_string = " - "
            
        #-- END check to see if unique_identifier. --#
            
        return string_OUT
        
    #-- END method __str__() --#
    
    
    def get_unique_mention_string_list( self, replace_white_space_IN = False, *args, **kwargs ):

        '''
        Retrieves all DataSetMention-s that relate to this DataSet, across
            all citations.  Builds and returns a set of the distinct strings
            used to refer to the dataset.
        '''
        
        # return reference
        mention_list_OUT = []
        
        # declare variables
        my_id = -1
        mention_set = set()
        data_set_citation_data_qs = None
        citation_data = None
        mention_qs = None
        mention = None
        mention_string = None
        
        # get citation data
        data_set_citation_data_qs = DataSetCitationData.objects.filter( data_set_citation__data_set = self )
        
        # for each citation data, get all mentions, and add the value of each
        #     to set.
        for citation_data in data_set_citation_data_qs:
        
            # get mentions
            mention_qs = citation_data.datasetmention_set.all()
            
            # for each mention, grab value and add to set if not already there.
            for mention in mention_qs:
            
                # get value
                mention_string = mention.value
                
                # is it in set?
                if ( mention_string not in mention_set ):
                
                    # are we replacing white space for javascript?
                    if ( replace_white_space_IN == True ):
                    
                        # replace more than one contiguous white space character
                        #     with a space.
                        mention_string = StringHelper.replace_white_space( mention_string )
                        
                    #-- END check if we unicode_escape --#
                
                    # no - add it.
                    mention_set.add( mention_string )
                    
                #-- END check to see if in set. --#
                
            #-- END loop over mentions. --#
            
        #-- END loop over citation data related to current data set --#
        
        # convert set to list.
        mention_list_OUT = list( mention_set )
        mention_list_OUT.sort()
        
        return mention_list_OUT

    #-- END method get_unique_mention_list() --#

#= End DataSet Model ======================================================


# DataSetIdentifier model
@python_2_unicode_compatible
class DataSetIdentifier( models.Model ):

    data_set = models.ForeignKey( 'DataSet', on_delete = models.CASCADE )
    name = models.CharField( max_length = 255, null = True, blank = True )
    identifier = models.TextField( blank = True, null = True )
    source = models.CharField( max_length = 255, null = True, blank = True )
    notes = models.TextField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # declare variables
        prefix_string = ""
        
        if ( self.id ):
        
            # yes. output.
            string_OUT += str( self.id )
            prefix_string = " - "

        #-- END check to see if ID --#

        if ( self.identifier ):
        
            string_OUT += prefix_string + self.identifier
            prefix_string = " - "
            
        #-- END check to see if identifier. --#
            
        if ( self.source ):
        
            string_OUT += prefix_string + " ( " + self.source + " )"
            prefix_string = " - "
            
        #-- END check to see if source. --#
            
        return string_OUT
        
    #-- END method __str__() --#


#= End Person_External_UUID Model ======================================================


# AbstractDataSetCitation model
@python_2_unicode_compatible
class AbstractDataSetCitation( models.Model ):


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    # citation types
    CITATION_TYPE_MENTION = "mention"
    CITATION_TYPE_ANALYSIS = "analysis"
    CITATION_TYPE_PROJECT = "project"
    CITATION_TYPE_STATISTIC = "statistic"
    CITATION_TYPE_DEFAULT = CITATION_TYPE_MENTION

    CITATION_TYPE_CHOICES = (
        ( CITATION_TYPE_MENTION, CITATION_TYPE_MENTION ),
        ( CITATION_TYPE_ANALYSIS, CITATION_TYPE_ANALYSIS ),
        ( CITATION_TYPE_PROJECT, CITATION_TYPE_PROJECT ),
        ( CITATION_TYPE_STATISTIC, CITATION_TYPE_STATISTIC )
    )


    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    article = models.ForeignKey( Article, on_delete = models.CASCADE )
    data_set = models.ForeignKey( 'DataSet', on_delete = models.CASCADE )
    citation_type = models.CharField( max_length = 255, choices = CITATION_TYPE_CHOICES, default = CITATION_TYPE_DEFAULT )

    # optional - who captured this?
    article_data = models.ForeignKey( Article_Data, on_delete = models.SET_NULL, blank = True, null = True )
    
    # details on automated matching, if attempted.
    # capture match confidence - start with 1 or 0, but leave room for
    #    decimal values.
    match_confidence_level = models.DecimalField( max_digits = 11, decimal_places = 10, blank = True, null = True, default = 0.0 )
    match_status = models.TextField( blank = True, null = True )

    # field to store how person was captured. - moved to Abstract_Person_Parent.
    capture_method = models.CharField( max_length = 255, blank = True, null = True )

    # notes
    notes = models.TextField( blank = True, null = True )

    # work log reference.
    work_log = models.ForeignKey( Work_Log, on_delete = models.SET_NULL, blank = True, null = True )
        
    # tags!
    tags = TaggableManager( blank = True )

    # score of match
    score = models.FloatField( blank = True, null = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True
        
    #-- END class Meta --#

    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------

    
    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( AbstractDataSetCitation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if id --#
        
        if ( self.article is not None ):
        
            string_OUT += " - article: {}".format( self.article.id )
        
        else:
        
            string_OUT += ' - no article?'
        
        #-- END check to see if article. --#
        
        if ( self.data_set is not None ):
        
            string_OUT += " - data set: {}".format( self.data_set.id )
        
        else:
        
            string_OUT += ' - no data set?'
        
        #-- END check to see if data set. --#
        
        return string_OUT
    
    #-- END method __str__() --#


    def get_article_id( self ):

        '''
        Returns ID of article associated with this record.
        '''

        # return reference
        id_OUT = ''

        # declare variables
        my_record = None

        # get associated record.
        my_record = self.article

        # see if there is a record
        if ( my_record is not None ):

            # retrieve and return ID.
            id_OUT = my_record.id

        #-- END check to make sure there is an associated person.

        return id_OUT

    #-- END method get_article_id() --#


    def get_data_set_id( self ):

        '''
        Returns ID of data set associated with this record.
        '''

        # return reference
        id_OUT = ''

        # declare variables
        my_record = None

        # get associated record.
        my_record = self.data_set

        # see if there is a record
        if ( my_record is not None ):

            # retrieve and return ID.
            id_OUT = my_record.id

        #-- END check to make sure there is an associated person.

        return id_OUT

    #-- END method get_data_set_id() --#


    def get_unique_mention_string_list( self, replace_white_space_IN = False, *args, **kwargs ):

        '''
        Retrieves all DataSetMention-s that relate to this DataSetCitation. 
            Builds and returns a set of the distinct strings used to refer to
            the dataset.
        '''
        
        # return reference
        mention_list_OUT = []
        
        # declare variables
        my_id = -1
        mention_set = set()
        data_set_citation_data_qs = None
        citation_data = None
        mention_qs = None
        mention = None
        mention_string = None
        
        # get citation data
        data_set_citation_data_qs = DataSetCitationData.objects.filter( data_set_citation = self )
        
        # for each citation data, get all mentions, and add the value of each
        #     to set.
        for citation_data in data_set_citation_data_qs:
        
            # get mentions
            mention_qs = citation_data.datasetmention_set.all()
            
            # for each mention, grab value and add to set if not already there.
            for mention in mention_qs:
            
                # get value
                mention_string = mention.value
                
                # is it in set?
                if ( mention_string not in mention_set ):
                
                    # are we replacing white space?
                    if ( replace_white_space_IN == True ):
                    
                        # replace more than one contiguous white space character
                        #     with a space.
                        mention_string = StringHelper.replace_white_space( mention_string )
                        
                    #-- END check if we unicode_escape --#
                
                    # no - add it.
                    mention_set.add( mention_string )
                    
                #-- END check to see if in set. --#
                
            #-- END loop over mentions. --#
            
        #-- END loop over citation data related to current data set --#
        
        # convert set to list.
        mention_list_OUT = list( mention_set )
        mention_list_OUT.sort()
        
        return mention_list_OUT

    #-- END method get_unique_mention_list() --#

#= END DataSetCitation Model ======================================================


# DataSetCitation model
@python_2_unicode_compatible
class DataSetCitation( AbstractDataSetCitation ):
    
    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataSetCitation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END class DataSetCitation --#


# DataSetCitationData model
@python_2_unicode_compatible
class DataSetCitationData( models.Model ):

    # mention types
    MENTION_TYPE_MENTION = DataSetCitation.CITATION_TYPE_MENTION
    MENTION_TYPE_ANALYSIS = DataSetCitation.CITATION_TYPE_ANALYSIS
    MENTION_TYPE_DEFAULT = MENTION_TYPE_ANALYSIS

    MENTION_TYPE_CHOICES = (
        ( MENTION_TYPE_MENTION, MENTION_TYPE_MENTION ),
        ( MENTION_TYPE_ANALYSIS, MENTION_TYPE_ANALYSIS ),
    )


    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------


    # who captured this?
    article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    # associated citation
    data_set_citation = models.ForeignKey( 'DataSetCitation', on_delete = models.CASCADE, blank = True, null = True )
    
    # meta-data about mention
    citation_type = models.CharField( max_length = 255, choices = MENTION_TYPE_CHOICES, default = MENTION_TYPE_DEFAULT )

    # work log reference.
    work_log = models.ForeignKey( Work_Log, on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # declare variables
        details_list = []
        
        # got id?
        if ( self.id ):
        
            string_OUT = str( self.id )
            
        #-- END check for ID. --#

        if ( self.data_set_citation ):
        
            string_OUT += " - Citation: {}".format( str( self.data_set_citation ) )
        
        #-- END check to see if article_subject. --#
        
        # got associated quotation?...
        if ( self.article_data ):
        
            string_OUT += "; Article_Data: {}".format( str( self.article_data ) )
                
        #-- END check to see if we have a quotation. --#
        
        return string_OUT

    #-- END __str__() method --#
    
#= End DataSetCitationData Model ======================================================


# AbstractDataMention model
@python_2_unicode_compatible
class AbstractDataMention( AbstractScoredTeamTextData ):

    # mention types
    MENTION_TYPE_MENTION = DataSetCitation.CITATION_TYPE_MENTION
    MENTION_TYPE_ANALYSIS = DataSetCitation.CITATION_TYPE_ANALYSIS
    MENTION_TYPE_DEFAULT = MENTION_TYPE_MENTION

    MENTION_TYPE_CHOICES = (
        ( MENTION_TYPE_MENTION, MENTION_TYPE_MENTION ),
        ( MENTION_TYPE_ANALYSIS, MENTION_TYPE_ANALYSIS ),
    )


    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    # inherited from AbstractSelectedArticleText:
    # associated article
    #article = models.ForeignKey( Article, on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this at the article level?
    #article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    # associated citation
    data_set_citation = models.ForeignKey( 'DataSetCitation', on_delete = models.CASCADE, blank = True, null = True )
    
    # associated citation data
    data_set_citation_data = models.ForeignKey( 'DataSetCitationData', on_delete = models.CASCADE, blank = True, null = True )
    
    # meta-data about mention
    mention_type = models.CharField( max_length = 255, choices = MENTION_TYPE_CHOICES, default = MENTION_TYPE_DEFAULT )
    
    # score of match
    score = models.FloatField( blank = True, null = True )

    # work log reference.
    work_log = models.ForeignKey( Work_Log, on_delete = models.SET_NULL, blank = True, null = True )
        
    # tags!
    tags = TaggableManager( blank = True )

    # Meta-data for this class.
    class Meta:

        abstract = True
        
    #-- END class Meta --#


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( AbstractDataMention, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    def __str__( self ):
        
        # return reference
        string_OUT = ""
        
        # declare variables
        details_list = []
        
        # got id?
        if ( self.id ):
        
            string_OUT = str( self.id )
            
        #-- END check for ID. --#

        if ( self.article ):
        
            string_OUT += " - pub. ID: {}".format( self.article.id )
        
        #-- END check to see if article. --#
        
        if ( self.data_set_citation ):
        
            string_OUT += " - " + str( self.data_set_citation )
        
        #-- END check to see if article_subject. --#
        
        # got associated quotation?...
        if ( self.value ):
        
            string_OUT += ": " + self.value
                
        #-- END check to see if we have a quotation. --#
        
        return string_OUT

    #-- END __str__() method --#
    
#= End AbstractDataMention Model ======================================================


# DataSetMention model
@python_2_unicode_compatible
class DataSetMention( AbstractDataMention ):

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataSetMention, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End DataSetMention Model ======================================================


# WorkDataSetCitation model
@python_2_unicode_compatible
class WorkDataSetCitation( AbstractDataSetCitation ):
    
    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    # team name
    team_name = models.CharField( max_length = 255, null = True, blank = True )

    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( WorkDataSetCitation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END WorkDataSetCitation Model --#


# WorkDataSetMention model
@python_2_unicode_compatible
class WorkDataSetCitationMention( AbstractDataMention ):

    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    # associated article
    article = models.ForeignKey( Article, on_delete = models.CASCADE )
    
    # associated WorkDataSetCitation
    work_data_set_citation = models.ForeignKey( 'WorkDataSetCitation', on_delete = models.CASCADE, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( WorkDataSetCitationMention, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
    
#= End WorkDataSetCitationMention Model ======================================================


# WorkDataSetMention model
@python_2_unicode_compatible
class WorkDataSetMention( AbstractDataMention ):

    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------


    # associated article
    article = models.ForeignKey( Article, on_delete = models.CASCADE )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( WorkDataSetMention, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    

#= End WorkDataSetMention Model ======================================================


# WorkResearchField model
@python_2_unicode_compatible
class WorkResearchField( AbstractScoredTeamTextData ):

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( WorkResearchField, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End WorkResearchField Model ======================================================


# WorkResearchMethod model
@python_2_unicode_compatible
class WorkResearchMethod( AbstractScoredTeamTextData ):

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( WorkResearchMethod, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End WorkResearchMethod Model ================================================


# DataReference model
@python_2_unicode_compatible
class DataReference( AbstractDataSetCitation ):

    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------


    # title
    title = models.TextField( blank = True, null = True )
    
    # data set link is optional, and want to keep reference if data set deleted.
    data_set = models.ForeignKey( 'DataSet', on_delete = models.SET_NULL, blank = True, null = True )
    related_data_sets = models.ManyToManyField( DataSet, related_name = "related_data_set_set" )
    
    # key terms
    key_terms = models.TextField( blank = True, null = True )
    
    # context text
    context_text = models.TextField( blank = True, null = True )
    
    # optional coder information - try to track coder through Article_Data.
    coder = models.ForeignKey( User, on_delete = models.CASCADE, blank = True, null = True )
    coder_type = models.CharField( max_length = 255, blank = True, null = True )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataReference, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):
        
        # return reference
        string_OUT = ""
        related_data_set_qs = None
        data_set = None
        data_set_id_list = None
        
        if ( self.id ):
        
            string_OUT += str( self.id )
            
        #-- END check to see if id --#
        
        if ( self.article is not None ):
        
            string_OUT += " - article: {}".format( self.article.id )
        
        else:
        
            string_OUT += ' - no article?'
        
        #-- END check to see if article. --#
        
        # related_data_sets
        related_data_set_qs = self.related_data_sets.all()
        if ( related_data_set_qs.count() > 0 ):
            
            string_OUT += "- related_data_sets:"
            data_set_id_list = []
            for data_set in related_data_set_qs:
            
                # get id and add to list.
                data_set_id = data_set.id
                data_set_id_list.append( str( data_set_id ) )
                
            #-- END loop over related data sets. --#
            
            # append list to string_OUT
            string_OUT += ", ".join( data_set_id_list )
        
        else:
        
            string_OUT += " - no related_data_sets"
        
        #-- END check to see if data sets --#
        
        if ( self.data_set is not None ):
        
            string_OUT += " - data set: {}".format( self.data_set.id )
        
        else:
        
            string_OUT += ' - no data_set'
        
        #-- END check to see if data set. --#
        
        return string_OUT
    
    #-- END method __str__() --#


    # just use the stuff in the parent class.
    
#-- END class DataReference --#


# DataMention model
@python_2_unicode_compatible
class DataReferenceMention( AbstractDataMention ):

    #----------------------------------------------------------------------------
    # inheritance
    #----------------------------------------------------------------------------

    # we inherit from sourcenet.models.AbstractSelectedText:
    # basics - value, text before and after the value, length and index of value.
    #value = models.TextField( blank = True, null = True )
    #value_in_context = models.TextField( blank = True, null = True )
    #value_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_length = models.IntegerField( blank = True, null = True, default = 0 )
    #canonical_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_start = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_end = models.IntegerField( blank = True, null = True, default = 0 )
    #paragraph_number = models.IntegerField( blank = True, null = True, default = 0 )
    #context_before = models.TextField( blank = True, null = True )
    #context_after = models.TextField( blank = True, null = True )

    # inherited from AbstractSelectedArticleText:
    # associated article
    #article = models.ForeignKey( Article, on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this at the article level?
    #article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    
    # associated citation
    #data_set_citation = models.ForeignKey( 'DataSetCitation', on_delete = models.CASCADE, blank = True, null = True )
    
    # associated citation data
    #data_set_citation_data = models.ForeignKey( 'DataSetCitationData', on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this at the article level?
    #article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    # meta-data about mention
    #mention_type = models.CharField( max_length = 255, choices = MENTION_TYPE_CHOICES, default = MENTION_TYPE_DEFAULT )
    
    # score of match
    #score = models.FloatField( blank = True, null = True )

    # work log reference.
    #work_log = models.ForeignKey( Work_Log, on_delete = models.SET_NULL, blank = True, null = True )
        
    # tags!
    #tags = TaggableManager( blank = True )
    

    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    
    # data reference link, want to delete mentions if linked reference is
    #    deleted.
    data_reference = models.ForeignKey( "DataReference", on_delete = models.CASCADE, blank = True, null = True )
    
    # ==> need some way to pinpoint location
    
    # in addition to inheritance from sourcenet.models.AbstractSelectedText:
    start_index = models.IntegerField( blank = True, null = True )
    occurrence_number = models.IntegerField( blank = True, null = True )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataReferenceMention, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End DataReferenceMention Model ======================================================


# DataMention model
@python_2_unicode_compatible
class DataReferenceContext( AbstractDataMention ):

    #----------------------------------------------------------------------------
    # inheritance
    #----------------------------------------------------------------------------

    # we inherit from sourcenet.models.AbstractSelectedText:
    # basics - value, text before and after the value, length and index of value.
    #value = models.TextField( blank = True, null = True )
    #value_in_context = models.TextField( blank = True, null = True )
    #value_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_length = models.IntegerField( blank = True, null = True, default = 0 )
    #canonical_index = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_start = models.IntegerField( blank = True, null = True, default = 0 )
    #value_word_number_end = models.IntegerField( blank = True, null = True, default = 0 )
    #paragraph_number = models.IntegerField( blank = True, null = True, default = 0 )
    #context_before = models.TextField( blank = True, null = True )
    #context_after = models.TextField( blank = True, null = True )

    # inherited from AbstractSelectedArticleText:
    # associated article
    #article = models.ForeignKey( Article, on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this at the article level?
    #article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    
    # associated citation
    #data_set_citation = models.ForeignKey( 'DataSetCitation', on_delete = models.CASCADE, blank = True, null = True )
    
    # associated citation data
    #data_set_citation_data = models.ForeignKey( 'DataSetCitationData', on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this at the article level?
    #article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    # meta-data about mention
    #mention_type = models.CharField( max_length = 255, choices = MENTION_TYPE_CHOICES, default = MENTION_TYPE_DEFAULT )
    
    # score of match
    #score = models.FloatField( blank = True, null = True )

    # work log reference.
    #work_log = models.ForeignKey( Work_Log, on_delete = models.SET_NULL, blank = True, null = True )
        
    # tags!
    #tags = TaggableManager( blank = True )
    

    #----------------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------------

    
    # data reference link, want to delete mentions if linked reference is
    #    deleted.
    data_reference = models.ForeignKey( "DataReference", on_delete = models.CASCADE, blank = True, null = True )
    
    # ==> need some way to pinpoint location
    
    # in addition to inheritance from sourcenet.models.AbstractSelectedText:
    start_index = models.IntegerField( blank = True, null = True )
    occurrence_number = models.IntegerField( blank = True, null = True )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataReferenceContext, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#= End DataReferenceContext Model ======================================================

