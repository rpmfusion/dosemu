Name:		dosemu
Version:	1.4.0.8
Release:	37.20131022git%{?dist}
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

# https://bugzilla.redhat.com/show_bug.cgi?id=1866474
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=5663
# memory.h: don't mark pointer to be modified as const
Patch0:    0001-memory.h-don-t-mark-pointer-to-be-modified-as-const.patch

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
BuildRequires:	%{_bindir}/bdftopcf
BuildRequires:	%{_bindir}/mkfontdir
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
%autosetup -p1

# lto doesn't seem to work:
# DEBUG: /usr/bin/ld: /tmp/dosemu.bin.1hmolM.ltrans0.ltrans.o: in function `stub_rep__':
# DEBUG: <artificial>:(.text+0xe): undefined reference to `rep_movs_stos'
%define _lto_cflags %{nil}
#gcc -Wl,-warn-common -Wl,-z,relro -Wl,--as-needed  -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1  -Wl,--build-id=sha1 -Wl,-dT,/builddir/build/BUILD/dosemu-1.4.0.8/.package_note-dosemu-1.4.0.8-32.20131022git.fc37.x86_64.ld -Wl,-Ttext,0,-e,_start16,--oformat,binary -nostdlib -s -o ../../1.4.0.8/commands/emufs.sys emufs.o
#/usr/bin/ld: section .note.gnu.property LMA [0000000000000000,000000000000002f] overlaps section .text LMA [0000000000000000,0000000000000293]
#collect2: error: ld returned 1 exit status
#make[2]: *** [Makefile:57: ../../1.4.0.8/commands/emufs.sys] Error 1
# https://www.mail-archive.com/grub-devel@gnu.org/msg32447.html
# With binutils 2.36
%undefine _hardened_build

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
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-37.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 01 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-36.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-35.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-34.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-33.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Apr 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0.8-32.20131022git
- Update BR for xorg-x11-font-utils split
- Undefined _hardened_build for now for binutils 2.36

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.0.8-31.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-30.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-29.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 23 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0.8-28.20131022git
- Don't mark pointers to be modified as const (bug 5663)
- Disable lto for now

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-27.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-26.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0.8-25.20131022git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

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

