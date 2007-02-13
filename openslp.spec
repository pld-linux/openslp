Summary:	OpenSLP implementation of Service Location Protocol V2
Summary(de.UTF-8):	Open source Implementierung des Service Location Protocols V2
Summary(es.UTF-8):	Implementación open source del Service Location Protocol V2
Summary(fr.UTF-8):	Implémentation Open Source du Service Location Protocol V2
Summary(it.UTF-8):	Implementazione open source del Service Location Protocol V2
Summary(pl.UTF-8):	Otwarta implementacja Service Location Protocol V2
Summary(pt.UTF-8):	Implementação 'open source' do protocolo Service Location Protocol V2
Name:		openslp
# note: 1.3.0 is "development" release _equal_ to 1.2.0
Version:	1.2.1
Release:	2
License:	LGPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/openslp/%{name}-%{version}.tar.gz
# Source0-md5:	ff9999d1b44017281dd00ed2c4d32330
Source1:	%{name}.init
Patch0:		%{name}-opt.patch
URL:		http://www.openslp.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Obsoletes:	libopenslp1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/openslp

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as
defined by RFC 2608 and RFC 2614. This package includes libraries.

%description -l de.UTF-8
Das Service Location Protocol ist ein IETF standard Protokoll welches
ein Gerüst bereitstellt um es Netzwerk-fähigen Anwendungen zu
ermöglichen die Existenz, den Ort und die Konfiguration von
Netzwerkdiensten in Unternehmensnetzwerken zu entdecken.

%description -l es.UTF-8
El Protocolo de Localización de Servicios es un protocolo de
seguimiento acorde al estándar IETF que proporciona un entorno para
permitir a las aplicaciones de red descubrir la existencia,
localización y configuración de servicios de red en redes
empresariales.

%description -l fr.UTF-8
Service Location Protocol est un protocole de suivi des normes IETF
qui fournit un cadre permettant à des applications réseau de découvrir
l'existence, l'emplacement et la configuration de services de réseau
dans les réseaux d'entreprise.

%description -l it.UTF-8
Il Service Location Protocol (protocollo di localizzazione di servizi)
è un protocollo standard IETF che fornisce un'infrastruttura per
permettere alle applicazioni di rete di scoprire l'esistenza, la
localizzazione e la configurazione dei servizi nelle reti delle
aziende.

%description -l pl.UTF-8
Service Location Protocol jest zgodnym ze standardem IETF protokołem
pozwalającym aplikacjom sieciowym na badanie istnienia, położenia i
konfiguracji usług sieciowych.

OpenSLP jest otwartą implementacją protokołu SLPv2 zdefiniowanego w
RFC 2608 i RFC 2614. Ten pakiet zawiera biblioteki.

%description -l pt.UTF-8
O Service Location Protocol é um protocolo normalizado pelo IETF que
oferece uma plataforma para permitir às aplicações de rede que
descubram a existência, localização e a configuração dos serviços de
rede nas redes duma empresa.

%package server
Summary:	OpenSLP server working as SA and DA
Summary(pl.UTF-8):	Serwer OpenSLP działający jako SA i DA
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description server
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as
defined by RFC 2608 and RFC 2614. This package includes the daemon.

%description server -l pl.UTF-8
Service Location Protocol jest zgodnym ze standardem IETF protokołem
pozwalającym aplikacjom sieciowym na badanie istnienia, położenia i
konfiguracji usług sieciowych.

OpenSLP jest otwartą implementacją protokołu SLPv2 zdefiniowanego w
RFC 2608 i RFC 2614. Ten pakiet zawiera demona.

%package devel
Summary:	OpenSLP development files
Summary(pl.UTF-8):	Część OpenSLP dla programistów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel >= 0.9.7c
Obsoletes:	libopenslp1-devel

%description devel
OpenSLP development files.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenSLP.

%package static
Summary:	OpenSLP static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenSLP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OpenSLP static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenSLP.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
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

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add slpd
%service slpd restart "OpenSLP server"

%preun server
if [ "$1" = "0" ]; then
	%service slpd stop
	/sbin/chkconfig --del slpd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/slp.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/slp.reg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/slp.spi
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files server
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/slpd
%attr(755,root,root) %{_sbindir}/slpd

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
