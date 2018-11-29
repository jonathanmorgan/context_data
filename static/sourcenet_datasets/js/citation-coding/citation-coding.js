//============================================================================//
// javascript for article coding.
//============================================================================//

// ! requires sourcenet.js
// ! requires find-in-text.js

//----------------------------------------------------------------------------//
// !====> namespace!
//----------------------------------------------------------------------------//


var SOURCENET = SOURCENET || {};


//----------------------------------------------------------------------------//
// !====> namespaced variables
//----------------------------------------------------------------------------//


// JSON to prepopulate page if we are editing.
SOURCENET.data_store_json = null;
SOURCENET.article_data_id = -1;

// mention store used to keep track of authors and mentions while coding.
SOURCENET.data_store = null;

// DEBUG!
SOURCENET.debug_flag = false;

// JSON property names
SOURCENET.JSON_PROP_MENTION_TEXT = "mention_text";
SOURCENET.JSON_PROP_FIXED_MENTION_TEXT = "fixed_mention_text";
SOURCENET.JSON_PROP_MENTION_TYPE = "mention_type";
SOURCENET.JSON_PROP_MENTION_INDEX = "mention_index";
SOURCENET.JSON_PROP_DATA_SET_MENTION_ID = "data_set_mention_id";
SOURCENET.JSON_PROP_ORIGINAL_MENTION_TYPE = "original_mention_type";

// mention types:
SOURCENET.MENTION_TYPE_CITED = "cited";
SOURCENET.MENTION_TYPE_ANALYZED = "analyzed";
SOURCENET.MENTION_TYPE_ARRAY = [ SOURCENET.MENTION_TYPE_CITED, SOURCENET.MENTION_TYPE_ANALYZED ];

// Mention coding submit button values
SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_WAIT = "Please wait...";
SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_PROCESS = "Process Article Coding";
SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_RESET = "Process Article Coding!";

// ! HTML element IDs
SOURCENET.DIV_ID_ARTICLE_BODY = "article_view";
SOURCENET.DIV_ID_MENTION_CODING = "mention-coding";
SOURCENET.INPUT_ID_MENTION_TEXT = "mention-text";
SOURCENET.INPUT_ID_MENTION_TYPE = "mention-type";
SOURCENET.INPUT_ID_MENTION_INDEX = "data-store-mention-index";
SOURCENET.INPUT_ID_ORIGINAL_MENTION_TYPE = "original-mention-type";
SOURCENET.INPUT_ID_DATA_SET_MENTION_ID = "data-set-mention-id";

// HTML elements - fix mention text
SOURCENET.DIV_ID_FIX_MENTION_TEXT_LINK = "fix-mention-text-link";
SOURCENET.DIV_ID_FIX_MENTION_TEXT = "fix-mention-text";
SOURCENET.INPUT_ID_FIXED_MENTION_TEXT = "fixed-mention-text";

// HTML elements - form submission
SOURCENET.INPUT_ID_SUBMIT_ARTICLE_CODING = "input-submit-article-coding";
SOURCENET.INPUT_ID_DATA_STORE_JSON = "id_data_store_json";

//----------------------------------------------------------------------------//
// ! FIND IN ARTICLE TEXT
//----------------------------------------------------------------------------//

// Find in Article Text - Dynamic CSS class names
//SOURCENET.CSS_CLASS_FOUND_IN_TEXT = "foundInText";
//SOURCENET.CSS_CLASS_FOUND_IN_TEXT_MATCHED_WORDS = "foundInTextMatchedWords";
//SOURCENET.CSS_CLASS_FOUND_IN_TEXT_RED = "foundInTextRed";
//SOURCENET.CSS_CLASS_FOUND_IN_TEXT_MATCHED_WORDS_RED = "foundInTextMatchedWordsRed";

// defaults:
//SOURCENET.CSS_CLASS_DEFAULT_P_MATCH = SOURCENET.CSS_CLASS_FOUND_IN_TEXT;
//SOURCENET.CSS_CLASS_DEFAULT_WORD_MATCH = SOURCENET.CSS_CLASS_FOUND_IN_TEXT_MATCHED_WORDS;

// Find in Article Text - HTML element IDs
//SOURCENET.INPUT_ID_TEXT_TO_FIND_IN_ARTICLE = "text-to-find-in-article";

// Find in Article Text - HTML for matched word highlighting
//SOURCENET.HTML_SPAN_TO_CLASS = "<span class=\""
//SOURCENET.HTML_SPAN_AFTER_CLASS = "\">";
//SOURCENET.HTML_SPAN_CLOSE = "</span>";
//SOURCENET.HTML_SPAN_MATCHED_WORDS = SOURCENET.HTML_SPAN_TO_CLASS + SOURCENET.CSS_CLASS_DEFAULT_WORD_MATCH + SOURCENET.HTML_SPAN_AFTER_CLASS;

// Data Set highlighting
SOURCENET.INPUT_ID_TOGGLE_DATA_SET_HIGHLIGHTING = "toggle-data-set_highlighting";
SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_ON = "<== highlight OFF";
SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_OFF = "<== highlight ON";

// Compress white space in values?
SOURCENET.compress_white_space = true;

// list of strings to highlight in the text for the current data set.
SOURCENET.data_set_string_list = [];
SOURCENET.data_set_mention_list = [];
SOURCENET.process_found_synonyms = false;

// ignore wrapping elements?
SOURCENET.article_text_ignore_p_tags == false;
SOURCENET.text_finder.ignore_wrapper_element = false;

// words to ignore
SOURCENET.text_to_ignore_list = [];
SOURCENET.text_to_ignore_list.push( "the" );
SOURCENET.text_to_ignore_list.push( "The" );
SOURCENET.FindInText.add_to_ignore_list( SOURCENET.text_to_ignore_list );

// find_in_article_text parameters
//SOURCENET.find_in_article_text_type = "phrase";
SOURCENET.find_in_article_text_type = "words";


//----------------------------------------------------------------------------//
// !====> function definitions
//----------------------------------------------------------------------------//


/**
 * Opposite of SOURCENET.fix_mention_text() - show()s link to fix mention text, 
 *     hides form input and buttons to fix mention text, removes current value
 *     from "fixed-mention-text" <input>.
 *
 * Preconditions: None.
 *
 * Postconditions: show()s link to fix mention text, hides form input and
 *     buttons to fix mention text, removes current value from
 *     "fixed-mention-text" <input>.
 */
SOURCENET.cancel_fix_mention_text = function()
{
    // declare variables
    var me = "SOURCENET.cancel_fix_mention_text";
    var fix_link_div_id = "";
    var fix_link_div = null;
    var fix_area_div_id = "";
    var fix_area_div = null;
    var input_element = null;
    
    // get div that contains actual fix area and hide() it.
    fix_area_div_id = SOURCENET.DIV_ID_FIX_MENTION_TEXT;
    fix_area_div = $( '#' + fix_area_div_id );
    fix_area_div.hide();

    // clear fixed-mention-text <input>.
    SOURCENET.clear_fixed_mention_text();
    
    // get div that contains link and show() it.
    fix_link_div_id = SOURCENET.DIV_ID_FIX_MENTION_TEXT_LINK;
    fix_link_div = $( '#' + fix_link_div_id );
    fix_link_div.show();
    
} //-- END function SOURCENET.cancel_fix_mention_text() --//


/**
 * Clears out coding form and status message area, and optionally displays a
 *    status message if one passed in.
 *
 * Preconditions: for anything to appear, SOURCENET.data_store must have been
 *    initialized and at least one mention added to it.
 *
 * @param {string} status_message_IN - message to place in status area.  If undefined, null, or "", no message output.
 */
SOURCENET.clear_coding_form = function( status_message_IN )
{
    
    // declare variables.
    var me = "SOURCENET.clear_coding_form";
    var property_list = null;
    var property_info = null;
    var current_index = -1;
    var property_count = -1;
    var current_property_name = "";
    var current_property_info = null;
    var clear_form_function = null;
    var input_id = "";
    var default_value = "";
    var temp_element = null;
    
    // declare variables - outputting status messages.
    var is_status_message_OK = false;
    var status_message_array = [];
    
    // clear the coding form.
    SOURCENET.log_message( "Top of " + me );

    // get property info.
    property_list = SOURCENET.Mention_property_name_list;
    property_info = SOURCENET.Mention_property_name_to_info_map;
        
    // loop over properties
    property_count = property_list.length;
    for ( current_index = 0; current_index < property_count; current_index++ )
    {
        
        // get current property name.
        current_property_name = property_list[ current_index ];
        
        // retrieve the property info.
        current_property_info = property_info[ current_property_name ];
        
        // clear the field.
        current_property_info.clear_value();
        
    } //-- END loop over Person properties --//
    
    // clear any find-in-article-text matches, and clear find text entry field.
    SOURCENET.clear_find_in_text();
    
    // got a status message?
    if ( ( status_message_IN != null ) && ( status_message_IN != "" ) )
    {
        // make status message array (empty message will clear status area).
        status_message_array = [];
        status_message_array.push( status_message_IN );
        
        // output it.
        SOURCENET.output_status_messages( status_message_array );
    }
    
} //-- END function SOURCENET.clear_coding_form() --//


/**
 * Loads current mention_text value into field where it can be manually fixed.
 */
SOURCENET.clear_fixed_mention_text = function()
{
    
    // declare variables
    var input_element = null;

    // get fixed_mention_text text field,  place value there.
    input_element = $( '#' + SOURCENET.INPUT_ID_FIXED_MENTION_TEXT );
    input_element.val( "" );
    
} //-- END function SOURCENET.clear_fixed_mention_text() --//


/**
 * Clears out hidden input used to hold the original mention type value when we
 *     update existing coding.
 *
 * Preconditions: None.
 *
 * @param {string} status_message_IN - message to place in status area.  If undefined, null, or "", no message output.
 */
SOURCENET.clear_original_mention_type = function( status_message_IN )
{
    
    // declare variables.
    var me = "SOURCENET.clear_original_mention_type";
    var status_message_array = [];
    var temp_element = null;
    
    // clear the coding form.
    SOURCENET.log_message( "Top of " + me );
        
    // original-mention-type
    temp_element = $( '#' + SOURCENET.INPUT_ID_ORIGINAL_MENTION_TYPE );
    temp_element.val( "" );
        
    // got a status message?
    if ( ( status_message_IN != null ) && ( status_message_IN != "" ) )
    {
        // make status message array (empty message will clear status area).
        status_message_array = [];
        status_message_array.push( status_message_IN );
        
        // output it.
        SOURCENET.output_status_messages( status_message_array );
    }
    
} //-- END function SOURCENET.clear_original_mention_type() --//


/**
 * Clears out mention type field, then calls a function to reset the form for
 *     the default mention type.
 *
 * Preconditions: None.
 *
 * @param {string} status_message_IN - message to place in status area.  If undefined, null, or "", no message output.
 */
SOURCENET.clear_mention_type = function( status_message_IN )
{
    
    // declare variables.
    var me = "SOURCENET.clear_mention_type";
    var status_message_array = [];
    var temp_element = null;
    
    // clear the coding form.
    SOURCENET.log_message( "Top of " + me );
        
    // mention-type
    temp_element = $( '#' + SOURCENET.INPUT_ID_MENTION_TYPE );
    temp_element.val( "" );
    
    // call SOURCENET.process_selected_mention_type();
    SOURCENET.process_selected_mention_type();
        
    // got a status message?
    if ( ( status_message_IN != null ) && ( status_message_IN != "" ) )
    {
        // make status message array (empty message will clear status area).
        status_message_array = [];
        status_message_array.push( status_message_IN );
        
        // output it.
        SOURCENET.output_status_messages( status_message_array );
    }
    
} //-- END function SOURCENET.clear_mention_type() --//


/**
 * Repaints the area where coded mentions are displayed.
 *
 * Preconditions: for anything to appear, SOURCENET.data_store must have been
 *    initialized and at least one mention added to it.
 */
