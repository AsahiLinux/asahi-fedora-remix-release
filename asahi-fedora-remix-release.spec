%if 0%{?fc37}
%define release_name Thirty Seven
%define is_rawhide 0
%elif 0%{?fc38}
%define release_name Thirty Eight
%define is_rawhide 0
%else
%define release_name Rawhide
%define is_rawhide 1
%endif

# This is going to go badly for you if you build on not-Fedora...
%if 0%{?fedora}
%define dist_version %{fedora}
%else
%define dist_version 39
%endif
%define rhel_dist_version 10

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%if 0%{?eln}
%bcond_with basic
%bcond_with cinnamon
%bcond_with cloud
%bcond_with compneuro
%bcond_with container
%bcond_with coreos
%bcond_with designsuite
%bcond_without eln
%bcond_with iot
%bcond_with kde
%bcond_with matecompiz
%bcond_with server
%bcond_with silverblue
%bcond_with kinoite
%bcond_with snappy
%bcond_with soas
%bcond_with workstation
%bcond_with xfce
%bcond_with i3
%bcond_with lxqt
%bcond_with budgie
%bcond_with sway
%bcond_with sericea
%else
%bcond_without basic
%bcond_without cinnamon
%bcond_without cloud
%bcond_without compneuro
%bcond_without container
%bcond_without coreos
%bcond_without designsuite
%bcond_with eln
%bcond_without iot
%bcond_without kde
%bcond_without matecompiz
%bcond_without server
%bcond_without silverblue
%bcond_without kinoite
%bcond_without snappy
%bcond_without soas
%bcond_without workstation
%bcond_without xfce
%bcond_without i3
%bcond_without lxqt
%bcond_without budgie
%bcond_without sway
%bcond_without sericea
%endif

%if %{with silverblue} || %{with kinoite} || %{with sericea}
%global with_ostree_desktop 1
%endif

%global dist %{?eln:.eln%{eln}}

Summary:        Asahi Fedora Remix release files
Name:           asahi-fedora-remix-release
Version:        %{dist_version}
# The numbering is 0.<r> before a given Fedora Linux release is released,
# with r starting at 1, and then just <r>, with r starting again at 1.
# Use '%%autorelease -p' before final, and then drop the '-p'.
Release:        %autorelease -p
License:        MIT
URL:            https://pagure.io/fedora-asahi/project

Source1:        LICENSE
Source2:        Fedora-Legal-README.txt

Source10:       85-display-manager.preset
Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset
Source14:       80-server.preset
Source15:       80-workstation.preset
Source16:       org.gnome.shell.gschema.override
Source17:       org.projectatomic.rpmostree1.rules
Source18:       80-iot.preset
Source19:       distro-template.swidtag
Source20:       distro-edition-template.swidtag
Source21:       fedora-workstation.conf
Source22:       80-coreos.preset
Source23:       zezere-ignition-url
Source24:       80-iot-user.preset
Source25:       plasma-desktop.conf
Source26:       80-kde.preset
Source27:       81-desktop.preset
Source28:       longer-default-shutdown-timeout.conf

BuildArch:      noarch

Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}

Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-basic if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-basic

# We replace fedora-release stuff
Conflicts:      fedora-release < 1:%{version}-%{release}
Conflicts:      fedora-release-identity

Obsoletes:      fedora-release < 1:%{version}-%{release}
Provides:       fedora-release = 1:%{version}-%{release}

BuildRequires:  redhat-rpm-config > 121-1
BuildRequires:  systemd-rpm-macros

%description
Asahi Fedora Remix release files such as various /etc/ files that define the release
and systemd preset files that determine which services are enabled by default.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/ for details.


%package common
Summary: Asahi Fedora release files

Requires:   asahi-fedora-remix-release-variant = %{version}-%{release}
Suggests:   asahi-fedora-remix-release

Requires:   fedora-repos(%{version})
Requires:   asahi-fedora-remix-release-identity = %{version}-%{release}

Obsoletes:  fedora-release-common < 1:%{version}-%{release}
Provides:   fedora-release-common = 1:%{version}-%{release}

%if %{is_rawhide}
# Make $releasever return "rawhide" on Rawhide
# https://pagure.io/releng/issue/7445
Provides:       system-release(releasever) = %{releasever}
%endif

# Fedora ships a generic-release package to make the creation of Remixes
# easier, but it cannot coexist with the asahi-fedora-remix-release[-*] packages, so we
# will explicitly conflict with it.
Conflicts:  generic-release

# rpm-ostree count me is now enabled in 90-default.preset
Obsoletes: fedora-release-ostree-counting <= 36-0.7

%description common
Release files common to all Editions and Spins of Fedora


%if %{with basic}
%package identity-basic
Summary:        Package providing the basic Asahi Fedora Remix identity

RemovePathPostfixes: .basic
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity

Obsoletes:      fedora-release-release-identity < 1:%{version}-%{release}
Provides:       fedora-release-release-identity = 1:%{version}-%{release}

%description identity-basic
Provides the necessary files for an Asahi Fedora Remix installation that is not identifying
itself as a particular Edition or Spin.
%endif


%if %{with cinnamon}
%package cinnamon
Summary:        Base package for Asahi Fedora Remix Cinnamon-specific default configurations

RemovePathPostfixes: .cinnamon
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-cinnamon < 1:%{version}-%{release}
Provides:       fedora-release-cinnamon = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-cinnamon if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-cinnamon


