Name:           ofono
Version:        1.15
Release:        0
License:        GPL-2.0
Summary:        Open Source Telephony
Url:            http://ofono.org
Group:          Telephony/Cellular
Source0:        %{name}-%{version}.tar.bz2
Source1012:     ofono.manifest
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(bluez) >= 4.85
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libudev) >= 145
BuildRequires:  pkgconfig(mobile-broadband-provider-info)
Requires:       dbus
Requires:       systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd


%description
Open Source Telephony stack.

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

cp %{SOURCE1012} .

%build
autoreconf --force --install

%configure --disable-static \
    --enable-test \
    --disable-bluez4 \
    --with-systemdunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system/network.target.wants
ln -s ../ofono.service %{buildroot}%{_prefix}/lib/systemd/system/network.target.wants/ofono.service

%install_service multi-user.target.wants ofono.service

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%config %{_sysconfdir}/dbus-1/system.d/*.conf
%{_sbindir}/*
%{_unitdir}/network.target.wants/ofono.service
%{_unitdir}/ofono.service
%{_unitdir}/multi-user.target.wants/ofono.service
%config %{_sysconfdir}/ofono/phonesim.conf

%files devel
%manifest %{name}.manifest
%{_includedir}/ofono/*.h
%{_libdir}/pkgconfig/ofono.pc

%files test
%manifest %{name}.manifest
%{_libdir}/%{name}/test/*

