#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona sprawdzające zgodność modułu ze standardem kodowania
Name:		pylint
Version:	2.12.2
Release:	1
License:	GPL v2+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pylint/
Source0:	https://github.com/PyCQA/pylint/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	655504bea72f87c9fbe604fcbfb5434f
URL:		http://www.pylint.org/
BuildRequires:	python3-astroid >= 2.5.1
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-mccabe
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:7.0
%if %{with tests} || %{with doc}
BuildRequires:	python3-isort >= 4.2.5
BuildRequires:	python3-mccabe >= 0.6
BuildRequires:	python3-platformdirs >= 2.2.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	py3lint = %{version}-%{release}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tool that checks if a module satisfy a coding standard.

%description -l pl.UTF-8
Narzędzie Pythona sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

%package -n py3lint
Summary:	Python 3 tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona 3 sprawdzające zgodność modułu ze standardem kodowania
Group:		Development/Languages/Python
Requires:	python3-pylint = %{version}-%{release}
Obsoletes:	pylint-python3 < 1.0.0-2

%description -n py3lint
Python 3 tool that checks if a module satisfy a coding standard.

Python 3.x version, available via the 'py3lint' command.

%description -n py3lint -l pl.UTF-8
Narzędzie Pythona 3 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Wersja dla Pythona 3.x, dostępna przez polecenie 'py3lint'.

%package -n python3-pylint
Summary:	Python 3 tool that checks if a module satisfy a coding standard (moduły)
Summary(pl.UTF-8):	Narzędzie Pythona 3 sprawdzające zgodność modułu ze standardem kodowania (modules)
Group:		Libraries/Python

%description -n python3-pylint
Python 3 tool that checks if a module satisfy a coding standard.

This package contains only the Python modules used by the tool.

%description -n python3-pylint -l pl.UTF-8
Narzędzie Pythona 3 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Ten pakiet zawiera tylko moduły Pythona używane przez to narzędzie.

%package doc
Summary:	Documentation for pylint
Summary(pl.UTF-8):	Dokumentacja do pylinta
Group:		Documentation

%description doc
Documentation for pylint.

%description doc -l pl.UTF-8
Dokumentacja do pylinta.

%prep
%setup -q

%build
%py3_build

%if %{with doc}
%{__make} -C doc text \
	PYTHONPATH=$PWD
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%py3_install

for tool in epylint pylint pyreverse symilar ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${tool} $RPM_BUILD_ROOT%{_bindir}/${tool}-3
	ln -s ${tool}-3 $RPM_BUILD_ROOT%{_bindir}/${tool}
done
# old PLD package compatibility
ln -s epylint-3 $RPM_BUILD_ROOT%{_bindir}/epy3lint
ln -s pylint-3 $RPM_BUILD_ROOT%{_bindir}/py3lint
ln -s pyreverse-3 $RPM_BUILD_ROOT%{_bindir}/py3reverse

cp -p examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epylint
%attr(755,root,root) %{_bindir}/pylint
%attr(755,root,root) %{_bindir}/pyreverse
%attr(755,root,root) %{_bindir}/symilar

%files -n py3lint
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epylint-3
%attr(755,root,root) %{_bindir}/pylint-3
%attr(755,root,root) %{_bindir}/pyreverse-3
%attr(755,root,root) %{_bindir}/symilar-3
%attr(755,root,root) %{_bindir}/epy3lint
%attr(755,root,root) %{_bindir}/py3lint
%attr(755,root,root) %{_bindir}/py3reverse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc

%files -n python3-pylint
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt ChangeLog README.rst examples
%{py3_sitescriptdir}/pylint
%{py3_sitescriptdir}/pylint-%{version}-py*.egg-info

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/_build/text/*
%endif
