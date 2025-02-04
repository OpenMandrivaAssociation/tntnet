# NOTE: when updating, make sure vdr-plugin-live still builds. -Anssi

%define major	10
%define libname	%mklibname tntnet %{major}
%define devname	%mklibname tntnet -d

Summary:	A web application server for web applications written in C++
Name:		tntnet
Version:	2.1
Release:	3
License:	LGPLv2.1+
Group:		System/Servers
URL:		https://www.tntnet.org/
Source0:	http://www.tntnet.org/download/%{name}-%{version}.tar.gz

BuildRequires:	zip
BuildRequires:	cxxtools-devel
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(zlib)

%description
Tntnet is a web application server for web applications written in C++.

You can write a Web-page with HTML and with special tags you embed
C++-code into the page for active contents. These pages, called
components are compiled into C++-classes with the ecpp-compilier
"ecppc", then compiled into objectcode and linked into a shared library.
This shared library is loaded by the webserver "tntnet" on request and
executed.

%package demos
Summary:	Demos for tntnet
Group:		System/Servers
Requires:	%{name} = %{version}

%description demos
Demo web applications for tntnet.

%package -n %{libname}
Summary:	Shared library of tntnet
Group:		System/Libraries

%description -n %{libname}
Tntnet library.

%package -n %{devname}
Summary:	Headers and static library for tntnet development
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	tntnet-devel = %{version}-%release

%description -n %{devname}
Headers and static library for tntnet development.

%prep
%setup -q

%build
autoreconf -fi
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config 

%multiarch_binaries %{buildroot}%{_bindir}/ecpp*

# TODO: patch to get compliant
rm -f %{buildroot}/etc/init.d/tntnet

%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/*.properties
%{_bindir}/tntnet
%dir %{_libdir}/tntnet
%{_libdir}/tntnet/tntnet.*
%{_mandir}/man7/ecpp.*
%{_mandir}/man7/tntnet.*
%{_mandir}/man8/tntnet.*

%files demos
%exclude %{_libdir}/tntnet/tntnet.*
%{_libdir}/tntnet/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc AUTHORS README TODO
%{_bindir}/%{name}-config
%{_bindir}/ecpp*
%{multiarch_bindir}/%{name}-config
%{multiarch_bindir}/ecpp*
%{_libdir}/*.so
%{_includedir}/tnt
%{_mandir}/man1/ecppc.*
%{_mandir}/man1/ecppl.*
%{_mandir}/man1/ecppll.*
%{_mandir}/man1/tntnet-config.*

