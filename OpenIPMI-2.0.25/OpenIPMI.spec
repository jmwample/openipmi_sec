# For common adjustments that are needed for this file, search for
# "USERFIX"

Name: OpenIPMI
Summary: %{name} - Library interface to IPMI
Version: 2.0.25
Release: 2
License: LGPL
URL: http://openipmi.sourceforge.net
Group: Utilities
Vendor: OpenIPMI Project
Packager: Tariq Shureih <tariq.shureih@intel.com>
Source: %{name}-2.0.25.tar.gz
Buildroot: /var/tmp/%{name}-root
BuildRequires: pkgconfig, perl >= 5, swig >= 1.3
Summary: IPMI Library
Group: Utilities

# Figure out if glib12 is installed
%define glib12 %(if ls -l /usr/lib/libglib-1.2* >/dev/null 2>&1; then echo yes; else echo no; fi)

%description 
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package devel
Summary: Development files for OpenIPMI
Group: Utilities
Requires: OpenIPMI = %{version}, pkgconfig

%description devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package perl
Summary: Perl interface for OpenIPMI
Group: Utilities
Requires: OpenIPMI = %{version}, perl >= 5

%description perl
A Perl interface for OpenIPMI.

%package python
Summary: Python interface for OpenIPMI
Group: Utilities
Requires: OpenIPMI = %{version}, python

%description python
A Python interface for OpenIPMI.

%package gui
Summary: GUI (in python) for OpenIPMI
Group: Utilities
Requires: OpenIPMI-python = %{version}, tkinter

%description gui
A GUI interface for OpenIPMI.  Written in python an requiring wxWidgets.

%package ui
Summary: User Interface (ui)
Group: Utilities
Requires: OpenIPMI = %{version}

%description ui
This package contains a user interface

%package lanserv
Summary: Emulates an IPMI network listener
Group: Utilities
Requires: OpenIPMI = %{version}

%description lanserv
This package contains a network IPMI listener.

###################################################
%prep
###################################################
%setup

###################################################
%build
###################################################
# USERFIX: Things you might have to add to configure:
#  --with-tclcflags='-I /usr/include/tclN.M' --with-tcllibs=-ltclN.M
#    Obviously, replace N.M with the version of tcl on your system.
%configure
make

###################################################
%install
###################################################
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/etc/sysconfig
install ipmi.init %{buildroot}/etc/init.d/ipmi
install ipmi.sysconf %{buildroot}/etc/sysconfig/ipmi

###################################################
%post
###################################################
chkconfig --add ipmi

###################################################
%preun
###################################################
if [ $1 = 0 ]; then
   /etc/init.d/ipmi stop >/dev/null 2>&1
   /sbin/chkconfig --del ipmi
fi

###################################################
%postun
###################################################
if [ "$1" -ge "1" ]; then
    /etc/init.d/ipmi condrestart >/dev/null 2>&1 || :
fi

###################################################
%files
###################################################
%defattr(-,root,root)
%{_libdir}/libOpenIPMIcmdlang.so.*
%{_libdir}/libOpenIPMIglib.so.*
# USERFIX: You might need to modify the following if glib12 is not
# handled properly by the autodetection
%if %{glib12} != "no"
  %{_libdir}/libOpenIPMIglib12.so.*
%endif
%{_libdir}/libOpenIPMItcl.so.*
%{_libdir}/libOpenIPMIposix.so.*
%{_libdir}/libOpenIPMIpthread.so.*
%{_libdir}/libOpenIPMI.so.*
%{_libdir}/libOpenIPMIutils.so.*
%doc COPYING COPYING.LIB FAQ INSTALL README README.Force
%doc README.MotorolaMXP CONFIGURING_FOR_LAN COPYING.BSD
/etc/init.d/ipmi
/etc/sysconfig/ipmi


###################################################
%files perl
###################################################
%defattr(-,root,root)
%{perl_vendorarch}
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

###################################################
%files python
###################################################
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*OpenIPMI.*
%doc swig/OpenIPMI.i

###################################################
%files gui
###################################################
%defattr(-,root,root)
%dir %{_libdir}/python*/site-packages/openipmigui
%{_libdir}/python*/site-packages/openipmigui/*
%{_bindir}/openipmigui

###################################################
%files devel
###################################################
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

###################################################
%files ui
###################################################
%defattr(-,root,root)
%{_bindir}/ipmi_ui
%{_bindir}/ipmicmd
%{_bindir}/openipmicmd
%{_bindir}/ipmish
%{_bindir}/openipmish
%{_bindir}/solterm
%{_bindir}/rmcp_ping
%{_libdir}/libOpenIPMIui.so.*
%doc %{_mandir}/man1/ipmi_ui.1*
%doc %{_mandir}/man1/openipmicmd.1*
%doc %{_mandir}/man1/openipmish.1*
%doc %{_mandir}/man1/openipmigui.1*
%doc %{_mandir}/man1/solterm.1*
%doc %{_mandir}/man1/rmcp_ping.1*
%doc %{_mandir}/man7/ipmi_cmdlang.7*
%doc %{_mandir}/man7/openipmi_conparms.7*

###################################################
%files lanserv
###################################################
%defattr(-,root,root)
%{_bindir}/ipmilan
%{_libdir}/libIPMIlanserv.so.*
%doc %{_mandir}/man8/ipmilan.8*

