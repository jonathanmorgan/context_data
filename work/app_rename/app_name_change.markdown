# Step-by-step, to rename <old_name> to <new_name>

1. Change the name of your application's directory from <old_name> to <new_name>.

    - a. Ex: from "sourcenet_datasets" to "context_datasets".

2. Update apps.py in the <old_name> sub-directory. In it put:

        class <new_name_leading_cap_no_underscores>Config(AppConfig):
                name = "<new_name>"
                label = "<new_name>"
                verbose_name = "<new_name>"

    Key among these is label which is going to change things.

3. In __init__.py in the <new_name> sub-directory, put:

        default_app_config = "<new_name>.apps.<new_name_leading_cap_no_underscores>Config"

4. In your settings.py change the INSTALLED_APPS entry for your app to '<new_name>.apps.<new_name_leading_cap>Config', …
5. In your base urls.py, update to reflect new folder name.
6. Look for the old name in files and in file and directory names within your project space.

    - Find files with matches: grep -r -i -l "<old_name>" .

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
    
    - Imports:
    
            grep -r -i -l "from <old_name>" . | xargs sed -i 's/from <old_name>/from <new_name>/g'
    
    - Update paths in "templates" and "static" folders, if you name-spaced your files with the name of the application (as you should).

        - If application is in git, use "git mv", not just "mv".
    
    - All of your migrations need to be edited in this step. In the dependencies list, you'll need to change '<old_name>' to '<new_name>'. In the ForeignKeys you'll need to also change '<old_name>.Something' to '<new_name>.Something' for every something in every migration file. Find these under pages/mitrations/nnnn_*.py
    
        - This wasn't so bad - only a few foreign keys and the dependency statement at the top.

    - If you refer to foreign keys in other modules by "from pages.models import Something" and then use ForeignKey(Something), you'll need to update those, as well. If you use ForeignKey('pages.Something') then you need to change those references to ForeignKey('phpages.Something'). I would assume other like-references are the same.

8. For the next 4 steps (7, 8, 9 and 10), I built pagestophpages.sql and added it to the pages sub-directory. It's not a standard django thing, but each test copy and each production copy of the database was going to need the same set of steps.
9. UPDATE django_content_type SET app_label='phpages' WHERE app_label='pages';
10. UPDATE django_migrations SET app='phpages' WHERE app='pages';
11. Now... in your database (my is PostgreSQL) there will be a bunch of tables that start with "pages". You need to list all of these. In PostgreSQL, in addition to tables, there will be sequences for each AutoField. For each table construct ALTER TABLE pages_something RENAME TO phpages_something; For each sequence ALTER SEQUENCE pages_something_id_seq RENAME TO phpages_something_id_seq; (Q - Indexes?)

    - Indexes (do first, since it depends on name of table)

        - Find indexes for tables that start with your "<old_name>":

                -- Get the table names of all the tables for this application.
                --     (and get each twice for ease of making ALTER TABLE statements)
                SELECT index_name, index_name
                FROM pg_indexes
                WHERE tablename LIKE 'sourcenet_datasets_%';

        - Create ALTER TABLE…RENAME TO… using Sublime and multi-cursors.
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
    
    - Sequences
        
        - Find sequences that start with your "<old_name>":

                -- Get the sequence names of all the sequences for this application.
                --     (and get each twice for ease of making ALTER SEQUENCE statements)
                select sequence_name, sequence_name
                from information_schema.sequences
                WHERE sequence_name LIKE 'sourcenet_datasets_%';

        - Create ALTER SEQUENCE…RENAME TO… using Sublime and multi-cursors.
        - Notes:

            - https://stackoverflow.com/questions/38194364/how-to-get-list-of-sequence-names-in-postgres

12. You should probably backup the database. You may need to try this a few times. Run your SQL script through your database shell. Note that all other changes can be propagated by source code control (git, svn, etc). This last step must be run on each and every database.

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
