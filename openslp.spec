Summary:	OpenSLP implementation of Service Location Protocol V2
Name:		openslp
Version:	1.0.1
Release:	1
License:	LGPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://prdownloads.sourceforge.net/openslp/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-ac25x.patch
URL:		http://www.openslp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Prereq:		rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/openslp

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as
defined by RFC 2608 and RFC 2614. This package include the daemon,
libraries, header files and documentation

%package devel
Summary:	OpenSLP develpment files
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}

%description devel
OpenSLP develpment files.

%package static
Summary:	OpenSLP staic libraries
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name}-devel = %{version}

%description static
OpenSLP staic libraries.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c
%configure \
	--enable-slpv1 \
	--enable-slpv2-security \
	--disable-predicates

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/slpd

gzip -9nf AUTHORS NEWS README doc/rfc/*txt

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
%dir %{_sysconfdir}
%config %{_sysconfdir}/slp.conf
%config %{_sysconfdir}/slp.reg
%config %{_sysconfdir}/slp.spi
%attr(754,root,root) /etc/rc.d/init.d/slpd
%attr(755,root,root) %{_sbindir}/slpd
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc *.gz doc/*
%{_includedir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
