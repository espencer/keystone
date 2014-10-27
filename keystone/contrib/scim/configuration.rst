..

==============
Extension SCIM
==============

Enabling the extension:

1. Add the ``scim_extension`` filter to the ``api_v3`` pipeline in
   ``keystone-paste.ini``. This must be added after ``json_body`` and before
   the last entry in the pipeline. For example::

    [pipeline:api_v3]
    pipeline = sizelimit url_normalize build_auth_context token_auth admin_token_auth xml_body_v3 json_body ec2_extension_v3 s3_extension simple_cert_extension revoke_extension scim_extension service_v3


=======
Testing
=======

Running functional tests

    tox -e py27 keystone.tests.test_scim

Running unit tests

    tox -e py27 keystone.tests.unit.contrib.scim

=========
Packaging
=========

Packaging creates RPM containing only the SCIM extension, ready to be deployed
onto an existing Keystone installation (installation only tested on Redhad/Centos,
building tested also on Mac OSX):

    sh keystone-scim.sh

==========
Installing
==========

Just install the created RPM in previous step on top of an existing Keystone
installation (RPM only works on Centos/Redhat)

    sudo rpm -ivh keystone-scim*.rpm

RPM installation automatically enables the SCIM extension, so no extra step
is needed further than restarting the Keystone server.

    sudo service openstack-keystone restart
