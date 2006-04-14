Summary:	Network library, for network administrators and network hackers
Summary(pl):	Biblioteka sieciowa dla administrator�w i hacker�w
Name:		netwib
Version:	5.34.0
Release:	1
Epoch:		0
License:	LGPL
Group:		Libraries
Source0:	http://www.laurentconstantin.com/common/netw/netwib/download/v5/%{name}-%{version}-src.tgz
# Source0-md5:	d0e483fb92c5a2c9c5e5be207e8c3a7c
URL:		http://www.laurentconstantin.com/en/netw/netwib/
Patch0:		%{name}-config.patch
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
Netwib to biblioteka sieciowa przeznaczona dla administrator�w sieci i
sieciowych hacker�w. Zapewnia:
 - funkcjonalno�� zwi�zan� z sieci�:
   - konwersj� adres�w
   - obs�ug� klient�w/serwer�w udp/tcp
   - kodowanie/dekodowanie/wy�wietlanie pakiet�w
   - spoofowanie
   - sniffowanie
   - itp.
 - oraz og�ln� funkcjonalno��:
   - konwersj� danych
   - listy i hashe
   - przeno�ne w�tki
   - itp.
Przy u�yciu tych wszystkich funkcji mo�na szybko tworzy� oprogramowanie
sieciowe.

%package devel
Summary:	Header files and development documentation for netwib
Summary(pl):	Pliki nag��wkowe i dokumentacja programisty dla netwib
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Header files and development documentation for netwib.

%description devel -l pl
Pliki nag��wkowe i dokumentacja programisty dla netwib.

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
%patch0 -p1

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man3}

%{__make} -C src installall \
	INSTINCLUDE=$RPM_BUILD_ROOT%{_includedir} \
	INSTLIB=$RPM_BUILD_ROOT%{_libdir} \
	INSTBIN=$RPM_BUILD_ROOT%{_bindir} \
	INSTMAN3=$RPM_BUILD_ROOT%{_mandir}/man3 \
	INSTUSERGROUP="$(id -u):$(id -g)"

rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib.3
echo ".so netwib533.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_dat.3
echo ".so netwib533_dat.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_dat.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_err.3
echo ".so netwib533_err.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_err.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_net.3
echo ".so netwib533_net.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_net.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_pkt.3
echo ".so netwib533_pkt.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_pkt.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_shw.3
echo ".so netwib533_shw.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_shw.3
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/netwib_sys.3
echo ".so netwib533_sys.3" > $RPM_BUILD_ROOT%{_mandir}/man3/netwib_sys.3


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
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
