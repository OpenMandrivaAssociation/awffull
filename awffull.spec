Summary:	AWFFull - A Webalizer Fork, Full o' Features!
Name:		awffull
Version:	3.7.4
Release:	%mkrel 0.beta2.1
License:	GPL
Group:		Monitoring
URL:		http://www.stedee.id.au/awffull
Source0:	http://www.stedee.id.au/files/%{name}-%{version}-beta2.tar.gz
Source1:	http://flags.blogpotato.de/zip/world.zip
Source2:	http://flags.blogpotato.de/zip/special.zip
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

%setup -q -n %{name}-%{version}-beta2
%patch0 -p0

unzip -d flags -f %{SOURCE1}
unzip -d flags -f %{SOURCE2}

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_localstatedir}/%{name}
install -d %{buildroot}%{_sysconfdir}

install -m0644 sample.conf %{buildroot}%{_sysconfdir}/awffull.conf
install -m0755 awffull_history_regen.pl %{buildroot}%{_bindir}/awffull_history_regen

install -d %{buildroot}/var/www/icons/flags
install -m0644 flags/*.png %{buildroot}/var/www/icons/flags/
install -m0644 flags/README %{buildroot}/var/www/icons/flags/

# apache configuration
install -d %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} configuration

Alias /%{name} %{_localstatedir}/%{name}

<Directory %{_localstatedir}/%{name}>
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
cat > %{buildroot}%{_sysconfdir}/cron.daily/%{name} <<'EOF'
#!/bin/sh

if [ -z "`grep "^HostName" %{_sysconfdir}/awffull.conf`" ]; then
    HOSTNAME="-n `hostname --fqdn`"
fi

%{_bindir}/awffull -c %{_sysconfdir}/awffull.conf $HOSTNAME
EOF
chmod 755 %{buildroot}%{_sysconfdir}/cron.daily/%{name}

cat > README.Mandriva << EOF

Currently on Mandriva you need to set three environment variables in order to
get the UTF-8 output in the language you want, so for Swedish you should do
like so:

LC_ALL=sv_SE.UTF-8 LANG=sv_SE.UTF-8 LANGUAGE=sv_SE.UTF-8:sv \\
awffull --output=/path/to/the/output/directory -n \$HOSTNAME \\
--use_geoip /path/to/the/apache/log/access_log
EOF

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ChangeLog PERFORMANCE_TIPS.txt README* TODO country-codes.txt
%config(noreplace) %{_sysconfdir}/awffull.conf
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%{_bindir}/awffull
%{_bindir}/awffull_history_regen
%{_mandir}/man1/*
%{_localstatedir}/%{name}
/var/www/icons/flags/*
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo


