#!/usr/bin/env python
# encoding: utf-8
"""
ninja.py

Bootstrap Django like a ninja! No more making all those files
manually. This highlights some examples of file management and argparse handling
This is a common way of handling passing in arguments to a script
when you are running something form a command line.

This has the following requirements:
1) django-admin must be accessible in your path
2) you must specify the directory you want the directory tree to be created_at
or it will use the working directory where this is run
"""

# Base modules
import sys, os
from subprocess import call

# Constants
INIT_FILE = '__init__.py'

INSTALLED_PACKAGES_STRING = 'INSTALLED_APPS = ['
URLS_IMPORT_STRING = 'from django.conf.urls import url'
URLS_PATTERNS_STRING = 'urlpatterns = ['

DJANGO_PROJECT_URLS_IMPORTS = 'from django.conf.urls import url, include\n'

APP_VIEWS_DEFAULT = [
            "# These are the most commonly used elements for application views",
            "from django.shortcuts import render, redirect",
            "from django.contrib import messages",
            "from django.core.urlresolvers import reverse",
            "",
            "# Import your models for this application",
            "# from .models import Course, Description, Comment",
            "",
            "# Import models from different applications",
            "# from ..<different_app>.models import <table_name>",
            "",
            "# Create your views here.",
            "def index(request):",
            "\tpass",
]


URL_FILE = [
            "# Import statements for application",
            "from django.conf.urls import url",
            "# Import your views",
            "from . import views",
            "# Use this if you want to import views from other applications",
            "# from ../<other_app> import views as <other_app_view_name>",
            "",
            "# URL patterns to process for the application",
            "urlpatterns = [",
            "\turl(r'^$', views.index, name='index'),",
            "\t#url(r'^course/add$', views.course_add, name='course_add'),",
            "\t#url(r'^course/destroy/(?P<course_id>\d+)$', views.course_destroy, name='destroy'),",
            "\t#url(r'^course/delete/(?P<course_id>\d+)$', views.course_remove, name='course_remove'),",
            "\t#url(r'^course/comment/(?P<course_id>\d+)$', views.course_comment, name='course_comment_show'),",
            "\t#url(r'^course/comment/add/(?P<course_id>\d+)$', views.course_comment_add, name='course_comment_add'),",
            "\t#url(r'^course/comment/delete/(?P<comment_id>\d+)$', views.course_comment_delete, name='course_comment_delete'),",
            "]",
]


# Initializer for argparse
def init():
    # Version Check for python.
    if sys.version_info[:2] < (2, 7):
        raise ValueError("You are running a Python version lower then 2.6. \
                          You must be running version 2.7 to use these scripts.  \
                          Please update your Python version")
    else:
        # Python preferred way of handling arguments. Only supported in 2.7+
        import argparse
        # Define the labels for the argparse object
        kwargs = {
            'description': 'Project Skeleton Generator',
            'epilog': 'Created by Ninja Josh'
        }
        """
        Define the argparse object. Here we do something called unpacking a dictionary
        This will expand the dictionary format from {key,value} to key=value.
        This is the format functions want their parameters passed in as and
        you get the added benefit of being able to pass around a dictionary.
        """
        parser = argparse.ArgumentParser(**kwargs)
        parser.add_argument('framework', metavar='framework', nargs='?',
                            default='django',
                            help='Framework you want to generate a skeleton for: \
                            example: django. django is the default if nothing \
                            is specified')
        parser.add_argument('projectname', metavar='project name', nargs='?',
                            default='main_project',
                            help='Name of the project you want to create. \
                            main_project is the default is none is specified')
        parser.add_argument('--directory', default=os.getcwd(), type=str,
                            help="Directory where you want these directories and files \
                            For example, you can use a relative path '~/Documents/<etc>' \
                            or you can use the exact path '/Users/<username>/Documents/<etc>' \
                            Must include the final / sign")
        parser.add_argument('--apps', default=['main_app'], type=str, nargs='*',
                            help='Applications you want to have configured. Multiple applications \
                            Can be specified. main_app is default if no applications \
                            are specified')
        args = parser.parse_args()
        # Return the arguements to the main script
        return args


# Touch a file. This results in an empty file
def touch(file, directory, times=None):
    with open(file, 'a'):
        os.utime(file, times)


# Create the application urls.py file
def create_app_url(directory):
    # Set the url.py location
    url_file = '/'.join([directory, 'urls.py'])
    # Create the urls.py file
    if not os.path.exists(url_file):
        with open(url_file, 'w') as filehandler:
            filehandler.writelines('%s\n' % line for line in URL_FILE)


def modify_settings(directory, modified):
    """
    This is not optimized, but easy to read
    This will modify the project settings.py file
    """
    # Set the settings file name
    settings_file = '/'.join([directory, 'settings.py'])
    # Make sure the file exists, otherwise ignore this step
    if os.path.exists(settings_file):
        # Open the file and get the items - ok since small file
        with open(settings_file, 'r') as filehandler:
            settings_list = filehandler.readlines()
        # Find the match and stash the index for the list insert
        # Store the index + 1 as we won't replace the matched line
        for index, line in enumerate(settings_list):
            if INSTALLED_PACKAGES_STRING in line:
                insert_index = index + 1
                break
        # Insert the new text lines
        for app in modified:
            text = ''.join(["\t'", app, "',\n"])
            settings_list.insert(insert_index, text)
            insert_index += 1
        # Overwrite the file with the new contents
        with open(settings_file, 'w') as filehandler:
            filehandler.writelines(settings_list)



def modify_urls(directory, modified):
    """
    This is not optimized, but easy to read
    This will modify the project urls.py file
    """
    # Set the settings file name
    urls_file = '/'.join([directory, 'urls.py'])
    # Make sure the file exists, otherwise ignore this step
    if os.path.exists(urls_file):
        # Open the file and get the items - ok since small file
        with open(urls_file, 'r') as filehandler:
            urls_list = filehandler.readlines()
        # Find the match and stash the index for the list insert
        # Match the exact index as we will replace this line
        for index, line in enumerate(urls_list):
            if URLS_IMPORT_STRING in line:
                import_insert_index = index
            elif URLS_PATTERNS_STRING in line:
                packages_begin_index = index
                break
        # Insert the new include
        urls_list[import_insert_index] = DJANGO_PROJECT_URLS_IMPORTS
        # Remove the existing packages
        urls_list = urls_list[:packages_begin_index + 1]
        # Overwrite the existing patterns
        for app in modified:
            # Create the initial url syntax
            url_initial = ''.join(["\turl(r'^", app, "', include('", modified[app]])
            # Add the namespace syntax
            full_url = "'".join([url_initial, ', namespace=', app, ")),\n"])
            # Add the formed url string to the list
            urls_list.append(full_url)
        # Make sure and close off the patterns
        urls_list.append(']')
        # Overwrite the file with the new contents
        with open(urls_file, 'w') as filehandler:
            filehandler.writelines(urls_list)


def modify_app_views(directory):
    """
    This is not optimized, but easy to read.
    This will append the default index function to the
    application view
    """
    # Set the settings file name
    views_file = '/'.join([directory, 'views.py'])
    # Make sure the file exists, otherwise ignore this step
    if os.path.exists(views_file):
        # Open the file and get the items - ok since small file
        with open(views_file, 'w') as filehandler:
            filehandler.writelines('%s\n' % line for line in APP_VIEWS_DEFAULT)


def create_content_directories(directory, app_name):
    """
    This will create the content directories for the
    application. This will ensure all static directories
    and the templates directory is configured
    """
    # Create the templates directory
    templates_dir = '/'.join([directory, 'templates', app_name])
    if not os.path.exists(templates_dir):
        try:
            os.makedirs(templates_dir)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    # Create the static directory tree
    statics_base_dir = '/'.join([directory, 'static', app_name])
    statics_css = '/'.join([statics_base_dir, 'css'])
    statics_js = '/'.join([statics_base_dir, 'js'])
    statics_img = '/'.join([statics_base_dir, 'img'])
    statics_tree = [statics_css, statics_js, statics_img]
    # Go through and create the static tree
    for static in statics_tree:
        if not os.path.exists(static):
            try:
                os.makedirs(static)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    raise


# Main function (default processor)
def main(args):
    # Pull out the projectname from the list
    projectname = args.projectname
    print('Calling for all skeleton setup for %s framework...' % args.framework)
    # Set the call args for the django-admin startproject
    call_args = ['django-admin', 'startproject', args.projectname]
    # Make an external call to django-admin for our startproject
    # Dirty, but gets the job done without creating an instance of the class
    result = call(call_args, cwd=args.directory)
    # Raise an exception if the call failed processing
    if result: raise Exception('Something went wrong with the project creation')
    # Create the apps skeleton
    base_project_path = '/'.join([args.directory, projectname, projectname])
    base_app_path = '/'.join([args.directory, projectname, 'apps'])
    # Only create the path if it does not exist
    if not os.path.exists(base_app_path):
        try:
            os.makedirs(base_app_path)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    # Create the __init__.py if it does not exist
    if not os.path.exists('/'.join([base_app_path, INIT_FILE])):
        try:
            touch(file='/'.join([base_app_path, INIT_FILE]), directory=base_app_path)
        except OSError as error:
            print (error)
    # Initialize the list of application strings for use in project
    apps_urls = {}
    apps_settings = []
    # Run through each application and setup the skeleton for each
    for app in args.apps:
        # Set the base application path
        app_path = base_app_path
        # Set the call args for the manage.py for startapp
        call_args = ['python', '../manage.py', 'startapp', app]
        # Make an external call to manage.py for our startapp
        # Dirty, but gets the job done without creating an instance of the class
        result = call(call_args, cwd=app_path)
        # Raise an exception if the call failed processing
        if result: raise Exception('Something went wrong with the application creation')
        # Make sure the urls.py get's created
        app_path = '/'.join([app_path, app])
        # Create the application url file
        create_app_url(directory=app_path)
        # Rewrite the application views file
        modify_app_views(directory=app_path)
        # Create all the content directories for the application
        create_content_directories(directory=app_path, app_name=app)
        # Add the formatted text to add to the project urls.py
        apps_urls[app] = '.'.join(['apps', app, 'urls'])
        # Add the formatted text to add to the project settings.py
        apps_settings.append('.'.join(['apps', app]))
    # Modify the existing project settings.py file
    modify_settings(directory=base_project_path, modified=apps_settings)
    # Modify the existing project urls.py file
    modify_urls(directory=base_project_path, modified=apps_urls)
    print ('Framework skeleton complete...')
    print ('Running migrations for initialization...')
    # Migrate settings so that request is proper and associated table exists
    call_args = ['python', 'manage.py', 'migrate']
    call(args=call_args, cwd='/'.join([args.directory, projectname]))
    print ('Project skeleton creation completed successfully!')


if __name__ == '__main__':
    main(init())
