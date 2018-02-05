AutoReqProv: no

%global currenf 59.0a1
%global _optdir /opt
%ifarch x86_64
%global arch x86_64
%else
%global arch i686
%endif

%define buildid %(curl https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.en-US.linux-%{arch}_info.txt 2>/dev/null | awk -F'=' '/buildID=/{ print $2 }')

Summary:  Standalone web browser from mozilla.org, nightly build
Name: firefox-nightly
Version: 60
Release: 0a1.%{buildid}%{?dist}
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Applications/Internet
URL: http://www.mozilla.org/projects/firefox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: wget tar

Requires: alsa-lib libX11 libXcomposite libXdamage libnotify libXt libXext glib2 dbus-glib libjpeg-turbo cairo-gobject libffi fontconfig freetype libgcc gtk3 gtk2 hunspell zlib
Requires: nspr >= 4.10.8
Requires: nss >= 3.19.2
Requires: sqlite >= 3.8.10.2

%description
Mozilla Firefox is an open-source web browser, designed for standards 
compliance, performance and portability.

%prep


%build
wget -c --no-check-certificate -P %{_builddir} https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.en-US.linux-%{arch}.tar.bz2 &>/dev/null
tar -jxvf firefox-%{currenf}.en-US.linux-*.tar.bz2  -C %{_builddir}

%install

install -dm 755 %{buildroot}/{usr/{bin,share/{applications,pixmaps}},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-%{version}/browser/defaults/preferences/

install -m644 %{_builddir}/firefox/browser/chrome/icons/default/default128.png %{buildroot}/usr/share/pixmaps/%{name}-icon.png
cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-%{version}/
ln -s /opt/firefox-%{version}/firefox %{buildroot}/usr/bin/firefox-nightly


cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Firefox Nightly
GenericName=Web Browser
Icon=/usr/share/pixmaps/firefox-nightly-icon.png
Type=Application
Categories=Application;Network;
MimeType=text/html
Encoding=UTF-8
Exec=firefox-nightly %u
Terminal=false
MultipleArgs=false
StartupNotify=false
EOF

cat > %{buildroot}/%{_datadir}/applications/%{name}-safe.desktop << EOF
[Desktop Entry]
Name=Firefox Nightly - Safe Mode
GenericName=Web Browser - Safe Mode
Icon=/usr/share/pixmaps/firefox-nightly-icon.png
Type=Application
Categories=Application;Network;
MimeType=text/html
Encoding=UTF-8
Exec=firefox-nightly -safe-mode %u
Terminal=false
MultipleArgs=false
StartupNotify=false
EOF

# disable update check
echo '// Disable update check
pref("app.update.enabled", false);' > %{buildroot}/opt/firefox-%{version}/browser/defaults/preferences/vendor.js

%clean
rm -rf $RPM_BUILD_ROOT


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}-icon.png
%{_optdir}/firefox-%{version}/

%changelog
* Mon Feb 05 2018 Maciej Sitarz <macieksitarz@wp.pl> 60-0a1.20180122100120
- Updated to 60.0a1

* Fri Dec 01 2017 Maciej Sitarz <macieksitarz@wp.pl> 59-0a1.20171201100115
- Fix icons copying during build 

* Thu Nov 16 2017 Maciej Sitarz <macieksitarz@wp.pl> 59-0a1.20171116100106
- Updated to 59.0a1 

* Sun Aug 20 2017 Maciej Sitarz <macieksitarz@wp.pl> 57-0a1.20170820100343
- Updated to 57.0a1

* Mon May 22 2017 Maciej Sitarz 55-0a1.20170522100359
- Redirect stderr of curl/wget to /dev/null

* Mon May 22 2017 Maciej Sitarz <maciej.sitarz@wp.pl> 55-0a1.20170522100359
- firefox-nightly updated to 55.0a1

* Thu Oct 20 2016 Maciej Sitarz <macieksitarz@wp.pl>
- firefox-nightly updated to 52.0a1 (macieksitarz@wp.pl)

* Fri Aug 05 2016 Maciej Sitarz <macieksitarz@wp.pl> 51-0a1
- Added dynamic version detection (macieksitarz@wp.pl)

* Thu Aug 4 2016  <macieksitarz AT wp DOT pl> - 51.0a1-1
- Updated to 51.0a1

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 48.0a1-1
- Updated to 48.0a1

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 43-0a1
- Initial build