SOURCENET.display_mentions = function()
{
    
    // declare variables.
    var me = "SOURCENET.display_mentions";
    var row_id_prefix = "";
    var my_data_store = null;
    var mention_list_element = null;
    var mention_index = -1;
    var mention_count = -1;
    var current_mention = null;
    var current_row_id = "";
    var current_row_selector = "";
    var current_row_element = null;
    var current_row_element_count = -1;
    var got_mention = false;
    var mention_string = "";
    var got_row= false;
    var do_create_row = false;
    var do_update_row = false;
    var do_remove_row = false;
    var row_contents = "";
    var button_element = null;
    var hide_empty_form = false;
    
    // declare variables - make form to submit list.
    var active_mention_count = -1;
    var div_mention_list_element = null;
    var form_element = null;
    
    // initialize variables
    row_id_prefix = "mention-";
    
    // get data store
    my_data_store = SOURCENET.get_data_store();
    
    // for now, display by SOURCENET.log_message()-ing JSON string.
    //SOURCENET.log_message( "In " + me + "(): DataStore = " + JSON.stringify( my_data_store ) );
    
    // get <table id="mention-list-table" class="mentionListTable">
    mention_list_element = $( '#mention-list-table' );
    
    // loop over the mentions in the list.
    mention_count = my_data_store.mention_array.length;
    SOURCENET.log_message( "In " + me + "(): Mention Count = " + mention_count );
    
    // check to see if one or more mentions.
    if ( mention_count > 0 )
    {

        // at least 1 - loop.
        active_mention_count = 0;
        for( mention_index = 0; mention_index < mention_count; mention_index++ )
        {
            
            // initialize variables.
            got_mention = false;
            got_row = false;
            do_create_row = false;
            do_update_row = false;
            do_remove_row = false;
            button_element = null;
            
            // get mention.
            current_mention = my_data_store.get_mention_at_index( mention_index );
    
            // got mention?
            if ( current_mention != null )
            {
                // yes - set flag, update mention_string.
                got_mention = true;
                active_mention_count += 1;
                mention_string = current_mention.to_table_cell_html();
                
            }
            else
            {
    
                // SOURCENET.log_message( "In " + me + "(): no mention for index " + mention_index );
                mention_string = "null";
    
            } //-- END check to see if mention --//
            
            SOURCENET.log_message( "In " + me + "(): Mention " + mention_index + ": " + mention_string );
            
            // try to get <tr> for that index.
            current_row_id = row_id_prefix + mention_index;
            current_row_selector = "#" + current_row_id;
            current_row_element = mention_list_element.find( current_row_selector );
            current_row_element_count = current_row_element.length;
            //SOURCENET.log_message( "DEBUG: row element: " + current_row_element + "; length = " + current_row_element_count );
            
            // matching row found?
            if ( current_row_element_count > 0 )
            {
                
                // yes - set flag.
                got_row = true;
    
            } //-- END check to see if row --//
            
            // based on mention and row, what do we do?
            if ( got_row == true )
            {
                
                //SOURCENET.log_message( "In " + me + "(): FOUND <li> for " + current_li_id );
                // got mention?
                if ( got_mention == true )
                {
                    
                    // yes.  convert to string and replace value, in case there have
                    //    been changes.
                    do_create_row = false;
                    do_update_row = true;
                    do_remove_row = false;
                    
                }
                else
                {
                    
                    // no mention - remove row
                    do_create_row = false;
                    do_update_row = false;
                    do_remove_row = true;                
                    
                }
                
            }
            else //-- no row --//
            {
                
                //SOURCENET.log_message( "In " + me + "(): NO row for " + current_row_id );
                // got mention?
                if ( got_mention == true )
                {
                    
                    // yes.  convert to string and replace value, in case there have
                    //    been changes.
                    do_create_row = true;
                    do_update_row = true;
                    do_remove_row = false;
                    
                }
                else
                {
                    
                    // no mention - nothing to do.
                    do_create_row = false;
                    do_update_row = false;
                    do_remove_row = false;                
                    
                }
    
            } //-- END check to see if row for current mention. --//
            
            // Paint!
            
            SOURCENET.log_message( "In " + me + "(): WHAT TO DO?: do_create_row = " + do_create_row + "; do_update_row = " + do_update_row + "; do_remove_row = " + do_remove_row );
            
            // crate new row?
            if ( do_create_row == true )
            {
                
                // create row with id = row_id_prefix + mention_index, store in
                //    current_row_element.
                current_row_element = $( '<tr></tr>' );
                current_row_element.attr( "id", row_id_prefix + mention_index );
                
                // prepend it to the mention_list_element
                mention_list_element.prepend( current_row_element );
                
            } //-- END check to see if do_create_li --//
            
            // update contents of <tr>?
            if ( do_update_row == true )
            {
                
                // for now, just place mention string in a <td>.
                row_contents = mention_string;
                
                // (and other stuff needed for that to work.)
                row_contents += '<td><input type="button" id="remove-mention-' + mention_index + '" name="remove-mention-' + mention_index + '" value="Remove" onclick="SOURCENET.remove_mention( ' + mention_index + ' )" /></td>';
                
                current_row_element.html( row_contents );
                
            } //-- END check to see if do_update_li --//
            
            // delete <tr>?
            if ( do_remove_row == true )
            {
                
                // delete <li>.
                current_row_element.remove();
                
            } //-- END check to see if do_delete_li --//
            
        } //-- END loop over mentions in list --//
        
        // try to find the form element.
        form_element = $( '#submit-article-coding' );
        
        // hide empty form?
        if ( hide_empty_form == true )
        {
            
            // got active mentions?
            if ( active_mention_count > 0 )
            {
                
                // make sure form is visible.
                SOURCENET.log_message( "In " + me + "(): active mentions, show coding submit <form>." );
                form_element.show();
                            
            }
            else //-- no active people. --//
            {
                
                // no active people, hide form.
                SOURCENET.log_message( "In " + me + "(): no mentions, hide coding submit <form>." );
                form_element.hide();
                        
            } //-- END check to see if active people. --//
            
        } //-- END check to see if we hide empty form --//

    }
    else
    {
        
        // nothing in list.  Move on, but output log since I'm not sure why we
        //    got here.
        SOURCENET.log_message( "In " + me + "(): Nothing in mention_array.  Moving on." );
        
    } //-- END check to see if at least 1 item in list. --//
    
} //-- END function SOURCENET.display_mentions() --//


/**
 * 
 */
SOURCENET.find_and_process_data_set_synonyms = function()
{
    // declare variables
    var article_body = null;
    var article_body_text = null;
    var mention_list = null;
    var mention_count = -1;
    var mention_index = -1;
    var current_mention = null;
    var find_index = -1;
    
    // get mention list
    mention_list = SOURCENET.data_set_mention_list;
    
    // loop over the mentions.
    mention_count = mention_list.length;
    
    // got any mentions?
    if ( mention_count > 0 )
    {
        
        // retrieve article body's text.
        article_body = SOURCENET.get_article_body();
        article_body_text = article_body.text();
        article_body_text = SOURCENET.compress_internal_white_space( article_body_text );
        
        for ( mention_index = 0; mention_index < mention_count; mention_index++ )
        {
            
            // get current mention.
            current_mention = mention_list[ mention_index ];
            current_mention = SOURCENET.compress_internal_white_space( current_mention );
            
            // find it in article text (not HTML).
            SOURCENET.text_finder.find_text_in_string( current_mention, article_body_text );
            find_index = SOURCENET.text_finder.find_text_in_string_index;

            // if found, process it.
            if ( find_index > 0 )
            {
                
                // grab mention, then process.
                SOURCENET.grab_mention( current_mention );
                SOURCENET.process_mention_coding();
                
            } //-- END look for find_index --//
            
        } //-- END loop over mentions --//
        
        // clear out the mention field.
        SOURCENET.clear_coding_form( "Data Set synonyms automatically matched - any found in article have \"new\" in second column below." )
        
    } //-- END check to see if mentions. --//
        
} //-- END function SOURCENET.find_and_process_data_set_synonyms() --//


/**
 * Retrieves current mention, then looks for it in article text.
 *
 * Preconditions: None.
 *
 * Postconditions: Updates classes on article <p> tags so any that contain
 *     current last name are assigned "foundInText".
 */
SOURCENET.find_mention_text_in_article_text = function( color_IN )
{
    // declare variables
    var me = "SOURCENET.find_mention_text_in_article_text";
    var mention_text = "";
    var input_element = null;
    var find_type = "";
    
    // get mention text
    mention_text = SOURCENET.get_mention_text_value();

    debug_message = "In " + me + " - mention text = " + mention_text;
    SOURCENET.log_message( debug_message );
    //console.log( debug_message );

    // get text-to-find-in-article text field, place value.
    SOURCENET.send_text_to_find_input( mention_text );
    
    // find in text.
    find_type = SOURCENET.find_in_article_text_type;
    if ( find_type == "phrase" )
    {
        SOURCENET.find_in_article_text( mention_text, true, color_IN );    
    }
    else if ( find_type == "word" )
    {
        SOURCENET.find_words_in_article_text( mention_text, true, color_IN );
    }
    else
    {
        // default is word.
        SOURCENET.find_words_in_article_text( mention_text, true, color_IN );
    }
    
} //-- END function SOURCENET.find_mention_text_in_article_text() --//
// ! ==> mention text - single string --> find_in_article_text()


/**
 * Hides link to fix mention text, reveals form input and buttons to fix mention
 *     text, places current mention text in "fixed-mention-text" <input>.
 *
 * Preconditions: None.
 *
 * Postconditions: Hides link to fix mention text, reveals form input and buttons
 *     to fix mention text, places current mention text in "fixed-mention-text"
 *     <input>.
 */
SOURCENET.fix_mention_text = function()
{
    // declare variables
    var me = "SOURCENET.fix_mention_text";
    var fix_link_div_id = "";
    var fix_link_div = null;
    var fix_area_div_id = "";
    var fix_area_div = null;
    var input_element = null;
    
    // get div that contains link and hide() it.
    fix_link_div_id = SOURCENET.DIV_ID_FIX_MENTION_TEXT_LINK;
    fix_link_div = $( '#' + fix_link_div_id );
    fix_link_div.hide();
    
    // load name into fixed-mention-text <input>.
    SOURCENET.load_mention_text_to_fix();
    
    // get div that contains actual fix area and show() it.
    fix_area_div_id = SOURCENET.DIV_ID_FIX_MENTION_TEXT;
    fix_area_div = $( '#' + fix_area_div_id );
    fix_area_div.show();

} //-- END function SOURCENET.fix_mention_text() --//


/**
 * checks to see if DataStore instance already around.  If so, returns it.
 *    If not, creates one, stores it, then returns it.
 *
 * Preconditions: None.
 *
 * Postconditions: If DataStore instance not already present in
 *    SOURCENET.data_store, one is created and stored there before it is
 *    returned.
 */
SOURCENET.get_data_store = function()
{
    
    // return reference
    var instance_OUT = null;
    
    // declare variables
    var me = "SOURCENET.get_data_store";
    var my_data_store = null;
    
    // see if there is already a data store.
    my_data_store = SOURCENET.data_store;
    if ( my_data_store == null )
    {
        
        // nope.  Make one, store it, then recurse.
        my_data_store = new SOURCENET.DataStore();
        SOURCENET.data_store = my_data_store;
        instance_OUT = SOURCENET.get_data_store();
        
    }
    else
    {
        
        instance_OUT = my_data_store;
        
    }
    
    return instance_OUT;
    
} //-- END function SOURCENET.get_data_store() --//


/**
 * Retrieves value in fixed-mention-text input.  If none present, returns null.
 *
 * Preconditions: None.
 *
 * Postconditions: None
 */
SOURCENET.get_fixed_mention_text_value = function()
{
    
    // return reference
    var value_OUT = null;
    
    // declare variables
    var me = "SOURCENET.get_fixed_mention_text_value";
    var fixed_mention_input_name = "";
    
    // get name of input for name from SOURCENET.
    fixed_mention_input_name = SOURCENET.INPUT_ID_FIXED_MENTION_TEXT;

    // get value for that name.
    value_OUT = SOURCENET.get_value_for_id( fixed_mention_input_name, null );
    
    return value_OUT;
    
} //-- END function SOURCENET.get_fixed_mention_text_value() --//


/**
 * Retrieves value in mention-text input.  If none present, returns null.
 *
 * Preconditions: None.
 *
 * Postconditions: None
 */
SOURCENET.get_mention_text = function()
{
    
    // return reference
    var value_OUT = null;
    
    // declare variables
    var me = "SOURCENET.get_mention_text_value";
    var fixed_value = "";
    var is_fixed_value_OK = false;
    
    // start with active value.
    value_OUT = SOURCENET.get_mention_text_value();
    
    SOURCENET.log_message( "In " + me + " - match text : " + value_OUT );
    
    
    // try to get fixed-mention-text.
    fixed_value = SOURCENET.get_fixed_mention_text_value();
    is_fixed_value_OK = SOURCENET.is_string_OK( fixed_value );
    if ( is_fixed_value_OK == true )
    {
        
        // looks like there is a fixed name.  Use it.
        value_OUT = fixed_name;
        
    }

    SOURCENET.log_message( "In " + me + " - match text : " + value_OUT );
    
    return value_OUT;
    
} //-- END function SOURCENET.get_mention_text() --//


/**
 * Retrieves value in mention-text input.  If none present, returns null.
 *
 * Preconditions: None.
 *
 * Postconditions: None
 */
SOURCENET.get_mention_text_value = function()
{
    
    // return reference
    var value_OUT = null;
    
    // declare variables
    var me = "SOURCENET.get_mention_text_value";
    var value_input_name = "";
    
    // get name of input for name from SOURCENET.
    value_input_id = SOURCENET.INPUT_ID_MENTION_TEXT;

    // get value for that name.
    value_OUT = SOURCENET.get_value_for_id( value_input_id, null );
    
    return value_OUT;
    
} //-- END function SOURCENET.get_mention_text_value() --//


