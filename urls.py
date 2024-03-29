from __future__ import unicode_literals

'''
Copyright 2010-2016 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_data.

context_data is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_data is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_data. If not, see http://www.gnu.org/licenses/.
'''

# import djanfgo.conf.urls.defaults stuff.
#from django.conf.urls.defaults import *
from django.urls import include
from django.urls import re_path

# and import stuff to use the admin's login page for all authentication.
from django.contrib.auth import views as auth_views

# import sourcent_datasets views
import context_data.views

'''
# !tastypie API
# import tastypie stuff, so we can make REST-ful API
from tastypie.api import Api
from context_text.tastypie_api.context_text_api import ArticleResource

# initialize context_text API, v1
v1_api = Api( api_name='v1' )

# register resources
v1_api.register( ArticleResource() )
'''

# polls-specific URL settings, intended to be included in master urls.py file.
urlpatterns = [

    # index page
    re_path( r'^index$', context_data.views.index, name = "context_data-index" ),

    # data set mention coding pages
    re_path( r'^dataset/code_mentions/list/', context_data.views.dataset_mention_coding_list, name = "context_data-dataset_mention_coding_list" ),
    re_path( r'^dataset/code_mentions/', context_data.views.dataset_code_mentions, name = "context_data-dataset_code_mentions" ),
    re_path( r'^dataset/code_citations/', context_data.views.article_code_citations, name = "context_data-article-code_data_set_mentions" ),

]
