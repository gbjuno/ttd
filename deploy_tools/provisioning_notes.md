Provisioning a new site
=======================

## Require packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host Config

* see nginx.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Upstart Job
* see gunicorn-upstart.template.conf
* replace SITENAME with, eg, staging.my-domain.com

## Folder structure：
Assume we have a user accouont at /home/username

/home/username
|___sites
    |___SITENAME
        |___database
        |___source
        |___static
        |___virtualenv

