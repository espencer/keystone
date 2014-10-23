"""Unit tests for SCIM converter."""

from keystone import tests
import keystone.contrib.scim.converter as conv

class TestScimConverter(tests.BaseTestCase):

    def test_user_scim2keystone(self):
        scim = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
            "id": "19041ee7679649879ada04417753ad4d",
            "userName": "alice",
            "emails": [
                {
                    "value": "alice@mailhost.com"
                }
            ],
            "password": "s0m3p4ssw0rd",
            "active": True,
            "urn:scim:schemas:extension:keystone:1.0": {
                "domain": "91d79dc2211d43a7985ebc27cdd146df"
            }
        }

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'password': 's0m3p4ssw0rd',
            'enabled': True
        }

        self.assertEqual(keystone, conv.user_scim2key(scim))

    def test_user_scim2keystone_no_mandatory_fields(self):
        scim = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
            "userName": "alice",
            "urn:scim:schemas:extension:keystone:1.0": {
                "domain": "91d79dc2211d43a7985ebc27cdd146df"
            }
        }

        keystone = {
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'alice',
        }

        self.assertEqual(keystone, conv.user_scim2key(scim))

    def test_user_key2scim(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'enabled': True
        }

        scim = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
            "id": "19041ee7679649879ada04417753ad4d",
            "userName": "alice",
            "emails": [
                {
                    "value": "alice@mailhost.com"
                }
            ],
            "active": True,
            "urn:scim:schemas:extension:keystone:1.0": {
                "domain": "91d79dc2211d43a7985ebc27cdd146df"
            }
        }

        self.assertEqual(scim, conv.user_key2scim(keystone))

    def test_user_key2scim_no_mandatory_fields(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
        }

        scim = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
            "id": "19041ee7679649879ada04417753ad4d",
            "urn:scim:schemas:extension:keystone:1.0": {
                "domain": "91d79dc2211d43a7985ebc27cdd146df"
            }
        }

        self.assertEqual(scim, conv.user_key2scim(keystone))


def test_user_scim2key_utf8(self):
    scim = {
        'userName': u'alice',
        'urn:scim:schemas:extension:keystone:1.0': {
            u'domain': u'91d79dc2211d43a7985ebc27cdd146df'
        },
        'emails': [{u'value': u'alice@mailhost.com'}],
        'active': True,
        'id': u'19041ee7679649879ada04417753ad4d',
        'schemas': [u'urn:scim:schemas:core:1.0',
                    u'urn:scim:schemas:extension:keystone:1.0']}

    keystone = {
        'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
        'email': 'alice@mailhost.com',
        'name': 'alice',
        'enabled': True
    }

    self.assertEqual(keystone, conv.user_key2scim(scim))