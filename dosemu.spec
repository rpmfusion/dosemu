Name:		dosemu
Version:	1.4.0.8
Release:	24.20131022git%{?dist}
Summary:	DOS Emulator for Linux
URL:		http://dosemu.sf.net
License:	GPLv2+

# For a breakdown of the licensing, see COPYING.DOSEMU

#
# FreeDOS is included as a boot image.  Source code is available at: 
# http://www.freedos.org/freedos/source/
# 
# License info is explained here:
# http://apps.sourceforge.net/mediawiki/freedos/index.php?title=Main_Page#License

# Got latest revision from SVN:
#   svn co https://dosemu.svn.sourceforge.net/svnroot/dosemu/trunk dosemu-1.4.0
#   tar --exclude .svn -czvf dosemu-1.4.0.tgz dosemu-1.4.0

Source:		%{name}-%{version}.tgz

# Made a FreeDOS bootable image, must be done manually.

Source1:	%{name}-freedos-bin.tgz

Source2:	%{name}.desktop
Source3:	freedos-source.tar.gz
Group:		Applications/Emulators

Requires:	hicolor-icon-theme
BuildRequires:	bison 
BuildRequires:	flex
BuildRequires:	gcc
BuildRequires:	slang-devel
BuildRequires:	libX11-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	libsndfile
BuildRequires:	desktop-file-utils
BuildRequires:	xorg-x11-font-utils
BuildRequires:	git

# At this time, Dosemu only works with Linux on x86, other ports are welcome.
# ExclusiveArch: %{ix86} can also be used, but some build clients such as
# Plague, may build RPM's for every x86 arch.

ExclusiveOS:	linux
ExclusiveArch:	i686 x86_64


%description
DOSEMU is a PC Emulator that allows Linux to run a DOS operating system 
in a virtual x86 machine.  This allows you to run all kinds of different 
DOS programs including DPMI applications.  Enjoy running your DOS 
programs forever!


%prep
%autosetup


%build
%configure --with-fdtarball=%{SOURCE1}
%make_build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%make_install

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}

mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 0644 etc/dosemu.xpm %{buildroot}%{_datadir}/pixmaps

# Correct some file permissions 
chmod 755 %{buildroot}%{_datadir}/dosemu \
%{buildroot}%{_datadir}/dosemu/drive_z \
%{buildroot}%{_datadir}/dosemu/drive_z/doc/exe2bin
chmod +x %{buildroot}%{_libdir}/dosemu/libplugin*.so

# Move configuration files to /etc/dosemu to make it FHS compliant
mkdir -p %{buildroot}%{_sysconfdir}/dosemu/drives
mv -f %{buildroot}%{_sysconfdir}/{dosemu.conf,dosemu.users,global.conf} \
%{buildroot}%{_sysconfdir}/dosemu
mv -f %{buildroot}%{_sysconfdir}/drives/* \
%{buildroot}%{_sysconfdir}/dosemu/drives
ln -s /etc/dosemu/dosemu.conf %{buildroot}%{_sysconfdir}/dosemu.conf

sed -i -e '/Encoding=UTF-8/d' %{buildroot}%{_datadir}/applications/%{name}.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_mandir}/ru/man1/*.1*
%{_libdir}/dosemu
%{_datadir}/dosemu
%doc %{_docdir}/%{name}-%{version}
%config(noreplace) %{_sysconfdir}/dosemu.conf
%config(noreplace) %{_sysconfdir}/dosemu
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/dosemu.xpm


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-24.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-23.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4.0.8-22.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.0.8-21.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.0.8-20.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 Sérgio Basto <sergio@serjux.com> - 1.4.0.8-19.20131022git
- Clean spec, with Vascom, rfbz #4195

* Wed Dec 25 2013 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0.8-18.20131022git
- updated to the latest build, fixes many bugs
- Added a symlink for /etc/dosemu, other minor fixes

* Mon Feb 11 2013 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0.8-15.20130205git
- updated to the latest build, including improvements for easier package builds

* Sun Jun 24 2012 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0.6-14.20120623git
- updated to the latest build, and changed the release tag for GIT since svn is no longer used
- updated GNU license URL in freedos dosemu-freedos-bin.tgz

* Mon Oct 03 2011 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-12.2058svn
- updated the svn build to fix a problem with dosemu hanging on startup

* Thu Sep 01 2011 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-9.2053svn
- updated the svn build

* Tue Aug 10 2010 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-8.1999svn
- updated the svn build, added Arch x86_64

* Sat Oct 3 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-7.1981svn
- updated the svn build, and changed ExclusiveArch to i686

* Thu Aug 27 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-6.1905svn
- added ExclusiveOS and ExclusiveArch to build for i386 only.

* Wed Aug 26 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-5.1905svn
- tested some new builds

* Tue Aug 25 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-4.1905svn
- added an extra BR and {?dist} to the spec file

* Sun Aug 02 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-3.1905svn
- used the latest SVN 1905 release

* Sun Mar 22 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-2.1868svn
- fixed some minor problems with the spec file

* Wed Jul 23 2008 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-1.1868svn
- Initial RPM release.

