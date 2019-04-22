from __future__ import unicode_literals

'''
Copyright 2010-2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_data.

context_data is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================


# python base imports
import calendar
#from datetime import date
import datetime

# django classes
from django.contrib.auth.models import User
from django.db.models import Q

# python_utilities
from python_utilities.parameters.param_container import ParamContainer
from python_utilities.rate_limited.basic_rate_limited import BasicRateLimited

# context_text
from context_text.shared.context_text_base import ContextTextBase

#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class ContextDataBase( ContextTextBase ):


    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish (building on ContextTextBase)
    #---------------------------------------------------------------------------


    # django_config - highlighting data set info in text
    DJANGO_CONFIG_NAME_PROCESS_FOUND_SYNONYMS = "process_found_synonyms"

    # View response dictionary keys - highlighting data set info in text
    VIEW_RESPONSE_KEY_PROCESS_FOUND_SYNONYMS = DJANGO_CONFIG_NAME_PROCESS_FOUND_SYNONYMS

        
    #-----------------------------------------------------------------------------
    # ! ==> class methods
    #-----------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ==> __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( ContextDataBase, self ).__init__()

        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase).
        self.set_logger_name( "context_data.shared.context_data_base" )
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # ! ==> instance methods, in alphabetical order
    #---------------------------------------------------------------------------


#-- END class ContextDataBase --#