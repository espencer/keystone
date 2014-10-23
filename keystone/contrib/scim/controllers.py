"""Extensions supporting SCIM."""

from keystone import config
from keystone.identity.controllers import UserV3
from keystone.openstack.common import log
import converter as conv

CONF = config.CONF
LOG = log.getLogger(__name__)


class ScimV3Controller(UserV3):

    collection_name = 'users'
    member_name = 'user'

    def __init__(self):
        super(ScimV3Controller, self).__init__()

    def list_users(self, context, filters=None):
        ref = super(ScimV3Controller, self).list_users(context)
        return conv.listusers_key2scim(ref["users"])

    def get_user(self, context, user_id):
        ref = super(ScimV3Controller, self).get_user(context, user_id=user_id)
        return conv.user_key2scim(ref["user"])

    def create_user(self, context, **kwargs):
        scim = self._denormalize(kwargs)
        user = conv.user_scim2key(scim)
        ref = super(ScimV3Controller, self).create_user(context, user=user)
        return conv.user_key2scim(ref.get("user", None))

    def patch_user(self, context, user_id, **kwargs):
        scim = self._denormalize(kwargs)
        user = conv.user_scim2key(scim)
        ref = super(ScimV3Controller, self).update_user(
            context, user_id=user_id, user=user)
        return conv.user_key2scim(ref.get("user", None))

    def put_user(self, context, user_id, **kwargs):
        return self.patch_user(context, user_id, **kwargs)

    def delete_user(self, context, user_id):
        return super(ScimV3Controller, self).delete_user(context, user_id=user_id)

    def _denormalize(self, data):
        data['urn:scim:schemas:extension:keystone:1.0'] = data.pop(
            'urn_scim_schemas_extension_keystone_1.0', {})
        return data

