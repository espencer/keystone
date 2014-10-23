"""Converters between SCIM JSON representation and Keystone"""

def user_key2scim(ref):
    scim = {
        "schemas": ["urn:scim:schemas:core:1.0",
                    "urn:scim:schemas:extension:keystone:1.0"],
        "id": ref.get("id", None),
        "userName": ref.get("name", None),
        "active": ref.get("enabled", None),
        "urn:scim:schemas:extension:keystone:1.0": {
            "domain": ref.get("domain_id", None)
        }
    }
    if "email" in ref:
        scim["emails"] = [
            {"value": ref["email"]}
        ]

    # rid of None values
    return dict(filter(lambda x: x[1], scim.items()))


def listusers_key2scim(ref):
    return {
        "schemas": ["urn:scim:schemas:core:1.0", "urn:scim:schemas:extension:keystone:1.0"],
        "Resources": map(user_key2scim, ref)
    }


def user_scim2key(scim):
    keystone = {
        "domain_id": scim.get("urn:scim:schemas:extension:keystone:1.0", {})
            .get("domain", None),
        "email": scim.get("emails", [{}])[0].get("value", None),
        "id": scim.get("id", None),
        "enabled": scim.get("active", None),
        "name": scim.get("userName", None),
        "password": scim.get("password", None)
    }

    # rid of None values
    return dict(filter(lambda x: x[1], keystone.items()))