%description cinnamon
Provides a base package for Asahi Fedora Remix Cinnamon-specific configuration files to
depend on as well as Cinnamon system defaults.


%package identity-cinnamon
Summary:        Package providing the identity for Asahi Fedora Remix Cinnamon Spin

RemovePathPostfixes: .cinnamon
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-cinnamon = %{version}-%{release}

Obsoletes:      fedora-release-identity-cinnamon < 1:%{version}-%{release}
Provides:       fedora-release-identity-cinnamon = 1:%{version}-%{release}

%description identity-cinnamon
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Cinnamon.
%endif


%if %{with cloud}
%package cloud
Summary:        Base package for Asahi Fedora Remix Cloud-specific default configurations

RemovePathPostfixes: .cloud
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-cloud < 1:%{version}-%{release}
Provides:       fedora-release-cloud = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-cloud if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-cloud


%description cloud
Provides a base package for Asahi Fedora Remix Cloud-specific configuration files to
depend on.


%package identity-cloud
Summary:        Package providing the identity for Asahi Fedora Remix Cloud Edition

RemovePathPostfixes: .cloud
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-cloud = %{version}-%{release}

Obsoletes:      fedora-release-identity-cloud < 1:%{version}-%{release}
Provides:       fedora-release-identity-cloud = 1:%{version}-%{release}

%description identity-cloud
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Cloud Edition.
%endif


%if %{with compneuro}
%package compneuro
Summary:        Base package for Asahi Fedora Remix Comp Neuro specific default configurations

RemovePathPostfixes: .compneuro
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-compneuro < 1:%{version}-%{release}
Provides:       fedora-release-compneuro = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-compneuro if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-compneuro


%description compneuro
Provides a base package for Asahi Fedora Remix Comp Neuro specific configuration files to
depend on as well as Comp Neuro system defaults.


%package identity-compneuro
Summary:        Package providing the identity for Asahi Fedora Remix Comp Neuro Lab

RemovePathPostfixes: .compneuro
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-compneuro = %{version}-%{release}

Obsoletes:      fedora-release-identity-compneuro < 1:%{version}-%{release}
Provides:       fedora-release-identity-compneuro = 1:%{version}-%{release}

%description identity-compneuro
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Comp Neuro Lab.
%endif


%if %{with container}
%package container
Summary:        Base package for Asahi Fedora Remix container specific default configurations

RemovePathPostfixes: .container
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-container < 1:%{version}-%{release}
Provides:       fedora-release-container = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-container if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-container


%description container
Provides a base package for Asahi Fedora Remix container specific configuration files to
depend on as well as container system defaults.


%package identity-container
Summary:        Package providing the identity for Asahi Fedora Remix Container Base Image

RemovePathPostfixes: .container
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-container = %{version}-%{release}

Obsoletes:      fedora-release-identity-container < 1:%{version}-%{release}
Provides:       fedora-release-identity-container = 1:%{version}-%{release}

%description identity-container
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as the Fedora Container Base Image.
%endif


%if %{with coreos}
%package coreos
Summary:        Base package for Asahi Fedora Remix CoreOS-specific default configurations

RemovePathPostfixes: .coreos
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-coreos < 1:%{version}-%{release}
Provides:       fedora-release-coreos = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-coreos if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-coreos


%description coreos
Provides a base package for Asahi Fedora Remix CoreOS Host-specific configuration files to
depend.


%package identity-coreos
Summary:        Package providing the identity for Asahi Fedora Remix CoreOS

RemovePathPostfixes: .coreos
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-coreos = %{version}-%{release}

Obsoletes:      fedora-release-identity-coreos < 1:%{version}-%{release}
Provides:       fedora-release-identity-coreos = 1:%{version}-%{release}


%description identity-coreos
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix CoreOS.
%endif


%if %{with designsuite}
%package designsuite
Summary:        Base package for Asahi Fedora Remix Design Suite specific default configurations

RemovePathPostfixes: .designsuite
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Provides:       system-release-product

Obsoletes:      fedora-release-designsuite < 1:%{version}-%{release}
Provides:       fedora-release-designsuite = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-designsuite if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-designsuite


%description designsuite
Provides a base package for Asahi Fedora Remix Design Suite specific configuration files to
depend on.


%package identity-designsuite
Summary:        Package providing the identity for Asahi Fedora Remix Design Suite Lab

RemovePathPostfixes: .designsuite
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-designsuite = %{version}-%{release}

Obsoletes:      fedora-release-identity-designsuite < 1:%{version}-%{release}
Provides:       fedora-release-identity-designsuite = 1:%{version}-%{release}


%description identity-designsuite
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Design Suite Lab.
%endif


%if %{with eln}
%package eln
Summary:        Base package for Asahi Fedora Remix ELN specific default configurations

RemovePathPostfixes: .eln
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:eln)
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Provides:       system-release-product
Requires:       fedora-repos-eln

Obsoletes:      fedora-release-eln < 1:%{version}-%{release}
Provides:       fedora-release-eln = 1:%{version}-%{release}

Obsoletes:      redhat-release
Provides:       redhat-release

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-eln if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-eln


%description eln
Provides a base package for Asahi Fedora Remix ELN specific configuration files to
depend on.


%package identity-eln
Summary:        Package providing the identity for Asahi Fedora Remix ELN

