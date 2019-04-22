from __future__ import unicode_literals

'''
Copyright 2010-2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_data.

context_data is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_data. If not, see http://www.gnu.org/licenses/.
'''

'''
How to add a value to one of these context_data forms and then get that value
properly passed through to all the things that might use it:

- 1) If your form input will have a set of values from which the user will
    choose, figure out what those values will be and make variables to hold the
    specific values and to hold a dictionary that maps values to display names
    in the appropriate class in context_data.  For example:
    - add parameters related to network output to the class NetworkOutput in
        file /export/network_output.py (though if those parameters will also be
        used by NetworkDataOutput, you should declare them there, then just
        reference them in NetworkOutput).
    - add parameters related to automated coding of articles to the class
        ArticleCoding, in file /article_coding/article_coding.py.
        
    Example - adding person query type values to NetworkDataOutput:
    
        # Person Query Types
        PERSON_QUERY_TYPE_ALL = "all"
        PERSON_QUERY_TYPE_ARTICLES = "articles"
        PERSON_QUERY_TYPE_CUSTOM = "custom"
        
        PERSON_QUERY_TYPE_CHOICES_LIST = [ 
            ( PERSON_QUERY_TYPE_ALL, "All persons" ),
            ( PERSON_QUERY_TYPE_ARTICLES, "From selected articles" ),
            ( PERSON_QUERY_TYPE_CUSTOM, "Custom, defined below" ),
        ]

    And then referencing them from NetworkOutput:
    
        # Person Query Types
        PERSON_QUERY_TYPE_ALL = NetworkDataOutput.PERSON_QUERY_TYPE_ALL
        PERSON_QUERY_TYPE_ARTICLES = NetworkDataOutput.PERSON_QUERY_TYPE_ARTICLES
        PERSON_QUERY_TYPE_CUSTOM = NetworkDataOutput.PERSON_QUERY_TYPE_CUSTOM
    
        PERSON_QUERY_TYPE_CHOICES_LIST = NetworkDataOutput.PERSON_QUERY_TYPE_CHOICES_LIST    

- 2) Add a PARAM_* constant that contains the input name you'll use to reference
    the new field in the form, and then subsequently whenever the associated 
    value is needed throughout the application.  Example - adding a person query
    type to tell network outputter how to figure out which people to include in
    the network, first to NetworkDataOutput:
    
        PARAM_PERSON_QUERY_TYPE = "person_query_type"

    Then, referring to it in NetworkOutput:
    
        PARAM_PERSON_QUERY_TYPE = NetworkDataOutput.PARAM_PERSON_QUERY_TYPE
        
- 3) Add that parameter to PARAM_NAME_TO_TYPE_MAP in NetworkOutput or
    ArticleCoding, with the parameter name mapped to the appropriate type from
    the ParamContainer class in python_utilities.  Example, adding our string
    person query type to NetworkOutput's PARAM_NAME_TO_TYPE_MAP:
    
        PARAM_PERSON_QUERY_TYPE : ParamContainer.PARAM_TYPE_STRING,

- 4) Add the value to the appropriate form below, using the same name as was in
    your PARAM_* constant.  Example - adding a person query type select box to
    the person select form, referencing the choices list defined above:

        person_query_type = forms.ChoiceField( required = False, choices = NetworkOutput.PERSON_QUERY_TYPE_CHOICES_LIST )

- 5) Into what function or method do I then update processing to include the
    new field?:
    - For network output, method that creates QuerySets from form parameters is
        create_query_set(), in context_data/export/network_output.py,
        NetworkOutput.create_query_set().  This method is called by both
        create_person_query_set() and create_network_query_set().  If you add
        a parameter to the article select and the person select, make sure
        make the name of the person input the same as the article one, but
        preceded by "person_".  That will make the single method able to
        process values for either the article or person form.  For example, the
        coder_type_filter_type, from NetworkDataOutput class:

            PARAM_CODER_TYPE_FILTER_TYPE = "coder_type_filter_type"
            PARAM_PERSON_CODER_TYPE_FILTER_TYPE = "person_" + PARAM_CODER_TYPE_FILTER_TYPE

'''

# import six for Python 2 and 3 compatibility.
import six

# import django form object.
from django import forms


#===============================================================================
# ! ==> Parent classes imported from python_utilities.django_utils.django_form_helper
#===============================================================================


#===============================================================================
# ! ==> Classes
#===============================================================================


class CodingSubmitForm( forms.Form ):

    '''
    form to hold coding details for a given coding exercise.
    '''

    # data store JSON
    data_store_json = forms.CharField( required = False, widget = forms.HiddenInput() )
    article_data_id = forms.IntegerField( required = False, widget = forms.HiddenInput() )

#-- END Form class CodingSubmitForm --#


class DataSetCitationLookupForm( forms.Form ):

    '''
    create a form to let a user lookup an article to view its contents.
    '''

    # DataSetCitation ID
    data_set_citation_id = forms.IntegerField( required = True, label = "DataSetCitation ID" )

#-- Form class END ArticleLookupForm --#


class DataSetMentionsCodingListForm( forms.Form ):

    '''
    form to hold lookup criteria for DataSetCitations that need to be coded.
        To start, just includes list of tags.
    '''

    # list of unique tags to limit to.
    tags_in_list = forms.CharField( required = True, label = "DataSetCitation Tag List (comma-delimited)" )

#-- END Form class DataSetMentionsCodingListForm --#

