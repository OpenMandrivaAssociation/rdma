#  Copyright (c) 2008 Red Hat, Inc.

#  There is no URL or upstream source entry as this package constitutes
#  upstream for itself.

Summary: Infiniband/iWARP Kernel Module Initializer
Name: rdma
Version: 2.0
Release: 13%{?dist}
License: GPLv2+

Source0: rdma.conf
Source1: rdma.udev-ipoib-naming.rules
Source2: rdma.fixup-mtrr.awk
Source4: rdma.ifup-ib
Source5: rdma.ifdown-ib
Source6: rdma.service
Source7: rdma.sbin
Source8: rdma.udev-rules

BuildArch: noarch
BuildRequires: systemd
Requires: udev >= 095
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description 
User space initialization scripts for the kernel InfiniBand/iWARP drivers

%prep

%build

%install
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}/lib/udev/rules.d

# Stuff to go into the base package
install -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/70-persistent-ipoib.rules
install -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/rdma.service
install -m 0755 %{SOURCE7} %{buildroot}%{_sbindir}/rdma-init-kernel
install -m 0644 %{SOURCE2} %{buildroot}%{_sbindir}/rdma-fixup-mtrr.awk
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -m 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
install -m 0644 %{SOURCE8} %{buildroot}/lib/udev/rules.d/98-rdma.rules

%post
%systemd_post rdma.service

%preun
%systemd_preun rdma.service

%postun
%systemd_postun

%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%{_unitdir}/%{name}.service
%{_sbindir}/rdma-init-kernel
%{_sbindir}/rdma-fixup-mtrr.awk
%{_sysconfdir}/sysconfig/network-scripts/*
/lib/udev/rules.d/*
