Name:		dosemu
Version:	1.4.0.6
Release:	14.20120623git%{?dist}
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
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	hicolor-icon-theme
BuildRequires:	bison 
BuildRequires:	flex
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
%setup -q


%build
%configure --with-fdtarball=%{SOURCE1}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make DESTDIR=$RPM_BUILD_ROOT install

desktop-file-install \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
  %{SOURCE2}

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
install -p -m 0644 etc/dosemu.xpm ${RPM_BUILD_ROOT}%{_datadir}/pixmaps

# Correct some file permissions 
chmod 755 $RPM_BUILD_ROOT%{_datadir}/dosemu \
$RPM_BUILD_ROOT%{_datadir}/dosemu/drive_z \
$RPM_BUILD_ROOT%{_datadir}/dosemu/drive_z/doc/exe2bin
chmod +x $RPM_BUILD_ROOT%{_libdir}/dosemu/libplugin*.so

# Move configuration files to /etc/dosemu to make it FHS compliant
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dosemu/drives
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/{dosemu.conf,dosemu.users,global.conf} \
$RPM_BUILD_ROOT%{_sysconfdir}/dosemu
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/drives/* \
$RPM_BUILD_ROOT%{_sysconfdir}/dosemu/drives


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/dosemu.bin
%{_bindir}/dosemu
%{_bindir}/mkfatimage
%{_bindir}/mkfatimage16
%{_bindir}/midid
%{_bindir}/dosdebug
%{_bindir}/xdosemu
%{_mandir}/man1/mkfatimage16.1*
%{_mandir}/man1/midid.1*
%{_mandir}/man1/dosdebug.1*
%{_mandir}/man1/dosemu.1*
%{_mandir}/man1/dosemu.bin.1*
%{_mandir}/man1/xdosemu.1*
%{_mandir}/ru/man1/mkfatimage16.1*
%{_mandir}/ru/man1/dosdebug.1*
%{_mandir}/ru/man1/dosemu.1*
%{_mandir}/ru/man1/dosemu.bin.1*
%{_mandir}/ru/man1/xdosemu.1*
%dir %{_libdir}/dosemu
%{_libdir}/dosemu/libplugin*.so
%dir %{_datadir}/dosemu
%{_datadir}/dosemu/commands
%{_datadir}/dosemu/freedos
%{_datadir}/dosemu/drive_z
%{_datadir}/dosemu/keymap
%{_datadir}/dosemu/Xfonts
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/announce
%doc %{_docdir}/%{name}-%{version}/BUGS
%doc %{_docdir}/%{name}-%{version}/ChangeLog
%doc %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/COPYING.DOSEMU
%doc %{_docdir}/%{name}-%{version}/DANG.txt
%doc %{_docdir}/%{name}-%{version}/dosemu-HOWTO.txt
%doc %{_docdir}/%{name}-%{version}/EMUfailure.txt
%doc %{_docdir}/%{name}-%{version}/NOVELL-HOWTO.txt
%doc %{_docdir}/%{name}-%{version}/NEWS
%doc %{_docdir}/%{name}-%{version}/README.bindist
%doc %{_docdir}/%{name}-%{version}/README.txt
%doc %{_docdir}/%{name}-%{version}/README-tech.txt
%doc %{_docdir}/%{name}-%{version}/README.gdb
%doc %{_docdir}/%{name}-%{version}/sound-usage.txt
%doc %{_docdir}/%{name}-%{version}/THANKS
%dir %{_sysconfdir}/dosemu
%dir %{_sysconfdir}/dosemu/drives
%config(noreplace) %{_sysconfdir}/dosemu/dosemu.conf
%config(noreplace) %{_sysconfdir}/dosemu/drives/c
%config(noreplace) %{_sysconfdir}/dosemu/drives/d
%config(noreplace) %{_sysconfdir}/dosemu/dosemu.users
%config(noreplace) %{_sysconfdir}/dosemu/global.conf
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/dosemu.xpm


%changelog

* Mon Jun 16 2012 Justin Zygmont <solarflow99[AT]gmail.com>
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

* Sun Oct 3 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-7.1981svn
- updated the svn build, and changed ExclusiveArch to i686

* Tue Aug 28 2009 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-6.1905svn
- added ExclusiveOS and ExclusiveArch to build for i386 only.

* Tue Aug 27 2009 Justin Zygmont <solarflow99[AT]gmail.com>
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

* Fri Jul 23 2008 Justin Zygmont <solarflow99[AT]gmail.com>
- 1.4.0-1.1868svn
- Initial RPM release.

