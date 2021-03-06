# Step-by-step, to rename <old_name> to <new_name>

1. Change the name of your application's directory from <old_name> to <new_name>.

    - a. Ex: from "sourcenet_datasets" to "context_data".

2. Update apps.py in the <old_name> sub-directory. In it put:

        class <new_name_leading_cap_no_underscores>Config(AppConfig):
                name = "<new_name>"
                label = "<new_name>"
                verbose_name = "<new_name>"

    Key among these is name which is going to change things.  Also, you don't need to have all of these.  If you just set name, the others will default to that value as well.

3. In __init__.py in the <new_name> sub-directory, put:

        default_app_config = "<new_name>.apps.<new_name_leading_cap_no_underscores>Config"

4. In your settings.py change the INSTALLED_APPS entry for your app to '<new_name>.apps.<new_name_leading_cap>Config', …
5. In your base urls.py, update to reflect new folder name.
6. Look for the old name in files and in file and directory names within your project space.

    - Find files with matches: `grep -r -i -l "<old_name>" .`

        - Examples

                grep -r -i -l "sourcenet_datasets" .
                grep -r -i -l --include "*.py" "sourcenet_datasets" . # just python files
                grep -r -i -l --include "*.ipynb" "sourcenet_datasets" . # just jupyter notebook files

        - Once you find files that match, either look at line numbers using grep (b, below), or go into the file and deal with it manually.  To look at just a particular folder:

                grep -r -i -l "sourcenet_datasets" <folder_path>

    - Inside the files, look at the matches: grep -r -i -n "<old_name>" .

        - Example: grep -r -i -n "sourcenet_datasets" .

    - In file names: find . -type f -iname "*<old_name>*"
        
        - Example: find . -type f -iname "*sourcenet\_datasets*"
    
    - In directory names: find . -type d -name "*<old_name>*"

        - Example: find . -type d -iname "*sourcenet\_datasets*" 

7. Update places that have old name in either file name or inside files.  Common things:
    
    - base django application files:
        
        - models.py
        - admin.py
        - forms.py
        - views.py
        - urls.py
    
    - Imports:
    
            grep -r -i -l "from sourcenet\_datasets\." .
            grep -r -i -n "from sourcenet\_datasets\." .
            # pattern: grep -r -i -l "from <old_name>\." . | xargs sed -i 's/from <old_name>\./from <new_name>\./g'
            grep -r -i -l "from sourcenet\_datasets\." . | xargs sed -i 's/from sourcenet\_datasets\./from context\_data\./g'
    
    - Table name prefix:
    
            grep -r -i -l "sourcenet\_datasets\_" .
            grep -r -i -n "sourcenet\_datasets\_" .
            # pattern: grep -r -i -l "<old_name>\_" . | xargs sed -i 's/<old_name>\_/<new_name>\_/g'
            grep -r -i -l "sourcenet\_datasets\_" . | xargs sed -i 's/sourcenet\_datasets\_/context\_data\_/g'
        
    - Update paths in "templates" and "static" folders, if you name-spaced your files with the name of the application (as you should).

        - If application is in git, use "git mv", not just "mv".
        
    - And, update the contents of templates (paths and labels from urls.py).
    - All of your migrations need to be edited in this step. In the dependencies list, you'll need to change '<old_name>' to '<new_name>'. In the ForeignKeys you'll need to also change '<old_name>.Something' to '<new_name>.Something' for every something in every migration file. Find these under pages/mitrations/nnnn_*.py
    
        - This wasn't so bad - only a few foreign keys and the dependency statement at the top.
        - For the bold, try, in the migrations directory:
        
                # pattern - grep -r -i -l "<old_name>" . | xargs sed -i 's/<old_name>/<new_name>/g'
                grep -r -i -l "sourcenet_datasets" . | xargs sed -i 's/sourcenet_datasets/context_data/g'

    - If you refer to foreign keys in other modules by "from pages.models import Something" and then use ForeignKey(Something), you'll need to update those, as well. If you use ForeignKey('pages.Something') then you need to change those references to ForeignKey('phpages.Something'). I would assume other like-references are the same.
    - `ContextDataBase` - need to make sure to:
    
        - rename the class inside context_data_base.py to `ContextDataBase` from `SourcenetDataSetsBase`.
        - then, find and fix all references to this class being renamed from `SourcenetDataSetsBase`.
    
                grep -r -i -l "SourcenetDataSetsBase" .

