from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2018 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_dataset.

sourcenet_dataset is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_dataset is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet_dataset. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# ! ==> Imports
#================================================================================

# django imports
from django.db import models

# django encoding imports (for supporting 2 and 3).
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible

# taggit tagging APIs
from taggit.managers import TaggableManager

# import six for Python 2 and 3 compatibility.
import six

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data
from sourcenet.models import Abstract_Selected_Text


#================================================================================
# ! ==> Shared variables and functions
#================================================================================


#================================================================================
# ! ==> Models
#================================================================================


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

    # tags!
    tags = TaggableManager( blank = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __str__( self ):
        string_OUT = self.name
        return string_OUT

#= End DataSet Model ======================================================


# DataSetIdentifier model
@python_2_unicode_compatible
class DataSetIdentifier( models.Model ):

    dataset = models.ForeignKey( 'DataSet', on_delete = models.CASCADE )
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


# ArticleDataSet model
@python_2_unicode_compatible
class DataSetCitation( models.Model ):


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    # citation types
    CITATION_TYPE_MENTION = "mention"
    CITATION_TYPE_ANALYSIS = "analysis"
    CITATION_TYPE_DEFAULT = CITATION_TYPE_MENTION

    CITATION_TYPE_CHOICES = (
        ( CITATION_TYPE_MENTION, CITATION_TYPE_MENTION ),
        ( CITATION_TYPE_ANALYSIS, CITATION_TYPE_ANALYSIS ),
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

    # tags!
    tags = TaggableManager( blank = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------

    
    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( DataSetCitation, self ).__init__( *args, **kwargs )

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


#= END DataSetCitation Model ======================================================


# DataSetMention model
@python_2_unicode_compatible
class DataSetMention( Abstract_Selected_Text ):

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


    # associated citation
    data_set_citation = models.ForeignKey( 'DataSetCitation', on_delete = models.CASCADE, blank = True, null = True )
    
    # optional - who captured this?
    article_data = models.ForeignKey( Article_Data, on_delete = models.CASCADE, blank = True, null = True )
    
    # meta-data about mention
    mention_type = models.CharField( max_length = 255, choices = MENTION_TYPE_CHOICES, default = MENTION_TYPE_DEFAULT )

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
        
            string_OUT += " - " + str( self.data_set_citation )
        
        #-- END check to see if article_subject. --#
        
        # got associated quotation?...
        if ( self.value ):
        
            string_OUT += ": " + self.value
                
        #-- END check to see if we have a quotation. --#
        
        return string_OUT

    #-- END __str__() method --#
    
#= End DataSetMention Model ======================================================


