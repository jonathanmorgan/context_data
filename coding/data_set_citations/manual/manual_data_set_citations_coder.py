from __future__ import unicode_literals

'''
Copyright 2010-2015 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_data.

context_data is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_data. If not, see http://www.gnu.org/licenses/.
'''

'''
This code file contains a class that implements functions for interacting with
   the Open Calais natural language processing API.  It includes methods for
   interacting with the Open Calais REST API and for processing the JSON response
   that the Open Calais REST API returns.

Configuration properties for it are stored in django's admins, in the
   django_config application.  The properties are stored in Application
   "OpenCalais_REST_API_v1":
   - open_calais_api_key - API key for accessing OpenCalais version 1 API.
   - submitter - submitter you want to report to the API.
'''

#================================================================================
# Imports
#================================================================================


# python standard libraries
import json
import sys

# mess with python 3 support
import six

# other imports
import regex

# django imports
from django.core.exceptions import MultipleObjectsReturned

# python utilities
from python_utilities.django_utils.django_string_helper import DjangoStringHelper
from python_utilities.json.json_helper import JSONHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.network.http_helper import Http_Helper
from python_utilities.sequences.sequence_helper import SequenceHelper
from python_utilities.strings.string_helper import StringHelper

# context_text classes

# shared
from context_text.shared.context_text_base import ContextTextBase

# models
from context_text.models import Article_Data
from context_text.models import Article_Data_Notes
from context_text.models import Article_Text

# parent abstract class.
from context_text.article_coding.article_coder import ArticleCoder

# context_data classes
from context_data.models import DataSetMention
from context_data.models import DataSetCitationData


#================================================================================
# Package constants-ish
#================================================================================


#================================================================================
# ManualDataSetCitationsCoder class
#================================================================================

