%define tog_pegasus_version 2:2.6.1-1
%define provider_dir %{_libdir}/cmpi

Name:           sblim-cmpi-sysfs
Version:        1.2.0
Release:        1%{?dist}
Summary:        SBLIM sysfs instrumentation

Group:          Applications/System
License:        EPL
URL:            http://sblim.wiki.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tog-pegasus-devel >= %{tog_pegasus_version}
BuildRequires:  sblim-cmpi-base-devel
Requires:       tog-pegasus >= %{tog_pegasus_version}
Requires:       sblim-cmpi-base

%description
Standards Based Linux Instrumentation Sysfs Providers

%package        test
Summary:        SBLIM Sysfs Instrumentation Testcases
Group:          Applications/System
Requires:       sblim-cmpi-sysfs = %{version}-%{release}
Requires:       sblim-testsuite
Requires:       tog-pegasus

%description test
SBLIM Base Params Testcase Files for SBLIM Testsuite

%prep
%setup -q
sed -ri 's,-type d -maxdepth 1 -mindepth 1,-maxdepth 1 -mindepth 1 -type d,g' \
        ./test/system/linux/*.{sh,system}


%build
%ifarch s390 s390x ppc ppc64
export CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
%else
export CFLAGS="$RPM_OPT_FLAGS"
%endif

%configure \
        TESTSUITEDIR=%{_datadir}/sblim-testsuite \
        CIMSERVER=pegasus \
        PROVIDERDIR=%{provider_dir}
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove unused libtool files
rm -f $RPM_BUILD_ROOT/%{_libdir}/*a
rm -f $RPM_BUILD_ROOT/%{provider_dir}/*a
# shared libraries
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/cmpi" > $RPM_BUILD_ROOT/%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
mv $RPM_BUILD_ROOT/%{_libdir}/libLinux_SysfsAttributeUtil.so $RPM_BUILD_ROOT/%{provider_dir}
mv $RPM_BUILD_ROOT/%{_libdir}/libLinux_SysfsDeviceUtil.so $RPM_BUILD_ROOT/%{provider_dir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,0755)
%dir %{provider_dir}
%{provider_dir}/libLinux_Sysfs*
%{_datadir}/sblim-cmpi-sysfs
%docdir %{_datadir}/doc/sblim-cmpi-sysfs-%{version}
%{_datadir}/doc/sblim-cmpi-sysfs-%{version}
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files test
%defattr(-,root,root,0755)
%{_datadir}/sblim-testsuite/sblim-cmpi-sysfs-test.sh
%{_datadir}/sblim-testsuite/cim/Linux_Sysfs*
%{_datadir}/sblim-testsuite/system/linux/Linux_Sysfs*


%define SYSFS_SCHEMA %{_datadir}/%{name}/Linux_SysfsAttribute.mof %{_datadir}/%{name}/Linux_SysfsBlockDevice.mof %{_datadir}/%{name}/Linux_SysfsBusDevice.mof %{_datadir}/%{name}/Linux_SysfsInputDevice.mof %{_datadir}/%{name}/Linux_SysfsNetworkDevice.mof %{_datadir}/%{name}/Linux_SysfsSCSIDevice.mof %{_datadir}/%{name}/Linux_SysfsSCSIHostDevice.mof %{_datadir}/%{name}/Linux_SysfsTTYDevice.mof
%define SYSFS_REGISTRATION %{_datadir}/%{name}/Linux_SysfsAttribute.registration %{_datadir}/%{name}/Linux_SysfsBlockDevice.registration %{_datadir}/%{name}/Linux_SysfsBusDevice.registration %{_datadir}/%{name}/Linux_SysfsInputDevice.registration %{_datadir}/%{name}/Linux_SysfsNetworkDevice.registration %{_datadir}/%{name}/Linux_SysfsSCSIDevice.registration %{_datadir}/%{name}/Linux_SysfsSCSIHostDevice.registration %{_datadir}/%{name}/Linux_SysfsTTYDevice.registration

%pre
if [ $1 -gt 1 ]; then
  %{_datadir}/%{name}/provider-register.sh -d \
        -t pegasus -r %{SYSFS_REGISTRATION} -m %{SYSFS_SCHEMA} > /dev/null 2>&1 || :;
fi

%post
/sbin/ldconfig
if [ $1 -ge 1 ]; then
   %{_datadir}/%{name}/provider-register.sh \
   -t pegasus -r %{SYSFS_REGISTRATION} -m %{SYSFS_SCHEMA} > /dev/null 2>&1 || :;
fi

%preun
if [ $1 -eq 0 ]; then
   %{_datadir}/%{name}/provider-register.sh -d \
   -t pegasus -r %{SYSFS_REGISTRATION} -m %{SYSFS_SCHEMA} > /dev/null 2>&1 || :;
fi

%postun -p /sbin/ldconfig


%changelog
* Wed Jun 30 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.2.0-1
- Update to sblim-cmpi-sysfs-1.2.0

* Wed Oct 14 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.1.9-1
- Initial support
