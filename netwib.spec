Summary:	Network library, for network administrators and network hackers
Summary(pl):	Biblioteka sieciowa dla administratorów i hackerów
Name:		netwib
Version:	5.12.0
Release:	1
Epoch:		0
License:	LGPL
Group:		Libraries
Source0:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-src.tgz
# Source0-md5:	fbc54d0bf68ad92974e31c650345e862
URL:		http://www.laurentconstantin.com/en/netw/netwib/
BuildRequires:	libnet-devel >= 1.0
BuildRequires:	libpcap-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Netwib is a network library, for network administrators and network
hackers. It provides :
  - network functionalities :
    + address conversion
    + udp/tcp clients/servers
    + packet encoding/decoding/displaying
    + spoofing
    + sniffing
    + etc.
  - and general functionalities :
    + data conversion
    + linked list, hash
    + portable threads
    + etc.
Using all these functions, a network program can be quickly created.

%description -l pl
Netwib to biblioteka sieciowa przeznaczona dla administratorów sieci i
sieciowych hackerów. Zapewnia:
 - funkcjonalno¶æ zwi±zan± z sieci±:
   - konwersjê adresów
   - obs³ugê klientów/serwerów udp/tcp
   - kodowanie/dekodowanie/wy¶wietlanie pakietów
   - spoofowanie
   - sniffowanie
   - itp.
 - oraz ogóln± funkcjonalno¶æ:
   - konwersjê danych
   - listy i hashe
   - przeno¶ne w±tki
   - itp.
Przy u¿yciu tych wszystkich funkcji mo¿na szybko tworzyæ oprogramowanie
sieciowe.

%package devel
Summary:	Header files and development documentation for netwib
Summary(pl):	Pliki nag³ówkowe i dokumentacja programisty dla netwib
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Header files and development documentation for netwib.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty dla netwib.

%package static
Summary:	Static netwib library
Summary(pl):	Statyczna biblioteka netwib
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static netwib library.

%description static -l pl
Statyczna biblioteka netwib.

%prep
%setup -q -n %{name}-%{version}-src

%build
cd src
%define         base_arch %(echo %{_target_cpu} | sed 's/i.86/i386/;s/athlon/i386/;s/ppc/powerpc/')
sed -i -e 's#NETWIBDEF_SYSARCH=i386#NETWIBDEF_SYSARCH=%{base_arch}#g' config.dat
sed -i -e 's#/bin/ip#/sbin/ip#g' netwib/net/priv/conf/conflinux.c
./genemake
sed -i -e 's#444#644#' -e 's#555#755#g' Makefile
%{__make} libnetwib.so libnetwib.a \
	CC="%{__cc}" \
	GCCOPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man{1,3}}

cd src
%{__make} installall \
	INSTINCLUDE=$RPM_BUILD_ROOT%{_includedir} \
	INSTLIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTBIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTMAN1=$RPM_BUILD_ROOT%{_mandir}/man1 \
	INSTMAN3=$RPM_BUILD_ROOT%{_mandir}/man3 \
	INSTUSERGROUP="$(id -u):$(id -g)"

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.txt
%attr(755,root,root) %{_libdir}/lib*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%{_mandir}/man?/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
