from __future__ import unicode_literals

'''
Copyright 2010-2018 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet_datasets.

sourcenet_datasets is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

sourcenet_datasets is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/sourcenet_datasets. If not, see http://www.gnu.org/licenses/.

Configuration properties for it are stored in django's admins, in the
   django_config application.  The properties for the article_code view are stored in Application
   "sourcenet-UI-article-code":
   - include_fix_person_name - boolean flag, if true outputs additional field to correct name text from article.
'''

#===============================================================================
# ! ==> imports (in alphabetical order by package, then by name)
#===============================================================================

# import Python libraries for CSV output
#import csv
import datetime
import json
#from StringIO import StringIO
#import pickle
import sys

# BeautifulSoup!
from bs4 import BeautifulSoup

from django.shortcuts import render

# import django authentication code.
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# import django code for csrf security stuff.
from django.template.context_processors import csrf

# django core imports
from django.urls import reverse

# import model classes
from sourcenet_datasets.models import DataSetCitation

# other sourcenet_datasets classes
from sourcenet_datasets.coding.data_set_mentions.manual.manual_data_set_mentions_coder import ManualDataSetMentionsCoder

# import form classes
from sourcenet_datasets.forms import CodingSubmitForm
from sourcenet_datasets.forms import DataSetMentionsCodingListForm
from sourcenet_datasets.forms import DataSetCitationLookupForm

# sourcenet imports
from sourcenet.models import Article
from sourcenet.models import Article_Data

# python_utilities imports
from python_utilities.django_utils.django_view_helper import DjangoViewHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.lists.list_helper import ListHelper
from python_utilities.strings.string_helper import StringHelper


#================================================================================
# ! ==> Shared variables and functions
#================================================================================

# configuration properties
# article_code view
CONFIG_APPLICATION_DATA_SET_MENTIONS_CODE = "sourcenet_datasets-UI-data_set_mentions-code"

# form input names
INPUT_NAME_CITATION_ID = "data_set_citation_id"
INPUT_NAME_SOURCE = "source"
INPUT_NAME_TAGS_IN_LIST = "tags_in_list"

# STATUSes
STATUS_SUCCESS = "Success!"


def get_request_data( request_IN ):
    
    '''
    Accepts django request.  Based on method, grabs the container for incoming
        parameters and returns it:
        - for method "POST", returns request_IN.POST
        - for method "GET", returns request_IN.GET
    '''
    
    # return reference
    request_data_OUT = None

    # call method in DjangoViewHelper
    request_data_OUT = DjangoViewHelper.get_request_data( request_IN )
    
    return request_data_OUT
    
#-- END function get_request_data() --#


'''
debugging code, shared across all models.
'''

DEBUG = True
LOGGER_NAME = "sourcenet.views"

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_logger_name = ""
    
    # got a logger name?
    my_logger_name = LOGGER_NAME
    if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
    
        # use logger name passed in.
        my_logger_name = logger_name_IN
        
    #-- END check to see if logger name --#

    # call DjangoViewHelper method.
    DjangoViewHelper.output_debug( message_IN,
                                   method_IN = method_IN,
                                   indent_with_IN = indent_with_IN,
                                   logger_name_IN = my_logger_name,
                                   debug_flag_IN = DEBUG )

#-- END method output_debug() --#


#===============================================================================
# ! ==> view action methods (in alphabetical order)
#===============================================================================