class ManualDataSetCitationsCoder( ArticleCoder ):

    '''
    This class is a helper for coding articles manually.
    '''

    #============================================================================
    # ! ==> Constants-ish
    #============================================================================
    

    # status constants - in parent (ArticleCoder) now:
    # STATUS_SUCCESS = "Success!"
    # STATUS_ERROR_PREFIX = "Error: "
    
    # logging
    LOGGER_NAME = "context_data.coding.data_set_citations.manual.manual_data_set_citations_coder"
    
    # config application
    CONFIG_APPLICATION = "Manual_Data_Set_Citations_Coding"
    CONFIG_NAME_ARTICLE_TEXT_RENDER_TYPE = ContextTextBase.DJANGO_CONFIG_PROP_ARTICLE_TEXT_RENDER_TYPE
    CONFIG_NAME_ARTICLE_TEXT_IS_PREFORMATTED = ContextTextBase.DJANGO_CONFIG_PROP_ARTICLE_TEXT_IS_PREFORMATTED
    CONFIG_NAME_ARTICLE_TEXT_WRAP_IN_P = ContextTextBase.DJANGO_CONFIG_PROP_ARTICLE_TEXT_WRAP_IN_P
    CONFIG_NAME_MENTION_TEXT_READ_ONLY = "mention_text_read_only"
    CONFIG_NAME_INCLUDE_FIND_IN_ARTICLE_TEXT = "include_find_in_article_text"
    CONFIG_NAME_DEFAULT_FIND_LOCATION = "default_find_location"
    CONFIG_NAME_IGNORE_WORD_LIST = "ignore_word_list"
    CONFIG_NAME_HIGHLIGHT_WORD_LIST = "highlight_word_list"
    CONFIG_NAME_DEFAULT_FIND_LOCATION = "default_find_location"
    CONFIG_NAME_BE_CASE_SENSITIVE = "be_case_sensitive"
    CONFIG_NAME_PROCESS_FOUND_SYNONYMS = "process_found_synonyms"
    CONFIG_NAME_SYNCHRONIZE_DATA_SET_FAMILIES = "synchronize_data_set_families"

    # kwarg parameter names
    KWARG_DATA_STORE_JSON_STRING = "data_store_json_string_IN"
    KWARG_ARTICLE_DATA_ID = "article_data_id_IN"
    KWARG_REQUEST = "request_IN"
    KWARG_RESPONSE_DICTIONARY = "response_dictionary_IN"

    # data store JSON property names (corresponds to "DataStore" javascript class in mention-coding.js)
    DATA_STORE_PROP_MENTION_ARRAY = "mention_array"
    DATA_STORE_PROP_NEXT_MENTION_INDEX = "next_mention_index"
    DATA_STORE_PROP_STATUS_MESSAGE_ARRAY = "status_message_array"
    DATA_STORE_PROP_LATEST_MENTION_INDEX = "latest_mention_index"
    
    # mention JSON property names (corresponds to "Mention" javascript class in mention-coding.js)
    DATA_STORE_PROP_MENTION_TEXT = "mention_text"
    DATA_STORE_PROP_FIXED_MENTION_TEXT = "fixed_mention_text"
    DATA_STORE_PROP_MENTION_TYPE = "mention_type"
    DATA_STORE_PROP_MENTION_INDEX = "mention_index"
    DATA_STORE_PROP_ORIGINAL_MENTION_TYPE = "original_mention_type"
    DATA_STORE_PROP_DATA_SET_MENTION_ID = "data_set_mention_id"    
        
    # mention types
    MENTION_TYPE_CITED = "cited"
    MENTION_TYPE_ANALYZED = "analyzed"
    
    # props for dictionary returned when getting Article_Data for article/user
    #    pair
    PROP_CITATION_DATA = "citation_data"

    #--------------------------------------------------------------------------#
    # HTML element IDs
    #--------------------------------------------------------------------------#

    DIV_ID_MENTION_CODING = "mention-coding"
    INPUT_ID_MENTION_TEXT = "mention-text"
    INPUT_ID_MENTION_TYPE = "mention-type"
    INPUT_ID_FIXED_MENTION_TEXT = "fixed-mention-text"
    INPUT_ID_DATA_SET_MENTION_ID = "data-set-mention-id"
    INPUT_ID_ORIGINAL_MENTION_TYPE = "original-mention-type"
    INPUT_ID_DATA_STORE_MENTION_INDEX = "data-store-mention-index"
    INPUT_ID_TEXT_TO_FIND_IN_ARTICLE = "text-to-find-in-article"
    
    # HTML elements - form submission
    INPUT_ID_SUBMIT_ARTICLE_CODING = "input-submit-article-coding";
    INPUT_ID_DATA_STORE_JSON = "id_data_store_json";
    
    # HTML elements - django-ajax-select HTML
    INPUT_ID_AJAX_ID_PERSON = "id_person";
    INPUT_ID_AJAX_ID_PERSON_TEXT = "id_person_text";
    DIV_ID_AJAX_ID_PERSON_ON_DECK = "id_person_on_deck";
    
    # HTML elements - find in text
    INPUT_ID_TEXT_TO_FIND_IN_ARTICLE = "text-to-find-in-article";


    #==========================================================================#
    # NOT Instance variables
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #==========================================================================#

    
    # declare variables
    #http_helper = None
    #content_type = ""
    #output_format = ""


    #==========================================================================#
    # ! ==> Constructor
    #==========================================================================#


    def __init__( self ):

        # call parent's __init__() - I think...
        super( ManualDataSetCitationsCoder, self ).__init__()
        
        # declare variables
        
        # set application string (for LoggingHelper parent class: (LoggingHelper -->
        #    BasicRateLimited --> ArticleCoder --> OpenCalaisArticleCoder).
        self.set_logger_name( self.LOGGER_NAME )
        
        # items for processing a given JSON response - should be updated with
        #    every new article coded.
        
        # coder type (defaults to self.CONFIG_APPLICATION).
        self.coder_type = self.CONFIG_APPLICATION

        # most recent Article_Data instance.
        self.latest_article_data = None
        
    #-- END method __init__() --#


    #==========================================================================#
    # ! ==> Class methods
    #==========================================================================#


    @classmethod
    def convert_article_data_to_data_store_json( cls, article_data_IN, return_string_IN = False ):

        '''
        Accepts Article_Data instance we want to convert to data store JSON and
            the citation that will tell us which data set we want mentions of.
            Retrieves DataSetMentions for data set referenced by citation 
            instance and makes JSON out of them.

        Returns Article_Data citation mention information in JSON format, either
            in dictionaries and lists (object format), or string JSON.
        '''

        # return reference
        json_OUT = ""

        # declare variables
        me = "convert_article_data_to_data_store_json"
        local_debug_flag = True
        status_message_list = []
        debug_message = ""
        mention_array_list = []
        text_to_mention_index_dict = {}
        data_store_dict = None
        get_citation_data_result = None
        citation_data = None
        citation_get_status = None
        citation_get_status_message = None
        data_set_mention_qs = None
        current_data_set_mention = None
        current_mention_text = ""
        current_mention_dict = None
        mention_index = -1
        
        # declare variables - logging
        my_resource_string = ""
        
        # local debug on?
        if ( local_debug_flag == True ):

            # initialize resource string and add it to the LoggingHelper class-level
            #     string.
            my_resource_string = cls.LOGGER_NAME + "." + me
            LoggingHelper.add_to_class_resource_string( my_resource_string )
            
        #-- END check to see if local debug on. --#

        # init data_store_dict.
        data_store_dict = {}

        # first, make sure we have something in article_data_IN.
        if ( ( article_data_IN is not None ) and ( article_data_IN != "" ) ):
        
            # we have Article_Data - do we have a citation instance?
            if ( citation_instance_IN is not None ):
            
                # we have Article_Data - First get DataSetCitation Data
                get_citation_data_result = cls.get_article_data_set_citation_data( article_data_IN, create_if_no_match_IN = False )
                
                # retrieve results
                if ( get_citation_data_result is not None ):
        
                    # get citation data, status, status message.
                    citation_data = get_citation_data_result.get( cls.PROP_CITATION_DATA, None )
                    citation_get_status = get_citation_data_result.get( cls.PROP_LOOKUP_STATUS, cls.PROP_LOOKUP_STATUS_VALUE_ERROR )
                    citation_get_status_message = get_citation_data_result.get( cls.PROP_STATUS_MESSAGE, None )
                    
                    # error?
                    if ( citation_get_status not in cls.PROP_LOOKUP_ERROR_STATUS_LIST ):
                    
                        # no - process.
                        
                        # then get list of DataSetMentions.
                        data_set_mention_qs = citation_data.datasetmention_set.all()
        
                        # filter mentions down to just those for citation.
                        data_set_mention_qs = data_set_mention_qs.filter( data_set_citation = citation_instance_IN )
                        
                        # loop over mentions.
                        for current_data_set_mention in data_set_mention_qs:
                        
                            # increment index
                            mention_index += 1
                            
                            # get values
                            current_mention_text = JSONHelper.escape_json_value( current_data_set_mention.value )
                        
                            # init mention dict
                            current_mention_dict = {}
                            current_mention_dict[ cls.DATA_STORE_PROP_MENTION_TEXT ] = current_mention_text
                            current_mention_dict[ cls.DATA_STORE_PROP_FIXED_MENTION_TEXT ] = ""
                            current_mention_dict[ cls.DATA_STORE_PROP_MENTION_TYPE ] = ""
                            current_mention_dict[ cls.DATA_STORE_PROP_MENTION_INDEX ] = mention_index
                            current_mention_dict[ cls.DATA_STORE_PROP_ORIGINAL_MENTION_TYPE ] = current_data_set_mention.mention_type
                            current_mention_dict[ cls.DATA_STORE_PROP_DATA_SET_MENTION_ID ] = int( current_data_set_mention.id )
                            
                            # add to mention array list.
                            mention_array_list.append( current_mention_dict )
                            text_to_mention_index_dict[ current_mention_text ] = mention_index
                            
                        #-- END loop over data set mentions --#
                        
                        # put it all together.
                        data_store_dict[ cls.DATA_STORE_PROP_MENTION_ARRAY ] = mention_array_list
                        data_store_dict[ cls.DATA_STORE_PROP_NEXT_MENTION_INDEX ] = mention_index + 1
                        data_store_dict[ cls.DATA_STORE_PROP_STATUS_MESSAGE_ARRAY ] = []
                        data_store_dict[ cls.DATA_STORE_PROP_LATEST_MENTION_INDEX ] = mention_index
                        data_store_dict[ 'article_data_id' ] = article_data_IN.id
                        data_store_dict[ 'citation_id' ] = citation_instance_IN.id
                        data_store_dict[ 'data_set_citation_data_id' ] = citation_data.id

                    else:
                    
                        # error.  No citation data.
                        status_message = "ERROR - status: {}; status message: {}.".format( citation_get_status, citation_get_status_message )
                        status_message_list.append( status_message )
                    
                    # END check to see if citation present. --#

                else:
                
                    # error.  No citation data response from get method.
                        
                    # Error.  Need a citation.
                    status_message = "ERROR - No response from call to cls.get_data_set_citation_data().  Very strange."
                    status_message_list.append( status_message )
                
                # END check to see if citation present. --#

            else:
            
                # Error.  Need a citation.
                status_message = "ERROR - No citation passed in, can't filter mentions to particular data set."
                status_message_list.append( status_message )
            
            # END check to see if citation present. --#

        else:
        
            # Error.  Need a citation.
            status_message = "ERROR - No article data passed in, what do you want me to do here?"
            status_message_list.append( status_message )
        
        #-- END check to see if we have Article_Data instance. --#

        # return string or objects?
        if ( return_string_IN == True ):

            # string - use json.dumps()
            json_OUT = JSONHelper.pretty_print_json( data_store_dict )

        else:

            # objects - just return the dictionary.
            json_OUT = data_store_dict

        #-- END check to see if return string or objects. --#
        
        debug_message = 'JSON: \n' + str( json_OUT )
        LoggingHelper.output_debug( debug_message, me, indent_with_IN = '====>', logger_name_IN = cls.LOGGER_NAME, resource_string_IN = my_resource_string )

        # local debug on?
        if ( local_debug_flag == True ):
        
            # log status message list
            for status_message in status_message_list:
            
                LoggingHelper.output_debug( status_message, me, indent_with_IN = '====>', logger_name_IN = cls.LOGGER_NAME, resource_string_IN = my_resource_string )
                
            #-- END logging of status messages --#

            # remove resource string from LoggingHelper instance-level string.
            LoggingHelper.remove_from_class_resource_string( my_resource_string )

        #-- END check to see if local debug is on. --#
        
        return json_OUT

    #-- END class method convert_article_data_to_json() --#


    @classmethod
    def get_article_data_set_citation_data( cls, article_data_IN, create_if_no_match_IN = True, *args, **kwargs ):
        
        '''
        Accepts article_data.  Tries to retrieve DataSetCitations for article.
           
        Returns a dictionary that contains:
        - PROP_CITATION_DATA = "citation_data" - either matching
            DataSetCitationData instance or None.
        - PROP_LOOKUP_STATUS = "lookup_status" - status code with one of the 
            following statuses:
            - PROP_LOOKUP_STATUS_VALUE_NEW = "new"
            - PROP_LOOKUP_STATUS_VALUE_EXISTING = "existing"
            - PROP_LOOKUP_STATUS_VALUE_MULTIPLE = "multiple"
            - PROP_LOOKUP_STATUS_VALUE_ERROR = "error"
        - PROP_STATUS_MESSAGE = "status_message" - if "multiple" or "error",
            explains what happened.  If "new" or "existing", empty.
        - PROP_EXCEPTION = "exception"
           
        Postconditions - Returns:
        - if single match found, returns it with status of "existing"
            (self.PROP_LOOKUP_STATUS_PROP_EXISTING) and no status message or
            exception.
        - if no match found, creates new instance, returns it with status of
            "new" (self.PROP_LOOKUP_STATUS_PROP_NEW) and no status message
            or exception.
        - if multiple matches found, returns None with status of "multiple"
            (self.PROP_LOOKUP_STATUS_PROP_MULTIPLE), status_message explaining,
            and no exception.
        - if other error, returns None, status of "error"
            (self.PROP_LOOKUP_STATUS_PROP_ERROR), status message that contains
            the exception cast as a string, and the exception itself.
        '''

        # return reference
        result_OUT = {}
        citation_data_OUT = None
        status_OUT = ""
        status_message_OUT = ""
        exception_OUT = None
        
        # declare variables
        me = "ManualDataSetCitationsCoder.get_data_set_citation_data()"
        local_debug_flag = False
        current_article_data = None
        citation_instance = None
        citation_data_qs = None
        citation_data = None
        citation_data_count = -1
        
        # declare variables - logging
        my_resource_string = ""
        
        # local debug on?
        if ( local_debug_flag == True ):

            # initialize resource string and add it to the LoggingHelper class-level
            #     string.
            my_resource_string = cls.LOGGER_NAME + "." + me
            LoggingHelper.add_to_class_resource_string( my_resource_string )
            
        #-- END check to see if local debug on. --#

        # init
        current_article_data = article_data_IN
        citation_instance = citation_IN
        
        # got article data?
        if ( current_article_data is not None ):
        
            # got citation?
            if ( citation_instance is not None ):
        
                # DataSetCitationData instance
                citation_data_qs = current_article_data.datasetcitationdata_set.all()
                citation_data_qs = citation_data_qs.filter( data_set_citation = citation_instance )
                
                # how many (should just be 1)
                citation_data_count = citation_data_qs.count()
                if ( citation_data_count == 0 ):
                
                    # create_if_no_match_IN?
                    if ( create_if_no_match_IN == True ):
                
                        # make one, associate it correctly, save.
                        citation_data = DataSetCitationData()
                        citation_data.article_data = current_article_data
                        citation_data.data_set_citation = citation_instance
                        if ( citation_type_IN is not None ):
                            citation_data.citation_type = citation_type_IN
                        #-- END check if type passed in. --#
                        citation_data.save()
                        
                        # set status to "new"
                        status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_NEW
                    
                    else:
                        
                        # No match, don't create, output message and
                        #     move on.
                        citation_data = None
                        
                        # ...set status to "multiple"...
                        status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_ERROR
    
                        # ...create status message...
                        status_message_OUT = "create_if_no_match_IN == False, no match for Article_Data: {}; and citation: {}".format( current_article_data, citation_instance )
    
                        # ...and log it.
                        LoggingHelper.output_debug( status_message_OUT, me, indent_with_IN = '====>', logger_name_IN = cls.LOGGER_NAME, resource_string_IN = my_resource_string )
                    
                    #-- END check to see if create_if_no_match_IN --#

                elif( citation_data_count == 1 ):
                
                    # get and use it.
                    citation_data = citation_data_qs.get()
                    
                    # set status to "existing"
                    status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_EXISTING

                else:
                
                    # error. Multiple matches. output message and
                    #     move on.
                    citation_data = None
                    
                    # ...set status to "multiple"...
                    status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_MULTIPLE

                    # ...create status message.
                    status_message_OUT = "Multiple DataSetCitationData found for Article_Data: {}; and citation: {}".format( current_article_data, citation_instance )

                #-- END check for DataSetCitationData --#
                
            else:
                        
                # error. No citation.
                citation_data = None
                status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_ERROR
                status_message_OUT = "Required DataSetCitation instance not passed in."
            
            #-- END check to see if citation instance --#

        else:
        
            # No article_data - error.
            citation_data = None
            status_OUT = cls.PROP_LOOKUP_STATUS_VALUE_ERROR
            status_message_OUT = "No Article_Data instance passed in.  Can't lookup DataSetCitationData if no article_data specified."
                    
        #-- END check to see if article_data passed in. --#
        
        # prepare output.
        citation_data_OUT = citation_data
        
        # pack up result dictionary.
        result_OUT[ cls.PROP_CITATION_DATA ] = citation_data_OUT
        result_OUT[ cls.PROP_LOOKUP_STATUS ] = status_OUT
        result_OUT[ cls.PROP_STATUS_MESSAGE ] = status_message_OUT
        result_OUT[ cls.PROP_EXCEPTION ] = exception_OUT
        
        # local debug on?
        if ( local_debug_flag == True ):
        
            # is there a status message?
            if ( ( status_message_OUT is not None ) and ( status_message_OUT != "" ) ):
            
                LoggingHelper.output_debug( status_message_OUT, me, indent_with_IN = '====>', logger_name_IN = cls.LOGGER_NAME, resource_string_IN = my_resource_string )
                
            #-- END check to see if status message --#
        
            # remove resource string from LoggingHelper instance-level string.
            LoggingHelper.remove_from_class_resource_string( my_resource_string )

        #-- END check to see if local debug is on. --#

        return result_OUT
        
    #-- END method get_data_set_citation_data() --#
    
    
    #============================================================================
    # ! ==> Instance methods
    #============================================================================


    def init_config_properties( self, *args, **kwargs ):

        '''
        purpose: Called as part of the base __init__() method, so that loading
           config properties can also be included in the parent __init__()
           method.  The application for django_config and any properties that
           need to be loaded should be set here.  To set a property use
           add_config_property( name_IN ).  To set application, use
           set_config_application( app_name_IN ).
           
        inheritance: This method overrides the abstract method of the same name in
           the ArticleCoder parent class.

        preconditions: None.

        postconditions: This instance should be ready to have
           load_config_properties() called on it after this method is invoked.
        '''

        self.set_config_application( self.CONFIG_APPLICATION )

    #-- END abstract method init_config_properties() --#
    

    def initialize_from_params( self, params_IN, *args, **kwargs ):

        '''
        purpose: Accepts a dictionary of run-time parameters, uses them to
           initialize this instance.

        inheritance: This method overrides the abstract method of the same name in
           the ArticleCoder parent class.

        preconditions: None.

        postconditions: None.
        '''

        # declare variables
        me = "initialize_from_params"
        
        # update config properties with params passed in.
        self.update_config_properties( params_IN )
        
    #-- END abstract method initialize_from_params() --#
    

    def process_article( self, article_IN, coding_user_IN = None, *args, **kwargs ):

        '''
        purpose: After the ArticleCoder is initialized, this method accepts one
           article instance and codes it for sourcing.  In regards to articles,
           this class is stateless, so you can process many articles with a
           single instance of this object without having to reconfigure each
           time.
           
        Accepts:
        - article_IN - article instance we will be coding.
        - coding_user_IN - user instance for coder who coded this article.
        - KWARG_DATA_STORE_JSON_STRING = "data_store_json_string_IN" - JSON string that contains coding for article we are processing.
        - KWARG_ARTICLE_DATA_ID = "article_data_id_IN" - ID of article data for this coder's coding on this article, if we are updating, not creating new.
        - KWARG_REQUEST = "request_IN" - if manual coding via web form, request instance of form submission.
        - KWARG_RESPONSE_DICTIONARY = "response_dictionary_IN" - if manual coding via web form, response dictionary that will be used to render response sent back to user.
        
        inheritance: This method overrides the abstract method of the same name in
           the ArticleCoder parent class.

        preconditions: load_config_properties() should have been invoked before
           running this method.

        postconditions: article passed in is coded, which means an Article_Data
           instance is created for it and populated to the extent the child
           class is capable of coding the article.
        '''

        # return reference
        status_OUT = self.STATUS_SUCCESS
        
        # declare variables
        me = "process_article"
        my_logger = None
        my_exception_helper = None
        data_store_json_string = ""
        article_data_id = -1
        request = None
        response_dictionary = ""
        article_data = None
        article_data_status_messages = "" 
        
        # get logger
        my_logger = self.get_logger()
        
        # get exception_helper
        my_exception_helper = self.get_exception_helper()

        '''        
        # get parameters for calling process_data_store_json()
        data_store_json_string = kwargs[ self.KWARG_DATA_STORE_JSON_STRING ]
        article_data_id = kwargs[ self.KWARG_ARTICLE_DATA_ID ]
        request = kwargs[ self.KWARG_REQUEST ]
        response_dictionary = kwargs[ KWARG_RESPONSE_DICTIONARY ]
        
        # try to retrieve citation from mentions.
        
        # call process_data_store_json()
        article_data = self.process_data_store_json( article_IN,
                                                     coding_user_IN,
                                                     data_store_json_string,
                                                     article_data_id,
                                                     request,
                                                     response_dictionary )

        # got article data?
        if ( article_data is not None ):

            # yes - store it off.
            self.latest_article_data = article_data

            # got status messages?
            article_data_status_messages = article_data.status_messages
            if ( ( article_data_status_messages is not None ) and ( article_data_status_messages != "" ) ):

                # yes.  what do you know.  Return it.
                status_OUT = article_data_status_messages

            #-- END check to see if status messages in Article_Data instance --#

        else:

            # ERROR - should have gotten Article_Data instance back.
            status_OUT = self.STATUS_ERROR_PREFIX + "In " + me + "(): ERROR - call to process_data_store_json() did not return Article_Data."

        #-- END check to see if we got anything back. --#
        '''
        
        return status_OUT

    #-- END method process_article() --#
    

    def process_data_store_json( self,
                                 citation_instance_IN,
                                 coder_user_IN,
                                 data_store_json_string_IN,
                                 article_data_id_IN = None,
                                 request_IN = None,
                                 response_dictionary_IN = None,
                                 compact_white_space_IN = False ):
    
        '''
        Accepts:
        - citation_instance_IN - citation for which we have mention coding data.
        - coder_user_IN - user instance for coder.
        - data_store_json_string_IN - JSON string that contains coding for article we are processing.
        - article_data_id_IN - optional - ID of article data for this coder's coding on this article, if we are updating, not creating new.
        - request_IN - optional - if manual coding via web form, request instance of form submission.
        - response_dictionary_IN - optional - if manual coding via web form, response dictionary that will be used to render response sent back to user.

        Purpose:
           This method accepts the above parameters.  It checks to make sure
           that there is acitation, a coder user, and JSON.  It tries to find
           an existing Article_Data record for the current citation and coder.
           If it finds 1, it updates it.  If it finds 0, it creates one.  If it
           finds more than 1, it returns an error message.  For each mention,
           this method looks for a record of that mention.  If present, does
           nothing.  If not, adds it.

        Preconditions:
           Must already have looked up and loaded the citation and coder user
           into instance variables.  Should have data store JSON to process,
           as well.

        Postconditions:
           Returns Article_Data instance.  If successful, it will be a
           fully-populated Article_Data instance that includes references to
           the mentions stored in JSON passed in.  If error, will be an empty
           Article_Data instance with no primary key, and error messages will
           be stored in the 'status_messages' field, with multiple messages
           separated by semi-colons.

        '''
    
        # return reference
        article_data_OUT = None
    
        # ! declare variables
        me = "process_data_store_json"
        
        # declare variables - coding submission.
        is_ok_to_process = True
        status_message = ""
        status_message_list = None
        coder_user = None
        data_store_json_string = ""
        data_store_json = None

        # declare variables - references to article and data set from citation.
        related_article = None
        related_data_set = None

        # declare variables - look for existing Article_Data
        lookup_result = None
        lookup_status = ""
        lookup_status_message = ""
        is_existing_article_data = False
        current_article_data = None

        # declare variables - make new Article_Data if needed.
        current_article = None
        current_person = None
        
        # declare variables - DataSetCitationData instance.
        citation_get_result = None
        citation_data = None
        citation_get_status = None
        citation_get_status_message = None
        
        # declare variables - remove obsolete - lists of IDs of DataSetMention
        #     childre that we started with (original), and then that were
        #     looked up in processing (processed), so we can remove any we
        #     started with that weren't referenced in the current run.
        data_set_mention_qs = None
        original_data_set_mention_id_list = []
        processed_data_set_mention_id_list = []
        deleted_data_set_mention_list = []

        # declare variables - store off JSON in a note.
        json_article_data_note = None
        
        # declare variables - loop over mention list in JSON.
        mention_list = []
        mention_count = -1
        mention_counter = -1
                
        # declare variables - get current mention's information.
        mention_text = ""
        mention_capture_method = ""
        
        # declare variables - for processing mention.
        processing_qs = None
        processing_count = -1
        current_data_set_mention = None
        current_data_set_mention_id = -1
        
        # start with is_ok_to_process = True and an empty status_message_list
        is_ok_to_process = True
        status_message = ""
        status_message_list = []
    
        # got a citation?
        if ( citation_instance_IN is not None ):
        
            # yes, we have a citation.  Get nested article and data set.
            related_article = citation_instance_IN.article
            related_data_set = citation_instance_IN.data_set
            
            # Got a coder user?
            coder_user = coder_user_IN
            if ( coder_user is None ):

                # got a request?
                if ( request_IN is not None ):

                    coder_user = request_IN.user

                #-- END check to see if we have a request. --#

            #-- END check to see if we have a coder user passed in. --#

            # after all that, got a coder user?
            if ( coder_user is not None ):
            
                # yes - Got a JSON string?
                data_store_json_string = data_store_json_string_IN
                if ( ( data_store_json_string is not None ) and ( data_store_json_string != "" ) ):
                
                    self.output_debug( data_store_json_string, me, "====> Data Store JSON\n\n" )
                    #status_message_list.append( data_store_json_string )

                    # got a JSON string, convert to Python objects.
                    data_store_json = json.loads( data_store_json_string )

                    # ! lookup Article_Data
                    lookup_result = self.lookup_article_data( related_article, coder_user, article_data_id_IN )
                    
                    # what have we got?
                    if ( lookup_result is not None ):
                    
                        # get Article_Data, status, status message.
                        current_article_data = lookup_result.get( self.PROP_ARTICLE_DATA, None )
                        lookup_status = lookup_result.get( self.PROP_LOOKUP_STATUS, self.PROP_LOOKUP_STATUS_VALUE_ERROR )
                        lookup_status_message = lookup_result.get( self.PROP_STATUS_MESSAGE, None )
                        
                        # set processing flags.
                        if ( lookup_status in self.PROP_LOOKUP_ERROR_STATUS_LIST ):
                        
                            # error.  Not OK to process...
                            is_ok_to_process = False
                            
                            # ...create error message...
                            status_message_list.append( lookup_status_message )

                            # ...and log it.
                            self.output_debug( lookup_status_message, me, indent_with_IN = "====>" )
                        
                        elif ( lookup_status == self.PROP_LOOKUP_STATUS_VALUE_NEW ):

                            # OK to process...
                            is_ok_to_process = True
                            
                            # ...and not an existing Article_Data instance
                            is_existing_article_data = False
                            
                        elif ( lookup_status == self.PROP_LOOKUP_STATUS_VALUE_EXISTING ):

                            # OK to process...
                            is_ok_to_process = True
                            
                            # ...and is an existing Article_Data instance
                            is_existing_article_data = True
                            
                        else:
                        
                            # error.  Not OK to process...
                            is_ok_to_process = False
                            
                            # ...create error message...
                            status_message = "ERROR - Unknown lookup_article_data() status " + lookup_status + ", message: " + lookup_status_message
                            status_message_list.append( status_message )

                            # ...and log it.
                            self.output_debug( status_message, me, indent_with_IN = "====>" )
                        
                            # unknown status.  Error.
                            
                        #-- END conditional over statuses. --#
                            
                    else:
                    
                        # no result - error.  Not OK to process...
                        is_ok_to_process = False
                        
                        # ...create error message...
                        status_message = "ERROR - Nothing came back from lookup_article_data() status."
                        status_message_list.append( status_message )

                        # ...and log it.
                        self.output_debug( status_message, me, indent_with_IN = "====>" )
                    
                        # unknown status.  Error.
                        
                    #-- END check to make sure we have a response. --#
                    
                    # ! is it OK to process JSON?
                    if ( is_ok_to_process == True ):

                        # got article data?
                        if ( current_article_data is not None ):
                        
                            # ! -- get/lookup DataSetCitationData instance
                            citation_get_result = self.get_data_set_citation_data( current_article_data, citation_instance_IN )
                        
                            # what have we got?
                            if ( citation_get_result is not None ):
                    
                                # get citation data, status, status message.
                                citation_data = citation_get_result.get( self.PROP_CITATION_DATA, None )
                                citation_get_status = citation_get_result.get( self.PROP_LOOKUP_STATUS, self.PROP_LOOKUP_STATUS_VALUE_ERROR )
                                citation_get_status_message = citation_get_result.get( self.PROP_STATUS_MESSAGE, None )
                                
                                # set processing flags.
                                if ( citation_get_status in self.PROP_LOOKUP_ERROR_STATUS_LIST ):
                                
                                    # error (error, or multiple found).  Not OK to process...
                                    citation_data = None
                                    
                                    # ...create error message...
                                    status_message_list.append( citation_get_status_message )
        
                                    # ...and log it.
                                    self.output_debug( citation_get_status_message, me, indent_with_IN = "====>" )
                                
                                elif ( citation_get_status in self.PROP_LOOKUP_FOUND_STATUS_LIST ):
        
                                    # OK to process...
                                    debug_message = "Found DataSetCitationData instance, status: {}; message: {}".format( citation_get_status, citation_get_status_message )
                                    self.output_debug( debug_message, me, indent_with_IN = "====>" )

                                else:
                                
                                    # unknown error.  Not OK to process...
                                    citation_data = None
                                    
                                    # ...create error message...
                                    status_message = "ERROR - Unknown get_data_set_citation_data() status: {}, message: {}".format( citation_get_status, citation_get_status_message )
                                    status_message_list.append( status_message )
        
                                    # ...and log it.
                                    self.output_debug( status_message, me, indent_with_IN = "====>" )
                                
                                    # unknown status.  Error.
                                    
                                #-- END conditional over statuses. --#
                                    
                            else:
                            
                                # no result - error.  Not OK to process...
                                citation_data = None
                                
                                # ...create error message...
                                status_message = "ERROR - Nothing came back from get_data_set_citation_data() status."
                                status_message_list.append( citation_get_status_message )
        
                                # ...and log it.
                                self.output_debug( citation_get_status_message, me, indent_with_IN = "====>" )
                            
                                # unknown status.  Error.
                                
                            #-- END check to make sure we have a response. --#
                                        
                            # got citation_data?
                            if ( citation_data is not None ):
                            
                                # make list of DataSetMentions for this citation
                                # before parsing.
                                data_set_mention_qs = citation_data.datasetmention_set.all()
                                original_data_set_mention_id_list = list( data_set_mention_qs.values_list( "id", flat = True ).order_by( "id" ) )
                                
                                # initialize other processing tracking lists.
                                processed_data_set_mention_id_list = []                            
                            
                                debug_message = "original_data_set_mention_id_list = {}".format( original_data_set_mention_id_list )
                                self.output_debug( debug_message, me, "@@@@@@@@>" )                                        
            
                                # yes - store JSON in an Article_Data_Note.
                                json_article_data_note = Article_Data_Notes()
                                json_article_data_note.article_data = current_article_data
                                json_article_data_note.content_type = Article_Data_Notes.CONTENT_TYPE_JSON
                                json_article_data_note.content = data_store_json_string
                                json_article_data_note.source = self.coder_type + " - user " + str( coder_user )
                                json_article_data_note.content_description = "Data Store JSON (likely from manual coding of mentions via data_set-mentions-code view) - DataSetCitationData: {}".format( citation_data )
                                json_article_data_note.save()
        
                                # store current_article_data in article_data_OUT.
                                article_data_OUT = current_article_data
        
                                # get list of mentions.
                                mention_list = data_store_json[ self.DATA_STORE_PROP_MENTION_ARRAY ]
                                
                                # get count of mentions
                                mention_count = len( mention_list )
                                
                                # got one or more mentions?
                                if ( mention_count > 0 ):
                                                        
                                    # !loop over mentions
                                    mention_counter = 0
                                    for current_mention in mention_list:
        
                                        # increment counter
                                        mention_counter += 1
                                    
                                        # check to see if it is an empty entry (happens
                                        #    when a mention is removed during coding).
                                        if ( current_mention is not None ):
                                    
                                            # get mention text.
                                            mention_text = current_mention.get( self.DATA_STORE_PROP_MENTION_TEXT, None )
                                            
                                            # set capture method.
                                            mention_capture_method = "manual_coding"
                                            
                                            # look up mention with this text.
                                            processing_qs = data_set_mention_qs.filter( value = mention_text )
                                            
                                            # how many?
                                            processing_count = processing_qs.count()
                                            if ( processing_count == 1 ):
                                            
                                                # got a match.  Add id to processed list and move on.
                                                current_data_set_mention = processing_qs.get()
                                                current_data_set_mention_id = current_data_set_mention.id
                                                
                                                # check to see if ID already in list
                                                if ( current_data_set_mention_id not in processed_data_set_mention_id_list ):
                                                
                                                    # not there - add it.
                                                    processed_data_set_mention_id_list.append( current_data_set_mention_id )
                                                    
                                                #-- END check to see if mention ID already in list. --#
                                                
                                            elif ( processing_count == 0 ):
                                            
                                                # new match - create new record.
                                                current_data_set_mention = DataSetMention()
                                                current_data_set_mention.value = mention_text
                                                current_data_set_mention.capture_method = mention_capture_method
                                                current_data_set_mention.data_set_citation = citation_instance_IN
                                                current_data_set_mention.data_set_citation_data = citation_data
                                                current_data_set_mention.article_data = article_data_OUT
                                                current_data_set_mention.save()
                                                
                                                # check to see if ID alread in the
                                                #     processed list (better not be
                                                #     there).
                                                current_data_set_mention_id = current_data_set_mention.id
                                                if ( current_data_set_mention_id not in processed_data_set_mention_id_list ):
                                                
                                                    # not there (and better not be
                                                    #     there) - add it.
                                                    processed_data_set_mention_id_list.append( current_data_set_mention_id )
                                                    
                                                #-- END check to see if mention ID already in list. --#
                                            
                                            else:
                                            
                                                # error.  Multiple matches.  output
                                                #     message and move on.
                                                debug_message = "ERROR: mention_list item {}, mention_text {}, has multiple matches.  Moving on.".format( mention_counter, mention_text )
                                                status_message_list.append( debug_message )
                                                self.output_debug( debug_message, me )
                                                
                                            #-- END check to see how many matches. --#
                                                                                    
                                        else:
                                        
                                            # empty mention list entry.  Make a note
                                            #     and move on.
                                            debug_message = "mention_list item " + str( mention_counter ) + " is None.  Moving on."
                                            # status_message_list.append( debug_message )
                                            debug_message = "WARNING: " + debug_message
                                            self.output_debug( debug_message, me )
                                        
                                        #-- END check to see if empty entry in mention list --#
        
                                    #-- END loop over persons --#
                                    
                                    # ! ==> removal check
                                    # Remove any DataSetMention whose ID is in the
                                    #     original list but not in the processed
                                    #     list.
                                    deleted_data_set_mention_list = self.winnow_orphaned_records(
                                            original_data_set_mention_id_list,
                                            processed_data_set_mention_id_list,
                                            DataSetMention
                                        )
                                                                    
                                #-- END check to see if there are any mentions. --#
                                
                            else:
                            
                                # No citation data instance.  Can't process. 
                                #    Add message to list, log it.
                                status_message = "ERROR - Even though  lookup indicated success, no Article_Data.  Don't know what to tell you."
                                status_message_list.append( status_message )
                                self.output_debug( status_message, me, "====> " )
                                article_data_OUT = None
                            
                            #-- END check to see if any DataSetCitationData --#

                        else:
                        
                            # No article data instance.  Can't process.  Add
                            #    message to list, log it.
                            status_message = "ERROR - Even though get_data_set_citation_data() indicated success, no citation data.  Don't know what to tell you."
                            status_message_list.append( status_message )
                            self.output_debug( status_message, me, "====> " )
                            article_data_OUT = None
                        
                        #-- END check to make sure we have article data --#
                                                    
                    else:

                        # Not OK to process.  Assume messages that explain why
                        #    have been placed in status_message_list.
                        pass

                    #-- END check to see if is_ok_to_process == True --#
    
                else:
                
                    # no JSON - can't process.  Add message to list, log it.
                    status_message = "ERROR - No JSON passed in - must have data in JSON to process that data."
                    status_message_list.append( status_message )
                    self.output_debug( status_message, me, "====> " )
                    article_data_OUT = None
                
                #-- END check to see if JSON string passed in.
                
            else:
            
                # no coder user?  That is an odd error.
                status_message = "ERROR - No coder user passed in - must have a coder user."
                status_message_list.append( status_message )
                self.output_debug( status_message, me, "====> " )
                article_data_OUT = None
                
            #-- END check to see if coder passed in. --#
            
        else:
        
            # no article - can't process.
            status_message = "ERROR - No article passed in - must have an article to code an article."
            status_message_list.append( status_message )
            self.output_debug( status_message, me, "====> " )
            article_data_OUT = None
        
        #-- END check to see if article ID passed in.

        # got status messages?
        if ( ( status_message_list is not None ) and ( len( status_message_list ) > 0 ) ):

            # we do.  Convert to semi-colon-delimited list, place in
            #    Article_Data.status_messages
            # create new empty Article_Data
            status_message = ";".join( status_message_list )

            # Overwrite existing status_messages.
            article_data_OUT.status_messages = status_message

        else:

            # no status messages, so status is success!
            article_data_OUT.status_messages = self.STATUS_SUCCESS

        #-- END check to see if status messages. --#
    
        return article_data_OUT
    
    #-- END function process_data_store_json() --#
    
    def winnow_orphaned_records( self, original_ID_list_IN, updated_ID_list_IN, class_IN, *args, **kwargs ):
        
        '''
        For objects of a given class (class_IN), accepts list of IDs originally
            associated with an entity, an updated list of IDs that are currently
            associated with that entity, and the class of the object we are
            winnowing.  For each ID in the original list, checks to see if it is
            in the updated list.  If not, looks up the instance by the ID using
            class_IN, then delete()'s the instance.  Returns list of instances
            that were deleted, post-delete.
            
        Postconditions: Records whose IDs are in the original list and not in
            the updated list will be permanently deleted after this routine is
            invoked.  Returns list of instances that were deleted.
        '''

        # return reference
        deleted_instances_list_OUT = []
        
        # declare variables
        me = "winnow_orphaned_records"
        original_id_count = -1
        original_id_counter = -1
        current_ID = None
        instance_qs = None
        current_instance = None
        deleted_id_list = []
        deleted_instance_list = []
        debug_message = ""
        
        debug_message = "Winnowing class " + str( class_IN ) + "\n- original_id_list_IN = " + str( original_ID_list_IN ) + "\n- updated_ID_list_IN = " + str( updated_ID_list_IN )
        self.output_debug( debug_message, me, "~~~~" )
        
        # got an original list?
        if ( original_ID_list_IN is not None ):
            
            # is it a list?
            if ( isinstance( original_ID_list_IN, list ) == True ):
                
                # does it have anything in it?
                original_id_count = len( original_ID_list_IN )
                if ( original_id_count > 0 ):
                
                    # yes - For each item, check to see if the ID stored in the list is
                    #     in the updated_ID_list_IN.
                    original_id_counter = 0
                    for current_ID in original_ID_list_IN:
                        
                        # increment counter
                        original_id_counter += 1
        
                        debug_message = "Original ID #" + str( original_id_counter ) + " = " + str( current_ID )
                        # self.output_debug( debug_message, me, "~~~~~~~~" )
                    
                        # check to see if it is in updated list.
                        if ( current_ID not in updated_ID_list_IN ):
                        
                            debug_message += " NOT IN updated_ID_list_IN ( " + str( updated_ID_list_IN ) + " )"
                            self.output_debug( debug_message, me, "~~~~~~~~" )
                    
                            # wrap in try, in case problem with class, or record DNE.
                            try:
                            
                                # it is not in the list.  Look up the instance...
                                instance_qs = class_IN.objects.all()                    
                                current_instance = instance_qs.get( pk = current_ID )
                                
                                # ...delete it...
                                current_instance.delete()
                                
                                # ...and add it to the deleted lists.
                                deleted_id_list.append( current_ID )
                                deleted_instance_list.append( current_instance )
                                
                                debug_message = "Deleted record with ID " + str( current_ID ) + " in class " + str( class_IN )
                                self.output_debug( debug_message, me, "~~~~~~~~~~~~" )
        
                            except MultipleObjectsReturned as mor_exception:
                            
                                debug_message = "Multiple matches for ID " + str( current_ID ) + " in class " + str( class_IN )
                                self.output_debug( debug_message, me, "~~~~~~~~~~~~" )
        
                            except class_IN.DoesNotExist as dne_exception:
        
                                debug_message = "No match for ID " + str( current_ID ) + " in class " + str( class_IN )
                                self.output_debug( debug_message, me, "~~~~~~~~~~~~" )
        
                            except Exception as e:
                                
                                debug_message = "Unexpected exception caught: " + str( e ) + " processing ID " + str( current_ID ) + " and class " + str( class_IN )
                                self.output_debug( debug_message, me, "~~~~~~~~~~~~" )
                                
                            #-- END try...except around lookup of instance, and then delete() --#
                            
                        else:
                            
                            debug_message += " IN updated_ID_list_IN ( " + str( updated_ID_list_IN ) + " ) - moving on."
                            self.output_debug( debug_message, me, "~~~~~~~~" )
        
                        #-- END check to see if current original ID is in updated list --#
        
                    #-- END loop over IDs in original list. --#

                else:
                    
                    debug_message = "updated_ID_list_IN ( " + str( updated_ID_list_IN ) + " ) has nothing in it ( " + str( original_id_count ) + " )."
                    self.output_debug( debug_message, me, "~~~~" )            
                    
                #-- END check to see if there is anything in "original" list --#
                    
            else:
                
                debug_message = "updated_ID_list_IN ( " + str( updated_ID_list_IN ) + " ) is not a list ( type = " + str( type( updated_ID_list_IN ) ) + " )."
                self.output_debug( debug_message, me, "~~~~" )            
                
            #-- END check to see if the "original" list is of type list --#
            
        else:
            
            debug_message = "updated_ID_list_IN ( " + str( updated_ID_list_IN ) + " ) is None."
            self.output_debug( debug_message, me, "~~~~" )            
            
        #-- END check to see if there is an "original" list --#
        
        # return instance list
        deleted_instances_list_OUT = deleted_instance_list

        return deleted_instances_list_OUT
        
    #-- END method winnow_orphaned_records() --#
    

#-- END class ManualDataSetCitationsCoder --#