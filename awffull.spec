%if %mdkver < 200800
%define _webappconfdir /etc/httpd/conf/webapps.d
%endif

Summary:	AWFFull - A Webalizer Fork, Full o' Features!
Name:		awffull
Version:	3.8.2
Release:	%mkrel 1
License:	GPL
Group:		Monitoring
URL:		http://www.stedee.id.au/awffull
# md5sum: 853f4947d22fe6e0b1f848a4c13de44c
Source0:	http://www.stedee.id.au/files/%{name}-%{version}.tar.gz
Source1:	http://flags.blogpotato.de/zip/world.zip
Source2:	http://flags.blogpotato.de/zip/special.zip
Source3:	awffull.cron.daily
Source4:	Vera.ttf
Source5:	VeraBd.ttf
Patch0:		awffull-mdv_conf.diff
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
Provides:	webalizer = %{version}-%{release}
Provides:	webalizer-catalan = %{version}-%{release}
Provides:	webalizer-chinese = %{version}-%{release}
Provides:	webalizer-croatian = %{version}-%{release}
Provides:	webalizer-czech = %{version}-%{release}
Provides:	webalizer-danish = %{version}-%{release}
Provides:	webalizer-dutch = %{version}-%{release}
Provides:	webalizer-estonian = %{version}-%{release}
Provides:	webalizer-finnish = %{version}-%{release}
Provides:	webalizer-french = %{version}-%{release}
Provides:	webalizer-galician = %{version}-%{release}
Provides:	webalizer-german = %{version}-%{release}
Provides:	webalizer-greek = %{version}-%{release}
Provides:	webalizer-hungarian = %{version}-%{release}
Provides:	webalizer-icelandic = %{version}-%{release}
Provides:	webalizer-indonesian = %{version}-%{release}
Provides:	webalizer-italian = %{version}-%{release}
Provides:	webalizer-japanese = %{version}-%{release}
Provides:	webalizer-korean = %{version}-%{release}
Provides:	webalizer-latvian = %{version}-%{release}
Provides:	webalizer-malay = %{version}-%{release}
Provides:	webalizer-norwegian = %{version}-%{release}
Provides:	webalizer-polish = %{version}-%{release}
Provides:	webalizer-portuguese = %{version}-%{release}
Provides:	webalizer-portuguese_brazil = %{version}-%{release}
Provides:	webalizer-romanian = %{version}-%{release}
Provides:	webalizer-russian = %{version}-%{release}
Provides:	webalizer-serbian = %{version}-%{release}
Provides:	webalizer-simplified_chinese = %{version}-%{release}
Provides:	webalizer-slovak = %{version}-%{release}
Provides:	webalizer-slovene = %{version}-%{release}
Provides:	webalizer-spanish = %{version}-%{release}
Provides:	webalizer-swedish = %{version}-%{release}
Provides:	webalizer-turkish = %{version}-%{release}
Provides:	webalizer-ukrainian = %{version}-%{release}
Obsoletes:	webalizer
Obsoletes:	webalizer-catalan
Obsoletes:	webalizer-chinese
Obsoletes:	webalizer-croatian
Obsoletes:	webalizer-czech
Obsoletes:	webalizer-danish
Obsoletes:	webalizer-dutch
Obsoletes:	webalizer-estonian
Obsoletes:	webalizer-finnish
Obsoletes:	webalizer-french
Obsoletes:	webalizer-galician
Obsoletes:	webalizer-german
Obsoletes:	webalizer-greek
Obsoletes:	webalizer-hungarian
Obsoletes:	webalizer-icelandic
Obsoletes:	webalizer-indonesian
Obsoletes:	webalizer-italian
Obsoletes:	webalizer-japanese
Obsoletes:	webalizer-korean
Obsoletes:	webalizer-latvian
Obsoletes:	webalizer-malay
Obsoletes:	webalizer-norwegian
Obsoletes:	webalizer-polish
Obsoletes:	webalizer-portuguese
Obsoletes:	webalizer-portuguese_brazil
Obsoletes:	webalizer-romanian
Obsoletes:	webalizer-russian
Obsoletes:	webalizer-serbian
Obsoletes:	webalizer-simplified_chinese
Obsoletes:	webalizer-slovak
Obsoletes:	webalizer-slovene
Obsoletes:	webalizer-spanish
Obsoletes:	webalizer-swedish
Obsoletes:	webalizer-turkish
Obsoletes:	webalizer-ukrainian
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

unzip -d flags -f %{SOURCE1}
unzip -d flags -f %{SOURCE2}

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
rm -rf %{buildroot}

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
    Order Deny,Allow
    Deny from All
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied. Please edit %{_webappconfdir}/%{name}.conf to give access to this resource."
</Directory>

Alias /flags /var/www/icons/flags

<Directory "/var/www/icons/flags">
    Options -Indexes MultiViews
    AllowOverride None
    Order allow,deny
    Allow from all
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

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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
