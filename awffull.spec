Summary:	A Webalizer Fork, Full o' Features!
Name:		awffull
Version:	3.10.2
Release:	9
License:	GPLv3+
Group:		Monitoring
URL:		http://www.stedee.id.au/awffull
# md5sum: 80acf755b354c49d78a5b9bb580196f2
Source0:	http://www.stedee.id.au/files/%{name}-%{version}.tar.gz
Source1:	http://flags.blogpotato.de/zip/large/world.zip
Source2:	http://flags.blogpotato.de/zip/large/special.zip
Source3:	awffull.cron.daily
Source4:	Vera.ttf
Source5:	VeraBd.ttf
Patch0:		awffull-mdv_conf.diff
Patch1:		awffull-3.10.2-upstreambug309617.diff
Requires:	apache
Requires:	geoip
# webapp macros and scriptlets
Requires(post): rpm-helper >= 0.16
Requires(postun): rpm-helper >= 0.16
BuildRequires:	rpm-helper >= 0.16
BuildRequires:	apache-base >= 2.0.54
BuildRequires:	jpeg-devel
BuildRequires:	freetype2-devel
BuildRequires:	png-devel
BuildRequires:	gd-devel
BuildRequires:	pcre-devel
BuildRequires:	libgeoip-devel
BuildRequires:	zlib-devel
BuildRequires:	gettext-devel
BuildRequires:	unzip

%description
Webalizer is a great weblog analysis program but hasn't been going anywhere in
recent years. AWFFull takes that base and starts to fix the niggles and
annoyances and hopefully become a useful enhancement. As a base, weblizer has
a stated goal of producing web server analysis. AWFFull on the other hand, will
gradually focus more on the business intelligence contained within those logs -
and not specifically limited just to web server logs.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p0

unzip -d flags -o -f %{SOURCE1}
unzip -d flags -o -f %{SOURCE2}

cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .

%build
%serverbuild

%configure2_5x \
    --with-etcdir=%{_sysconfdir}/%{name} \
    --with-font-default=%{_datadir}/%{name}/VeraBd.ttf \
    --with-font-label=%{_datadir}/%{name}/Vera.ttf

%make

%install
%makeinstall_std

install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}

install -m0644 sample.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m0644 sample.css %{buildroot}%{_localstatedir}/lib/%{name}/%{name}.css
install -m0755 contrib/awffull_history_regen.pl %{buildroot}%{_bindir}/awffull_history_regen
install -m0644 Vera.ttf %{buildroot}%{_datadir}/%{name}/
install -m0644 VeraBd.ttf %{buildroot}%{_datadir}/%{name}/

