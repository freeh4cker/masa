# MASA

## Quick start

Filter freedivers given criteria and date. criteria are given as option.
the output can be a

* list of emails: *email_1@domain.org, email_2@domain.org*
* extended list of emails: *"Nom_1 Prenom" <email_1@domain.org>, "Nom_2 Prenom" <email_2@domain.org>*
* full freedivers information


    Prenom Nom_1          indoor/outdoor RIFAA     CACI      2021-09-20  L2 email@domain.org
    Prenom Nom_2          indoor/outdoor NO RIFAA  CACI      2021-09-20  L1 email@domain.org
    Prenom Nom_3          indoor/outdoor RIFAA     QS        2021-09-20  L1 email@domain.org
    Prenom Nom_4          indoor/outdoor RIFAA     NO certif 2021-09-20  L2 email@domain.org

if no date (in yyyy-mm-dd format) is provided *today* is used

for instance:

Displays the freedivers emails who are eligible to participate at *VLG fosse* today.

    masa --fosse

Displays the freedivers emails who are eligible to participate at VLG fosse the 30th June of 2021

    masa --fosse 2021-06-30

Displays the freedivers emails who are in *ligne 1* and are eligible to participate at VLG fosse the 30th June of 2021

    masa --fosse 2021-06-30 --l1

To know all options

    masa --help

## Installation

Use *pip* to install the package.
You need to have a internet connection to allow pip to download the dependencies.

    pip install -u masa-<version>.tar.gz

to upgrade an installed version

    pip install -u --upgrade masa-<version>.tar.gz

or

    pip install -u -U masa-<version>.tar.gz

dependencies
------------

* python >= 3.7
* pandas