8. For the next 4 steps (7, 8, 9 and 10), I built update_database.pg.sql and added it to the `work/app_rename` sub-directory. It's not a standard django thing, but each test copy and each production copy of the database was going to need the same set of steps.
9. `UPDATE django_content_type SET app_label='<new_name>' WHERE app_label='<old_name>';`
10. `UPDATE django_migrations SET app='<new_name>' WHERE app='<old_name>';
11. Now... in your database (mine is PostgreSQL) there will be a bunch of tables that start with "<old_name>". You need to list all of these. In PostgreSQL, in addition to tables, there will be sequences for each AutoField, and many related indexes.

    - Indexes (do first, since it depends on name of table)

        - Find indexes for tables that start with your "<old_name>":

                -- Get the table names of all the tables for this application.
                --     (and get each twice for ease of making ALTER TABLE statements)
                SELECT index_name, index_name
                FROM pg_indexes
                WHERE tablename LIKE 'sourcenet_datasets_%';

        - Create ALTER TABLE…RENAME TO… using Sublime and multi-cursors.
        
            - Example: `ALTER INDEX pages_something_id_seq RENAME TO phpages_something_id_seq;`
        
        - Notes:

            - https://stackoverflow.com/questions/2204058/list-columns-with-indexes-in-postgresql
            - http://www.postgresqltutorial.com/postgresql-indexes/postgresql-list-indexes/
    - Tables:
     
        - Find tables that start with your "<old_name>":

                -- Get the table names of all the tables for this application.
                --     (and get each twice for ease of making ALTER TABLE statements)
                SELECT table_name, table_name
                FROM information_schema.tables
                WHERE table_name LIKE 'sourcenet_datasets_%'
                    AND table_type='BASE TABLE';

        - Create ALTER TABLE…RENAME TO… using Sublime and multi-cursors.
        
            - For each table construct `ALTER TABLE <old_name>_something RENAME TO <new_name>_something;`
    
    - Sequences
        
        - Find sequences that start with your "<old_name>":

                -- Get the sequence names of all the sequences for this application.
                --     (and get each twice for ease of making ALTER SEQUENCE statements)
                select sequence_name, sequence_name
                from information_schema.sequences
                WHERE sequence_name LIKE 'sourcenet_datasets_%';

        - Create ALTER SEQUENCE…RENAME TO… using Sublime and multi-cursors.
        
            - For each sequence `ALTER SEQUENCE <old_name>_something_id_seq RENAME TO <new_name>_something_id_seq;`
        
        - Notes:

            - https://stackoverflow.com/questions/38194364/how-to-get-list-of-sequence-names-in-postgres

12. You should probably backup the database. You may need to try this a few times. Run your SQL script through your database shell. Note that all other changes can be propagated by source code control (git, svn, etc). This last step must be run on each and every database.

13. If you have any links that refer to the old URLs, you'll need to update them.

13. If you clone out of github: After everything is working, commit and push all changes.  Then, 

14. Update ansible scripts for sourcenet_dev to refer to the new repository.

Based on: https://stackoverflow.com/questions/42059381/django-migrate-change-of-app-name-active-project

# sourcenet_datasets TODO

- Search for:

    - // SourcenetDataSetsBase
    - // sourcenet_datasets_base
    - // sourcenet_datasets.
    - // from sourcenet_datasets
    - // sourcenet/datasets (from urls.py)

- Move "sourcenet.shared.sourcenet_base.SourcenetBase" into "context.shared…"
- Remember:

    - views.py
    - urls.py

- Update RichContextV2 repository.
- Update phd_work repository.
- The old code is in branch "pre_name_change".