SOURCENET.grab_mention = function( text_IN )
{

    // declare variables
    var me = "SOURCENET.grab_mention";
    var selected_text = "";
    var debug_message = "";

    // get selection
    selected_text = text_IN;
    
    // got something?
    if ( ( selected_text !== undefined ) && ( selected_text != null ) && ( selected_text != "" ) )
    {
        
        selected_text = selected_text.trim();
        
        if ( SOURCENET.compress_white_space == true )
        {
            // replace more than one contiguous internal white space
            //     character with a single space.
            selected_text = SOURCENET.compress_internal_white_space( selected_text );
        }
    
        //SOURCENET.log_message( "selected text : \"" + selected_text + "\"" );
    
        $( '#' + SOURCENET.INPUT_ID_MENTION_TEXT ).val( selected_text );
        
        debug_message = "In " + me + " - before SOURCENET.find_mention_text_in_article_text(), selected text = " + selected_text;
        SOURCENET.log_message( debug_message );
        //console.log( debug_message );
       
        // place last name in text-to-find-in-article <input>, then try
        //     to find in text.
        SOURCENET.find_mention_text_in_article_text();
        
        debug_message = "In " + me + " - after SOURCENET.find_mention_text_in_article_text(), selected text = " + selected_text;
        SOURCENET.log_message( debug_message );
        //console.log( debug_message );

        // clear out the fix name area.
        SOURCENET.cancel_fix_mention_text();

    } //-- END check to see if we have some text. --//
                    
} //-- END function SOURCENET.grab_mention() --//


/**
 * Retrieves the list of strings we want to highlight words from for a given
 *     data set, then calls highlight_unique_words() to create list of unique
 *     words, then find and highlight each in yellow (orange).
 */
SOURCENET.highlight_data_set_terms = function()
{

    // declare variables
    var me = "SOURCENET.highlight_data_set_terms";
    var find_in_text_list = null;
    var mention_list = null;
     
    // get list
    find_in_text_list = SOURCENET.data_set_string_list;
    
    // call highlight function.
    SOURCENET.highlight_unique_words( find_in_text_list, "yellow" );
    
} //-- END function SOURCENET.highlight_data_set_terms --//



/**
 * Retrieves the list of strings we want to highlight words from for a given
 *     data set, then calls highlight_unique_words() to create list of unique
 *     words, then find and highlight each in yellow (orange).
 */
SOURCENET.highlight_data_set_mentions = function()
{

    // declare variables
    var me = "SOURCENET.highlight_data_set_mentions";
    var mention_list = null;
     
    // get list
    mention_list = SOURCENET.data_set_mention_list;
    
    // call highlight function.
    //SOURCENET.highlight_unique_words( mention_list, "green" );
    SOURCENET.find_strings_in_article_text( mention_list, false, "green" );
    
} //-- END function SOURCENET.highlight_data_set_mentions --//



/**
 * Accepts index to mention in DataStore.mention_array.  Retrieves mention 
 *     instance at the index passed in.  If not null, calls
 *     Mention.populate_form() to put its values into the form.
 */
SOURCENET.load_mention_into_form = function( index_IN )
{
    
    // declare variables
    var me = "SOURCENET.load_mention_into_form";
    var is_index_OK = false;
    var my_data_store = null;
    var my_instance = null;
    var status_message_array = [];
    
    SOURCENET.log_message( "In " + me + "(): index_IN = " + index_IN );
    
    // see if index is OK.
    is_index_OK = SOURCENET.is_integer_OK( index_IN );
    if ( is_index_OK == true )
    {
        
        // retrieve data store.
        my_data_store = SOURCENET.get_data_store();
        
        // get mention at index passed in.
        my_instance = my_data_store.get_mention_at_index( index_IN );
        
        // call populate_form()
        my_instance.populate_form();
        
        // place last name in text-to-find-in-article <input>, then try to find
        //     in text.
        SOURCENET.find_mention_text_in_article_text();
    }
    else
    {
       
        // make status message array (empty message will clear status area).
        status_message_array = [];
        status_message_array.push( "Could not load mention data - invalid index ( \"" + index_IN + "\" )" );
    
        // output it.
        SOURCENET.output_status_messages( status_message_array );
 
    }
    
} //-- END function SOURCENET.load_mention_into_form() --//
 
 
/**
 * Loads current mention_text value into field where it can be manually fixed.
 */
SOURCENET.load_mention_text_to_fix = function()
{
    
    // declare variables
    var mention_text = "";
    var input_element = null;

    // get selection
    mention_text = SOURCENET.get_mention_text_value();
    //SOURCENET.log_message( "mention text : " + mention_text );

    // get fixed-mention-text text field,  place value there.
    input_element = $( '#' + SOURCENET.INPUT_ID_FIXED_MENTION_TEXT );
    input_element.val( mention_text );
    
} //-- END function SOURCENET.load_mention_text_to_fix() --//


/**
 * Gets fixed-mention-text value.  If not empty, enables the fix-mention-text
 *     part of the form, then places value there.  If empty, puts default in
 *     <input>, but does not enable the field by default.
 */
SOURCENET.load_value_fixed_mention_text = function( mention_IN )
{
    // declare variables
    var me = "SOURCENET.load_value_fixed_mention_text";
    var fixed_mention_text_property_name = null;
    var fixed_mention_text_property_info = null;
    var input_id = "";
    var fixed_mention_text = "";
    var value_to_load = "";

    // get property info for fixed-mention-text.
    fixed_mention_text_property_name = SOURCENET.ObjectProperty_names.FIXED_MENTION_TEXT;
    fixed_mention_text_property_info = SOURCENET.Mention_property_name_to_info_map[ fixed_mention_text_property_name ];
    
    // and get input_id of input for this field.
    input_id = fixed_mention_text_property_info.input_id;
    default_value = fixed_mention_text_property_info.default_value;

    // get fixed-mention-text value
    fixed_mention_text = mention_IN.fixed_mention_name;

    // got a value?
    if ( ( fixed_mention_text != null ) && ( fixed_mention_text != "" ) )
    {
        // yes - reveal field to fix mention text if present.
        SOURCENET.fix_mention_text();
        
        // store value in element
        value_to_load = fixed_mention_text;
    }
    else
    {
        // no value in instance, so set to default.
        value_to_load = default_value;
    } //-- END check to see if we have value --//
    
    // place value_to_load in input.
    SOURCENET.set_value_for_id( input_id, value_to_load );
    
} //-- END function SOURCENET.load_value_fixed_mention_text() --//


/**
 * Gets mention_type value.  If not empty, enables the fix_mention_text
 *     part of the form, then places value there.  If empty, puts default in
 *     <input>, but does not enable the field by default.
 */
SOURCENET.load_value_mention_type = function( mention_IN )
{
    // declare variables
    var me = "SOURCENET.load_value_mention_type";
    var mention_type_property_name = null;
    var mention_type_property_info = null;
    var input_id = "";
    var mention_type = "";
    var value_to_load = "";
    var temp_value = "";

    // get property info for mention_type.
    property_name = SOURCENET.ObjectProperty_names.MENTION_TYPE;
    property_info = SOURCENET.Mention_property_name_to_info_map[ property_name ];
    
    // and get input_id of input for this field.
    input_id = property_info.input_id;
    default_value = property_info.default_value;

    // get mention_type
    mention_type = mention_IN.mention_type;

    // got a value?
    if ( ( mention_type != null ) && ( mention_type != "" ) )
    {
        // yes - store value in element
        value_to_load = mention_type;
    }
    else
    {
        // no value in instance, so set to default.
        value_to_load = default_value;
    } //-- END check to see if we have value --//
    
    // place value_to_load in input.
    temp_value = SOURCENET.set_selected_value_for_id( input_id, value_to_load );
    
    // process the selected mention type:
    SOURCENET.process_selected_mention_type();
    
    // sanity check
    if ( temp_value != mention_type )
    {
        
        // the value of the select is not what we passed to it.
        SOURCENET.log_message( "In " + me + "(): value for select with ID = " + input_id + " is \"" + temp_value + "\"; should be = \"" + mention_type + "\"" );
        
    }
    
} //-- END function SOURCENET.load_value_mention_type() --//


/**
 * Event function that is called when coder is finished coding a particular
 *    mention and is ready to add it to the list of mentions in the article.
 *
 * Preconditions: Mention coding form should be filled out as thoroughly as
 *    possible.  At the least, must have a mention text.  If text not present,
 *    the mention is invalid, will not be accepted.
 *
 * Postconditions: If mention accepted, after this function is called, the
 *    mention will be added to the internal structures to list and map mentions,
 *    and will also be added to the list of mentions who have been coded so far.
 */
SOURCENET.process_mention_coding = function()
{
    // declare variables
    var me = "SOURCENET.process_mention_coding";
    var form_element = null;
    var mention_instance = null;
    var status_message_array = [];
    var status_message_count = -1;
    var work_element = null;
    var existing_mention_index = -1;
    var status_string = "";
    var data_store = null;
    var mention_message_array = [];
    var mention_error_count = -1;

    SOURCENET.log_message( "In " + me + "(): PROCESS MENTION CODING!!!" );
    
    // get form element.
    form_element = $( '#' + SOURCENET.DIV_ID_MENTION_CODING );
    
    // create Mention instance.
    mention_instance = new SOURCENET.Mention();
    
    // populate it from the form.
    status_message_array = mention_instance.populate_from_form( form_element );
    
    // valid?
    status_message_count = status_message_array.length;
    if ( status_message_count == 0 )
    {
        
        // valid.
        SOURCENET.log_message( "In " + me + "(): Valid mention.  Adding to DataStore." );
        
        // get mention store
        data_store = SOURCENET.get_data_store();
        
        // add mention
        mention_message_array = data_store.process_mention( mention_instance );
        
        // errors?
        mention_error_count = mention_message_array.length;
        if ( mention_error_count == 0 )
        {
            
            // no errors.

            // output mention store
            SOURCENET.display_mentions();
                    
            // clear the coding form.
            SOURCENET.clear_coding_form( "Processed: " + mention_instance.to_string() );

        }
        else
        {
            
            // errors - output messages.
            SOURCENET.output_status_messages( mention_message_array );
            
        } //-- END check for errors adding mention to DataStore. --//
        
    }
    else
    {
        
        // not valid - for now, add message to overall status message.
        status_message_array.push( "Mention not valid." );
        
    }
    
    // got any messages?
    status_message_count = status_message_array.length;
    if ( status_message_count > 0 )
    {
        
        // yes, there are messages.  Output them.
        SOURCENET.output_status_messages( status_message_array );
        
    } //-- END check to see if messages --//    
    
} //-- END function SOURCENET.process_mention_coding() --#


SOURCENET.process_selected_mention_type = function()
{
    // declare variables
    var me = "SOURCENET.process_selected_mention_type";
    var selected_value = "";
    var p_source_quote_element = null;

    SOURCENET.log_message( "In " + me + "(): Process Selected Mention Type!" );
    
    // get select element.
    selected_value = SOURCENET.get_selected_value_for_id( 'mention-type' );
    
} //-- END function SOURCENET.process_selected_mention_type() --#


/**
 * Accepts the index of a mention in the DataStore's mention_array that one
 *    wants removed.  Gets the DataStore and calls the
 *    remove_mention_at_index() method on it to remove the mention, then calls
 *    SOURCENET.display_mentions() to repaint the list of mentions.  If any
 *    status messages, outputs them at the end using
 *    SOURCENET.output_status_messages()
 */
SOURCENET.remove_mention = function( index_IN )
{
    
    // declare variables
    var me = "SOURCENET.remove_mention";
    var selected_index = -1;
    var is_index_OK = false;
    var status_message_array = [];
    var status_message_count = -1;
    var data_store = null;
    var remove_message_array = [];
    var remove_error_count = -1;

    // make sure index is an integer.
    selected_index = parseInt( index_IN );
    
    // got an index?
    is_index_OK = SOURCENET.is_integer_OK( selected_index, 0 );
    if ( is_index_OK == true )
    {
        
        // get data store
        data_store = SOURCENET.get_data_store();
        
        // remove mention
        remove_message_array = data_store.remove_mention_at_index( selected_index );
        
        SOURCENET.log_message( "In " + me + "(): Mention Store: " + JSON.stringify( data_store ) );
        
        // errors?
        remove_error_count = remove_message_array.length;
        if ( remove_error_count == 0 )
        {
            
            // no errors.

            // output mention store
            SOURCENET.display_mentions();
            
            // add status message.
            status_message_array.push( "Removed mention at index " + selected_index );
            
        }
        else
        {
            
            // errors - append to status_message_array.
            status_message_array = status_message_array.concat( remove_message_array );
            
        } //-- END check for errors removing mention from DataStore. --//
        
    }
    else
    {
        
        // not valid - for now, output message(s).
        status_message_array.push( "Index value of " + selected_index + " is not valid.  Can't remove mention." );
        
    }
    
    // got any messages?
    status_message_count = status_message_array.length;
    if ( status_message_count > 0 )
    {
        
        // yes, there are messages.  Output them.
        SOURCENET.output_status_messages( status_message_array );
        
    } //-- END check to see if messages --//
        
} //-- END function SOURCENET.remove_mention --//


