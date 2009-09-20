
%define name	tntnet
%define version	1.6.3
%define rel	2

%define major	8
%define libname	%mklibname tntnet %major
%define devname	%mklibname tntnet -d

Summary:	A web application server for web applications written in C++
Name:		%name
Version:	%version
Release:	%mkrel %rel
License:	LGPLv2.1+
Group:		System/Servers
URL:		http://www.tntnet.org/
Source:		http://www.tntnet.org/download/%name-%version.tar.gz
Patch0:		tntnet-underlinking.patch
Patch1:		tntnet-includes.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	cxxtools-devel
BuildRequires:	gnutls-devel
BuildRequires:	zlib-devel
BuildRequires:	zip

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

%package -n %libname
Summary:	Shared library of tntnet
Group:		System/Libraries

%description -n %libname
Tntnet library.

%package -n %devname
Summary:	Headers and static library for tntnet development
Group:		Development/C++
Requires:	%libname = %version
Provides:	tntnet-devel = %version-%release

%description -n %devname
Headers and static library for tntnet development.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
autoreconf -fi
%configure2_5x --disable-static
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config %{buildroot}%{_bindir}/ecpp*

# TODO: patch to get compliant
rm -f %{buildroot}/etc/init.d/tntnet

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

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

%files -n %libname
%{_libdir}/*.so.%{major}*

%files -n %devname
%doc AUTHORS README TODO
%{_bindir}/%{name}-config
%{_bindir}/ecpp*
%{multiarch_bindir}/%{name}-config
%{multiarch_bindir}/ecpp*
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/tnt
%{_mandir}/man1/ecppc.*
%{_mandir}/man1/ecppl.*
%{_mandir}/man1/ecppll.*
%{_mandir}/man1/tntnet-config.*
