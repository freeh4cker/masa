.. masa filter MASA freedivers

.. _user_guide:

**********
User Guide
**********


Quick start
***********

Filter freedivers given criteria and date. criteria are given as option.
the output can be a

* list of emails: *email_1@domain.org, email_2@domain.org*
* extended list of emails: *"Nom_1 Prenom" <email_1@domain.org>, "Nom_2 Prenom" <email_2@domain.org>*
* full freedivers information

.. code-block:: text

    Prenom Nom_1          indoor/outdoor RIFAA     CACI      2021-09-20  L2 email@domain.org
    Prenom Nom_2          indoor/outdoor NO RIFAA  CACI      2021-09-20  L1 email@domain.org
    Prenom Nom_3          indoor/outdoor RIFAA     QS        2021-09-20  L1 email@domain.org
    Prenom Nom_4          indoor/outdoor RIFAA     NO certif 2021-09-20  L2 email@domain.org

if no date (in yyyy-mm-dd format) is provided *today* is used

for instance:

Displays the freedivers emails who are eligible to participate at *VLG fosse* today.

:code:`masa --fosse`

Displays the freedivers emails who are eligible to participate at VLG fosse the 30th June of 2021

:code:`masa --fosse 2021-06-30`

Displays the freedivers emails who are in *ligne 1* and are eligible to participate at VLG fosse the 30th June of 2021

:code:`masa --fosse 2021-06-30 --l1`



The available options are listed bellow
.. raw::

    usage: masa [-h] [--autonomie-absolue-piscine [AUTONOMIE_ABSOLUE_PISCINE] | --autonomie-relative-piscine [AUTONOMIE_RELATIVE_PISCINE] | --fosse [FOSSE] | --rifaa |
                --no-rifaa | --valid [VALID] | --not-valid [NOT_VALID] | --warning [WARNING] | --all] [--version] [-v]

     __  __    _    ____    _
    |  \/  |  / \  / ___|  / \
    | |\/| | / _ \ \___ \ / _ \
    | |  | |/ ___ \ ___) / ___ \
    |_|  |_/_/   \_\____/_/   \_\  freediver filtering software

    optional arguments:
      -h, --help            show this help message and exit
      --autonomie-absolue-piscine [AUTONOMIE_ABSOLUE_PISCINE]
                            list of emails with valid CACI or QS at the specified date (yyyy-mm-dd)
                            and allow to dive in autonomie absolue in pool (default=today)
      --autonomie-relative-piscine [AUTONOMIE_RELATIVE_PISCINE]
                            list of emails with valid CACI or QS at the specified date (yyyy-mm-dd)
                            and allow to dive in autonomie relative in pool (default=today)
      --fosse [FOSSE]       list of emails with valid CACI or QS at the specified date (yyyy-mm-dd)
                            and allow to dive at VLG (default=today)
      --profondeur [PROFONDEUR]
                            list of emails with valid CACI at the specified date (yyyy-mm-dd)
                            (default=today)
      --rifaa               freedivers who held RIFAA
      --no-rifaa            freedivers who do NOT held RIFAA
      --valid [VALID]       list of emails with valid CACI or QS at the specified date (yyyy-mm-dd) (default=today)
      --not-valid [NOT_VALID]
                            list of emails with NO valid CACI or QS at the specified date (yyyy-mm-dd) (default=today)
      --warning [WARNING]   list of emails with valid CACI or QS today but
                            expire at today + delta time (in days) (default=15 days)
      --all                 list of emails of all freedivers
      --l1                  Filter only divers in Ligne 1.
                            - This option must be combined with previous ones.
                            - This option is mutually exclusive with --L2
      --l2                  Filter only divers in Ligne 2.
                            - This option must be combined with previous ones.
                            - This option is mutually exclusive with --L1
      --data DATA           The path to the 'masa.tsv' data file, by default provide with release
      --version             show program's version number and exit
      -v, --verbose         increase verbosity
                            -v displays email in long version "Prenom Nom" <email>'
                            -vv displays all info Prenom Nom indoor/outdoor rifaa CACI|QS date email


Installation
************

for users
=========

Use *pip* to install the package.
You need to have a internet connection to allow pip to download the dependencies.

:code:`pip install -u masa-<version>.tar.gz`

dependencies
------------

* python >= 3.7
* pandas