@login_required
def dataset_code_mentions( request_IN ):

    '''
    View for coding a single DataSetCitation.  Form accepts DataSetCitation ID.
        If DataSetCitation ID present, looks up coding for the related article
        for current user.  If found, loads it, if not, initializes to empty.
        Loads article, loads coding form, then if existing coding, pre-populates
        coding form.
    '''

    # return reference
    response_OUT = None

    # declare variables
    me = "dataset_code_mentions"
    logger_name = ""
    debug_message = ""
    
    # declare variables - exception handling
    exception_message = ""
    is_exception = False
    do_cleanup_post_exception = False
    
    # declare variables - processing request
    response_dictionary = {}
    default_template = ''
    article_lookup_form = None
    is_form_ready = False
    request_data = None
    source = None
    tags_in_list = None
    citation_id = -1
    citation_qs = None
    citation_count = -1
    citation_instance = None
    article_id = -1
    article_instance = None
    article_paragraph_list = None
    
    # declare variables - coding submission.
    data_store_json_string = ""
    current_user = None
    has_existing_article_data = False
    article_data_qs = None
    article_data_count = -1
    article_data_instance = None
    article_data_id = -1
    article_data_id_list = []
    is_ok_to_process_coding = True
    manual_article_coder = None
    result_article_data = None
    coding_status = ""
    new_data_store_json = None
    new_data_store_json_string = ""
    page_status_message = ""
    page_status_message_list = []
    
    # declare variables - interacting with article text
    article_content = ""
    article_content_line_list = []
    article_text_custom = ""
    article_content_bs = None
    p_tag_list = []
    p_tag_count = -1
    rendered_article_html = ""
    paragraph_index = -1
    paragraph_number = -1
    p_tag_bs = None
    p_tag_html = ""

    # declare variables - data set citation coding
    data_set_citation_lookup_form = None
    
    # declare variables - submit coding back to server
    coding_submit_form = None

    # set logger_name
    logger_name = "sourcenet.views." + me
    
    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )
    response_dictionary[ 'manual_article_coder' ] = None
    response_dictionary[ 'article_instance' ] = None
    response_dictionary[ 'article_text' ] = None
    response_dictionary[ 'article_text_custom' ] = None
    response_dictionary[ 'article_text_render_type' ] = "custom"  # one of "table", "raw", "custom", "pdf"
    response_dictionary[ 'article_text_is_preformatted' ] = False
    response_dictionary[ 'article_text_wrap_in_p' ] = True
    response_dictionary[ 'mention_text_read_only' ] = False
    response_dictionary[ 'include_find_in_article_text' ] = True
    response_dictionary[ 'data_set_instance' ] = None
    response_dictionary[ 'base_simple_navigation' ] = True
    response_dictionary[ 'base_post_login_redirect' ] = reverse( dataset_code_mentions )
    response_dictionary[ 'existing_data_store_json' ] = ""
    response_dictionary[ 'page_status_message_list' ] = page_status_message_list
    
    # create manual coder and place in response so we can access constants-ish.
    manual_coder = ManualDataSetMentionsCoder()
    response_dictionary[ 'manual_coder' ] = manual_coder
    
    # set my default rendering template
    default_template = 'sourcenet_datasets/data_sets/data_set-mentions-code.html'

    # init coding status variables
    # start with it being OK to process coding.
    is_ok_to_process_coding = True
    
    # ! ---- process input parameters
    
    # do we have input parameters?
    request_data = get_request_data( request_IN )
    if ( request_data is not None ):

        # get information needed from request, add to response dictionary.

        # ==> citation_id (passed by article_code_list).
        citation_id = int( request_data.get( INPUT_NAME_CITATION_ID, -1 ) )
        response_dictionary[ INPUT_NAME_CITATION_ID ] = citation_id

        # check to see if ""
        if ( citation_id == "" ):
        
            citation_id = -1
            
        #-- END check to see if citation_id = "" --#
        
        # see if citation_id is set
        if ( citation_id > 0 ):
    
            # retrieve QuerySet that contains that citation.
            citation_qs = DataSetCitation.objects.filter( pk = citation_id )
        
            # get count of citations
            citation_count = citation_qs.count()
        
            # should only be one.
            if ( citation_count == 1 ):
            
                # get citation instance
                citation_instance = citation_qs.get()
                
                # get related instances
                article_instance = citation_instance.article
                data_set_instance = citation_instance.data_set
                #response_dictionary[ 'data_set_instance' ] = data_set_instance
        
            #-- END check if single citation. --#
            
        #-- END check to see if citation ID set --#
    
        # ==> source (passed by article_code_list).
        source = request_data.get( INPUT_NAME_SOURCE, "" )
        response_dictionary[ INPUT_NAME_SOURCE ] = source
        
        # ==> tags_in_list (passed by article_code_list).
        tags_in_list = request_data.get( INPUT_NAME_TAGS_IN_LIST, [] )
        response_dictionary[ INPUT_NAME_TAGS_IN_LIST ] = tags_in_list

        # OK to process.
        is_form_ready = True
        
    #-- END check to see if we have request data. --#
    
    # set up form objects.

    # make instance of article coding submission form.
    coding_submit_form = CodingSubmitForm( request_data )

    # make instance of DataSetCitationLookupForm
    data_set_citation_lookup_form = DataSetCitationLookupForm( request_data )

    # get current user.
    current_user = request_IN.user

    # ! ---- Article_Data

    # for now, not accepting an Article_Data ID from page, looking for
    #    Article_Data that matches current user and current article
    #    instead.
    #article_data_id = request_data.get( "article_data_id", -1 )

    # see if existing Article_Data for user and article
    if ( citation_instance is not None ):

        # we have a citation - should also have an article...
        article_instance = citation_instance.article
        article_id = article_instance.id
        
        # look up coding in database for this article by current user.
        article_data_qs = Article_Data.objects.filter( coder = current_user )
        article_data_qs = article_data_qs.filter( article = article_instance )
        
        # how many matches?
        article_data_count = article_data_qs.count()

    else:
    
        # no citation instance, so error - but, also, no article_data matches.
        article_instance = None
        article_id = -1
        article_data_count = -1

    #-- END check for citation_instance --#
    
    # DEBUG
    if ( DEBUG == True ):
        page_status_message = "data_set_citation_id {}; Citation instance {}; Article {}; article ID: {};  user {}".format( citation_id, citation_instance, article_instance, article_id, current_user )
        page_status_message_list.append( page_status_message )
    #-- END DEBUG --#
        
    if ( article_data_count == 1 ):

        # found one.  Get ID so we can update it.
        article_data_instance = article_data_qs.get()
        article_data_id = article_data_instance.id
        has_existing_article_data = True

    else:

        # either 0 or > 1.  See if > 1.
        if ( article_data_count > 1 ):

            # error - don't want to allow multiple for now.
            is_ok_to_process_coding = False

            # output log message, output status message on screen,
            #    reload coding into page from JSON.
            page_status_message = "Multiple Article_Data instances found (IDs: "

            # loop to make list of IDs
            for article_data_instance in article_data_qs:

                # add ID to status message
                article_data_id_list.append( str( article_data_instance.id ) )

            #-- END loop over Article_Data instances --#
            
            # add Article_Data ids to message
            page_status_message += ", ".join( article_data_id_list )

            # and finish message
            page_status_message += ") for user " + str( current_user ) + " and article " + str( article_instance ) + ".  There should be only one.  Did not store coding."

            # log the message.
            output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

            # place in status message variable.
            page_status_message_list.append( page_status_message )
            
            has_existing_article_data = True

        else:

            # not greater than 1, so 0 or negative (!).  OK to process.
            #is_ok_to_process_coding = True
            has_existing_article_data = False

        #-- END check to see if greater than 1. --#

    #-- END dealing with either 0 or > 1 Article_Data --#

    # ! ---- Do we have form inputs?
    if ( is_form_ready == True ):
    
        # ! ------> yes - process coding submission?
        if ( coding_submit_form.is_valid() == True ):

            # it is valid - retrieve data_store_json and article_data_id
            data_store_json_string = request_data.get( "data_store_json", "" )

            # got any JSON?
            data_store_json_string = data_store_json_string.strip()
            if ( ( data_store_json_string is None ) or ( data_store_json_string == "" ) ):

                # no JSON - no need to process coding.
                is_ok_to_process_coding = False

            #-- END check to see if we have any JSON --#
                        
            # OK to process coding?
            if ( is_ok_to_process_coding == True ):

                # Wrap this all in a try-except, so we can return decent error
                #    messages.
                try:

                    # process data store JSON.
                    article_data_instance = manual_coder.process_data_store_json( citation_instance,
                                                                                  current_user,
                                                                                  data_store_json_string,
                                                                                  article_data_id,
                                                                                  request_IN,
                                                                                  response_dictionary )
    
                    # got anything back?
                    coding_status = ""
                    if ( article_data_instance is not None ):
    
                        # get status from article data instance
                        coding_status = article_data_instance.status_messages
    
                    #-- END check to see if we have an Article_Data instance --#
    
                    # got a status?
                    if ( ( coding_status is not None ) and ( coding_status != "" ) ):
    
                        # short circuit article lookup (use empty copy of form) if success.
                        if ( coding_status == STATUS_SUCCESS ):
    
                            # no longer emptying things out - load existing
                            #    coding, so you can edit.

                            # Add status message that just says that Coding was saved.
                            page_status_message_list.append( "Article data successfully saved!" )
    
                        elif ( coding_status != "" ):
    
                            # got an error status.  Log and output it.
                            page_status_message = "There was an error processing your coding: " + coding_status
    
                            # log it...
                            output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )
    
                            # ...and output it.
                            page_status_message_list.append( page_status_message )
    
                        #-- END check to see what status message is --#
    
                    #-- END check to see if status message returned at all --#
                    
                except Exception as e:
                
                    # set exception flag
                    is_exception = True
                
                    # Capture exception message.
                    my_exception_helper = ExceptionHelper()

                    # log exception, no email or anything.
                    exception_message = "Exception caught for user " + str( current_user.username ) + ", article " + str( article_id )
                    my_exception_helper.process_exception( e, exception_message )
                    
                    output_debug( exception_message, me, indent_with_IN = "======> ", logger_name_IN = logger_name )
                    
                    # and, create status message from Exception message.
                    page_status_message = "There was an unexpected exception caught while processing your coding: " + str( e )

                    # log it...
                    output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                    # ...and output it.
                    page_status_message_list.append( page_status_message )    

                #-- END try/except around article data processing. --#

            #-- END check to see if OK to process coding. --#
            
        #-- END check to see if coding form is valid (do we process a coding submission?). --#

        # ! ---- figure out if there is coding data to provide to page.
        #            ...if and which data store JSON we return.

        # check to see if error processing data (exception).
        if ( is_exception == True ):
        
            # yes, exception.  In "existing_data_store_json", override to pass
            #    back what was passed in.
            if ( ( data_store_json_string is not None ) and ( data_store_json_string != "" ) ):
            
                #output_debug( "\n\ndata_store_json_string : \n\n" + data_store_json_string, me )
                
                '''
                # got JSON that was passed in.  After escaping nested quotes,
                #    return it.
                new_data_store_json = json.loads( data_store_json_string )
                
                # escape string values
                new_data_store_json = JSONHelper.escape_all_string_json_values( new_data_store_json, do_double_escape_quotes_IN = True )
                
                # convert to string
                new_data_store_json_string = json.dumps( new_data_store_json )
                '''
                
                new_data_store_json_string = data_store_json_string.replace( "\\\"", "\\\\\\\"" )
                
                # output_debug( "\n\nnew_data_store_json_string : \n\n" + new_data_store_json_string, me )

                # store in response dictionary.
                response_dictionary[ 'existing_data_store_json' ] = new_data_store_json_string

            #-- END check to see if existing JSON. --#

            # got Article_Data that we created new?
            if ( ( has_existing_article_data == False ) and ( article_data_instance is not None ) ):
            
                # we created an Article_Data, then had an exception.  Delete?
                if ( do_cleanup_post_exception == True ):
                
                    # delete Article_Data and all child records.
                    article_data_instance.delete()
                    article_data_instance = None
                    
                #-- END check to see if we are to clean up after an exception. --#
                
            #-- END check to see if we have a new Article_Data instance --#

        else:
        
            # got article_data?
            if ( article_data_instance is not None ):
    
                # convert to JSON and store in response dictionary - so data is displayed.
                new_data_store_json = ManualDataSetMentionsCoder.convert_article_data_to_data_store_json( article_data_instance, citation_instance )
                new_data_store_json_string = json.dumps( new_data_store_json )
                #output_debug( "\n\nnew_data_store_json_string : \n\n" + new_data_store_json_string, me )
                response_dictionary[ 'existing_data_store_json' ] = new_data_store_json_string
    
                # output a message that we've done this.
                page_status_message = "Loaded article " + str( article_instance.id ) + " coding for user " + str( current_user )
                page_status_message_list.append( page_status_message )
    
            #-- END check to see if we have an Article_Data instance --#
                
        #-- END check to see if exception --#
        
        # ! ---- process DataSetCitation lookup?
        if ( data_set_citation_lookup_form.is_valid() == True ):

            # retrieve DataSetCitation specified by the input parameter, then
            #   create HTML output of article plus Article_Text.
            
            # get article ID.
            # already populated above.
            #article_id = request_IN.POST.get( "article_id", -1 )

            # retrieve QuerySet that contains that article.
            article_qs = Article.objects.filter( pk = article_id )

            # get count of queryset return items
            if ( ( article_qs != None ) and ( article_qs != "" ) ):

                # get count of articles
                article_count = article_qs.count()
    
                # should only be one.
                if ( article_count == 1 ):
                
                    # get article instance
                    article_instance = article_qs.get()
                    
                    # ! ---- retrieve article text.
                    article_text = article_instance.article_text_set.get()
                    
                    # get content
                    article_content = article_text.get_content()
                    
                    # ! ------ create custom text
                    article_content_line_list = article_content.split( "\n" )
                    article_text_custom = "<p>" + "</p>\n<p>".join( article_content_line_list ) + "</p>"
                    response_dictionary[ 'article_text_custom' ] = article_text_custom
                    
                    # ! ------ table HTML
                    # parse with beautifulsoup
                    article_content_bs = BeautifulSoup( article_content, "html5lib" )
                    
                    # get paragraph tag list
                    p_tag_list = article_content_bs.find_all( 'p' )
                    p_tag_count = len( p_tag_list )
                    
                    # got p-tags?
                    if ( p_tag_count > 0 ):
                    
                        # yes.  create a table with two columns per row:
                        # - paragraph number
                        # - paragraph text
                        rendered_article_html = '''
                            <table class="gridtable">
                                <tr>
                                    <th>graf#</th>
                                    <th>text</th>
                                </tr>
                        '''
                    
                        # for each paragraph, grab that <p> and place it in a table
                        #    cell.
                        for paragraph_index in range( p_tag_count ):
                        
                            # paragraph number is index + 1
                            paragraph_number = paragraph_index + 1
                            
                            # get <p> tag with ID of paragraph_number
                            p_tag_bs = article_content_bs.find( id = str( paragraph_number ) )
                            
                            # render row
                            p_tag_html = p_tag_bs.prettify()
                            #p_tag_html = StringHelper.encode_string( p_tag_html, output_encoding_IN = StringHelper.ENCODING_UTF8 )
                            debug_message = "p_tag_html type = " + str( type( p_tag_html ) )
                            output_debug( debug_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                            # calling str() on any part of a string being
                            #    concatenated causes all parts of the string to
                            #    try to encode to default encoding ('ascii').
                            #    This breaks if there are non-ascii characters.
                            rendered_article_html += "\n        <tr><td>" + StringHelper.object_to_unicode_string( paragraph_number ) + "</td><td>" + p_tag_html + "</td></tr>"
                        
                        #-- END loop over <p> ids. --#
                        
                        rendered_article_html += "</table>"
                    
                    else:
                    
                        # no p-tags - just use article_text.
                        rendered_article_html = article_content
                        
                    #-- END check to see if paragraph tags. --#
                    
                    # seed response dictionary.
                    response_dictionary[ 'citation_instance' ] = citation_instance
                    response_dictionary[ 'article_instance' ] = article_instance
                    response_dictionary[ 'article_text' ] = article_text
                    response_dictionary[ 'data_set_instance' ] = data_set_instance
                    response_dictionary[ 'article_content' ] = rendered_article_html
                    response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form
                    response_dictionary[ 'coding_submit_form' ] = coding_submit_form
                    response_dictionary[ 'base_include_django_ajax_selects' ] = True
                    
                    # get paragraph list
                    #article_paragraph_list = article_text.get_paragraph_list()
                    
                elif ( article_count > 1 ):

                    # error - multiple articles found for ID. --#

                    # create error message.
                    page_status_message = "ERROR - lookup for article ID " + str( article_id ) + " returned " + str( article_count ) + " records.  Oh my..."
                    
                    # log it...
                    output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                    # ...and output it.
                    page_status_message_list.append( page_status_message )

                    # and pass on the form.
                    response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form

                elif ( article_count == 0 ):

                    # error - multiple articles found for ID. --#

                    # create error message.
                    page_status_message = "No article found for article ID " + str( article_id ) + "."

                    # log it...
                    output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                    # ...and output it.
                    page_status_message_list.append( page_status_message )

                    # and pass on the form.
                    response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form

                else:
                
                    # unknown error. --#

                    # create error message.
                    page_status_message = "Unknown error encountered looking up article ID " + str( article_id ) + "."

                    # log it...
                    output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                    # ...and output it.
                    page_status_message_list.append( page_status_message )

                    # and pass on the form.
                    response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form
                    
                #-- END check to see if there is one or other than one. --#

            else:
            
                # ERROR - nothing returned from attempt to get queryset (would expect empty query set)

                    # create error message.
                    page_status_message = "ERROR - no QuerySet returned from call to filter().  This is odd."

                    # log it...
                    output_debug( page_status_message, me, indent_with_IN = "====> ", logger_name_IN = logger_name )

                    # ...and output it.
                    page_status_message_list.append( page_status_message )

                    # and pass on the form.
                    response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form

            #-- END check to see if query set is None --#

        else:

            # not valid - render the form again
            response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form

        #-- END check to see whether or not form is valid. --#

    else:
    
        # new request, make an empty instance of DataSetCitationLookup form.
        data_set_citation_lookup_form = DataSetCitationLookupForm()
        response_dictionary[ 'data_set_citation_lookup_form' ] = data_set_citation_lookup_form

    #-- END check to see if new request or POST --#
    
    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method dataset_code_mentions() --#


@login_required
def dataset_mention_coding_list( request_IN ):

    '''
    This view allows a user to look up a set of data set citations (first by
        entering a tag to use to filter), and then see which have been coded.
        Regardless, for each article provides a link to code.
    '''

    #return reference
    response_OUT = None

    # declare variables
    me = "dataset_mention_coding_list"
    current_user = None
    response_dictionary = {}
    default_template = ''
    request_inputs = None
    dataset_mention_coding_list_form = None
    tags_in_list = []
    is_form_ready = False
    citation_qs = None
    citation_counter = -1
    article_data_qs = None
    citation_details_list = []
    citation_details = {}
    citation_instance = ""
    
    # declare variables - Article_Data lookup
    related_article = None
    related_data_set = None
    related_article_id = None
    article_data = None
    citation_status = ""
    mention_qs = None
    mention_count = -1
    
    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )
    response_dictionary[ 'base_simple_navigation' ] = True
    response_dictionary[ 'base_post_login_redirect' ] = reverse( dataset_mention_coding_list )

    # set my default rendering template
    default_template = 'sourcenet_datasets/data_sets/data_set-mentions-code-list.html'
    
    # get current user
    current_user = request_IN.user

    # variables for building, populating person array that is used to control
    #    building of network data matrices.

    # do we have input parameters?
    request_inputs = get_request_data( request_IN )
    
    # got inputs?
    if ( request_inputs is not None ):
        
        # create ArticleCodingListForm
        dataset_mention_coding_list_form = DataSetMentionsCodingListForm( request_inputs )

        # get information we need from request.
        tags_in_list = request_inputs.get( INPUT_NAME_TAGS_IN_LIST, [] )

        is_form_ready = True
    
    else:
    
        # no inputs - create empty form
        dataset_mention_coding_list_form = DataSetMentionsCodingListForm()

        is_form_ready = False
    
    #-- END check to see if inputs. --#

    # store form in response
    response_dictionary[ 'dataset_mention_coding_list_form' ] = dataset_mention_coding_list_form

    # store tags in list value in response dictionary.
    response_dictionary[ 'tags_in_list' ] = tags_in_list
    
    # form ready?
    if ( is_form_ready == True ):

        if ( dataset_mention_coding_list_form.is_valid() == True ):

            # retrieve DataSetCitations specified by the input parameters,
            #     ordered by ID, then create HTML output of list of articles.
            #     For each, output:
            #     - article string and data set strings
            #     - link to code mentions for citation.
            
            # retrieve QuerySet that contains citations with requested tag(s).
            tags_in_list = ListHelper.get_value_as_list( tags_in_list )
            
            # filter?
            if ( ( tags_in_list is not None ) and ( len( tags_in_list ) > 0 ) ):

                # something in list - filter.
                citation_qs = DataSetCitation.objects.filter( tags__name__in = tags_in_list )
                citation_qs = citation_qs.order_by( "id" )
            
            #-- END check to see if anything in list. --#

            # get count of queryset return items
            if ( ( citation_qs != None ) and ( citation_qs != "" ) ):

                # get count of citations
                citation_count = citation_qs.count()
    
                # got one or more?
                if ( citation_count >= 1 ):
                
                    # yes - initialize list of citation_details
                    citation_details_list = []
                
                    # loop over citations
                    citation_counter = 0
                    for citation_instance in citation_qs:
                    
                        # increment citation_counter
                        citation_counter += 1
                    
                        # new citation_details
                        citation_details = {}
                        
                        # store index and article
                        citation_details[ "index" ] = citation_counter
                        citation_details[ "citation_instance" ] = citation_instance
                        
                        # see if there is an Article_Data for current user.
                        try:
                        
                            # look up Article_Data for this user...
                            article_data_qs = Article_Data.objects.filter( coder = current_user )
                            
                            # ...and the article related to this citation...
                            related_article = citation_instance.article
                            article_data = article_data_qs.get( article = related_article )
                            
                            # then look for mentions related to the dataset.
                            related_data_set = citation_instance.data_set
                            mention_qs = article_data.datasetmention_set.filter( data_set = related_data_set )
                            mention_count = mention_qs.count()
                            
                            # got any mentions?
                            if ( mention_count > 0 ):
                            
                                # if we get here, one Article_Data, and mentions
                                citation_status = "coded"
                                
                            else:
                            
                                # if we get here, one Article_Data, no mentions
                                citation_status = "pending"
                                
                            #-- END check to see if mentions coded for this article. --#  
                            
                        except Article_Data.MultipleObjectsReturned as amore:
                        
                            # multiple returned.
                            article_data = None
                            citation_status = "multiple"

                        except Article_Data.DoesNotExist as adne:
                        
                            # None returned.
                            article_data = None
                            citation_status = "new"

                        except Exception as e:
                        
                            # multiple returned.
                            article_data = None
                            citation_status = "error" + str( e )
                            
                        #-- END attempt to get Article_Data for current user. --#
                        
                        # place article_data in article_details
                        citation_details[ "article_data" ] = article_data
                        citation_details[ "citation_status" ] = citation_status
                        
                        # add details to list.
                        citation_details_list.append( citation_details )

                    #-- END loop over citations --#
                    
                    # seed response dictionary.
                    response_dictionary[ 'citation_details_list' ] = citation_details_list
                    
                else:
                
                    # error - none or multiple articles found for ID. --#
                    print( "No citation returned for ID passed in." )
                    response_dictionary[ 'output_string' ] = "ERROR - nothing in QuerySet returned from call to DataSetCitation.filter() ( tags_in_list_IN = " + str( tags_in_list ) + " )."
                    response_dictionary[ 'dataset_mention_coding_list_form' ] = dataset_mention_coding_list_form
                    
                #-- END check to see if there is one or other than one. --#

            else:
            
                # ERROR - nothing returned from attempt to get queryset (would expect empty query set)
                response_dictionary[ 'output_string' ] = "ERROR - no QuerySet returned from call to DataSetCitation.filter().  This is odd."
                
            #-- END check to see if query set is None --#

        else:

            # not valid - render the form again
            response_dictionary[ 'output_string' ] = "DataSetMentionsCodingListForm is not valid."

        #-- END check to see whether or not form is valid. --#

    else:
    
        # new request, just use empty instance of form created and stored above.
        pass

    #-- END check to see if new request or POST --#
    
    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view function dataset_mention_coding_list() --#

    
@login_required
def index( request_IN ):
    
    # return reference
    me = "index"
    response_OUT = None
    response_dictionary = {}
    default_template = ''

    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'sourcenet_datasets/index.html'

    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method index() --#

