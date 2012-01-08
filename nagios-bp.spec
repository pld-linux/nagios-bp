%include	/usr/lib/rpm/macros.perl
Summary:	Nagios Business Process AddOns
Name:		nagios-bp
Version:	0.9.6
Release:	0.6
License:	GPL v2
Group:		Applications/WWW
Source0:	http://bp-addon.monitoringexchange.org/download/nagios-business-process-addon-%{version}.tar.gz
# Source0-md5:	8b88a1729f6c6324e410a285e1a493fd
Patch0:		DESTDIR.patch
Patch1:		paths.patch
URL:		http://bp-addon.monitoringexchange.org/
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	nagios-cgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapp		nagiosbp
%define		_sysconfdir	/etc/nagios/%{_webapp}
%define		appdir		%{_datadir}/nagios/%{_webapp}
%define		cgidir		%{_libdir}/nagios/cgi
%define		htmldir		%{_prefix}/share/nagios
%define		plugindir	%{_prefix}/lib/nagios/plugins

%define		_noautoreq	perl(bsutils) perl(nagiosBp) perl(ndodb) perl(settings)
%define		_noautoprov	%{_noautoreq}

%description
The AddOn Business Process View takes results of the single nagios
checks and builds up aggregated states. How they are associated is
described in one or more config files. There is the possibility to
make "and" conjuctions, "or" conjunction and other...

A business process (as defined by such a formula) can be used as a
part of another business process. So You can build up a hirachical
structure to describe the state of Your Application.

The AddOn Business Impact Analysis allows You to simulate Outages. You
can set manually the state of each single component to each state You
like and look, how this would impact Your applications.

%prep
%setup -q -n nagios-business-process-addon-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure \
	--bindir=%{_sbindir} \
	--sbindir=%{cgidir} \
	--datadir=%{htmldir} \
	--libexecdir=%{plugindir} \
	--libdir=%{_libdir}/nagios/nbp \
	--with-nagiosbp-user=%(id -un) \
	--with-nagiosbp-group=%(id -gn) \
	--with-cgiurl=/nagios/cgi-bin \
	--with-htmurl=/nagios/bp \
	--with-httpd-conf=/etc/webapps/nagios \
	--with-apache-user=http \
	--with-cron-d-dir=/etc/cron.d \
	--with-nagetc=/etc/nagios \
	--with-naghtmurl=/nagios \
	--with-nagcgiurl=/nagios/cgi-bin \
	--with-apache-authname=Nagios

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{appdir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# nagios-cgi provides neccessary access and aliases
%{__rm} $RPM_BUILD_ROOT/etc/webapps/nagios/%{_webapp}.conf
# remove -sample suffix
mv $RPM_BUILD_ROOT%{_sysconfdir}/nagios-bp.conf{-sample,}
mv $RPM_BUILD_ROOT%{_sysconfdir}/ndo.cfg{-sample,}

# remove .ext
mv $RPM_BUILD_ROOT%{plugindir}/check_bp_status{.pl,}
mv $RPM_BUILD_ROOT%{_sbindir}/bp_cfg2service_cfg{.pl,}
mv $RPM_BUILD_ROOT%{_sbindir}/nagios-bp-check-ndo-connection{.pl,}
mv $RPM_BUILD_ROOT%{_sbindir}/nagios-bp-consistency-check{.pl,}

# in %doc
%{__rm} $RPM_BUILD_ROOT%{_prefix}/{README,AUTHORS,CHANGES,INSTALL,LICENSE,UPDATE}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc API-DOC AUTHORS CHANGES INSTALL README UPDATE
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.cfg
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/nagiosbp
%attr(755,root,root) %{cgidir}/nagios-bp.cgi
%attr(755,root,root) %{cgidir}/whereUsed.cgi
%attr(755,root,root) %{plugindir}/check_bp_status

%attr(755,root,root) %{_sbindir}/bp_cfg2service_cfg
%attr(755,root,root) %{_sbindir}/nagios-bp-check-ndo-connection
%attr(755,root,root) %{_sbindir}/nagios-bp-consistency-check
%attr(755,root,root) %{_sbindir}/nagios_bp_session_timeout

%dir %{_libdir}/nagios/nbp
%{_libdir}/nagios/nbp/*.pm

%{htmldir}/info4.gif
%dir %{htmldir}/lang
%{htmldir}/stylesheets/nagios-bp.css
%{htmldir}/stylesheets/user.css
%{htmldir}/tree.gif
%{htmldir}/lang/i18n_en.txt
%lang(de) %{htmldir}/lang/i18n_de.txt
