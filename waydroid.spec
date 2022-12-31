Summary:	A container-based approach to boot a full Android system on a regular GNU/Linux system
Name:		waydroid
Version:	1.3.4
Release:	0.1
License:	GPL v3
Group:		Applications/Emulators
Source0:	https://github.com/waydroid/waydroid/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3b8fd9641a7304572798bd080a0bbdc5
URL:		https://waydro.id/
BuildRequires:	rpmbuild(macros) >= 2.011
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	systemd-units >= 1:250.1
Requires:	python3-gbinder
Requires:	python3-pyclipper
Requires:	python3-pygobject3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A container-based approach to boot a full Android system on a regular
GNU/Linux system.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	SYSD_DIR=%{systemdunitdir} \
	WAYDROID_DIR=%{_datadir}/waydroid \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
	$RPM_BUILD_ROOT%{_datadir}/waydroid/waydroid.py

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post waydroid-container.service

%preun
%systemd_preun waydroid-container.service

%postun
%systemd_postun waydroid-container.service

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/%{name}*
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/waydroid.py
%{_datadir}/%{name}/data
%{_datadir}/%{name}/tools
%{systemdunitdir}/waydroid-container.service
%{_desktopdir}/Waydroid.desktop
%{_desktopdir}/waydroid.market.desktop
%{_datadir}/metainfo/id.waydro.waydroid.metainfo.xml