/**
 * Creates basic form with a submit button whose onsubmit event calls
 *    SOURCENET.render_coding_form_inputs.  On submit, that method pulls the
 *    data needed to submit together and places it in hidden <inputs> associated
 *    with this form, and if no problems, returns true so form submits.  Returns
 *    <form> jquery element, suitable for adding to an element on the page.
 *
 * Postconditions: none.
 */
SOURCENET.render_coding_form = function()
{

    // return reference
    form_element_OUT = true;
    
    // declare variables
    form_HTML_string = "";
    
    // build form HTML string.
    form_HTML_string += '<form method="post" name="submit-article-coding" id="submit-article-coding">';
    form_HTML_string += '<input type="submit" value="Submit Article Coding" name="input-submit-article-coding" id=input-submit-article-coding" onsubmit="SOURCENET.render_coding_form_inputs( this )" />';
    form_HTML_string += '</form>';
    
    // render into JQuery element.
    form_element_OUT = $( form_HTML_string );
    
    return form_element_OUT;
   
} //-- END function to render form to submit coding.


/**
 * Accepts <form> jquery instance.  Adds inputs to the form to hold serialized
 *    JSON object of the DataStore, the results of the coding.  Designed to
 *    be used as a <form>'s onsubmit event handler.
 *
 * Postconditions: Will return false, causing submit to abort, if errors or
 *    warnings.  If returns false, also outputs messages of why using
 *    output_status_messages().
 *
 * References:
 *    - http://stackoverflow.com/questions/6099301/dynamically-adding-html-form-field-using-jquery
 *    - http://www.w3schools.com/js/js_popup.asp
 *
 * @param {jquery:element} form_IN - <form> we are going to append inputs to.
 */
SOURCENET.render_coding_form_inputs = function( form_IN )
{

    // return reference
    do_submit_OUT = true;
    
    // declare variables
    me = "SOURCENET.render_coding_form_inputs";
    form_element = null;
    my_data_store = null;
    author_count = -1;
    is_author_count_valid = false;
    source_count = -1;
    is_source_count_valid = false;
    do_confirm_submit = true;
    ok_to_submit = false;
    data_store_json = "";
    data_store_json_input_element = null;
    submit_button_element = null;
        
    // convert form DOM element to JQuery object.
    //form_element = $( form_IN )
    
    // get data store
    my_data_store = SOURCENET.get_data_store();
    
    //------------------------------------------------------------------------//
    // validation
    //------------------------------------------------------------------------//

    // canceled?
    if ( do_submit_OUT == true )
    {
        
        // not canceled yet, keep checking...
        
        // Is there at least one mention?
        mention_count = my_data_store.get_mention_count();
        if ( mention_count <= 0 )
        {
            
            // no mentions - see if that is correct.
            is_mention_count_valid = confirm( "No mentions coded.  Is this correct?" );
            if ( is_mention_count_valid == false )
            {
                
                // oops - forgot to code mentions.  Back to form.
                do_submit_OUT = false;
                SOURCENET.log_message( "In " + me + "(): forgot to code mentions - back to form!" );
                
            } //-- END check to see if no mentions --//
            
        } //-- END check to see if mention count is 0 --//

    } //-- END check to see if we are already canceled, so don't need to keep checking --//
        
    // canceled?
    if ( do_submit_OUT == true )
    {
        
        // not canceled yet, keep checking...
        
        // confirm submit?
        if ( do_confirm_submit == true )
        {
            
            // We are confirming submit - ask for confirmation.
            ok_to_submit = confirm( "OK to submit coding?" );
            if ( ok_to_submit == false )
            {
                
                // Not ready to submit just yet.  Back to form.
                do_submit_OUT = false;
                SOURCENET.log_message( "In " + me + "(): User not ready to submit.  Back to the form!" );
                
            } //-- END check to see if ready to submit --//
            
        } //-- END check to see if we are confirming submission --//
        
    } //-- END check to see if we are already canceled, so don't need to keep checking --//
    
    // no sense doing anything more if we aren't submitting.
    if ( do_submit_OUT == true )
    {
        
        // need JSON of DataStore.
        data_store_json = JSON.stringify( my_data_store );
        
        // add it to the hidden input:
        // <input id="id_data_store_json" name="data_store_json" type="hidden">
        
        // get <input> element
        input_id_string = "#" + SOURCENET.INPUT_ID_DATA_STORE_JSON;
        data_store_json_input_element = $( input_id_string );

        // make sure we found the element.
        if ( data_store_json_input_element.length > 0 )
        {
            
            // got it.  Place JSON in it.
            data_store_json_input_element.val( data_store_json );
            
            // explicitly set to true.
            do_submit_OUT = true;

            // do_submit_OUT = false;
            if ( do_submit_OUT == false )
            {
                
                SOURCENET.log_message( "In " + me + "(): Placed the following JSON in \"" + input_id_string + "\"" );
                SOURCENET.log_message( "In " + me + "(): " + data_store_json );            

            } //-- END check to see if we output debug.
            
        }
        else
        {
            
            // did not find <input> element.  Log message, don't submit.
            do_submit_OUT = false;
            SOURCENET.log_message( "In " + me + "(): Could not find input for selector: \"" + input_id_string + "\".  No place to put JSON.  Back to form!" );
            
        } //-- END check to see if we found input element. --//
        
    } //-- END check to see if validation was OK before we actually populate inputs. --//
    
    // are we allowing submit?
    if ( do_submit_OUT == true )
    {
        
        // we are.  Retrieve submit button, disable it, and then change text
        //    to say "Please wait...".
        submit_button_element = $( "#" + SOURCENET.INPUT_ID_SUBMIT_ARTICLE_CODING );
        submit_button_element.prop( 'disabled', true );
        submit_button_element.val( SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_WAIT );
        
    } //-- END check to see if we are submitting. --//
    
    return do_submit_OUT;
   
} //-- END function to render form to submit coding.


//----------------------------------------------------------------------------//
// !====> object class definitions
//----------------------------------------------------------------------------//


//=======================//
// !--> DataStore class
//=======================//

// DataStore constructor

/**
 * Stores and indexes mentions in an article.
 * @constructor
 */
SOURCENET.DataStore = function()
{
    // instance variables
    this.mention_array = [];
    this.next_mention_index = 0;
    this.text_to_mention_index_map = {};
    
    // instance variables - status messages
    this.status_message_array = [];
    this.latest_mention_index = -1;
}

// SOURCENET.DataStore methods

/**
 * Accepts a Mention instance.  First, checks to see if the mention is valid.
 *    If no, returns validation messages as error.  If mention has a data set
 *    mention ID, checks to see if the ID is already a key in this.id_to_index_map.
 *    If so, returns an error.  If no ID, checks to see if name is already in
 *    this.text_to_mention_index_map.  If so, returns an error.  If no errors,
 *    then adds the mention to all the appropriate places:
 *    - this.mention_array
 *    - this.text_to_mention_index_map with mention_text as key, index of mention
 *       in the mention_array as the value.
 */
SOURCENET.DataStore.prototype.add_mention = function( instance_IN )
{
    
    // return reference
    var status_array_OUT = [];
    
    // declare variables.
    var me = "SOURCENET.DataStore.prototype.add_mention"
    var is_ok_to_add = true;
    var validation_status_array = [];
    var validation_status_count = -1;
    var my_mention_text = "";
    var is_mention_text_OK = false;
    var mention_text_index = -1;
    var mention_index = -1;
    var text_map_status_array = [];
    
    SOURCENET.log_message( "Top of " + me )
    
    // make sure we have an instance.
    if ( ( instance_IN !== undefined ) && ( instance_IN != null ) )
    {
        
        // got an instance.  Is it valid?
        validation_status_array = instance_IN.validate();
        validation_status_count = validation_status_array.length;
        if ( validation_status_count == 0 )
        {

            // Got mention text?
            my_mention_text = instance_IN.mention_text;
            is_mention_text_OK = SOURCENET.is_string_OK( my_mention_text );
            if ( is_mention_text_OK == true )
            {
                
                // mention text present (as it should be at this point).  See if
                //    this text is already in the DataStore.
                mention_text_index = this.get_index_for_mention_text( my_mention_text );
                if ( mention_text_index >= 0 )
                {
                    
                    // already in map...  Error.
                    is_ok_to_add = false;
                    status_array_OUT.push( "Mention text \"" + my_mention_text + "\" already present in DataStore." );
                    
                } //-- END check to see if mention text already stored. --//
                
            }
            else
            {
                
                // no mention text! ERROR.
                is_ok_to_add = false;
                status_array_OUT.push( "Mention has no text.  Not sure how you got this far, but error." );
                
            } //-- END check to see if mention text present. --//

            // OK to add?
            if ( is_ok_to_add == true )
            {
                
                // no errors so far...  Add mention to array.
                mention_index = this.add_mention_to_array( instance_IN );
                
                // got an index back?
                if ( mention_index > -1 )
                {
                    
                    // got one.  Now, add to map of name and ID to index.
                    
                    // add to text map.
                    text_map_status_array = this.update_mention_in_text_to_index_map( instance_IN, mention_index );
                    
                    // any errors?
                    if ( text_map_status_array.length > 0 )
                    {
                        
                        // yes.  Add to status array, fall out.
                        status_array_OUT = status_array_OUT.concat( text_map_status_array );
                    
                    }
                    
                }
                else
                {
                
                    // no.  Interesting.  Error.
                    status_array_OUT.push( "attempt to add mention to Array resulted in no index.  Not good." );
                    
                } //-- END check to see if index of mention greater than -1. --//
                
            } //-- END check to see if OK to add? --//
            
        }
        else
        {

            // not valid.  Error.  Concat validation errors with any other
            //    errors.
            status_array_OUT = status_array_OUT.concat( validation_status_array );

        } //-- END check to see if mention is valid. --//
        
    }
    else
    {
        
        // no mention passed in.  Error.
        status_array_OUT.push( "No mention instance passed in." );
        
    } //-- END check to see if mention passed in. --//
    
    return status_array_OUT;
    
} //-- END SOURCENET.DataStore method add_mention() --//


/**
 * Accepts a mention instance - adds it to the mention array at the next index.
 *    Returns the index.  Mention is not checked to see if it is a duplicate.
 *    At this point, it is too late for that.  You should have checked earlier.
 *
 * Assumptions: We always push mentions onto array, never remove.  Index should
 *    equal this.mention_array.length - 1, but keep separate variables as well
 *    as a sanity check.
 *
 * @param {Mention} instance_IN - instance we want to add to the mention array.
 * @returns {int} - index of mention in mention array.
 */
SOURCENET.DataStore.prototype.add_mention_to_array = function( instance_IN )
{
    
    // return reference
    var index_OUT = -1;
    
    // declare variables
    var me = "SOURCENET.DataStore.prototype.add_mention_to_array";
    var my_mention_array = [];
    var my_next_index = -1;
    var my_latest_index = -1;
    var mention_array_length = -1;
    
    // got an instance?
    if ( ( instance_IN !== undefined ) && ( instance_IN != null ) )
    {
        
        // yes - get relevant variables.
        my_mention_array = this.mention_array;
        my_next_index = this.next_mention_index;
        my_latest_index = this.latest_mention_index;
    
        // push mention onto array.
        my_mention_array.push( instance_IN );
        
        // increment next index, make sure it equals length - 1.
        my_next_index += 1;
        mention_array_length = my_mention_array.length;
        if ( my_next_index != mention_array_length )
        {
            
            // hmmm... Disconnect.  Next index should equal length of current
            //    array since arrays are 0-indexed and we only ever add one.
            //    Output alert.
            SOURCENET.log_message( "In " + me + "(), next index ( " + my_next_index + " ) not equal to array length ( " + mention_array_length + " )." );
            
        }
                    
        // Store next and latest values based on array length.
        this.next_mention_index = mention_array_length;
        
        // return index of length of array minus 1.
        index_OUT = mention_array_length -1;
        this.latest_mention_index = index_OUT;
        
        // and store index in instance.
        instance_IN.mention_index = index_OUT;

    }
    else
    {
        
        // no.  Return -1.
        index_OUT = -1;
        
    } //-- END check to see if mention instance.
    
    return index_OUT;
    
} //-- END SOURCENET.DataStore method add_mention_to_array() --//


/**
 * Accepts a mention text - Checks to see if text string is a key in the map of
 *    mention text values to indexes in the master mention array.  If so,
 *    returns that index.  If not, returns -1.
 *
 * @param {string} value_IN - mention text string for mention we want to find in
 *    mention array.
 * @returns {int} - index of mention in mention array, or -1 if mention name not
 *    found.
 */
SOURCENET.DataStore.prototype.get_index_for_mention_text = function( value_IN )
{
    
    // return reference.
    var index_OUT = -1;
    
    // declare variables
    var is_value_OK = false;
    var text_to_index_map = null;
    var is_in_map = false;
    
    // got a mention text value?
    is_value_OK = SOURCENET.is_string_OK( value_IN );
    if ( is_value_OK == true )
    {

        // get text_to_index_map.
        text_to_index_map = this.text_to_mention_index_map;
        
        // see if text passed in is a key in this.text_to_mention_index_map.hasOwnProperty( value_IN );
        is_in_map = text_to_index_map.hasOwnProperty( value_IN );
        if ( is_in_map == true )
        {
            
            // it is in the mention store.  retrieve index for this mention text.
            index_OUT = text_to_index_map[ value_IN ];
            
        }
        else
        {
            
            // nope.  Return -1.
            index_OUT = -1;
            
        }
        
    }
    else
    {
        
        // no name passed in.  Return -1.
        index_OUT = -1;
        
    }

    return index_OUT;

} //-- END SOURCENET.DataStore method get_index_for_mention_text() --//