# When running a compose for ELN, we want to make sure that we pull in the
# correct templates when lorax is installed. This Suggests: will clue
# libdnf to use this set of templates instead of lorax-templates-generic.
Suggests: lorax-templates-rhel

RemovePathPostfixes: .eln
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-eln = %{version}-%{release}

Obsoletes:      fedora-release-identity-eln < 1:%{version}-%{release}
Provides:       fedora-release-identity-eln = 1:%{version}-%{release}


%description identity-eln
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix ELN.
%endif


%if %{with iot}
%package iot
Summary:        Base package for Asahi Fedora Remix IoT specific default configurations

RemovePathPostfixes: .iot
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-iot < 1:%{version}-%{release}
Provides:       fedora-release-iot = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-iot if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-iot


%description iot
Provides a base package for Asahi Fedora Remix IoT specific configuration files to
depend on as well as IoT system defaults.


%package identity-iot
Summary:        Package providing the identity for Asahi Fedora Remix IoT Edition

RemovePathPostfixes: .iot
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-iot = %{version}-%{release}

Obsoletes:      fedora-release-identity-iot < 1:%{version}-%{release}
Provides:       fedora-release-identity-iot = 1:%{version}-%{release}


%description identity-iot
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix IoT Edition.
%endif


%if %{with kde}
%package kde
Summary:        Base package for Asahi Fedora Remix KDE Plasma-specific default configurations

RemovePathPostfixes: .kde
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-kde < 1:%{version}-%{release}
Provides:       fedora-release-kde = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-kde if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-kde


%description kde
Provides a base package for Asahi Fedora Remix KDE Plasma-specific configuration files to
depend on as well as KDE Plasma system defaults.


%package identity-kde
Summary:        Package providing the identity for Asahi Fedora Remix KDE Plasma Spin

RemovePathPostfixes: .kde
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-kde = %{version}-%{release}

Obsoletes:      fedora-release-identity-kde < 1:%{version}-%{release}
Provides:       fedora-release-identity-kde = 1:%{version}-%{release}


%description identity-kde
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix KDE Plasma Spin.
%endif


%if %{with matecompiz}
%package matecompiz
Summary:        Base package for Asahi Fedora Remix MATE-Compiz-specific default configurations

RemovePathPostfixes: .matecompiz
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-matecompiz < 1:%{version}-%{release}
Provides:       fedora-release-matecompiz = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-matecompiz if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-matecompiz


%description matecompiz
Provides a base package for Asahi Fedora Remix MATE-compiz-specific configuration files to
depend on as well as MATE-Compiz system defaults.


%package identity-matecompiz
Summary:        Package providing the identity for Asahi Fedora Remix MATE-Compiz Spin

RemovePathPostfixes: .matecompiz
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-matecompiz = %{version}-%{release}

Obsoletes:      fedora-release-identity-matecompiz < 1:%{version}-%{release}
Provides:       fedora-release-identity-matecompiz = 1:%{version}-%{release}


%description identity-matecompiz
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix MATE-Compiz.
%endif


%if %{with server}
%package server
Summary:        Base package for Asahi Fedora Remix Server-specific default configurations

RemovePathPostfixes: .server
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-server < 1:%{version}-%{release}
Provides:       fedora-release-server = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-server if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-server


%description server
Provides a base package for Asahi Fedora Remix Server-specific configuration files to
depend on.


%package identity-server
Summary:        Package providing the identity for Asahi Fedora Remix Server Edition

RemovePathPostfixes: .server
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-server = %{version}-%{release}

Obsoletes:      fedora-release-identity-server < 1:%{version}-%{release}
Provides:       fedora-release-identity-server = 1:%{version}-%{release}


%description identity-server
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Server Edition.
%endif


%if %{with silverblue}
%package silverblue
Summary:        Base package for Asahi Fedora Remix Silverblue-specific default configurations

RemovePathPostfixes: .silverblue
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Requires:       asahi-fedora-remix-release-ostree-desktop = %{version}-%{release}

Obsoletes:      fedora-release-silverblue < 1:%{version}-%{release}
Provides:       fedora-release-silverblue = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-silverblue if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-silverblue


%description silverblue
Provides a base package for Asahi Fedora Remix Silverblue-specific configuration files to
depend on as well as Silverblue system defaults.


%package identity-silverblue
Summary:        Package providing the identity for Asahi Fedora Remix Silverblue

RemovePathPostfixes: .silverblue
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-silverblue = %{version}-%{release}


%description identity-silverblue
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Silverblue.
%endif


%if %{with kinoite}
%package kinoite
Summary:        Base package for Asahi Fedora Remix Kinoite-specific default configurations

RemovePathPostfixes: .kinoite
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Requires:       asahi-fedora-remix-release-ostree-desktop = %{version}-%{release}

Obsoletes:      fedora-release-kinoite < 1:%{version}-%{release}
Provides:       fedora-release-kinoite = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-kinoite if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-kinoite


%description kinoite
Provides a base package for Asahi Fedora Remix Kinoite-specific configuration files to
depend on as well as Kinoite system defaults.


%package identity-kinoite
Summary:        Package providing the identity for Asahi Fedora Remix Kinoite

RemovePathPostfixes: .kinoite
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-kinoite = %{version}-%{release}

Obsoletes:      fedora-release-identity-kinoite < 1:%{version}-%{release}
Provides:       fedora-release-identity-kinoite = 1:%{version}-%{release}


