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
Hacking
=======

Running functional tests

    tox -e py27 keystone.tests.test_scim.UserCRUDTests

Running unit tests

    tox -e py27 keystone.tests.unit.contrib.scim

