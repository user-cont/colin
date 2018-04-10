%global pypi_name colin

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           %{pypi_name}
Version:        0.0.3
Release:        1%{?dist}
Summary:        Tool to check generic rules/best-practices for containers/images/dockerfiles.

License:        GPLv3+
URL:            https://github.com/user-cont/colin
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch


%description
`colin` is a tool to check generic rules/best-practices
for containers/images/dockerfiles.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-docker
Requires:       python3-requests
Requires:       python3-pyxattr
#Requires:       conu
Recommends:     atomic
Recommends:     docker

%description -n python3-%{pypi_name}
`colin` as a tool to check generic rules/best-practices
for containers/images/dockerfiles.

%package -n %{pypi_name}-doc
Summary:        colin documentation

%description -n %{pypi_name}-doc
Documentation for colin.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info/
%{_datadir}/%{pypi_name}/*
%{_datadir}/bash-completion/completions/%{pypi_name}
%exclude %{python3_sitelib}/tests

%files -n %{pypi_name}-doc
%doc docs
%license LICENSE
%doc README.md

%changelog
* Mon Apr 09 2018 Petr Hracek <phracek@redhat.com> - 0.0.3-1
- Initial package.