%description identity-kinoite
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Kinoite.
%endif


%if %{with ostree_desktop}
%package ostree-desktop
Summary:        Configuration package for rpm-ostree variants to add rpm-ostree polkit rules

%description ostree-desktop
Configuration package for rpm-ostree variants to add rpm-ostree polkit rules
%endif


%if %{with snappy}
%package snappy
Summary:        Base package for Asahi Fedora Remix snap specific default configurations

RemovePathPostfixes: .snappy
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-snappy < 1:%{version}-%{release}
Provides:       fedora-release-snappy = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-snappy if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-snappy


%description snappy
Provides a base package for Asahi Fedora Remix snap specific configuration files to
depend on as well as Snappy system defaults.


%package identity-snappy
Summary:        Package providing the identity for Asahi Fedora Remix Snappy environments

RemovePathPostfixes: .snappy
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-snappy = %{version}-%{release}

Obsoletes:      fedora-release-identity-snappy < 1:%{version}-%{release}
Provides:       fedora-release-identity-snappy = 1:%{version}-%{release}


%description identity-snappy
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix's snappy environment.
%endif


%if %{with soas}
%package soas
Summary:        Base package for Asahi Fedora Remix Sugar on a Stick-specific default configurations

RemovePathPostfixes: .soas
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-soas < 1:%{version}-%{release}
Provides:       fedora-release-soas = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-soas if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-soas


%description soas
Provides a base package for Asahi Fedora Remix Sugar on a Stick-specific configuration
files to depend on as well as SoaS system defaults.


%package identity-soas
Summary:        Package providing the identity for Asahi Fedora Remix Sugar on a Stick

RemovePathPostfixes: .soas
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-soas = %{version}-%{release}

Obsoletes:      fedora-release-identity-soas < 1:%{version}-%{release}
Provides:       fedora-release-identity-soas = 1:%{version}-%{release}


%description identity-soas
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Sugar on a Stick.
%endif


%if %{with workstation}
%package workstation
Summary:        Base package for Asahi Fedora Remix Workstation-specific default configurations

RemovePathPostfixes: .workstation
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Provides:       system-release-product

Obsoletes:      fedora-release-workstation < 1:%{version}-%{release}
Provides:       fedora-release-workstation = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-workstation if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-workstation


%description workstation
Provides a base package for Asahi Fedora Remix Workstation-specific configuration files to
depend on.


%package identity-workstation
Summary:        Package providing the identity for Asahi Fedora Remix Workstation Edition

RemovePathPostfixes: .workstation
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-workstation = %{version}-%{release}

Obsoletes:      fedora-release-identity-workstation < 1:%{version}-%{release}
Provides:       fedora-release-identity-workstation = 1:%{version}-%{release}


%description identity-workstation
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Workstation Edition.
%endif


%if %{with xfce}
%package xfce
Summary:        Base package for Asahi Fedora Remix Xfce specific default configurations

RemovePathPostfixes: .xfce
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-xfce < 1:%{version}-%{release}
Provides:       fedora-release-xfce = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-xfce if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-xfce


%description xfce
Provides a base package for Asahi Fedora Remix Xfce specific configuration files to
depend on as well as Xfce system defaults.


%package identity-xfce
Summary:        Package providing the identity for Asahi Fedora Remix Xfce Spin

RemovePathPostfixes: .xfce
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-xfce = %{version}-%{release}

Obsoletes:      fedora-release-identity-xfce < 1:%{version}-%{release}
Provides:       fedora-release-identity-xfce = 1:%{version}-%{release}


%description identity-xfce
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Xfce.
%endif


%if %{with i3}
%package i3
Summary:        Base package for Asahi Fedora Remix i3 specific default configurations

RemovePathPostfixes: .i3
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-i3 < 1:%{version}-%{release}
Provides:       fedora-release-i3 = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-i3 if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-i3


%description i3
Provides a base package for Asahi Fedora Remix i3 specific configuration files to
depend on.


%package identity-i3
Summary:        Package providing the identity for Asahi Fedora Remix i3 Spin

RemovePathPostfixes: .i3
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-i3 = %{version}-%{release}

Obsoletes:      fedora-release-identity-i3 < 1:%{version}-%{release}
Provides:       fedora-release-identity-i3 = 1:%{version}-%{release}


%description identity-i3
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix i3.
%endif


%if %{with lxqt}
%package lxqt
Summary:        Base package for Asahi Fedora Remix LXQt specific default configurations

RemovePathPostfixes: .lxqt
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-lxqt < 1:%{version}-%{release}
Provides:       fedora-release-lxqt = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-lxqt if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-lxqt


%description lxqt
Provides a base package for Asahi Fedora Remix LXQt specific configuration files to
depend on as well as LXQt system defaults.


%package identity-lxqt
Summary:        Package providing the identity for Asahi Fedora Remix LXQt Spin

RemovePathPostfixes: .lxqt
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-lxqt = %{version}-%{release}

Obsoletes:      fedora-release-identity-lxqt < 1:%{version}-%{release}
Provides:       fedora-release-identity-lxqt = 1:%{version}-%{release}

%description identity-lxqt
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix LXQt.
%endif

%if %{with budgie}
%package budgie
Summary:        Base package for Asahi Fedora Remix Budgie specific default configurations

