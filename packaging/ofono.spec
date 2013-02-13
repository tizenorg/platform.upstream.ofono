Name:           ofono
Version:        1.12
Release:        0
License:        GPL-2.0
Summary:        Open Source Telephony
Url:            http://ofono.org
Group:          Telephony/Cellular
Source0:        %{name}-%{version}.tar.bz2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(bluez) >= 4.85
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libudev) >= 145
BuildRequires:  pkgconfig(mobile-broadband-provider-info)
Requires:       dbus

%description
Oprn Source Telephony stack.

%package devel
Summary:        Headers for oFono
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Development headers and libraries for oFono

%package test
Summary:        Test Scripts for oFono
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       dbus-python
Requires:       python-gobject
Requires:       python-xml

%description test
Scripts for testing oFono and its functionality

%prep
%setup -q

%build
autoreconf --force --install

%configure --disable-static \
    --enable-test \
    --with-systemdunitdir="/usr/lib/systemd/system"

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/network.target.wants
ln -s ../ofono.service %{buildroot}%{_prefix}/lib/systemd/system/network.target.wants/ofono.service

%docs_package

%files
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*.conf
%{_sbindir}/*
%{_prefix}/lib/systemd/system/network.target.wants/ofono.service
%{_prefix}/lib/systemd/system/ofono.service
%config %{_sysconfdir}/ofono/phonesim.conf

%files devel
%{_includedir}/ofono/*.h
%{_libdir}/pkgconfig/ofono.pc

%files test
%{_libdir}/%{name}/test/*