/**
 * Accepts an index into the mention array - Checks to see if index is present
 *    in master mention array, if so, returns what is in that index.  If not,
 *    returns null.
 *
 * @param {int} index_IN - index in mention array whose contents we want.
 * @returns {SOURCENET.Mention} - instance of Mention at the index passed in.
 */
SOURCENET.DataStore.prototype.get_mention_at_index = function( index_IN )
{
    
    // return reference.
    var instance_OUT = null;
    
    // declare variables
    var is_index_OK = false;
    var my_mention_array = -1;
    
    // got an index?
    is_index_OK = SOURCENET.is_integer_OK( index_IN, 0 );
    if ( is_index_OK == true )
    {
        
        // I think so...  Get mention array
        my_mention_array = this.mention_array;
        
        //  check to see if index present.
        instance_OUT = my_mention_array[ index_IN ];
        
        // is it undefined?
        if ( instance_OUT === undefined )
        {
            
            // it is.  For this function, return null instead.
            instance_OUT = null;
            
        } //-- END check to see if undefined --//
        
    }
    else
    {
        
        // no valid index - error - return null
        instance_OUT = null;
        
    } //-- END check to see if valid index passed in. --//
    
    return instance_OUT;

} //-- END SOURCENET.DataStore method get_mention_at_index() --//


/**
 * Returns a count of mentions in this data store.
 *
 * @returns {int} - count of mentions in this data store.
 */
SOURCENET.DataStore.prototype.get_mention_count = function()
{
    
    // return reference.
    var count_OUT = 0;
    
    // declare variables
    var me = "SOURCENET.DataStore.prototype.get_mention_count";
    var my_mention_array = null;
    var mention_array_length = -1;
    var mention_index = -1;
    var mention_counter = -1;
    var current_mention = -1;
    
    // get mention array.
    my_mention_array = this.mention_array;
    
    // loop over array.
    mention_array_length = my_mention_array.length;
    mention_counter = 0;
    for( mention_index = 0; mention_index < mention_array_length; mention_index++ )
    {
        
        // increment counter
        mention_counter += 1;
        
        // get item at current index.
        current_mention = my_mention_array[ mention_index ];
        
        // is it null?
        if ( current_mention != null )
        {
            
            // not null - add to count.
            count_OUT += 1;

        } //-- END check if mention associated with current array index --//
        
    } //-- END loop over mention_array --//
    
    SOURCENET.log_message( "In " + me + "(): count = " + count_OUT );
    
    return count_OUT;

} //-- END SOURCENET.DataStore method get_mention_count() --//


/**
 * Accepts mention text - Checks to see if index in master mention array tied to
 *     the mention text.  If so, retrieves Mention at that index and returns it.
 *     If not, returns null.
 *
 * @param {string} value_IN - mention text of mention we want to find in array.
 * @returns {SOURCENET.Mention} - instance of Mention related to the mention text passed in.
 */
SOURCENET.DataStore.prototype.get_mention_for_text = function( value_IN )
{
    
    // return reference.
    var instance_OUT = null;
    
    // declare variables
    var is_value_OK = false;
    var mention_index = -1;
    var is_mention_index_OK = false;
    
    // got a value?
    is_value_OK = SOURCENET.is_string_OK( value_IN );
    if ( is_value_OK == true )
    {

        // I think so...  See if there is an entry in text map for this name.
        mention_index = this.get_index_for_mention_text( value_IN );
        
        // is mention_index present, and greater than -1?
        is_mention_index_OK = SOURCENET.is_integer_OK( mention_index, 0 );
        if ( is_mention_index_OK == true )
        {
            
            // looks like there is an index.  Get Mention at that index.
            instance_OUT = this.get_mention_at_index( mention_index );
            
        }
        else
        {
            
            // not present in map object.  Return null.
            instance_OUT = null;
            
        }
        
    }
    else
    {
        
        // no mention text - error - return null
        instance_OUT = null;
        
    }
    
    return instance_OUT;

} //-- END SOURCENET.DataStore method get_mention_for_text() --//


/**
 * Checks to see if SOURCENET.data_store_json is not null and not "".  If
 *    populated, retrieves value in variable, converts JSON string to Javascript
 *    objects, then uses those objects to populate DataStore.
 */
SOURCENET.DataStore.prototype.load_from_json = function()
{
    
    // declare variables
    var me = "SOURCENET.DataStore.load_from_json";
    var my_data_store_json_string = "";
    var my_data_store_json = null;
    var my_next_index = -1;
    var my_text_to_mention_index_map = {};
    var my_status_message_array = [];
    var my_latest_index = -1;

    // declare variables - mention processing.
    var my_mention_array = [];
    var mention_count = -1;
    var mention_index = -1;
    var current_mention_text = "";
    var current_fixed_mention_text = "";
    var current_mention_type = "";
    var current_original_mention_type = "";
    var current_data_set_mention_id = "";
    var current_mention_index = -1;
    var current_mention_data = null;
    var current_mention = null;
    
    // got JSON?
    if ( ( SOURCENET.data_store_json != null ) && ( SOURCENET.data_store_json != "" ) )
    {
        
        // it is null.  Person already removed at this index.
        SOURCENET.log_message( "In " + me + "(): Making sure this is running." );

        // try to parse JSON string into javascript objects.
        my_data_store_json_string = SOURCENET.data_store_json;

        SOURCENET.log_message( "In " + me + "(): JSON before decode: " + my_data_store_json_string );

        // decode
        my_data_store_json_string = SOURCENET.decode_html( my_data_store_json_string );

        SOURCENET.log_message( "In " + me + "(): JSON after decode: " + my_data_store_json_string );

        // parse to JSON objects
        my_data_store_json = JSON.parse( my_data_store_json_string );

        // use the pieces of the JSON to populate this object.
        my_mention_array = my_data_store_json[ "mention_array" ];
        my_next_mention_index = my_data_store_json[ "next_mention_index" ];
        my_text_to_mention_index_map = my_data_store_json[ "text_to_mention_index_map" ];
        my_status_message_array = my_data_store_json[ "status_message_array" ];
        my_latest_mention_index = my_data_store_json[ "latest_mention_index" ];

        // do we have any mentions?
        if ( ( my_mention_array !== undefined ) && ( my_mention_array != null ) )
        {
            
            // loop over mention array to create and store SOURCENET.Mention
            //    instances.
            // how many we got?
            mention_count = my_mention_array.length;
    
            SOURCENET.log_message( "In " + me + "(): mention_count = " + mention_count );
    
            // !---- mention loop
            for ( mention_index = 0; mention_index < mention_count; mention_index++ )
            {
    
                SOURCENET.log_message( "In " + me + "(): mention_index = " + mention_index );
    
                // get mention at current index
                current_mention_data = my_mention_array[ mention_index ];
    
                // get values
                current_mention_text = current_mention_data[ "mention_text" ];
                current_fixed_mention_text = current_mention_data[ "fixed_mention_text" ];
                current_mention_type = current_mention_data[ "mention_type" ];
                current_original_mention_type = current_mention_data[ "original_mention_type" ];
                current_data_set_mention_id = current_mention_data[ "data_set_mention_id" ];
                current_mention_index = current_mention_data[ "mention_index" ];
    
                // create and populate Mention instance.
                current_instance = new SOURCENET.Mention();
                
                // mention type
                current_instance.mention_type = current_mention_type;
                current_instance.original_mention_type = current_original_mention_type;
    
                // ID for DataSetMention instance.
                current_instance.data_set_mention_id = current_data_set_mention_id;
                
                // mention text - are verbatim and name different?
                if ( ( current_fixed_mention_text != null )
                    && ( current_fixed_mention_text != "" )
                    && ( current_fixed_mention_text != current_mention_text ) )
                {
                    
                    // they are different - store each in their appropriate field.
                    current_instance.mention_text = current_mention_text;
                    current_instance.fixed_mention_text = current_fixed_mention_text;
                    
                }
                else
                {
                    
                    // nothing fancy, just resting a bit.
                    current_instance.mention_text = current_mention_text;
                    current_instance.fixed_mention_text = "";
    
                } //-- END check to see if mention text has been fixed --//
                
                current_instance.mention_index = mention_index;
    
                // add mention to this DataStore.
                this.add_mention( current_instance );
    
            } //-- END loop over mentions --//
            
    
            /*
            // No need to do this - add_mention() builds all this stuff for you.
            // then store off all the rest of the stuff.
            this.next_mention_index = my_next_mention_index;
            this.text_to_mention_index_map = my_text_to_mention_index_map;
            this.status_message_array = my_status_message_array;
            this.latest_mention_index = my_latest_mention_index;
             */
    
        }
        else
        {
            SOURCENET.log_message( "In " + me + "(): mention_array is undefined or null" );
        } //-- END check to see if any mentions at all --//

    } //-- END check to see if JSON passed in. --//

} //-- END SOURCENET.DataStore method load_from_json() --//


/**
 * Accepts a Mention instance.  Checks if there is a mention index in instance.
 *     If so, calls update_mention().  If not, calls add_mention().
 *     Returns the status array that results from either invocation.
 */
SOURCENET.DataStore.prototype.process_mention = function( instance_IN )
{
    
    // return reference
    var status_array_OUT = [];
    
    // declare variables.
    var me = "SOURCENET.DataStore.prototype.process_mention"
    var my_mention_index = -1
    var is_index_ok = true;
    
    SOURCENET.log_message( "Top of " + me );
    
    // got a valid index?
    my_mention_index = instance_IN.mention_index
    is_index_ok = SOURCENET.is_integer_OK( my_mention_index, 0 );
    if ( is_index_ok == true )
    {
        
        // We do.  Call update_mention().
        status_array_OUT = this.update_mention( instance_IN );
        
    }
    else
    {
        
        // We do not.  Call add_mention().
        status_array_OUT = this.add_mention( instance_IN );
        
    }
    
    return status_array_OUT;
    
} //-- END DataStore method process_mention() --//


/**
 * Accepts an index into the mention array - Retrieves Mention at that index.
 *    If null, nothing there, nothing to remove.  If not null, makes that index
 *    in the array refer to null.  Then, looks for the index value in the values
 *    stored within the name-to-index map.  If index value found, key-value pair
 *    with the index as the value is removed.  Returns a list of messages.  If
 *    empty, success.
 *
 * Postconditions: Also logs warnings to console.log(), so if you want to see if
 *    there are any warnings (tells things like whether the mention exists at
 *    the index passed in, if there might have been more than one name or mention
 *    ID that reference the index, etc.).  If it finds bad data, this method
 *    will clean it up.  When we remove a mention at an index, removes all
 *    references to that index in the text to index map, even if there
 *    are mutiple in that map.
 *
 * @param {int} index_IN - index in mention array that contains mention we want to remove.
 * @returns {Array:string} - array of status messages that result from processing.
 */
SOURCENET.DataStore.prototype.remove_mention_at_index = function( index_IN )
{
    
    // return reference.
    var status_array_OUT = [];
    
    // declare variables
    var me = "SOURCENET.DataStore.remove_mention_at_index";
    var selected_index = -1;
    var is_index_OK = false;
    var my_mention_array = -1;
    var mention_to_remove = null;
    var my_mention_text = "";
    var text_to_index_map = {};
    var current_key = "";
    var current_value = "";
    
    // make sure index is an integer.
    selected_index = parseInt( index_IN );
    
    // got an index?
    is_index_OK = SOURCENET.is_integer_OK( selected_index, 0 );
    if ( is_index_OK == true )
    {
        
        // I think so...  Get mention array
        my_mention_array = this.mention_array;
        
        //  check to see if index present.
        mention_to_remove = my_mention_array[ selected_index ];
        
        // is it undefined or null?
        if ( mention_to_remove === undefined )
        {
            
            // it is undefined.  Index not present in array.
            SOURCENET.log_message( "In " + me + "(): Index " + selected_index + " is undefined - not present in array." );
            my_mention_name = null;
            
        }
        else if ( mention_to_remove == null )
        {
            
            // it is null.  Mention already removed at this index.
            SOURCENET.log_message( "In " + me + "(): Mention at index " + selected_index + " already removed ( == null )." );
            my_mention_name = null;
            
        }
        else
        {
            
            // there is a mention here.  Get text.
            my_mention_text = mention_to_remove.mention_text;
            
            // and, set the index to null.
            my_mention_array[ selected_index ] = null;
            
        } //-- END check to see if mention instance referenced by index is undefined or null. --//
            
            
        // look for values that reference index in:
        // - this.text_to_mention_index_map
        
        // always check, even of index reference is null or undefined, just as a
        //    sanity check to keep the maps clean.

        // text-to-index map --> this.text_to_mention_index_map
        text_to_index_map = this.text_to_mention_index_map;
        
        // loop over keys, checking if value for each matches value of index_IN.
        for ( current_key in text_to_index_map )
        {
            
            // get value.
            current_value = text_to_index_map[ current_key ];
            
            // convert to integer (just in case).
            current_value = parseInt( current_value );
            
            // compare to selected_index.
            if ( current_value == selected_index )
            {
                
                // we have a match.  Sanity check - see if the key matches the
                //    name from the mention.
                if ( current_key != my_mention_text )
                {
                    
                    // matching index, but key doesn't match.  Output message.
                    SOURCENET.log_message( "In " + me + "(): Mention text key \"" + current_key + "\" references index " + current_value + ".  Key should be \"" + my_mention_text + "\".  Hmmm..." );
                    
                }
                
                // remove key-value pair from object.
                delete text_to_index_map[ current_key ];
                
            } //-- END check to see if vkey references the index we've been asked to remove --//
            
        } //-- END loop over keys in this.text_to_mention_index_map --//
        
    }
    else //-- index is not OK. --//
    {
        
        // no valid index - error - return null
        status_array_OUT.push( "Index " + index_IN + " is not valid - could not remove mention." );
        
    } //-- END check to see if valid index passed in. --//
    
    return status_array_OUT;

} //-- END SOURCENET.DataStore method remove_mention_at_index() --//