RemovePathPostfixes: .budgie
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-budgie < 1:%{version}-%{release}
Provides:       fedora-release-budgie = 1:%{version}-%{release}

# asahi-fedora-remix-release-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-budgie if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-budgie


%description budgie
Provides a base package for Asahi Fedora Remix Budgie specific configuration files to
depend on as well as Budgie system defaults.


%package identity-budgie
Summary:        Package providing the identity for Asahi Fedora Remix Budgie Spin

RemovePathPostfixes: .budgie
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-budgie = %{version}-%{release}

Obsoletes:      fedora-release-identity-budgie < 1:%{version}-%{release}
Provides:       fedora-release-identity-budgie = 1:%{version}-%{release}

%description identity-budgie
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Budgie.
%endif


%if %{with sway}
%package sway
Summary:        Base package for Asahi Fedora Remix Sway specific default configurations

RemovePathPostfixes: .sway
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}

Obsoletes:      fedora-release-sway < 1:%{version}-%{release}
Provides:       fedora-release-sway = 1:%{version}-%{release}

# asahi-fedora-remix-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-sway if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-sway


%description sway
Provides a base package for Asahi Fedora Remix Sway specific configuration files to
depend on.


%package identity-sway
Summary:        Package providing the identity for Asahi Fedora Remix Sway Spin

RemovePathPostfixes: .sway
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-sway = %{version}-%{release}

Obsoletes:      fedora-release-identity-sway < 1:%{version}-%{release}
Provides:       fedora-release-identity-sway = 1:%{version}-%{release}


%description identity-sway
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Sway.
%endif


%if %{with sericea}
%package sericea
Summary:        Base package for Asahi Fedora Remix Sericea specific default configurations

RemovePathPostfixes: .sericea
Provides:       asahi-fedora-remix-release = %{version}-%{release}
Provides:       asahi-fedora-remix-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       asahi-fedora-remix-release-common = %{version}-%{release}
Requires:       asahi-fedora-remix-release-ostree-desktop = %{version}-%{release}

Obsoletes:      fedora-release-sericea < 1:%{version}-%{release}
Provides:       fedora-release-sericea = 1:%{version}-%{release}

# asahi-fedora-remix-common Requires: asahi-fedora-remix-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# asahi-fedora-remix-release-identity-sericea if nothing else is already doing so.
Recommends:     asahi-fedora-remix-release-identity-sericea


%description sericea
Provides a base package for Asahi Fedora Remix Sericea specific configuration
files to depend on.


%package identity-sericea
Summary:        Package providing the identity for Asahi Fedora Remix Sericea

RemovePathPostfixes: .sericea
Provides:       asahi-fedora-remix-release-identity = %{version}-%{release}
Conflicts:      asahi-fedora-remix-release-identity
Requires(meta): asahi-fedora-remix-release-sericea = %{version}-%{release}

Obsoletes:      fedora-release-identity-sericea < 1:%{version}-%{release}
Provides:       fedora-release-identity-sericea = 1:%{version}-%{release}

%description identity-sericea
Provides the necessary files for an Asahi Fedora Remix installation that is identifying
itself as Asahi Fedora Remix Sericea.
%endif


%prep
mkdir -p licenses
sed 's|@@VERSION@@|%{dist_version}|g' %{SOURCE2} >licenses/Fedora-Legal-README.txt

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Fedora release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/fedora-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/fedora-release %{buildroot}%{_sysconfdir}/fedora-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s fedora-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s fedora-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}
%define starts_with(str,prefix) (%{expand:%%{lua:print(starts_with(%1, %2) and "1" or "0")}})
%if %{starts_with "a%{release}" "a0"}
  %global prerelease \ Prerelease
%endif

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor Fedora Asahi
%global dist_name   Asahi Fedora Linux Remix

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://pagure.io/fedora-asahi/project

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://bugzilla.redhat.com/

# debuginfod server, as used in elfutils.spec.
%global dist_debuginfod_url https://debuginfod.fedoraproject.org/
# -------------------------------------------------------------------------

cat << EOF >> os-release
NAME="%{dist_name}"
VERSION="%{dist_version} (%{release_name}%{?prerelease})"
ID=asahi-fedora-remix
ID_LIKE=fedora
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PLATFORM_ID="platform:f%{dist_version}"
PRETTY_NAME="Asahi Fedora Linux Remix %{dist_version} (%{release_name}%{?prerelease})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:asahi-fedora-remix:%{dist_version}"
DEFAULT_HOSTNAME="fedora"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora/%{doc_version}/system-administrators-guide/"
SUPPORT_URL="https://ask.fedoraproject.org/"
BUG_REPORT_URL="%{dist_bug_report_url}"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different editions

%if %{with basic}
# Basic
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic
%endif

%if %{with cinnamon}
# Cinnamon
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.cinnamon
echo "VARIANT=\"Cinnamon\"" >> %{buildroot}%{_prefix}/lib/os-release.cinnamon
echo "VARIANT_ID=cinnamon" >> %{buildroot}%{_prefix}/lib/os-release.cinnamon
sed -i -e "s|(%{release_name}%{?prerelease})|(Cinnamon%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.cinnamon
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Cinnamon/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cinnamon
%endif

%if %{with cloud}
# Cloud
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT=\"Cloud Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.cloud
echo "VARIANT_ID=cloud" >> %{buildroot}%{_prefix}/lib/os-release.cloud
sed -i -e "s|(%{release_name}%{?prerelease})|(Cloud Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.cloud
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Cloud/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cloud
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.cloud
%endif

