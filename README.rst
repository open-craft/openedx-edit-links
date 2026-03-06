openedx-edit-links
=============================

An Open edX backend plugin that provides a way to embed links to the course content stored in Git repositories as HTML files in the `Open Learning XML <https://docs.openedx.org/en/latest/educators/olx/what-is-olx.html>`_ format.

The plugin implements an `openedx-filters <https://github.com/openedx/openedx-filters/>`_ pipeline that hooks into the `VerticalBlockChildRenderStarted <https://github.com/openedx/openedx-filters/blob/da2326a3adbb6fce898a348e7a6ca66d76114bb4/openedx_filters/learning/filters.py#L846>`_ event on the ``VerticalBlock`` XBlock.
The pipeline modifies the HTML content of ``HTMLBlock`` to add necessary HTML that renders an **Edit on Git** link on top of each child of the ``VerticalBlock``.

Pre-requisites
--------------

In order for this plugin to be used effectively the course content should be stored in a public repostiory in the `Open Learning XML <https://docs.openedx.org/en/latest/educators/olx/what-is-olx.html>`_ format. This allows the plugin to link each section of the course content to it's corresponding HTML file by automatically appending the filenames to the base URL of the repository.

Installation
------------

* Install the plugin by adding ``git+https://github.com/open-craft/openedx-edit-links.git`` to your ``EDXAPP_EXTRA_REQUIREMENTS`` of your deployment. On Tutor, this can be accomplished by

.. code-block:: sh

    tutor config save --append OPENEDX_EXTRA_PIP_REQUIREMENTS=git+https://github.com/open-craft/openedx-edit-links.git


Configuration
-------------

#. Configure the plugin variables by setting the the following 2 values

   * ``EDIT_LINKS_PLUGIN_GIT_REPOS`` - a map of course IDs and the correspondint Git URLs. This URLs used here would be considered as the base of the ``course`` folder of the course content. For eg.,

      .. code-block:: python

          EDIT_LINKS_PLUGIN_GIT_REPOS = {
              "course-v1:OpenedX+DemoX+DemoCourse": "https://github.com/openedx/openedx-demo-course/edit/master/demo-course/course/",
          }


   * ``EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL`` - an OPTIONAL configuration which lets you specify the word to use in the links ``Edit on <label>``. Defaults to **Git**.

      .. code-block:: python

          EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL = "Gitlab"


#. Configure ``openedx-filters`` to run the plugin's pipeline

   .. code-block:: python

       OPEN_EDX_FILTERS_CONFIG = {
           "org.openedx.learning.vertical_block_child.render.started.v1": {
               "fail_silently": False,
               "pipeline": [
                   "edit_links.pipeline.AddEditLink"
               ]
           }
       }

**Note:** The base URL in the configuration should point the OLX course directory in your Git repo. The plugin adds ``/html/<filename.html>`` to take the user to the relevant file.


As a Tutor Plugin
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from tutor import hooks

    hooks.Filters.ENV_PATCHES.add_item(
        (
            "openedx-common-settings",
            """
    EDIT_LINKS_PLUGIN_GIT_REPOS = {
        "course-v1:OpenedX+DemoX+DemoCourse": "https://github.com/openedx/openedx-demo-course/edit/master/demo-course/course/",
    }

    EDIT_LINKS_PLUGIN_GIT_EDIT_LABEL = "Github"

    OPEN_EDX_FILTERS_CONFIG = {
        "org.openedx.learning.vertical_block_child.render.started.v1": {
            "fail_silently": False,
            "pipeline": [
                "edit_links.pipeline.AddEditLink"
            ]
        }
    }
    """),
    )



Development Workflow
--------------------

The plugin can be developed using a Tutor dev environment.

1. Clone the repo.
2. Add the repo as a Tutor mount. ``tutor mounts add /path/to/openedx-edit-links``.
3. Rebuild the ``openedx-dev`` image. ``tutor images build openedx-dev``.
4. Create a Tutor plugin based the example above and enable it.
5. Restart the services.

Now the edit links should to become available in the course. Any changes to the plugin should restart the LMS service.


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

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


License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://docs.openedx.org/en/latest/developers/quickstarts/so_you_want_to_contribute.html>`_ for details.
Even though they were written with ``openedx-platform`` in mind, the guidelines
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

Our real-time conversations are on Slack. You can join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _community Slack workspace: https://openedx.org/slack
.. _Getting Help: https://openedx.org/getting-help
