"""WSGI Routers for the SCIM API."""

import functools

from keystone.common import json_home
from keystone.common import wsgi
from keystone.contrib.scim import controllers


build_resource_relation = functools.partial(
    json_home.build_v3_extension_resource_relation,
    extension_name='OS-SCIM', extension_version='1.0')


class ScimRouter(wsgi.V3ExtensionRouter):

    PATH_PREFIX = '/OS-SCIM'

    def add_routes(self, mapper):
        controller = controllers.ScimV3Controller()

        self._add_resource(
            mapper, controller,
            path=self.PATH_PREFIX + '/Users',
            get_action='list_users',
            post_action='create_user',
            rel=build_resource_relation(resource_name='users'))

        self._add_resource(
            mapper, controller,
            path=self.PATH_PREFIX + '/Users/{user_id}',
            get_action='get_user',
            patch_action='patch_user',
            put_action='put_user',
            delete_action='delete_user',
            rel=build_resource_relation(resource_name='users'))