/**
 * Accepts a Mention instance that contains an index in mention array.  First, 
 *     see if the mention is valid.  If no, returns validation messages
 *     as error.  If valid, checks to make sure that there is an index in the
 *     mention.  If not, returns an error.  If no errors, updates information on
 *     the mention in all the appropriate places:
 *     - this.mention_array
 *     - this.text_to_mention_index_map with mention_text as key, index of
 *         mentino in the mention_array as the value.
 */
SOURCENET.DataStore.prototype.update_mention = function( instance_IN )
{
    
    // return reference
    var status_array_OUT = [];
    
    // declare variables.
    var me = "SOURCENET.DataStore.prototype.update_mention"
    var is_index_ok = true;
    var is_ok_to_update = true;
    var validation_status_array = [];
    var validation_status_count = -1;
    var mention_index = -1;
    var text_map_status_array = [];
    
    SOURCENET.log_message( "Top of " + me );
    
    // make sure we have an instance.
    if ( ( instance_IN !== undefined ) && ( instance_IN != null ) )
    {
        
        // and make sure we have an index.
        index_IN = instance_IN.mention_index;
        is_index_ok = SOURCENET.is_integer_OK( index_IN, 0 );
        if ( is_index_ok == true )
        {
        
            // got an index and a mention.  Is mention valid?
            validation_status_array = instance_IN.validate();
            validation_status_count = validation_status_array.length;
            if ( validation_status_count == 0 )
            {
                
                // do update-specific validation here - none for now...
                is_ok_to_update = true;
                
                // make sure that index passed in matches index in mention.
                mention_index = instance_IN.mention_index;
                if ( mention_index != index_IN )
                {
                    
                    // they do not match.  This is an error.
                    is_ok_to_update = false;
                    status_array_OUT.push( "Index mismatch: index_IN = " + index_IN + "; instance_IN.mention_index = " + mention_index );
                
                } //-- END check to see if index passed in matches instance_IN.mention_index --#
            
                // OK to update?
                if ( is_ok_to_update == true )
                {
                    
                    // no errors so far...  Update in mention array.
                    this.mention_array[ index_IN ] = instance_IN;
                    
                    // update in text map.
                    text_map_status_array = this.update_mention_in_text_to_index_map( instance_IN, index_IN );
                    
                    // any errors?
                    if ( text_map_status_array.length > 0 )
                    {
                        
                        // yes.  Add to status array, fall out.
                        status_array_OUT = status_array_OUT.concat( text_map_status_array );
                    
                    }
                        
                } //-- END check to see if OK to update? --//
                
            }
            else
            {
    
                // not valid.  Error.  Concat validation errors with any other
                //    errors.
                status_array_OUT = status_array_OUT.concat( validation_status_array );
    
            } //-- END check to see if mention is valid. --//
            
        }
        else
        {
            
            // no index passed in.  Error.
            status_array_OUT.push( "No index passed in." );
            
        } //-- END check to see if index passed in --//
        
    }
    else
    {
        
        // no mention passed in.  Error.
        status_array_OUT.push( "No mention instance passed in." );
        
    } //-- END check to see if mention passed in. --//
    
    return status_array_OUT;
    
} //-- END SOURCENET.DataStore method update_mention_at_index() --//


/**
 * Accepts a Mention instance and that mention's index in the mention array.
 *     If both passed in, updates mapping of name to index in name_to_index_map
 *     in DataStore.  If not, does nothing.
 *
 * @param {Mention} instance_IN - mention we want to add to update in the map of mention name strings to indexes in mention array.
 * @param {int} index_IN - index in mention array we want text associated with.  If -1 passed in, effectively removes mention from map.
 * @returns {Array} - Array of status messages - empty array = success.
 */
SOURCENET.DataStore.prototype.update_mention_in_text_to_index_map = function( instance_IN, index_IN )
{
    
    // return reference
    var status_array_OUT = [];
    
    // declare variables.
    var me = "SOURCENET.DataStore.prototype.update_mention_in_text_to_index_map";
    var my_mention_text = "";
    var is_mention_text_OK = false;
    var my_text_to_index_map = {};
    
    // got a mention?
    if ( ( instance_IN !== undefined ) && ( instance_IN != null ) )
    {
        
        // yes - get relevant variables.
        my_text_to_index_map = this.text_to_mention_index_map;
        
        // get mention text
        my_mention_text = instance_IN.mention_text;
        
        // got text?
        is_mention_text_OK = SOURCENET.is_string_OK( my_mention_text );
        if ( is_mention_text_OK == true )
        {
            
            // yes.  Set value for that name in map.
            my_text_to_index_map[ my_mention_text ] = index_IN;
            
        }
        else
        {
            
            // no - error.
            status_array_OUT.push( "In " + me + "(): no text in mention (ERROR).  Can't do anything." );
            
        }

    }
    else
    {
        
        // no.  Error.
        status_array_OUT.push( "No mention passed in.  What?" );
        
    } //-- END check to see if mention instance.
    
    return status_array_OUT;
    
} //-- END SOURCENET.DataStore method update_mention_in_text_to_index_map() --//


//=====================//
// END DataStore
//=====================//


//============================//
// !--> ObjectProperty class
//============================//

// ObjectProperty Property Names
SOURCENET.ObjectProperty_names = {};
SOURCENET.ObjectProperty_names[ "MENTION_TEXT" ] = SOURCENET.JSON_PROP_MENTION_TEXT; // "mention_text"
SOURCENET.ObjectProperty_names[ "FIXED_MENTION_TEXT" ] = SOURCENET.JSON_PROP_FIXED_MENTION_TEXT; // "fixed_mention_text"
SOURCENET.ObjectProperty_names[ "MENTION_TYPE" ] = SOURCENET.JSON_PROP_MENTION_TYPE; // "mention_type"
SOURCENET.ObjectProperty_names[ "MENTION_INDEX" ] = SOURCENET.JSON_PROP_MENTION_INDEX; // "mention_index"
SOURCENET.ObjectProperty_names[ "DATA_SET_MENTION_ID" ] = SOURCENET.JSON_PROP_DATA_SET_MENTION_ID; // "data_set_mention_id"
SOURCENET.ObjectProperty_names[ "ORIGINAL_MENTION_TYPE" ] = SOURCENET.JSON_PROP_ORIGINAL_MENTION_TYPE; // "original_mention_type"

// ObjectProperty Property Types
SOURCENET.ObjectProperty_data_types = {};
SOURCENET.ObjectProperty_data_types[ "INTEGER" ] = "integer";
SOURCENET.ObjectProperty_data_types[ "STRING" ] = "string";

// MentionProperty Property Input Types
SOURCENET.ObjectProperty_input_types = {};
SOURCENET.ObjectProperty_input_types[ "TEXT" ] = "text";
SOURCENET.ObjectProperty_input_types[ "TEXTAREA" ] = "textarea";
SOURCENET.ObjectProperty_input_types[ "HIDDEN" ] = "hidden";
SOURCENET.ObjectProperty_input_types[ "SELECT" ] = "select";

// ObjectProperty constructor

/**
 * Represents one of the pieces of information about an entity stored in an
 *     object.
 * @constructor
 */
SOURCENET.ObjectProperty = function()
{   
    // names of properties
    this.prop_names = SOURCENET.ObjectProperty_names;
    
    // item types
    this.prop_data_types = SOURCENET.ObjectProperty_data_types;

    // input types
    this.input_types = SOURCENET.ObjectProperty_input_types;
            
    // instance variables
    this.name = null;
    this.type = null;
    this.default_value = null;
    this.min_value = null;
    this.default_value = null;
    this.input_id = null;
    this.input_type = null;
    this.function_load_form = null;
    this.function_get_value = null;
    this.function_clear_form = null;
} //-- END SOURCENET.ObjectProperty constructor --//

// ObjectProperty methods


/**
 * For property defined in current instance, checks to see if there is a clear
 *     function specified.  If so, calls it.  If not, looks up the input ID
 *     for the property and places the default value in that input.
 *
 * Preconditions: None.
 *
 * Postconditions: None.
 */
SOURCENET.ObjectProperty.prototype.clear_value = function()
{
    
    // declare variables
    var me = "SOURCENET.ObjectProperty.prototype.clear_value";
    var clear_form_function = "";
    var input_id = "";
    var default_value = "";

    // got a function for clearing form?
    clear_form_function = this.function_clear_form;
    if ( clear_form_function != null )
    {
        
        // there is a function to call for clearing.  Call it.
        clear_form_function();
        
    }
    else
    {
        
        // no function.  Use <input> ID and default value to clear by
        //     resetting the <input> to the default value.
        input_id = this.input_id;
        default_value = this.default_value;
        
        // call SOURCENET.set_value_for_id()
        SOURCENET.set_value_for_id( input_id, default_value );
        
    } //-- END check to see if we have a clear function to call --//
    
} //-- END method SOURCENET.ObjectProperty.prototype.clear_value --//
        

/**
 * Checks to see if there is a "get_value" function referenced in this instance.
 *     If so, calls it.  If not, calls get_value_from_form() on this instance to
 *     retrieve the value from the form in the standard way.  Returns value,
 *     regardless of how it was found, returns null if not found or error.
 *
 * Preconditions: None.
 *
 * Postconditions: None.
 *
 * @returns {string} - value of input matching ID passed in, else null if error.
 */
SOURCENET.ObjectProperty.prototype.get_value = function()
{
    // return reference
    var value_OUT = null;

    // declare variables
    var me = "SOURCENET.MentionProperty.prototype.get_value";
    
    // declare variables - processing mention properties.
    var get_value_function = null;
    
    // retrieve info on current property.
    get_value_function = this.function_get_value;
    
    // got a function for getting property value?
    if ( get_value_function != null )
    {
        
        // there is a function to call for retrieving value..  Call it.
        value_OUT = get_value_function();
        
    }
    else
    {
        
        // no fancy function - get value from form.
        value_OUT = this.get_value_from_form();
        
    } //-- END check to see if we have a clear function to call --//

    return value_OUT;
    
} //-- END ObjectProperty method get_value() --#


/**
 * Gets id of input whose value we want to retrieve from current instance. Looks
 *     for input with that ID.  If one found, gets value from that input and
 *     returns it.
 *
 * Preconditions: None.
 *
 * Postconditions: None.
 *
 * @returns {string} - value of input matching ID passed in, else null if error.
 */
SOURCENET.ObjectProperty.prototype.get_value_from_form = function()
{
    // return reference
    var value_OUT = [];

    // declare variables
    var me = "SOURCENET.ObjectProperty.prototype.get_value_from_form";
    
    // declare variables - processing properties.
    var data_type = "";
    var default_value = "";
    var input_id = -1;
    var input_type = "";
    var select_input_type = "";
    var integer_data_type = "";
    
    // initialize values
    select_input_type = SOURCENET.ObjectProperty_input_types[ "SELECT" ];
    integer_data_type = SOURCENET.ObjectProperty_data_types[ "INTEGER" ]
        
    // retrieve info on current property.
    data_type = this.type;
    default_value = this.default_value;
    input_id = this.input_id;
    input_type = this.input_type;
    
    // see how we retrieve value based on input type - there are
    //     separate functions for <select> and <input> (though they work
    //     the same at this point).
    if ( input_type == select_input_type )
    {
        
        // <select> - use SOURCENET.get_selected_value_for_id().
        value_OUT = SOURCENET.get_selected_value_for_id( input_id );
        
    }
    else
    {
    
        // if not select, treat all the rest the same - call
        //     SOURCENET.get_value_for_id().
        value_OUT = SOURCENET.get_value_for_id( input_id, default_value );
        
    }

    // based on data type, see if we need to do anything to the value.
    if ( data_type == integer_data_type )
    {
        
        // integer - cast potentially string value to be an integer.
        value_OUT = parseInt( value_OUT, 10 );
        
    }

    return value_OUT;
    
} //-- END ObjectProperty method get_value_from_form() --#


