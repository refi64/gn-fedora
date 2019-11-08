%define commit ad9e442d

Name:    gn
Version: 1634
Release: 1%{?dist}.%{commit}
Summary: A meta build system

License: BSD-3-Clause
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: python3

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

Source0: https://gn.googlesource.com/gn/+archive/%{commit}.tar.gz#/gn.tar.gz
Patch0: 0001-Use-Python-3-in-the-unit-tests.patch

%description
GN is a meta-build system that generates build files for Ninja.

%prep
%setup -q -c -n gn
%patch0 -p1

%build

%set_build_flags
export CC=gcc
export CXX=g++

python3 build/gen.py --no-last-commit-position --no-static-libstdc++ --no-strip

# last_commit_position.h generation wants Git, so write it manually.
cat > out/last_commit_position.h <<EOF
#ifndef OUT_LAST_COMMIT_POSITION_H_
#define OUT_LAST_COMMIT_POSITION_H_

#define LAST_COMMIT_POSITION "%{version} (%{commit})"

#endif  // OUT_LAST_COMMIT_POSITION_H_
EOF

%ninja_build -C out

%install
install -Dm 755 out/gn %{buildroot}/%{_bindir}/gn

%check
out/gn_unittests

%files
%{_bindir}/gn
