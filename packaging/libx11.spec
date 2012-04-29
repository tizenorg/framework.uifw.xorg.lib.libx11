Name:       libx11
Summary:    X11 runtime library
Version:    1.4.0
Release:    1.6
Group:      System/Libraries
License:    MIT
URL:        http://www.x.org/
Source0:    http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz
Patch1:     003_recognize_glibc_2.3.2_locale_names.diff
Patch2:     006_tailor_pt_BR.UTF-8_Compose.diff
Patch3:     007_iso8859-15_Compose_fix.diff
Patch4:     008_remove_ko_Compose.diff
Patch5:     009_remove_th_Compose.diff
Patch6:     015_russian_locale_alias.diff
Patch7:     100_latin_locale_alias.diff
Patch8:     101_klingon_locale_alias.diff
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xproto)
BuildRequires:  pkgconfig(xextproto)
BuildRequires:  pkgconfig(xtrans)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xcmiscproto)
BuildRequires:  pkgconfig(bigreqsproto)
BuildRequires:  pkgconfig(kbproto)
BuildRequires:  pkgconfig(inputproto)

%description
Description: %{summary}


%package devel
Summary:    X.Org X11 libX11 development package
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Description: %{summary}


%prep
%setup -q -n %{name}-%{version}

# 003_recognize_glibc_2.3.2_locale_names.diff
%patch1 -p1

# 006_tailor_pt_BR.UTF-8_Compose.diff
%patch2 -p1

# 007_iso8859-15_Compose_fix.diff
%patch3 -p1

# 008_remove_ko_Compose.diff
%patch4 -p1

# 009_remove_th_Compose.diff
%patch5 -p1

# 015_russian_locale_alias.diff
%patch6 -p1

# patches/100_latin_locale_alias.diff
%patch7 -p1

# patches/101_klingon_locale_alias.diff
%patch8 -p1




%build

%reconfigure --enable-specs \
	--enable-man-pages=3 \
	--with-xcb=yes \
	CFLAGS="-D_F_ENABLE_XI2_SENDEVENT_" \
	LDFLAGS="-Wl,--hash-style=both -Wl,--as-needed"

# Call make instruction with smp support
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install




%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig



%files
%dir %{_datadir}/X11
%{_datadir}/X11/locale/*
%{_datadir}/X11/XErrorDB
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.3.0
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0


%files devel
%dir %{_includedir}/X11
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
%{_libdir}/X11/Xcms.txt
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc

