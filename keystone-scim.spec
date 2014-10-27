Name: keystone-scim
Version: 0.0.1
Release: 1
Summary: Keystone SCIM extension
License: Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
Distribution: noarch
Vendor: Telefonica I+D
Group: Applications/System
Packager: Telefonica I+D
Requires: openstack-keystone
autoprov: no
autoreq: no
Prefix: /opt
BuildArch: noarch

%define _target_os Linux
%define python_lib /usr/lib/python2.6/site-packages
%define keystone_paste /usr/share/keystone/keystone-dist-paste.ini

%description
SCIM (System for Cross-domain Identity Management) extension for Keystone


%install
mkdir -p $RPM_BUILD_ROOT/%{python_lib}/keystone/contrib
cp -a %{_root}/keystone/contrib/scim $RPM_BUILD_ROOT/%{python_lib}/keystone/contrib
find $RPM_BUILD_ROOT/%{python_lib}/keystone/contrib -name "*.pyc" -delete

%files
"/usr/lib/python2.6/site-packages/keystone/contrib/scim"

%post
if ! grep -q -F "[filter:scim_extension]" "%{keystone_paste}"; then
  echo "Adding SCIM extension to Keystone configuration."
  sed -i \
  -e '/^\[pipeline:api_v3\]$/,/^\[/ s/^pipeline\(.*\) service_v3$/pipeline\1 scim_extension service_v3/' \
  -e 's/\[pipeline:api_v3\]/[filter:scim_extension]\npaste.filter_factory = keystone.contrib.scim.routers:ScimRouter.factory\n\n&/' \
  %{keystone_paste}
else
  echo "SCIM extension already configured. Skipping."
fi
echo "SCIM extension installed successfully. Restart Keystone daemon to take effect."

%preun
if grep -q -F "[filter:scim_extension]" "%{keystone_paste}"; then
  echo "Removing SCIM extension from Keystone configuration."
  sed -i \
  -e "/\[filter:scim_extension\]/,+2 d" \
  -e 's/scim_extension //g' \
  %{keystone_paste}
else
  echo "SCIM extension not configured. Skipping."
fi