/**
 * Checks to see if there is a "load_form" function referenced in this instance.
 *     If so, calls it.  If not, calls put_value_into_form() on this instance to
 *     retrieve the value from the form in the standard way.  Returns value,
 *     regardless of how it was found, returns null if not found or error.
 *
 * Preconditions: None.
 *
 * Postconditions: None.
 *
 * @returns {string} - value of input matching ID passed in, else null if error.
 */
SOURCENET.ObjectProperty.prototype.put_value = function( instance_IN )
{
    // return reference
    var value_OUT = null;

    // declare variables
    var me = "SOURCENET.ObjectProperty.prototype.put_value";
    
    // declare variables - processing mention properties.
    var load_form_function = null;
    
    // retrieve info on current property.
    load_form_function = this.function_load_form;
    
    // got a function for loading property value into form?
    if ( load_form_function != null )
    {
        
        // there is a function to call for retrieving value..  Call it.
        value_OUT = load_form_function( instance_IN );
        
    }
    else
    {
        
        // no fancy function - get value place into form.
        value_OUT = this.put_value_into_form( instance_IN );
        
    } //-- END check to see if we have a clear function to call --//

    return value_OUT;
    
} //-- END ObjectProperty method put_value() --#


/**
 * Accepts mention instance whose value we want to put into form.  After making
 *     sure we have an OK ID, looks for input with that ID.  If one found, gets
 *     value from that input and returns it.
 *
 * Preconditions: None.
 *
 * Postconditions: None.
 *
 * @param {Mention} instance_IN - Mention instance whose value we want to put into form.
 * @returns {string} - value of input matching ID passed in, else null if error.
 */
SOURCENET.ObjectProperty.prototype.put_value_into_form = function( instance_IN )
{
    // return reference
    var value_OUT = [];

    // declare variables
    var me = "SOURCENET.ObjectProperty.prototype.put_value_into_form";
    var property_element = null;
        
    // declare variables - processing properties.
    var property_name = "";
    var data_type = "";
    var default_value = "";
    var input_id = -1;
    var input_type = "";
    var select_input_type = "";
    var integer_data_type = "";
    var my_value = null;
    var is_value_OK = false;
    
    // got an instance?
    if ( instance_IN != null )
    {
        
        // initialize values
        select_input_type = SOURCENET.ObjectProperty_input_types[ "SELECT" ];
        integer_data_type = SOURCENET.ObjectProperty_data_types[ "INTEGER" ];
            
        // retrieve info on current property.
        property_name = this.name;
        data_type = this.type;
        default_value = this.default_value;
        input_id = this.input_id;
        input_type = this.input_type;
        
        // get the property value.
        my_value = instance_IN[ property_name ];
        
        // if integer data type, see if the integer is valid.
        if ( data_type == integer_data_type )
        {
            
            // it is an integer.  Is it OK?
            is_value_OK = SOURCENET.is_integer_OK( my_value, 0 );
            
        }
        else
        {
            
            // not integer.  Check as string.
            is_value_OK = SOURCENET.is_string_OK( my_value );
            
        }
        
        // Is the value OK?
        if ( is_value_OK == false )
        {
            
            // no.  Use default.
            my_value = default_value;
            
        }
        
        // see how we put in form value based on input type - there are
        //     separate functions for <select> and <input> (though they work
        //     the same at this point).
        if ( input_type == select_input_type )
        {
            
            // <select> - use SOURCENET.set_selected_value_for_id().
            value_OUT = SOURCENET.set_selected_value_for_id( input_id, my_value );
            
        }
        else
        {
        
            // if not select, treat all the rest the same - call
            //     SOURCENET.set_value_for_id().
            value_OUT = SOURCENET.set_value_for_id( input_id, my_value );
            
        } //-- END check to see if the input we are messing with is a <select>. --//
    
    } //-- END check to make sure instance_IN is not null --//

    return value_OUT;
    
} //-- END ObjectProperty method put_value_into_form() --#


//=====================//
// !--> Mention class
//=====================//

// !---- Mention properties

// declare a variable
var temp_property = null;

// make list of properties, map names to info.
SOURCENET.Mention_property_name_list = [];
SOURCENET.Mention_property_name_to_info_map = {};

// mention_text
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.MENTION_TEXT;
temp_property.type = temp_property.prop_data_types.STRING;
temp_property.default_value = "";
temp_property.min_value = null;
temp_property.input_id = SOURCENET.INPUT_ID_MENTION_TEXT;
temp_property.input_type = temp_property.input_types.TEXTAREA;
temp_property.function_load_form = null;
temp_property.function_get_value = null;
temp_property.function_clear_form = null;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

// fixed_mention_text
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.FIXED_MENTION_TEXT;
temp_property.type = temp_property.prop_data_types.STRING;
temp_property.default_value = "";
temp_property.min_value = null;
temp_property.input_id = SOURCENET.INPUT_ID_FIXED_MENTION_TEXT;
temp_property.input_type = temp_property.input_types.TEXTAREA;
temp_property.function_load_form = SOURCENET.load_value_fixed_mention_text;
temp_property.function_get_value = null;
temp_property.function_clear_form = SOURCENET.cancel_fix_mention_text;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

// mention_type
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.MENTION_TYPE;
temp_property.type = temp_property.prop_data_types.STRING;
temp_property.default_value = "";
temp_property.min_value = null;
temp_property.input_id = SOURCENET.INPUT_ID_MENTION_TYPE;
temp_property.input_type = temp_property.input_types.SELECT;
temp_property.function_load_form = SOURCENET.load_value_mention_type;
temp_property.function_get_value = null;
temp_property.function_clear_form = SOURCENET.clear_mention_type;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

// mention_index
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.MENTION_INDEX;
temp_property.type = temp_property.prop_data_types.INTEGER;
temp_property.default_value = -1;
temp_property.min_value = 0;
temp_property.input_id = SOURCENET.INPUT_ID_MENTION_INDEX;
temp_property.input_type = temp_property.input_types.HIDDEN;
temp_property.function_load_form = null;
temp_property.function_get_value = null;
temp_property.function_clear_form = null;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

// original_mention_type
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.ORIGINAL_MENTION_TYPE;
temp_property.type = temp_property.prop_data_types.STRING;
temp_property.default_value = "";
temp_property.min_value = null;
temp_property.input_id = SOURCENET.INPUT_ID_ORIGINAL_MENTION_TYPE;
temp_property.input_type = temp_property.input_types.HIDDEN;
temp_property.function_load_form = null;
temp_property.function_get_value = null;
temp_property.function_clear_form = SOURCENET.clear_original_mention_type;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

// data_set_mention_id
temp_property = new SOURCENET.ObjectProperty();
temp_property.name = temp_property.prop_names.DATA_SET_MENTION_ID;
temp_property.type = temp_property.prop_data_types.INTEGER;
temp_property.default_value = -1;
temp_property.min_value = 1;
temp_property.input_id = SOURCENET.INPUT_ID_DATA_SET_MENTION_ID;
temp_property.input_type = temp_property.input_types.HIDDEN;
temp_property.function_load_form = null;
temp_property.function_get_value = null;
temp_property.function_clear_form = SOURCENET.clear_data_set_mention_id;
SOURCENET.Mention_property_name_to_info_map[ temp_property.name ] = temp_property;
SOURCENET.Mention_property_name_list.push( temp_property.name );

SOURCENET.log_message( "Property names: " + SOURCENET.Mention_property_name_list );

// ! ---- Mention constructor

/**
 * Represents a mention in an article.
 * @constructor
 */
SOURCENET.Mention = function()
{   
    // declare variables
    var me = "SOURCENET.Mention() constructor";
    var property = null;
    
    // instance variables
    this.mention_text = "";
    this.fixed_mention_text = "";
    this.mention_type = "";
    this.mention_index = -1;
    this.original_mention_type = "";
    this.data_set_mention_id = null;
    
} //-- END SOURCENET.Mention constructor --//

// !---- Mention methods

/**
 * populates Mention entry form inputs from values in this object instance.
 */
SOURCENET.Mention.prototype.populate_form = function()
{
    
    // return reference
    var validate_status_array_OUT = [];

    // declare variables
    var me = "SOURCENET.Mention.populate_form";
    
    // declare variables - processing mention properties.
    var my_mention_text = "";
    var property_list = null;
    var property_info = null;
    var property_count = -1;
    var current_index = -1;
    var current_property_name = "";
    var current_property_info = null;
    var current_value = "";
    var data_type = "";
    var default_value = "";
    var input_id = -1;
    var input_type = "";
    var get_value_function = null;
    var status_message_array = null;

    // start by clearing coding form
    SOURCENET.clear_coding_form( "Loading data" );

    // retrieve values from instance and use to populate the form.
    
    // get property info.
    property_list = SOURCENET.Mention_property_name_list;
    property_info = SOURCENET.Mention_property_name_to_info_map;
        
    // loop over properties
    property_count = property_list.length;
    for ( current_index = 0; current_index < property_count; current_index++ )
    {
        
        // get current property name.
        current_property_name = property_list[ current_index ];
        
        // retrieve the property info.
        current_property_info = property_info[ current_property_name ];
        
        // load the value
        current_value = current_property_info.put_value( this );
        
        // is it the mention text?
        if ( current_property_name == SOURCENET.JSON_PROP_MENTION_TEXT )
        {
            
            // yes - store mention text.
            my_mention_text = current_value;
            
        } //-- END check to see if mention text --//
        
    } //-- END loop over Mention properties --//
    
    // got a mention text?
    if ( ( my_mention_text != null ) && ( my_mention_text != "" ) )
    {
        
        // yes.  make status message array (empty message will clear status area).
        status_message_array = [];
        status_message_array.push( "Loaded data for mention: " + my_mention_text );
        
        // output it.
        SOURCENET.output_status_messages( status_message_array );

        
    } //-- END check to see if mention name --//

    SOURCENET.log_message( "In " + me + "(): Mention JSON = " + JSON.stringify( this ) );
    
    // validate
    validate_status_array_OUT = this.validate();
    
    // SOURCENET.log_message( "validate_status = " + validate_status )
    
    return validate_status_array_OUT;
    
} //-- END SOURCENET.Mention method populate_form() --//


/**
 * populates Mention object instance from form inputs.
 * @param {jquery element} form_element_IN - Form element that contains inputs we will use to populate this instance.
 * @returns {Array} - list of validation messages.  If empty, all is well.  If array.length > 0, then there were validation errors.
 */
SOURCENET.Mention.prototype.populate_from_form = function( form_element_IN )
{
    
    // return reference
    var validate_status_array_OUT = [];

    // declare variables
    var me = "SOURCENET.Mention.populate_from_form";
    
    // declare variables - processing mention properties.
    var property_list = null;
    var property_info = null;
    var property_count = -1;
    var current_index = -1;
    var current_property_name = "";
    var current_property_info = null;
    var current_value = "";
    var data_type = "";
    var default_value = "";
    var input_id = -1;
    var input_type = "";
    var get_value_function = null;
    var select_input_type = "";
    var integer_data_type = "";
    
    // initialize values
    select_input_type = SOURCENET.ObjectProperty_input_types[ "SELECT" ];
    integer_data_type = SOURCENET.ObjectProperty_data_types[ "INTEGER" ];

    // get form element
    form_element = form_element_IN
    
    // retrieve values from form inputs and store in instance.
    
    // get property info.
    property_list = SOURCENET.Mention_property_name_list;
    property_info = SOURCENET.Mention_property_name_to_info_map;
        
    // loop over properties
    property_count = property_list.length;
    for ( current_index = 0; current_index < property_count; current_index++ )
    {
        
        // get current property name.
        current_property_name = property_list[ current_index ];
        
        // retrieve the property info.
        current_property_info = property_info[ current_property_name ];
        
        // get the value
        current_value = current_property_info.get_value();
        
        // place the value in the specified property.
        property_name = current_property_info.name;
        this[ property_name ] = current_value;

    } //-- END loop over Person properties --//

    SOURCENET.log_message( "In " + me + "(): Person JSON = " + JSON.stringify( this ) );
    
    // validate
    validate_status_array_OUT = this.validate();
    
    // SOURCENET.log_message( "validate_status = " + validate_status )
    
    return validate_status_array_OUT;
    
} //-- END SOURCENET.Mention method populate_from_form() --//


/**
 * Converts mention to a string value.
 */
SOURCENET.Mention.prototype.to_string = function()
{
    
    // return reference
    var value_OUT = "";
    
    // declare variables.
    var my_mention_text = "";
    var my_mention_type = "";
    var my_data_set_mention_id = -1;
    var is_id_ok = false;
    
    // got data set mention ID?
    my_data_set_mention_id = this.data_set_mention_id;
    is_id_ok = SOURCENET.is_integer_OK( my_data_set_mention_id, 1 );
    if ( is_id_ok == true )
    {
        value_OUT += my_data_set_mention_id;
    }
    else
    {
        value_OUT += "new";
    }
    value_OUT += " - ";
    
    // mention text.
    my_mention_text = this.mention_text;
    value_OUT += my_mention_text;
    
    // mention type
    my_mention_type = this.mention_type;
    if ( ( my_mention_type != null ) && ( my_mention_type != "" ) )
    {
        value_OUT += " - " + my_mention_type;
    }

    return value_OUT;
    
} //-- END SOURCENET.Mention method to_string() --//


