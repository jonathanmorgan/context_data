# context_data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3523010.svg)](https://doi.org/10.5281/zenodo.3523010)

<!-- TOC -->

context_data is a django application for capturing and analyzing mentions of data in articles.

It is built upon and depends on:

- the base context django application: [https://github.com/jonathanmorgan/context](https://github.com/jonathanmorgan/context)
- the context_text django application: [https://github.com/jonathanmorgan/context_text](https://github.com/jonathanmorgan/context_text)

# Installation and configuration

Below, there used to be detailed instructions for installing all the things to get django running on apache with a PostgreSQL database backend on an Ubuntu server (these are preserved for reference in `archive/README-manual_install.md`.  Now, I've created ansible scripts with all the steps that you can configure and run against Ubuntu 18.04 or 16.04 (VM, cloud server, or physical machine).

These scripts are in my "ansible-patterns" repository: [https://github.com/jonathanmorgan/ansible-patterns](https://github.com/jonathanmorgan/ansible-patterns)

These ansible scripts can also be used to setup a server with virtualenvwrapper, postgresql, apache, django, jupyterhub, and R, and the context django applications and databases.  See the readme for detailed instructions.

I might make dockerfile(s) for this eventually, too, but for now, there's ansible.

I've left in a few notes below, regarding different package and installation choices, but the best doc is the ansible repo.

## Basic installation

To start with a fresh install of ubuntu 18.04 server and install `context_data` from scratch, in the [ansible-patterns README](https://github.com/jonathanmorgan/ansible-patterns), follow the [Setup Steps](https://github.com/jonathanmorgan/ansible-patterns/blob/master/README.md#setup) and then the ["research" quick start](https://github.com/jonathanmorgan/ansible-patterns/blob/master/README.md#research-quick-start).  You'll use ansible to install both the "research.yml" playbook and the "only_sourcenet_dev.yml" playbook.  If you want to use a server name other than "research" and domain name other than "research.local", there are instructions for that in the quick start.

## Python packages

- depending on database:

    - postgresql - psycopg2 - Before you can connect to Postgresql with this code, you need to do the following (based on [http://initd.org/psycopg/install/](http://initd.org/psycopg/install/)):

        - install the PostgreSQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libpq-dev) ( [source](http://initd.org/psycopg/install/) ).
        - install the psycopg2 python package.  Install using pip (`sudo pip install psycopg2`).  
        
    - mysql - mysqlclient - Before you can connect to MySQL with this code, you need to do the following:
    
        - mysqlclient

            - install the MySQL client if it isn't already installed.  On linux, you'll also need to install a few dev packages (python-dev, libmysqlclient-dev) ( [source](http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/) ).
            - install the mysqlclient python package using pip (`(sudo) pip install mysqlclient`).

- python packages that I find helpful:

    - ipython - `(sudo) pip install ipython`

- Natural Language Processing (NLP) APIs, if you are building your own thing (I don't use Alchemy API right now, and I built my own OpenCalais client):

    - To use Alchemy API, clone the `Alchemy_API` python client into your django project's root folder:
    
        - `git clone https://github.com/alchemyapi/alchemyapi_python`
        
    - To use the pycalais package for OpenCalais's REST API, clone the pycalais git repository into your django project directory, then copy the calais folder into your django project directory:
    
        - `git clone https://github.com/ubergrape/pycalais`
        - `cp ./calais ../`
        
        - You can also use python_utilities.network.http_helper.Http_Helper to connect directly (or requests package) see the sample code in /examples/NLP/OpenCalais_API.py for more details.

## settings.py - Configure logging, database, applications:

The following are some django settings you might want to tweak in the settings.py file in your django project.  If you created a project named "research", this will be located at `research/research/settings.py`.

### logging

Edit the `research/research/settings.py` file and update it with details of your logging configuration
    
- Example that logs any messages INFO and above to standard out:

        import logging

        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )

- Example that logs any messages INFO and above to a file:

        import logging

        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            filename = '<log_folder>/django-research.log',
            filemode = 'w'
        )

    - WHERE `<log_folder>` is a folder that any users that will be used to interact with context_data have access to.  This includes the user your web server runs as (for admins and other django web pages) and the user you use to develop, and so that might run things from the python shell.

        - the easiest way to get this working:

            - make the `<log_folder>` somewhere outside the web root.
            - set the permissions on `<log_folder>` to 777.
            - create the file `django-research.log` there.
            - set its permissions also to 777.

        - This is not necessarily optimally secure, but truly securing this is beyond the scope of this README.

- You can set `level` to any of the following, which are organized from most detail (`logging.DEBUG`) to least (`logging.CRITICAL`):

    - `logging.DEBUG`
    - `logging.INFO`
    - `logging.WARNING`
    - `logging.ERROR`
    - `logging.CRITICAL`

- Python logging HOWTO: [https://docs.python.org/2/howto/logging.html](https://docs.python.org/2/howto/logging.html)
- Python logging cookbook: [https://docs.python.org/2/howto/logging-cookbook.html](https://docs.python.org/2/howto/logging-cookbook.html)

### database

Edit the research/research/settings.py file and update it with details of your database configuration.

In general, for any database other than sqlite3, in your database system of choice you'll need to:

- create a database for django to use (I typically use `research`).

    - postgresql - at the unix command line:
    
            # su to the postgres user
            su - postgres
            
            # create the database at the unix shell
            #createdb <database_name>
            createdb research

- create a database user for django to use that is not an admin (I typically use `django_user`).

    - postgresql - at the unix command line:
    
            # su to the postgres user
            su - postgres
            
            # create the user at the unix shell
            #createuser --interactive -P <username>
            createuser --interactive -P django_user

- give the django database user all privileges on the django database.
- place connection information for the database - connecting as your django database user to the django database - in settings.py.

An example for postgresql looks like this:

    DATABASES = {
        'default': {        
            # PostgreSQL - research
            'ENGINE': 'django.db.backends.postgresql', # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'research',                      # Or path to database file if using sqlite3.
            'USER': 'django_user',                      # Not used with sqlite3.
            'PASSWORD': '<db_password>',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        },
    }

More information:
    
- [https://docs.djangoproject.com/en/dev/intro/tutorial01/#database-setup](https://docs.djangoproject.com/en/dev/intro/tutorial01/#database-setup)
- [https://docs.djangoproject.com/en/dev/ref/settings/#databases](https://docs.djangoproject.com/en/dev/ref/settings/#databases)

# Testing

## Basic tests

- test by going to the URL:

        http://<your_server>/research/admin/

- and then logging in with the django superuser created by ansible scripts (this will be the use in the ansible "`ansible_user`" variable, and the password in the "`ansible_become_password`" variable in your host variables file).
- to test coding pages, test by going to the URL:

        http://<your_server>/research/context_data/index

- log in with your django superuser user.
- You should see a home page for context_data with a welcome message and a header that lists out the pages in the context_data application.

## Other applications

- You should also see on the root index page the other applications installed (jupyterhub, rstudio, etc.).