%if %{with compneuro}
# Comp Neuro
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.compneuro
echo "VARIANT=\"Comp Neuro\"" >> %{buildroot}%{_prefix}/lib/os-release.compneuro
echo "VARIANT_ID=compneuro" >> %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e "s|(%{release_name}%{?prerelease})|(CompNeuro%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://neuro.fedoraproject.org"|' %{buildroot}%{_prefix}/lib/os-release.compneuro
sed -i -e 's|HOME_URL=.*|HOME_URL="https://labs.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.compneuro
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/CompNeuro/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.compneuro
%endif

%if %{with container}
# Container
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT=\"Container Image\"" >> %{buildroot}%{_prefix}/lib/os-release.container
echo "VARIANT_ID=container" >> %{buildroot}%{_prefix}/lib/os-release.container
sed -i -e "s|(%{release_name}%{?prerelease})|(Container Image%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.container
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Container/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.container
%endif

%if %{with coreos}
# CoreOS
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.coreos
echo "VARIANT=\"CoreOS\"" >> %{buildroot}%{_prefix}/lib/os-release.coreos
echo "VARIANT_ID=coreos" >> %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e "s|(%{release_name}%{?prerelease})|(CoreOS%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-coreos/"|' %{buildroot}%{_prefix}/lib/os-release.coreos
sed -i -e 's|HOME_URL=.*|HOME_URL="https://getfedora.org/coreos/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|SUPPORT_URL=.*|SUPPORT_URL="https://github.com/coreos/fedora-coreos-tracker/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://github.com/coreos/fedora-coreos-tracker/"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Fedora CoreOS %{dist_version}"|' %{buildroot}/%{_prefix}/lib/os-release.coreos
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/CoreOS/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.coreos
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.coreos
install -Dm0644 %{SOURCE22} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
%endif


%if %{with designsuite}
# Design Suite
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.designsuite
echo "VARIANT=\"Design Suite\"" >> %{buildroot}%{_prefix}/lib/os-release.designsuite
echo "VARIANT_ID=designsuite" >> %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e "s|(%{release_name}%{?prerelease})|(Design Suite%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://fedoraproject.org/wiki/Design_Suite"|' %{buildroot}%{_prefix}/lib/os-release.designsuite
sed -i -e 's|HOME_URL=.*|HOME_URL="https://labs.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.designsuite
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/DesignSuite/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.designsuite
%endif

%if %{with eln}
# ELN
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT=\"ELN\"" >> %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT_ID=eln" >> %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e 's|PLATFORM_ID=.*|PLATFORM_ID="platform:eln"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Fedora ELN"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/eln/"|' %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.eln
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/ELN/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif

%if %{with iot}
# IoT
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.iot
echo "VARIANT=\"IoT Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.iot
echo "VARIANT_ID=iot" >> %{buildroot}%{_prefix}/lib/os-release.iot
sed -i -e "s|(%{release_name}%{?prerelease})|(IoT Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.iot
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/IoT/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.iot
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.iot
install -p %{SOURCE23} %{buildroot}/%{_prefix}/lib/
install -Dm0644 %{SOURCE18} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE24} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
%endif

%if %{with kde}
# KDE Plasma
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT=\"KDE Plasma\"" >> %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT_ID=kde" >> %{buildroot}%{_prefix}/lib/os-release.kde
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
# Add plasma-desktop to dnf protected packages list for KDE
install -Dm0644 %{SOURCE25} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with matecompiz}
# MATE-Compiz
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.matecompiz
echo "VARIANT=\"MATE-Compiz\"" >> %{buildroot}%{_prefix}/lib/os-release.matecompiz
echo "VARIANT_ID=matecompiz" >> %{buildroot}%{_prefix}/lib/os-release.matecompiz
sed -i -e "s|(%{release_name}%{?prerelease})|(MATE-Compiz%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.matecompiz
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/MATE-Compiz/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.matecompiz
%endif

%if %{with server}
# Server
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT=\"Server Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT_ID=server" >> %{buildroot}%{_prefix}/lib/os-release.server
sed -i -e "s|(%{release_name}%{?prerelease})|(Server Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.server
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Server/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.server
install -Dm0644 %{SOURCE14} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif

%if %{with silverblue}
# Silverblue
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.silverblue
echo "VARIANT=\"Silverblue\"" >> %{buildroot}%{_prefix}/lib/os-release.silverblue
echo "VARIANT_ID=silverblue" >> %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -i -e "s|(%{release_name}%{?prerelease})|(Silverblue%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-silverblue/"|' %{buildroot}%{_prefix}/lib/os-release.silverblue
sed -i -e 's|HOME_URL=.*|HOME_URL="https://silverblue.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.silverblue
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://github.com/fedora-silverblue/issue-tracker/issues"|' %{buildroot}/%{_prefix}/lib/os-release.silverblue
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Silverblue/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.silverblue
%endif

%if %{with kinoite}
# Kinoite
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kinoite
echo "VARIANT=\"Kinoite\"" >> %{buildroot}%{_prefix}/lib/os-release.kinoite
echo "VARIANT_ID=kinoite" >> %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -i -e "s|(%{release_name}%{?prerelease})|(Kinoite%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora-kinoite/"|' %{buildroot}%{_prefix}/lib/os-release.kinoite
sed -i -e 's|HOME_URL=.*|HOME_URL="https://kinoite.fedoraproject.org"|' %{buildroot}/%{_prefix}/lib/os-release.kinoite
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://pagure.io/fedora-kde/SIG/issues"|' %{buildroot}/%{_prefix}/lib/os-release.kinoite
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Kinoite/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kinoite
%endif