install -d %{buildroot}/var/www/icons/flags
install -m0644 flags/*.png %{buildroot}/var/www/icons/flags/
install -m0644 flags/README %{buildroot}/var/www/icons/flags/

# apache configuration
install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} configuration

Alias /%{name} %{_localstatedir}/lib/%{name}

<Directory %{_localstatedir}/lib/%{name}>
    Require all granted
</Directory>

Alias /flags /var/www/icons/flags

<Directory /var/www/icons/flags>
    Options -Indexes +MultiViews
    AllowOverride None
    Require all granted
</Directory>

EOF

# cron task
install -d %{buildroot}%{_sysconfdir}/cron.daily
install -m0755 awffull.cron.daily %{buildroot}%{_sysconfdir}/cron.daily/%{name}

cat > README.Mandriva << EOF

The default configuration file has been moved from /etc/awffull.conf to
/etc/awffull/awffull.conf

Currently on Mandriva you need to set two environment variables in order to
get the UTF-8 output in the language you want, so for Swedish you should do
like so:

LANG=sv_SE.UTF-8 LANGUAGE=sv_SE.UTF-8:sv \\
awffull --output=/path/to/the/output/directory -n \$HOSTNAME \\
--use_geoip /path/to/the/apache/log/access_log

If you have many virtual hosts you can copy the default /etc/awffull/awffull.conf
to /etc/awffull/virtual_host_name.conf and edit that file to point to the correct
logfile, output directory and such. The new /etc/cron.daily/awffull script will
look for the following settings in the /etc/awffull/virtual_host_name.conf file
and automatically generate the output in the desired language:

#AWFFULL_LANG=
#AWFFULL_LANGUAGE=

So if you for example want the output in Swedish change this to:

#AWFFULL_LANG=sv_SE.UTF-8
#AWFFULL_LANGUAGE=sv_SE.UTF-8:sv

EOF



%clean

%files
%doc COPYING ChangeLog PERFORMANCE_TIPS.txt README* TODO country-codes.txt sample.minimal.conf sample.css
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_webappconfdir}/%{name}.conf
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%attr(0755,root,root) %{_bindir}/awffull
%attr(0755,root,root) %{_bindir}/awffull_history_regen
%attr(0755,root,root) %dir %{_localstatedir}/lib/%{name}
%attr(0644,root,root) %config(noreplace) %{_localstatedir}/lib/%{name}/%{name}.css
%attr(0755,root,root) %dir /var/www/icons/flags
%attr(0644,root,root) /var/www/icons/flags/*
%attr(0644,root,root) %{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%attr(0644,root,root) %{_datadir}/%{name}/*.ttf
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man5/*


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 3.10.2-6mdv2012.0
+ Revision: 772939
- relink against libpcre.so.1

* Thu Nov 18 2010 Oden Eriksson <oeriksson@mandriva.com> 3.10.2-5mdv2011.0
+ Revision: 598773
- cleanup the spec file a bit

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.10.2-4mdv2010.1
+ Revision: 513158
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- switch to "open to all" default access policy

* Mon Dec 28 2009 Oden Eriksson <oeriksson@mandriva.com> 3.10.2-3mdv2010.1
+ Revision: 483013
- rebuild
- fix upstream bug 309617

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 3.10.2-2mdv2010.0
+ Revision: 436714
- rebuild

* Mon Dec 15 2008 Oden Eriksson <oeriksson@mandriva.com> 3.10.2-1mdv2009.1
+ Revision: 314464
- 3.10.2

* Mon Nov 24 2008 Oden Eriksson <oeriksson@mandriva.com> 3.10.1-1mdv2009.1
+ Revision: 306323
- 3.10.1 (GPLv3+)
- rediffed P0

* Wed Nov 19 2008 Oden Eriksson <oeriksson@mandriva.com> 3.9.1-1mdv2009.1
+ Revision: 304434
- 3.9.1

* Mon Nov 17 2008 Oden Eriksson <oeriksson@mandriva.com> 3.9.1-0.beta3.3mdv2009.1
+ Revision: 303960
- 3.9.1-beta3

* Sun Aug 03 2008 Oden Eriksson <oeriksson@mandriva.com> 3.8.2-4mdv2009.0
+ Revision: 261842
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Nov 14 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.2-1mdv2008.1
+ Revision: 108692
- 3.8.2

* Wed Nov 07 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-1mdv2008.1
+ Revision: 106694
- 3.8.1

* Thu Oct 11 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta3.2mdv2008.1
+ Revision: 97035
- provide the fonts so it's self contained
- make it backportable

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta3.1mdv2008.0
+ Revision: 77390
- 3.8.1-beta3

* Wed Aug 15 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta2.1mdv2008.0
+ Revision: 63641
- 3.8.1-beta2
- drop upstream patches; P1,P2
- rediffed P0

* Tue Jul 24 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta1.5mdv2008.0
+ Revision: 54998
- point to the correct default fonts and fix deps

* Fri Jul 20 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta1.4mdv2008.0
+ Revision: 53861
- added one security fix (P2) by mrl?

* Sat Jun 23 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta1.3mdv2008.0
+ Revision: 43401
- use the new %%serverbuild macro

* Fri Jun 22 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta1.2mdv2008.0
+ Revision: 43003
- used a modified cronscript from debian

* Sun Jun 17 2007 Oden Eriksson <oeriksson@mandriva.com> 3.8.1-0.beta1.1mdv2008.0
+ Revision: 40489
- 3.8.1-beta1
- rediffed P0

* Sun May 20 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.5-1mdv2008.0
+ Revision: 28873
- 3.7.5

* Mon May 07 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.4-1mdv2008.0
+ Revision: 24151
- 3.7.4

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.4-0.beta3.1mdv2008.0
+ Revision: 14040
- 3.7.4-beta3


* Wed Apr 04 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.4-0.beta2.1mdv2007.1
+ Revision: 150520
- 3.7.4-beta2

* Thu Mar 01 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.4-0.beta1.1mdv2007.1
+ Revision: 130414
- 3.7.4-beta1
- 3.7.3
- drop the no_utf-8 patch
- don't use the locale rpm macros, it is a lot of overhead if you
  want to use uninstalled languages later on...

* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.2-1mdv2007.1
+ Revision: 110572
- 3.7.2
- drop upstream implemented patches

* Tue Jan 09 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.1-4mdv2007.1
+ Revision: 106432
- rebuild
- fix buffer overflows after looking at debian

* Sun Jan 07 2007 Oden Eriksson <oeriksson@mandriva.com> 3.7.1-2mdv2007.1
+ Revision: 105298
- added the language flags and corresponding apache config (S1,S2,P0)
- fixed a small issue in the etcdir (P1)
- make localization work as intended, call it like this
  "LANG=de_DE LANGUAGE=de_DE:de awffull" to use it
- disable non working UTF-8 (P2)
- fix build deps

* Sun Oct 15 2006 Oden Eriksson <oeriksson@mandriva.com> 3.7.1-1mdv2007.1
+ Revision: 64956
- Import awffull

* Sun Oct 15 2006 Oden Eriksson <oeriksson@mandriva.com> 3.7.1-1mdv2007.1
- 3.7.1
- restrict access by default, but tell how to fix it. please do not change 
  this again as it can pose a security threat to let everyone look at  your
  apache log statistics, ie. your apache log files...
- rediff P0
- add the localization

* Wed Sep 06 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.5.1-4mdv2007.0
- web macros
- apply web policy
- output files in /var/lib/awffull
- don't restrict access by default, this is an admin decision
- clean spec

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 3.5.1-3mdv2007.0
- make it provide and obsolete webalizer

* Tue Sep 05 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.5.1-2mdv2007.0
- don't forget to install cron task

* Mon Jun 26 2006 Oden Eriksson <oeriksson@mandriva.com> 3.5.1-1mdv2007.0
- 3.5.1

* Sat Jun 10 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4.3-1mdv2007.0
- 3.4.3

* Thu Mar 23 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4.1-1mdk
- 3.4.1
- rediffed P0

* Wed Mar 01 2006 Oden Eriksson <oeriksson@mandriva.com> 3.3.1-1mdk
- initial Mandriva package

