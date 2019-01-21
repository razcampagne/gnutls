%define gnutls_version 2.12.23

Summary: A TLS protocol implementation
Name: gnutls
Version: %{gnutls_version}.4
Release: 1
# The libgnutls core library is LGPLv2+, MeeGo doesn't ship other
# utilities or remaining libraries
License: LGPLv2+
Group: System/Libraries
BuildRequires: libgcrypt-devel >= 1.2.2, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel
BuildRequires: lzo-devel, libtool, automake, autoconf
BuildRequires: p11-kit-devel
URL: http://www.gnutls.org/
#Source0: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz
#Source1: ftp://ftp.gnutls.org/pub/gnutls/%{name}-%{version}.tar.gz.sig
# XXX patent tainted SRP code removed.
Source0: %{name}-%{gnutls_version}.tar.bz2
Source1: %{name}-%{gnutls_version}.tar.bz2.sig
Source2: libgnutls-config
Patch0: gnutls-2.12.9-compile-fix.patch
Patch1: CVE-2013-2116.patch
Patch2: CVE-2014-0092.patch
Patch3: CVE-2014-3466.patch
Patch4: CVE-2015-0294.patch
Patch5: CVE-2015-0282.patch
Patch6: GNUTLS-SA-2015-2-1.patch
Patch7: GNUTLS-SA-2015-2-2.patch
Patch8: disable-sslv3.patch
Patch9: eliminate-cert-sign-algo.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libgcrypt >= 1.2.2

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: pkgconfig

%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.

%prep
%setup -q -n %{name}-%{gnutls_version}

# gnutls-2.12.9-compile-fix.patch
%patch0 -p1
# CVE-2013-2116.patch
%patch1 -p1
# CVE-2014-0092.patch
%patch2 -p1
# CVE-2014-3466.patch
%patch3 -p0
# CVE-2015-0294.patch
%patch4 -p1
# CVE-2015-0282.patch
%patch5 -p1
# GNUTLS-SA-2015-2-1.patch
%patch6 -p1
# GNUTLS-SA-2015-2-2.patch
%patch7 -p1
# disable-sslv3.patch
%patch8 -p1
# eliminate-cert-sign-algo.patch
%patch9 -p1

# Remove other utils files
rm -rf maint.mk libextra doc gl lib/gl/test \
  build-aux/vc-list-files \
  build-aux/useless-if-before-free \
  build-aux/pmccabe2html

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
# On MeeGo we build core lib only
pushd lib
%configure --disable-srp-authentication \
           --with-libgcrypt

make
cp COPYING COPYING.LIB
popd

%install
rm -fr $RPM_BUILD_ROOT
pushd lib
%makeinstall
popd
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
install -d $RPM_BUILD_ROOT%{_bindir}
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        README AUTHORS

%find_lang libgnutls

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libgnutls.lang
%defattr(-,root,root,-)
%license lib/COPYING.LIB
%{_libdir}/libgnutls*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/libgnutls*.a
%{_libdir}/libgnutls*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
