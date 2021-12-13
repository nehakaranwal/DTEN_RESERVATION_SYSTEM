# DTEN_RESERVATION_SYSTEM

Install One API toolkit from https://www.intel.com/content/www/us/en/developer/articles/guide/download-documentation-intel-oneapi-toolkits-components.html
Django Tutorial in Visual Studio Code

To successfully complete this Django tutorial, you must do the following (which are the same steps as in the general Python tutorial):

Install the Python extension.

Install a version of Python 3 (for which this tutorial is written). Options include:

(All operating systems) A download from python.org; typically use the Download Python 3.9.1 button that appears first on the page (or whatever is the latest version).
(Linux) The built-in Python 3 installation works well, but to install other Python packages you must run sudo apt install python3-pip in the terminal.
(macOS) An installation through Homebrew on macOS using brew install python3 (the system install of Python on macOS is not supported).
(All operating systems) A download from Anaconda (for data science purposes).
On Windows, make sure the location of your Python interpreter is included in your PATH environment variable. You can check the location by running path at the command prompt. If the Python interpreter's folder isn't included, open Windows Settings, search for "environment", select Edit environment variables for your account, then edit the Path variable to include that folder.

Create a superuser and enable the administrative interface#
By default, Django provides an administrative interface for a web app that's protected by authentication. The interface is implemented through the built-in django.contrib.admin app, which is included by default in the project's INSTALLED_APPS list (settings.py), and authentication is handled with the built-in django.contrib.auth app, which is also in INSTALLED_APPS by default.

Perform the following steps to enable the administrative interface:

Create a superuser account in the app by opening a Terminal in VS Code for your virtual environment, then running the command python manage.py createsuperuser --username=<username> --email=<email>, replacing <username> and <email>, of course, with your personal information. When you run the command, Django prompts you to enter and confirm your password.

Be sure to remember your username and password combination. These are the credentials you use to authenticate with the app.

Add the following URL route in the project-level urls.py (web_project/urls.py in this tutorial) to point to the built-in administrative interface:

# This path is included by default when creating the app
 path("admin/", admin.site.urls),
Run the server, then open a browser to the app's /admin page (such as http://127.0.0.1:8000/admin when using the development server).

A login page appears, courtesy of django.contrib.auth. Enter your superuser credentials.

Django tutorial: default Django login prompt
