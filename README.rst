openedx-edit-links
=============================

|pypi-badge| |ci-badge| |codecov-badge| |doc-badge| |pyversions-badge|
|license-badge|

Edit Links is an Open edX plugin application that provides a way to embed links to the course content stored in Git repositories as HTML files in the `Open Learning XML <https://edx.readthedocs.io/projects/edx-open-learning-xml/en/latest/front_matter/read_me.html>`_ format.

Overview
--------

The plugin implements an `openedx-filters <https://github.com/openedx/openedx-filters/>`_ pipeline that hooks into the `VerticalBlockChildRenderStarted` event on the `VerticalBlock` XBlock on platform.
The pipeline modifies the HTML content of `HTMLBlock` blocks and appends necessary html to add an "Edit on Git" link on top of each child block of the `VerticalBlock`.

Documentation
-------------

Pre-requisites
~~~~~~~~~~~~~~
In order for this plugin to be used effectively the course content should be stored in a public repostiory in the `Open Learning XML <https://edx.readthedocs.io/projects/edx-open-learning-xml/en/latest/front_matter/read_me.html>`_ format. This allows the plugin to link each section of the course content to it's corresponding HTML file by automatically appending the filenames to the base URL of the repository. 

Installation
~~~~~~~~~~~~

* Install the plugin by adding `git+https://github.com/open-craft/openedx-edit-links.git` to your `EDXAPP_EXTRA_REQUIREMENTS` of your deployment.
* Make sure you have the latest version of `openedx-filters` installed as well.


Configuration
~~~~~~~~~~~~~

The plugin can be configured by adding custom settings to your deployment's `lms.yml`.

#. Configure the plugin variables by setting the the following 2 values
    * `EDIT_LINKS_PLUGIN_GIT_REPOS` - a map of course ids and the correspondint Git urls. This urls used here would be considered as the base of the `course` folder of the course content. For eg., 

    .. code-block::

        EDIT_LINKS_PLUGIN_GIT_REPOS = {
            "course-v1:my+awesome+course": "https://gitlab.com/awesome-course/-/tree/master/course/",
            "course-v1:foss+course+2022": "https://gitlab.com/foss-course/-/tree/master/2022/course/",
        }
    
    * `EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL` - an OPTIONAL configuration which lets you specify the word to use in the links "Edit on <label>". Defaults to `Git`.

    .. code-block::

        EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL = "Gitlab"

#. Configure `openedx-filters` to run the plugin's pipeline

    .. code-block::

        OPEN_EDX_FILTERS_CONFIG = {
            "org.openedx.learning.verticalblockchild.render.started.v1": {
                "fail_silently": False,
                "pipeline": [
                    "edit_links.pipeline.AddEditLink"
                ]
            }
        }


Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block::

  # Clone the repository
  git clone git@github.com:open-craft/openedx-edit-links.git
  cd openedx-edit-links

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-edit-links


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

  # Activate the virtualenv
  workon openedx-edit-links

  # Grab the latest code
  git checkout main
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

Developing with the Devstack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Clone the repository to your `/edx/src/` folder
#. Install the plugin inside your lms container

    .. code-block::

        make lms-shell
        pip install -e /edx/src/openedx-edit-links

#. Add the necessary configuration (as mentioned in the "Configuration" section above) to your `edx-platform/lms/envs/private.py`
#. Restart the lms container to ensure everything is loaded `make lms-restart`

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx-slack-invite.herokuapp.com/
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |pypi-badge| image:: https://img.shields.io/pypi/v/openedx-edit-links.svg
    :target: https://pypi.python.org/pypi/openedx-edit-links/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/edx/openedx-edit-links/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/edx/openedx-edit-links/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/edx/openedx-edit-links/coverage.svg?branch=main
    :target: https://codecov.io/github/edx/openedx-edit-links?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/openedx-edit-links/badge/?version=latest
    :target: https://openedx-edit-links.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/openedx-edit-links.svg
    :target: https://pypi.python.org/pypi/openedx-edit-links/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/edx/openedx-edit-links.svg
    :target: https://github.com/edx/openedx-edit-links/blob/main/LICENSE.txt
    :alt: License