/**
 * Converts mention to a string value.
 */
SOURCENET.Mention.prototype.to_table_cell_html = function()
{
    
    // return reference
    var value_OUT = "";
    
    // declare variables.
    var my_mention_text = "";
    var my_mention_type = "";
    var my_mention_index = -1;
    var my_data_set_mention_id = -1;
    var is_id_ok = false;
    
    // mention type
    my_mention_type = this.mention_type;
    if ( ( my_mention_type != null ) && ( my_mention_type != "" ) )
    {
        value_OUT += "<td>" + my_mention_type + "</td>";
    }

    // mention text.
    my_mention_text = this.mention_text;
    my_mention_index = this.mention_index;
    value_OUT += "<td><a href=\"#\" onclick=\"SOURCENET.load_mention_into_form( " + my_mention_index + " ); return false;\">" + my_mention_text + "</a></td>";

    // got data set mention ID?
    my_data_set_mention_id = this.data_set_mention_id;
    is_id_ok = SOURCENET.is_integer_OK( my_data_set_mention_id, 1 );
    value_OUT += "<td>";
    if ( is_id_ok == true )
    {
        value_OUT += my_data_set_mention_id;
    }
    else
    {
        value_OUT += "new";
    }
    value_OUT += "</td>";
    
    return value_OUT;
    
} //-- END SOURCENET.Mention method to_table_cell_html() --//


/**
 * validates Mention object instance.
 * @returns {Array} - list of validation messages.  If empty, all is well.  If array.length > 0, then there were validation errors.
 */
SOURCENET.Mention.prototype.validate = function()
{

    // return reference
    var status_array_OUT = [];  // empty list = valid, non-empty list = list of error messages, invalid.

    // declare variables
    var my_mention_text = "";
    var is_value_OK = false;
    var my_mention_type = "";
    var is_mention_type_OK = false;
    var status_string = "";
    
    
    //------------------------------------------------------------------------//
    // must have mention text
    my_mention_text = this.mention_text;
    is_value_OK = SOURCENET.is_string_OK( my_mention_text );
    if ( is_value_OK == false )
    {
        // no mention_text - invalid.
        status_array_OUT.push( "Must have a mention text." );
    }
    
    /*
    //------------------------------------------------------------------------//
    // must have a mention type
    my_mention_type = this.mention_type;
    
    // check if empty.
    is_mention_type_OK = SOURCENET.is_string_OK( my_mention_type );
    if ( is_mention_type_OK == true )
    {
        // not empty - make sure it is a known value.
        if ( SOURCENET.PERSON_TYPE_ARRAY.indexOf( my_mention_type ) == -1 )
        {
            
            // it is not.  Curious.  Error.
            status_array_OUT.push( "Person type value " + my_mention_type + " is unknown ( known values: " + SOURCENET.PERSON_TYPE_ARRAY + " )" );
            
        }
    }
    else
    {
        
        // no mention type.  Got to have one.
        status_array_OUT.push( "Must have a mention type." );
        
    } //-- END Check to see if there is a mention type. --//
     */

    // convert list of status messages to string.
    //if ( status_list_OUT.length > 0 )
    //{
        
        // join the messages.
        //status_string = status_list_OUT.join( ", " );
        // SOURCENET.log_message( "status = " + status_string )
        
    //}
    
    return status_array_OUT;
    
} //-- END SOURCENET.Mention method validate() --//

//=====================//
// END Mention
//=====================//

//----------------------------------------------------------------------------//
// !====> jquery event handlers
//----------------------------------------------------------------------------//


// javascript to keep the coding area on right from scrolling off page.
$( function(){

    // set the offset pixels automatically on how much the sidebar height is.
    // plus the top margin or header height
    //var offsetPixels = $('.sidebarBox').outerHeight() + 30;
    var offsetPixels = 0;
        
    $(window).scroll( function() {
        if ( $(window).scrollTop() > offsetPixels ) {
            $('.scrollingBox').css({
                'position': 'fixed',
                'top': '40px'
            });
        } else {
            $('.scrollingBox').css({
                'position': 'static'
            });
        }
    });
});

// ! document.ready( button - #select-text )
// javascript to pull text selection into a text input.
// Get selected text / 選択部分のテキストを取得
$( document ).ready(
    function()
    {
        $( '#select-text' ).click(        
            function()
            {
                // declare variables
                var selected_text = "";
                var selected_text_input = null;
    
                // get selection
                selected_text = $.selection();
                //SOURCENET.log_message( "selected text : " + selected_text );
                
                // get input
                selected_text_input = $( '#selected-text' );
                
                // set value
                selected_text_input.val( selected_text );
            }
        )
    }
);


// ! document.ready( button - #store-mention )
// javascript to store selected text as mention text.
$( document ).ready(
    function()
    {
        $( '#store-mention' ).click(        
            function()
            {
                // declare variables
                var selected_text = "";
                var last_name_text = "";
                var input_element = null;
    
                // get selection
                selected_text = $.selection();
                
                // grab it form
                SOURCENET.grab_mention( selected_text );
            }
        )
    }
); //-- END document.ready( #store-mention ) --//


// ! document.ready( button - #fix-mention-text )
// javascript to copy name from #source-name to the Lookup text field.
$( document ).ready(
    function()
    {
        $( '#fix-mention-text' ).click(        
            function()
            {
                // declare variables
                var mention_text = "";
                var input_element = null;
    
                // get selection
                mention_text = SOURCENET.get_mention_text_value();
                //SOURCENET.log_message( "mention text : " + source_text );

                // get fixed-mention-text text field,  place value. 
                input_element = $( '#' + SOURCENET.INPUT_ID_FIXED_MENTION_TEXT );
                input_element.val( mention_text );
            }
        )
    }
); //-- END document.ready( button - #fix-mention-text ) --//


// ! document.ready( button - #find-mention-in-article-text )
// javascript to copy name from #mention-text to the Find in Article Text text
//     input.
$( document ).ready(
    function()
    {
        $( '#find-mention-in-article-text' ).click(        
            function()
            {
                // declare variables
                var value = "";
    
                // get value
                value = SOURCENET.get_mention_text();

                // send to find input.
                SOURCENET.send_text_to_find_input( value );
                
                SOURCENET.log_message( "In document.ready( button - #find-mention-in-article-text ) - match text : " + value );
            }
        )
    }
); //-- END document.ready( button - #find-mention-in-article-text ) --//


// ! document.ready( button - #find-in-article-text )
// javascript to look for whatever is in the <input> with
//     id="text-to-find-in-article" inside the article's text, and highlight any
//     paragraphs that contain a match.
$( document ).ready(
    function()
    {
        $( '#find-in-article-text' ).click(        
            function()
            {

                // declare variables
                var me = "document.ready( button - #find-in-article-text )";
                var input_element = "";
                var find_text = "";
    
                // get text-to-find-in-article text field,  get value, then
                //    find_in_article_text().
                input_element = $( '#' + SOURCENET.INPUT_ID_TEXT_TO_FIND_IN_ARTICLE );
                find_text = input_element.val();

                SOURCENET.log_message( "In " + me + " - find text : " + find_text );

                // find in text...
                SOURCENET.find_in_article_text( find_text, false, "red" );
                
            }
        )
    }
); //-- END document.ready( button - #find-in-article-text ) --//


// ! document.ready( button - #find-words-in-article-text )
// javascript to look for whatever is in the <input> with
//     id="text-to-find-in-article" inside the article's text, and highlight any
//     paragraphs that contain a match.
$( document ).ready(
    function()
    {
        $( '#find-words-in-article-text' ).click(        
            function()
            {

                // declare variables
                var me = "document.ready( button - #find-words-in-article-text )";
                var input_element = "";
                var find_text = "";
    
                // get text-to-find-in-article text field,  get value, then
                //    find_in_article_text().
                input_element = $( '#' + SOURCENET.INPUT_ID_TEXT_TO_FIND_IN_ARTICLE );
                find_text = input_element.val();

                SOURCENET.log_message( "In " + me + " - find text : " + find_text );

                // find in text...
                SOURCENET.find_words_in_article_text( find_text, false, "red" );
                
            }
        )
    }
); //-- END document.ready( button - #find-in-article-text ) --//


// ! document.ready( button - #clear-find-in-article-text )
// javascript to unmark all paragraphs that have matches in them.
$( document ).ready(
    function()
    {
        $( '#clear-find-in-article-text' ).click(        
            function()
            {
                // declare variables
                var me = "document.ready( button - #clear-find-in-article-text )";
                var name_text = "";
                var input_element = "";
    
                // clear matches.
                SOURCENET.clear_find_in_text();
                
                SOURCENET.log_message( "In " + me );
            }
        )
    }
); //-- END document.ready( button - #clear-find-in-article-text ) --//


// ! ----> load existing coding data

// !document.ready( load existing coding data )
// javascript to load existing coding data if present.
$( document ).ready(

    function()
    {

        // declare variables
        var me = "SOURCENET.load_existing_coding_data";
        var my_data_store = null;
    
        // got anything to load?
        if ( ( SOURCENET.data_store_json != null ) && ( SOURCENET.data_store_json != "" ) )
        {
            
            // yes - get data store
            my_data_store = SOURCENET.get_data_store();
        
            // call load_from_json()
            my_data_store.load_from_json();

            // repaint coding area
            SOURCENET.display_mentions();
        
        }
    
    }

); //-- END document.ready( load existing coding data ) --//


// ! ----> force activation of coding submit button.


// !document.ready( activate coding submit button )
// javascript to load existing coding data if present.
$( document ).ready(

    function()
    {

        // declare variables
        var me = "SOURCENET.activate_coding_submit_button";
        var submit_button_element = null;
        var submit_button_disabled = false;
        var submit_button_value = "";
    
        // Retrieve submit button, enable it, and then change text
        //    to say "Submit Article Coding!".
        submit_button_element = $( '#' + SOURCENET.INPUT_ID_SUBMIT_ARTICLE_CODING );
        
        // if disabled, enable.
        submit_button_disabled = submit_button_element.prop( 'disabled' );
        if ( submit_button_disabled == true )
        {
            
            // disabled.  Enable.
            submit_button_element.prop( 'disabled', false );
            
        }

        // Make sure value isn't "Please wait..."
        submit_button_value = submit_button_element.val();
        if ( submit_button_value == SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_WAIT )
        {
            
            // it says wait.  Change it to reset value.
            submit_button_element.val( SOURCENET.ARTICLE_CODING_SUBMIT_BUTTON_VALUE_RESET );
            
        }
    
    }

); //-- END document.ready( activate coding submit button ) --//

// ! ----> highlight data set terms in the text.

// !document.ready( button - #toggle-data-set-highlighting
// javascript to place or clear data set highlighted information.
$( document ).ready(

    function()
    {
        $( '#' + SOURCENET.INPUT_ID_TOGGLE_DATA_SET_HIGHLIGHTING ).click(        
            function()
            {
        
                // declare variables
                var me = "document.ready( button - #toggle-data-set-highlighting";
                var button_element = null;
                var button_value = "";
            
                // Retrieve submit button, enable it, and then change text
                //    to say "Submit Article Coding!".
                button_element = $( '#' + SOURCENET.INPUT_ID_TOGGLE_DATA_SET_HIGHLIGHTING );
                
                // get button value
                button_value = button_element.val();
                
                // if button set to ON, clear, then switch button to OFF.
                if ( button_value == SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_ON )
                {
                    // clear
                    SOURCENET.clear_yellow_highlight();
                    SOURCENET.clear_green_highlight();
                    
                    // change button to OFF.
                    button_element.val( SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_OFF );
                }
                // if button set to OFF, highlight, then switch button to ON.
                else if ( button_value == SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_OFF )
                {
                    // highlight
                    SOURCENET.highlight_data_set_mentions();
                    SOURCENET.highlight_data_set_terms();
                    
                    // change button to ON.
                    button_element.val( SOURCENET.DATA_SET_HIGHLIGHTING_BUTTON_VALUE_ON );   
                }
                
                SOURCENET.log_message( "In " + me );
            
            }
        )
    }
); //-- END document.ready( toggle data set term highlighting ) --//

// !document.ready( highlight data set terms )
// javascript to highlight data set terms.
/*
$( document ).ready(

    function()
    {

        // call the highlight data_set_mentions function.
        SOURCENET.highlight_data_set_mentions();
        
        // call the highlight data set terms function.
        SOURCENET.highlight_data_set_terms();
        
        // process found synonyms?
        if ( SOURCENET.process_found_synonyms == true )
        {
           
            // pre-populate the mention area any mentions present in text.
            SOURCENET.find_and_process_data_set_synonyms();
 
        } //-- END check to see if we process synonyms. --//
        
    } //-- END function --//

); //-- END document.ready( load existing coding data ) --//
*/

