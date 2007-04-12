%define name	cuiterm
%define version	0.9.8
%define release %mkrel 2

Name: 	 	%{name}
Summary: 	Composite user interface terminal
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
URL:		http://linux.pte.hu/~pipas/CUI/
License:	GPL
Group:		Terminals
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	bison flex
BuildRequires:	libgnome2-devel libgnome-vfs2-devel
Requires(post): scrollkeeper
Requires(postun):scrollkeeper

%description
CUI (Composite User Interface) is a compound type of user interface which
incorporates the features of the GUI (Graphical User Interface) and the CLI
(Command Line Interface) by realizing both interface in one area at the same
time.

An other relevant feature of the CUI method is that it uses generated
commands. When the user activated some GUI part of the user interface an
automatically generated command appears to complete the task so the user
can observ how the CLI part of the user interface can be used.

The cuiterm is a pilot application for the CUI methodology made to
demonstrate the power of the composite user interfaces. As terminals are
usually used with some shell to start simple UNIX utility programs, the
CUI library can be considered as a composite user interface for the shell
and some UNIX utilities.

%prep
%setup -q

%build
%configure2_5x --disable-gtk-doc
perl -pi -e 's|/usr/share/pixmaps|%{buildroot}/%{_datadir}/pixmaps||g' Makefile
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -fr %buildroot/var

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="CUI Term" longtitle="Composite user interface" section="System/Terminals" xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=CUI Term
Comment=Composite user interface
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
Categories=GNOME;GTK;X-MandrivaLinux-System-Terminals;TerminalEmulator;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 pixmaps/tux.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 pixmaps/tux.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 pixmaps/tux.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
%update_scrollkeeper
		
%postun
%clean_menus
%clean_scrollkeeper

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README NEWS TODO
%{_bindir}/%name
%{_datadir}/pixmaps/%name
%{_datadir}/gnome/help/%name
%{_datadir}/gtk-doc/html/%name
%{_datadir}/omf/%name
%{_menudir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
