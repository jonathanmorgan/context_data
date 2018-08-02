from django.contrib import admin

# Register your models here.

import six
from six.moves import range

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Import models
from sourcenet_datasets.models import DataSet
from sourcenet_datasets.models import DataSetIdentifier
from sourcenet_datasets.models import DataSetCitation
from sourcenet_datasets.models import DataSetMention

admin.site.register( DataSet )
admin.site.register( DataSetIdentifier )
#admin.site.register( DataSetCitation )
admin.site.register( DataSetMention )

#-------------------------------------------------------------------------------
# DataSetCitation admin definition
#-------------------------------------------------------------------------------

class DataSetCitationAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in sourcenet.ajax-select-lookups.py
    form = make_ajax_form( DataSetCitation, dict( article = 'article', data_set = 'datasets', article_data = 'article_data' ) )

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'article', 'data_set', 'citation_type', 'tags' ]
            }
        ),
        (
            "More details (Optional)",
            {
                'fields' : [ 'article_data', 'match_confidence_level', 'match_status', 'capture_method', 'notes' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'citation_type', 'article', 'data_set', 'create_date' )
    list_display_links = ( 'id', 'citation_type' )
    search_fields = [ 'id' ]
    date_hierarchy = 'create_date'

admin.site.register( DataSetCitation, DataSetCitationAdmin )

