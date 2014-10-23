import uuid

from keystone import config
from keystone.contrib.scim import controllers
from keystone.tests import test_v3

CONF = config.CONF


class ScimTests(test_v3.RestfulTestCase):

    EXTENSION_NAME = 'scim'
    EXTENSION_TO_ADD = 'scim_extension'

    USERS_URL = '/OS-SCIM/Users'

    def setUp(self):
        super(ScimTests, self).setUp()

        self.base_url = 'http://localhost/v3'
        self.controller = controllers.ScimV3Controller()


class UserCRUDTests(ScimTests):

    def _build_user(self, username, domain, user_id=None, password=None,
                    remove=[]):
        proto = {
            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
            "userName": username,
            "password": password,
            "id": user_id,
            "emails": [
                {
                    "value": "%s@mailhost.com" % username
                }
            ],
            "active": True,
            "urn:scim:schemas:extension:keystone:1.0": {
                "domain": domain
            }
        }
        return dict((key, value)
                    for key, value in proto.iteritems()
                    if value is not None and key not in remove)

    def test_user_create(self):
        username = uuid.uuid4().hex
        user = self._build_user(username, self.domain_id, password='passw0rd')
        resp = self.post(self.USERS_URL, body=user).result

        self.assertIsNotNone(resp["id"])
        self.assertIsNone(resp.get("password", None))

        expected_user = self._build_user(username, self.domain_id,
                                         user_id=resp['id'])
        self.assertEqual(expected_user, resp)

    def test_user_list(self):
        username = uuid.uuid4().hex
        user = self._build_user(username, self.domain_id, password='passw0rd')
        self.post(self.USERS_URL, body=user)

        users_url = ('%(base)s?domain_id=%(domain_id)s' %
                     {'base': self.USERS_URL,'domain_id': self.domain_id})
        users = self.get(users_url).result
        matching_listed_user = [u for u in users["Resources"]
                       if u.get('userName', '') == username]

        self.assertEqual(1, len(matching_listed_user))
        expected_user = self._build_user(username, self.domain_id,
                                         user_id=matching_listed_user[0]["id"])
        self.assertEqual(expected_user, matching_listed_user[0])

    def test_user_get(self):
        username = uuid.uuid4().hex
        user = self._build_user(username, self.domain_id, password='passw0rd')
        resp = self.post(self.USERS_URL, body=user).result

        user_url = '%s/%s' % (self.USERS_URL, resp['id'])
        got_user = self.get(user_url).result

        expected_user = self._build_user(username, self.domain_id,
                                         user_id=resp['id'])

        self.assertEqual(expected_user, got_user)

    def test_user_update(self):
        username = uuid.uuid4().hex
        user = self._build_user(username, self.domain_id, password='passw0rd')
        resp = self.post(self.USERS_URL, body=user).result

        user['id'] = resp['id']
        user['emails'][0]['value'] = 'other@mail.com'

        user_url = '%s/%s' % (self.USERS_URL, resp['id'])
        self.put(user_url, body=user, expected_status=200)
        got_user = self.get(user_url).result

        expected_user = self._build_user(username, self.domain_id,
                                         user_id=resp['id'])
        expected_user['emails'][0]['value'] = 'other@mail.com'

        self.assertEqual(expected_user, got_user)

    def test_user_delete(self):
        username = uuid.uuid4().hex
        user = self._build_user(username, self.domain_id, password='passw0rd')
        resp = self.post(self.USERS_URL, body=user).result

        user_url = '%s/%s' % (self.USERS_URL, resp['id'])
        self.delete(user_url, expected_status=204)
        self.get(user_url, expected_status=404)
