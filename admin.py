from django.contrib import admin

# Register your models here.

import six
from six.moves import range

# import code for AJAX select
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Import models
from context_data.models import DataSet
from context_data.models import DataSetIdentifier
from context_data.models import DataSetCitation
from context_data.models import DataSetCitationData
from context_data.models import DataSetMention
from context_data.models import WorkDataSetCitation
from context_data.models import WorkDataSetCitationMention
from context_data.models import WorkDataSetMention
from context_data.models import WorkResearchField
from context_data.models import WorkResearchMethod
from context_data.models import DataReference
from context_data.models import DataReferenceMention
from context_data.models import DataReferenceContext

#admin.site.register( DataSet )
admin.site.register( DataSetIdentifier )
#admin.site.register( DataSetCitation )
admin.site.register( DataSetCitationData )
admin.site.register( DataSetMention )
admin.site.register( WorkDataSetCitation )
admin.site.register( WorkDataSetCitationMention )
admin.site.register( WorkDataSetMention )
admin.site.register( WorkResearchField )
admin.site.register( WorkResearchMethod )
#admin.site.register( DataReference )
admin.site.register( DataReferenceMention )
admin.site.register( DataReferenceContext )

#-------------------------------------------------------------------------------
# DataSet admin definition
#-------------------------------------------------------------------------------

class DataSetIdentifierInline( admin.TabularInline ):

    model = DataSetIdentifier
    extra = 1
    fk_name = 'data_set'

#-- END Person_Newspaper_Inline model --#

class DataSetAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context_text.lookups.py
    form = make_ajax_form( DataSet, dict( parent_data_set = 'datasets' ) )

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'name', 'title', 'unique_identifier', 'family_identifier', 'parent_data_set', 'description', 'date', 'tags' ]
            }
        ),
        (
            "More details (Optional)",
            {
                'fields' : [ 'citation', 'coverages', 'subjects', 'methodology', 'additional_keywords' ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    inlines = [
        DataSetIdentifierInline
    ]

    list_display = ( 'id', 'name', 'unique_identifier', 'family_identifier', 'title', 'date' )
    list_display_links = ( 'id', 'name' )
    search_fields = [ 'name', 'title', 'unique_identifier', 'description', 'citation', 'coverages', 'subjects', 'methodology', 'additional_keywords' ]
    date_hierarchy = 'create_date'

admin.site.register( DataSet, DataSetAdmin )


#-------------------------------------------------------------------------------
# DataSetCitation admin definition
#-------------------------------------------------------------------------------

class DataSetCitationAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context_text.lookups.py
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


#-------------------------------------------------------------------------------
# DataReference admin definition
#-------------------------------------------------------------------------------

class DataReferenceAdmin( admin.ModelAdmin ):

    # set up ajax-selects - for make_ajax_form, 1st argument is the model you
    #    are looking to make ajax selects form fields for; 2nd argument is a
    #    dict of pairs of field names in the model in argument 1 (with no quotes
    #    around them) mapped to lookup channels used to service them (lookup
    #    channels are defined in settings.py, implenented in a separate module -
    #    in this case, implemented in context_text.lookups.py
    form = make_ajax_form( DataReference, dict( article = 'article', related_data_sets = 'datasets', data_set = 'datasets', article_data = 'article_data' ) )

    fieldsets = [
        (
            None,
            {
                'fields' : [ 'article', 'citation_type', 'related_data_sets', 'title', 'key_terms', 'tags' ]
            }
        ),
        (
            "More details (Optional)",
            {
                'fields' : [
                    'score',
                    'match_confidence_level',
                    'match_status',
                    'capture_method',
                    'notes',
                    'context_text',
                    'article_data',
                    'work_log',
                    'coder',
                    'coder_type',
                    'data_set'
                ],
                'classes' : ( "collapse", )
            }
        ),
    ]

    list_display = ( 'id', 'citation_type', 'article', 'key_terms', 'create_date' )
    list_display_links = ( 'id', 'citation_type' )
    search_fields = [ 'id' ]
    date_hierarchy = 'create_date'

admin.site.register( DataReference, DataReferenceAdmin )

