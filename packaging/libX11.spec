%define tarball libX11
#define gitdate 20090805

Summary: Core X11 protocol client library
Name: libX11
Version: 1.6.2
Release: 0
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: %{name}-%{version}.tar.gz
Source1001: 	libX11.manifest
BuildRequires:  pkgconfig(xcmiscproto)
BuildRequires:  pkgconfig(bigreqsproto)
BuildRequires:  pkgconfig(kbproto)
BuildRequires:  pkgconfig(inputproto)
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xextproto)
BuildRequires: pkgconfig(xproto) >= 7.0.15
BuildRequires: xorg-x11-xtrans-devel >= 1.0.3-4
BuildRequires: libxcb-devel >= 1.2

Requires: %{name}-common = %{version}-%{release}
Provides: libx11

%description
Core X11 protocol client library.

%package common
Summary: Common data for libX11
Group: System Environment/Libraries
BuildArch: noarch

%description common
libX11 common data

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libx11-devel

%description devel
X.Org X11 libX11 development package

%prep
%setup -q
cp %{SOURCE1001} .

%build
# sodding libtool
%if "%{?tizen_profile_name}" == "tv"
%reconfigure --disable-static \
           CFLAGS="${CFLAGS} -D_F_REDUCE_SYSCALL -D_FIX_MEM_LEAK_ -D_F_XDEFAULT_ERR_LOG_ON_SERIAL_ -D_F_BLOCK_XINITTHREAD_BEFORE_XOPEN_ -D_F_FIX_XIOERROR_" \
           LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed -lpthread"
%else
%reconfigure --disable-static \
           CFLAGS="${CFLAGS} -D_F_REDUCE_SYSCALL -D_FIX_MEM_LEAK_" \
           LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"
%endif

make %{?jobs:-j%jobs}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
cp -af COPYING %{buildroot}/usr/share/license/%{name}-common
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
find $RPM_BUILD_ROOT -type f -name '*.la' -delete

# FIXME: Don't install Xcms.txt - find out why upstream still ships this.
find $RPM_BUILD_ROOT -name 'Xcms.txt' -delete

# FIXME package these properly
rm -rf $RPM_BUILD_ROOT%{_docdir}

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.3.0
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0

%files common
%manifest %{name}.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}-common
#%doc AUTHORS COPYING README NEWS
%{_datadir}/X11/locale/*
%{_datadir}/X11/XErrorDB

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/XKBlib.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib-xcb.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/cursorfont.h
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
#%{_mandir}/man3/*.3*
#%{_mandir}/man5/*.5*