%if %{with snappy}
# Snappy
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.snappy
echo "VARIANT=\"Snappy\"" >> %{buildroot}%{_prefix}/lib/os-release.snappy
echo "VARIANT_ID=snappy" >> %{buildroot}%{_prefix}/lib/os-release.snappy
sed -i -e "s|(%{release_name}%{?prerelease})|(Snappy%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.snappy
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Snappy/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.snappy
%endif

%if %{with soas}
# Sugar on a Stick
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.soas
echo "VARIANT=\"Sugar on a Stick\"" >> %{buildroot}%{_prefix}/lib/os-release.soas
echo "VARIANT_ID=soas" >> %{buildroot}%{_prefix}/lib/os-release.soas
sed -i -e "s|(%{release_name}%{?prerelease})|(Sugar on a Stick%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.soas
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Sugar/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.soas
%endif

%if %{with workstation}
# Workstation
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT=\"Workstation Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT_ID=workstation" >> %{buildroot}%{_prefix}/lib/os-release.workstation
sed -i -e "s|(%{release_name}%{?prerelease})|(Workstation Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.workstation
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Workstation/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
# Add Fedora Workstation dnf protected packages list
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with silverblue} || %{with workstation}
# Silverblue and Workstation
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
# Override the list of enabled gnome-shell extensions for Workstation
install -Dm0644 %{SOURCE16} -t %{buildroot}%{_datadir}/glib-2.0/schemas/
%endif

%if %{with kde} || %{with kinoite}
# Common desktop preset and spin specific preset
install -Dm0644 %{SOURCE26} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif

%if %{with ostree_desktop}
# Install rpm-ostree polkit rules
install -Dm0644 %{SOURCE17} -t %{buildroot}%{_datadir}/polkit-1/rules.d/
%endif

%if %{with iot} || %{with ostree_desktop}
# Statically enable rpm-ostree-countme timer
install -dm0755 %{buildroot}%{_unitdir}/timers.target.wants/
ln -s ../rpm-ostree-countme.timer %{buildroot}%{_unitdir}/timers.target.wants/
%endif

%if %{with xfce}
# Xfce
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT=\"Xfce\"" >> %{buildroot}%{_prefix}/lib/os-release.xfce
echo "VARIANT_ID=xfce" >> %{buildroot}%{_prefix}/lib/os-release.xfce
sed -i -e "s|(%{release_name}%{?prerelease})|(Xfce%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.xfce
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Xfce/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.xfce
%endif

%if %{with i3}
cp -p os-release %{buildroot}%{_prefix}/lib/os-release.i3
echo "VARIANT=\"i3\"" >> %{buildroot}%{_prefix}/lib/os-release.i3
echo "VARIANT_ID=i3" >> %{buildroot}%{_prefix}/lib/os-release.i3
sed -i -e "s|(%{release_name}%{?prerelease})|(i3%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.i3
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/i3/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.i3
%endif

%if %{with lxqt}
# LXQt
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.lxqt
echo "VARIANT=\"LXQt\"" >> %{buildroot}%{_prefix}/lib/os-release.lxqt
echo "VARIANT_ID=lxqt" >> %{buildroot}%{_prefix}/lib/os-release.lxqt
sed -i -e "s|(%{release_name}%{?prerelease})|(LXQt%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.lxqt
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/LXQt/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.lxqt
%endif

%if %{with budgie}
# Budgie
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.budgie
echo "VARIANT=\"Budgie\"" >> %{buildroot}%{_prefix}/lib/os-release.budgie
echo "VARIANT_ID=budgie" >> %{buildroot}%{_prefix}/lib/os-release.budgie
sed -i -e "s|(%{release_name}%{?prerelease})|(Budgie%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.budgie
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Budgie/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.budgie
%endif

%if %{with sway}
cp -p os-release %{buildroot}%{_prefix}/lib/os-release.sway
echo "VARIANT=\"Sway\"" >> %{buildroot}%{_prefix}/lib/os-release.sway
echo "VARIANT_ID=sway" >> %{buildroot}%{_prefix}/lib/os-release.sway
sed -i -e "s|(%{release_name}%{?prerelease})|(Sway%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.sway
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://gitlab.com/fedora/sigs/sway/SIG/-/issues"|' %{buildroot}/%{_prefix}/lib/os-release.sway
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Sway/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.sway
%endif

%if %{with sericea}
cp -p os-release %{buildroot}%{_prefix}/lib/os-release.sericea
echo "VARIANT=\"Sericea\"" >> %{buildroot}%{_prefix}/lib/os-release.sericea
echo "VARIANT_ID=sericea" >> %{buildroot}%{_prefix}/lib/os-release.sericea
sed -i -e "s|(%{release_name}%{?prerelease})|(Sericea%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.sericea
sed -i -e 's|BUG_REPORT_URL=.*|BUG_REPORT_URL="https://gitlab.com/fedora/sigs/sway/SIG/-/issues"|' %{buildroot}/%{_prefix}/lib/os-release.sericea
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Sericea/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.sericea
%endif

# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release


# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%if 0%{?eln}
%%rhel              %{rhel_dist_version}
%%el%{rhel_dist_version}                1
# Although eln is set in koji tags, we put it in the macros.dist file for local and mock builds.
%%eln              %{eln}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%%{eln}%%{?with_bootstrap:%{__bootstrap}}
%else
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.fc%%{fedora}%%{?with_bootstrap:%{__bootstrap}}
%endif
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
%%dist_debuginfod_url %{dist_debuginfod_url}
EOF

# Install licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE

# Default system wide
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s --relative %{buildroot}%{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/fedoraproject.org

# Create the copr vendor file
install -d %{buildroot}%{_datadir}/dnf/plugins
cat >> %{buildroot}%{_datadir}/dnf/plugins/copr.vendor.conf << EOF
[main]
distribution = fedora
releasever = %{releasever}
EOF


%files common
%license licenses/LICENSE licenses/Fedora-Legal-README.txt
%{_prefix}/lib/fedora-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/fedora-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d
%dir %{_datadir}/dnf/plugins
%{_datadir}/dnf/plugins/copr.vendor.conf


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif


%if %{with cinnamon}
%files cinnamon
%files identity-cinnamon
%{_prefix}/lib/os-release.cinnamon
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cinnamon
%endif


%if %{with cloud}
%files cloud
%files identity-cloud
%{_prefix}/lib/os-release.cloud
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.cloud
%endif


%if %{with compneuro}
%files compneuro
%files identity-compneuro
%{_prefix}/lib/os-release.compneuro
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.compneuro
%endif


%if %{with container}
%files container
%files identity-container
%{_prefix}/lib/os-release.container
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.container
%endif


%if %{with coreos}
%files coreos
%files identity-coreos
%{_prefix}/lib/systemd/system-preset/80-coreos.preset
%{_prefix}/lib/systemd/system.conf.d/longer-default-shutdown-timeout.conf
%{_prefix}/lib/systemd/user.conf.d/longer-default-shutdown-timeout.conf
%{_prefix}/lib/os-release.coreos
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.coreos
%endif


%if %{with designsuite}
%files designsuite
%files identity-designsuite
%{_prefix}/lib/os-release.designsuite
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.designsuite
%endif


%if %{with eln}
%files eln
%files identity-eln
%{_prefix}/lib/os-release.eln
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif


%if %{with iot}
%files iot
%files identity-iot
%{_prefix}/lib/os-release.iot
%{_prefix}/lib/systemd/system-preset/80-iot.preset
%{_prefix}/lib/systemd/user-preset/80-iot-user.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.iot
%{_prefix}/lib/zezere-ignition-url
%{_unitdir}/timers.target.wants/rpm-ostree-countme.timer
%endif


%if %{with kde}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde
%{_prefix}/lib/systemd/system-preset/80-kde.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
%{_sysconfdir}/dnf/protected.d/plasma-desktop.conf
%endif


%if %{with matecompiz}
%files matecompiz
%files identity-matecompiz
%{_prefix}/lib/os-release.matecompiz
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.matecompiz
%endif


%if %{with server}
%files server
%files identity-server
%{_prefix}/lib/os-release.server
%{_prefix}/lib/systemd/system-preset/80-server.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
%endif


%if %{with silverblue}
%files silverblue
%files identity-silverblue
%{_prefix}/lib/os-release.silverblue
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.silverblue
# Keep this in sync with workstation below
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%{_unitdir}/timers.target.wants/rpm-ostree-countme.timer
%endif


%if %{with kinoite}
%files kinoite
%files identity-kinoite
%{_prefix}/lib/os-release.kinoite
%{_prefix}/lib/systemd/system-preset/80-kde.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kinoite
%{_unitdir}/timers.target.wants/rpm-ostree-countme.timer
%endif


%if %{with ostree_desktop}
%files ostree-desktop
%attr(0644,root,root) %{_prefix}/share/polkit-1/rules.d/org.projectatomic.rpmostree1.rules
%endif


%if %{with snappy}
%files snappy
%files identity-snappy
%{_prefix}/lib/os-release.snappy
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.snappy
%endif


%if %{with soas}
%files soas
%files identity-soas
%{_prefix}/lib/os-release.soas
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.soas
%endif


%if %{with workstation}
%files workstation
%files identity-workstation
%{_prefix}/lib/os-release.workstation
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
%{_sysconfdir}/dnf/protected.d/fedora-workstation.conf
# Keep this in sync with silverblue above
%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%endif


%if %{with xfce}
%files xfce
%files identity-xfce
%{_prefix}/lib/os-release.xfce
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.xfce
%endif


%if %{with i3}
%files i3
%files identity-i3
%{_prefix}/lib/os-release.i3
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.i3
%endif


%if %{with lxqt}
%files lxqt
%files identity-lxqt
%{_prefix}/lib/os-release.lxqt
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.lxqt
%endif

%if %{with budgie}
%files budgie
%files identity-budgie
%{_prefix}/lib/os-release.budgie
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.budgie
%endif


%if %{with sway}
%files sway
%files identity-sway
%{_prefix}/lib/os-release.sway
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.sway
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%endif


%if %{with sericea}
%files sericea
%files identity-sericea
%{_prefix}/lib/os-release.sericea
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.sericea
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%{_unitdir}/timers.target.wants/rpm-ostree-countme.timer
%endif


%changelog
%autochangelog
