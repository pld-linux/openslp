Summary:	OpenSLP implementation of Service Location Protocol V2
Name:		openslp
Version:	0.9.0
Release:	1
License:	LGPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}.tar.gz
Source1:	%{name}.sysconfig
URL:		http://www.openslp.org/
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%defin		_sysconfdir		/etc/openslp

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as
defined by RFC 2608 and RFC 2614. This package include the daemon,
libraries, header files and documentation

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install etc/slpd.all_init $RPM_BUILD_ROOT/etc/rc.d/init.d/slpd

gzip -9nf AUTHORS NEWS README doc/rfc/*

%post
/sbin/ldconfig
/sbin/chkconfig --add slpd

if [ -r /var/lock/subsys/slpd ]; then
	/etc/rc.d/init.d/slpd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/slpd start\" to start OpenSLP server."
fi


%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/slpd ]; then
		/etc/rc.d/init.d/slpd stop
	fi
	/sbin/chkconfig --del slpd
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz doc/*
%dir %{_sysconfdir}
%config %{_sysconfdir}/slp.conf
%config %{_sysconfdir}/slp.reg
/etc/rc.d/init.d/slpd
%{_libdir}/libslp*
%{_includedir}/slp.h
%attr(755,root,root) %{_sbindir}/slpd
