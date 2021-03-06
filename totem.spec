Summary:	Movie player for GNOME
Name:		totem
Version:	3.14.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Multimedia
Source0:	http://ftp.gnome.org/pub/gnome/sources/totem/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	c794736ef65fde6c781ae4ba7f850849
Patch0:		%{name}-mercyful.patch
URL:		http://www.gnome.org/projects/totem/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	clutter-gst-devel
BuildRequires:	clutter-gtk-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	adwaita-icon-theme-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gstreamer-plugins-base-devel >= 1.2.4
BuildRequires:	intltool
BuildRequires:	iso-codes
BuildRequires:	libgdata-devel
BuildRequires:	libpeas-gtk-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	totem-pl-parser-devel >= 3.10.0
BuildRequires:	tracker-devel
BuildRequires:	xorg-libXv-devel
BuildRequires:	xorg-libXxf86vm-devel
BuildRequires:	xorg-proto
BuildRequires:  libtool
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gstreamer-clutter
Requires:	gstreamer-libav
Requires:	gstreamer-plugins-bad
Requires:	gstreamer-plugins-base >= 1.2.4
Requires:	gstreamer-plugins-good
Requires:	gstreamer-plugins-ugly
Obsoletes:	browser-plugin-totem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Totem is simple movie player for the GNOME desktopr.
It features a simple playlist, a full-screen mode, seek and volume
controls, as well as a pretty complete keyboard navigation.

%package libs
Summary:	Totem libraries
Group:		X11/Libraries

%description libs
This package contains Totem libraries.

%package devel
Summary:	Header files for totem
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the files necessary to develop applications
using Totem's libraries.

%package apidocs
Summary:	Totem API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Totem API documentation.

%package plugins
Summary:	Totem plugins
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-modules
Requires:	python-pygtk

%description plugins
Totem plugins.

%package -n nautilus-extension-totem
Summary:	Totem extension for Nautilus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus

%description -n nautilus-extension-totem
Shows video properties and generates thumbnails in Nautilus.

%prep
%setup -q
%patch0 -p1

# kill gnome common deps
%{__sed} -i -e '/GNOME_COMPILE_WARNINGS.*/d'	\
    -i -e '/GNOME_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/GNOME_COMMON_INIT/d'		\
    -i -e '/GNOME_DEBUG_CHECK/d' 		\
    -i -e '/GNOME_CXX_WARNINGS/d' 		\
    -i -e 's/codegen.py/codegen.pyc/g' configure.ac

%{__sed} -i -e '/APPDATA_XML/d' data/appdata/Makefile.am

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I libgd
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static		\
	--disable-vala			\
	--enable-nautilus		\
	--with-html-dir=%{_gtkdocdir}

%{__make} -j1 -C help
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-3.0/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/totem/plugins/*/*.{la,py}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf

%py_comp $RPM_BUILD_ROOT%{_libdir}/totem
%py_ocomp $RPM_BUILD_ROOT%{_libdir}/totem

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_gsettings_cache

%post   libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/totem
%attr(755,root,root) %{_bindir}/totem-audio-preview

%dir %{_libexecdir}
%dir %{_libdir}/totem/plugins
%dir %{_libdir}/totem/plugins/properties
%attr(755,root,root) %{_libdir}/totem/plugins/properties/*.so
%{_libdir}/totem/plugins/properties/*.plugin

%{_datadir}/dbus-1/services/org.gnome.Totem.service
%{_datadir}/glib-2.0/schemas/org.gnome.totem.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.totem.gschema.xml

%{_datadir}/thumbnailers/totem.thumbnailer

%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/*.*
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libtotem.so.?
%attr(755,root,root) %{_libdir}/libtotem.so.*.*.*
%{_libdir}/girepository-1.0/Totem-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtotem.so
%{_includedir}/totem
%{_pkgconfigdir}/totem.pc
%{_datadir}/gir-1.0/Totem-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/totem

%files plugins
%defattr(644,root,root,755)
%dir %{_libdir}/totem/plugins/apple-trailers
%dir %{_libdir}/totem/plugins/autoload-subtitles
%dir %{_libdir}/totem/plugins/brasero-disc-recorder
%dir %{_libdir}/totem/plugins/chapters
%dir %{_libdir}/totem/plugins/dbus
%dir %{_libdir}/totem/plugins/gromit
%dir %{_libdir}/totem/plugins/im-status
%dir %{_libdir}/totem/plugins/media-player-keys
%dir %{_libdir}/totem/plugins/ontop
%dir %{_libdir}/totem/plugins/opensubtitles
%dir %{_libdir}/totem/plugins/pythonconsole
%dir %{_libdir}/totem/plugins/recent
%dir %{_libdir}/totem/plugins/save-file
%dir %{_libdir}/totem/plugins/screensaver
%dir %{_libdir}/totem/plugins/screenshot
%dir %{_libdir}/totem/plugins/skipto
%dir %{_libdir}/totem/plugins/vimeo

%{_datadir}/glib-2.0/schemas/org.gnome.totem.plugins.opensubtitles.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.totem.plugins.pythonconsole.gschema.xml

%attr(755,root,root) %{_libdir}/totem/plugins/*/*.so
%{_libdir}/totem/plugins/*/*.plugin
%{_libdir}/totem/plugins/*/*.ui
%{_libdir}/totem/plugins/*/*.py[oc]

%exclude %{_libexecdir}/plugins/properties/*.plugin
%exclude %{_libexecdir}/plugins/properties/*.so

%files -n nautilus-extension-totem
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/totem-video-thumbnailer
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/*.so

