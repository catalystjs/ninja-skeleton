# ninja-skeleton
Bootstrap Django like a ninja! No more making all those files
manually. This highlights some examples of file management and argparse handling
This is a common way of handling passing in arguments to a script
when you are running something form a command line.

This has the following requirements:
1) django-admin must be accessible in your path
2) you must specify the directory you want the directory tree to be created_at
or it will use the working directory where this is run
3) supply a project name and application name(s). Defaults are used if nothing is supplied

Example output (no passed arguments):
JOSHUAs-MBP:Django joshuasummers$ python ~/Documents/Personal/Python/dojo-scripts/ninja.py 
Calling for all skeleton setup for django framework...
Framework skeleton complete...
Running migrations for initialization...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
Project skeleton creation completed successfully!

JOSHUAs-MBP:Django joshuasummers$ find main_project -type d -print
main_project
main_project/apps
main_project/apps/main_app
main_project/apps/main_app/migrations
main_project/apps/main_app/static
main_project/apps/main_app/static/main_app
main_project/apps/main_app/static/main_app/css
main_project/apps/main_app/static/main_app/img
main_project/apps/main_app/static/main_app/js
main_project/apps/main_app/templates
main_project/apps/main_app/templates/main_app
main_project/main_project

Example output (passed arguments):
JOSHUAs-MBP:Django joshuasummers$ python ~/Documents/Personal/Python/dojo-scripts/ninja.py example_project --apps app1 app2 app3
Calling for all skeleton setup for example_project framework...
Framework skeleton complete...
Running migrations for initialization...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
Project skeleton creation completed successfully!

JOSHUAs-MBP:Django joshuasummers$ find example_project -type d -print
example_project
example_project/apps
example_project/apps/app1
example_project/apps/app1/migrations
example_project/apps/app1/static
example_project/apps/app1/static/app1
example_project/apps/app1/static/app1/css
example_project/apps/app1/static/app1/img
example_project/apps/app1/static/app1/js
example_project/apps/app1/templates
example_project/apps/app1/templates/app1
example_project/apps/app2
example_project/apps/app2/migrations
example_project/apps/app2/static
example_project/apps/app2/static/app2
example_project/apps/app2/static/app2/css
example_project/apps/app2/static/app2/img
example_project/apps/app2/static/app2/js
example_project/apps/app2/templates
example_project/apps/app2/templates/app2
example_project/apps/app3
example_project/apps/app3/migrations
example_project/apps/app3/static
example_project/apps/app3/static/app3
example_project/apps/app3/static/app3/css
example_project/apps/app3/static/app3/img
example_project/apps/app3/static/app3/js
example_project/apps/app3/templates
example_project/apps/app3/templates/app3
example_project/example_project
