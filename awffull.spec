Summary:	A Webalizer Fork, Full o' Features!
Name:		awffull
Version:	3.10.2
Release:	10
License:	GPLv3+
Group:		Monitoring
Url:		http://www.stedee.id.au/awffull
# md5sum: 80acf755b354c49d78a5b9bb580196f2
Source0:	http://www.stedee.id.au/files/%{name}-%{version}.tar.gz
Source1:	http://flags.blogpotato.de/zip/large/world.zip
Source2:	http://flags.blogpotato.de/zip/large/special.zip
Source3:	awffull.cron.daily
Source4:	Vera.ttf
Source5:	VeraBd.ttf
Patch0:		awffull-mdv_conf.diff
Patch1:		awffull-3.10.2-upstreambug309617.diff
Requires:	apache-base
Requires:	geoip
BuildRequires:	gd-devel
BuildRequires:	gettext-devel
BuildRequires:	jpeg-devel
BuildRequires:	apache-base >= 2.0.54
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(geoip)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	unzip

%description
Webalizer is a great weblog analysis program but hasn't been going anywhere in
recent years. AWFFull takes that base and starts to fix the niggles and
annoyances and hopefully become a useful enhancement. As a base, weblizer has
a stated goal of producing web server analysis. AWFFull on the other hand, will
gradually focus more on the business intelligence contained within those logs -
and not specifically limited just to web server logs.

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

#----------------------------------------------------------------------------

%prep
%setup -q
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

