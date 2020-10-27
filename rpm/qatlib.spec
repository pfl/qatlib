################################################################
#   BSD LICENSE
# 
#   Copyright(c) 2007-2020 Intel Corporation. All rights reserved.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions
#   are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     * Neither the name of Intel Corporation nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
# 
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
################################################################
%global soversion 0

Name:             qatlib
Version:          20.08.0
Release:          1%{?dist}
Summary:          Intel QuickAssist user space library
License:          BSD and (BSD or GPLv2) and OpenSSL
URL:              https://github.com/intel/%{name}
Source0:          https://github.com/intel/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    systemd gcc make autoconf automake libtool systemd-devel openssl-devel zlib-devel
Requires(pre):    shadow-utils
# Upstream ticket to remove bundled implementation of libcrypto:
# https://github.com/intel/qatlib/issues/2
Provides:         bundled(libcrypto) = 1.1.1c

%{?systemd_requires}

%description
Intel QuickAssist Technology (Intel QAT) provides hardware acceleration
for offloading security, authentication and compression services from the
CPU, thus significantly increasing the performance and efficiency of
standard platform solutions.

Its services include symmetric encryption and authentication,
asymmetric encryption, digital signatures, RSA, DH and ECC, and
lossless data compression.

This package provides user space libraries that allow access to
Intel QuickAssist devices and expose the Intel QuickAssist APIs.

%package       devel
Summary:       Headers and libraries to build applications that use qatlib
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description   devel
This package contains headers and libraries required to build applications
that use the Intel QuickAssist APIs.

%prep
%autosetup

%build
autoreconf -vif
%configure
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_mandir}/man8

install -p -m 0755 .libs/libqat.so.0.0.0 %{buildroot}%{_libdir}/libqat.so.%{soversion}.%{version}
install -p -m 0755 .libs/libusdm.so.0.0.0 %{buildroot}%{_libdir}/libusdm.so.%{soversion}.%{version}
ln -s -f libqat.so.%{soversion}.%{version} %{buildroot}%{_libdir}/libqat.so.%{soversion}
ln -s -f libusdm.so.%{soversion}.%{version} %{buildroot}%{_libdir}/libusdm.so.%{soversion}
ln -s -f libqat.so.%{soversion}.%{version} %{buildroot}%{_libdir}/libqat.so
ln -s -f libusdm.so.%{soversion}.%{version} %{buildroot}%{_libdir}/libusdm.so

install -p -m 0755 qatmgr %{buildroot}%{_sbindir}
install -p -m 0755 quickassist/utilities/service/qat_init.sh %{buildroot}%{_sbindir}
install -p -m 0644 quickassist/utilities/service/qat.service %{buildroot}%{_unitdir}

install -p -m 0644 qat_init.sh.8 %{buildroot}%{_mandir}/man8
install -p -m 0644 qatmgr.8 %{buildroot}%{_mandir}/man8

mkdir -p %{buildroot}%{_includedir}/qat

install -p -m 0644 quickassist/include/cpa.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/cpa_types.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_common.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_dh.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_drbg.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_dsa.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_ecdh.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_ecdsa.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_ec.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_im.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_key.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_ln.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_nrbg.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_prime.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_rsa.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_sym_dp.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/lac/cpa_cy_sym.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/dc/cpa_dc.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/dc/cpa_dc_dp.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/include/dc/cpa_dc_chain.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/lookaside/access_layer/include/icp_sal_poll.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/lookaside/access_layer/include/icp_sal_user.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/lookaside/access_layer/include/icp_sal.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/lookaside/access_layer/include/icp_sal_versions.h %{buildroot}%{_includedir}/qat
install -p -m 0644 quickassist/utilities/libusdm_drv/qae_mem.h %{buildroot}%{_includedir}/qat

%pre
getent group qat >/dev/null || groupadd -r qat
exit 0

%post
%systemd_post qat.service

%preun
%systemd_preun qat.service

%postun
%systemd_postun_with_restart qat.service

%files
%license LICENSE*
%{_libdir}/libqat.so.%{soversion}.%{version}
%{_libdir}/libusdm.so.%{soversion}.%{version}
%{_libdir}/libqat.so.%{soversion}
%{_libdir}/libusdm.so.%{soversion}
%{_sbindir}/qatmgr
%{_sbindir}/qat_init.sh
%{_unitdir}/qat.service
%{_mandir}/man8/qat_init.sh.8*
%{_mandir}/man8/qatmgr.8*

%files         devel
%{_libdir}/libqat.so
%{_libdir}/libusdm.so
%{_includedir}/qat

%changelog
* Fri Oct 23 2020 Giovanni Cabiddu <giovanni.cabiddu@intel.com> - 20.08.0-1
- Fixes to spec from first round of review

* Mon Aug 10 2020 Mateusz Polrola <mateuszx.potrola@intel.com> - 20.08.0
- Initial version of the package
