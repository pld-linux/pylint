# TODO:
# - include examples in package

# Conditional build:
%bcond_with	python2	# Python 2.x version
%bcond_without	python3	# Python 3.x version (available as 'py3lint')
%bcond_without	doc	# Documentation
%bcond_with	tests	# unit tests

Summary:	Python 2 tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona 2 sprawdzające zgodność modułu ze standardem kodowania
Name:		pylint
Version:	2.4.3
Release:	2
License:	GPL v2+
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pylint/
Source0:	https://github.com/PyCQA/pylint/archive/%{name}-%{version}.tar.gz
# Source0-md5:	742ac2d6e2528e0d2f52edadd31c837b
URL:		http://www.pylint.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:3.5
BuildRequires:	python-modules >= 1:3.5
BuildRequires:	python-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python-astroid >= 2.3.0
BuildRequires:	python-astroid < 2.4
BuildRequires:	python-isort >= 4.2.5
BuildRequires:	python-isort < 5
BuildRequires:	python-mccabe >= 0.6
BuildRequires:	python-mccabe < 0.7
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 7.0
%if %{with tests}
BuildRequires:	python3-astroid >= 1.5.3
BuildRequires:	python3-isort >= 4.2.5
BuildRequires:	python3-isort < 5
BuildRequires:	python3-mccabe >= 0.6
BuildRequires:	python3-mccabe < 0.7
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-pylint = %{version}-%{release}
Suggests:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# /etc/pylintrc is deliberately packaged to both packages with same name
%define		_duplicate_files_terminate_build	0

%description
Python 2 tool that checks if a module satisfy a coding standard.

%description -l pl.UTF-8
Narzędzie Pythona 2 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

%package -n python-pylint
Summary:	Python 2 tool that checks if a module satisfy a coding standard (modules)
Summary(pl.UTF-8):	Narzędzie Pythona sprawdzające zgodność modułu ze standardem kodowania (moduły)
Group:		Libraries/Python

%description -n python-pylint
Python 2 tool that checks if a module satisfy a coding standard.

This package contains only the Python modules used by the tool.

%description -n python-pylint -l pl.UTF-8
Narzędzie Pythona 2 sprawdzające zgodność modułów napisanych w języku
Python z regułami tworzenia kodu źródłowego.

Ten pakiet zawiera tylko moduły Pythona używane przez to narzędzie.

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
%setup -q -n pylint-pylint-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%if %{with doc}
%{__make} -C doc text \
	PYTHONPATH=$PWD
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1}

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/epylint $RPM_BUILD_ROOT%{_bindir}/epy3lint
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pylint $RPM_BUILD_ROOT%{_bindir}/py3lint
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pyreverse $RPM_BUILD_ROOT%{_bindir}/py3reverse
cp -p man/epylint.1 $RPM_BUILD_ROOT%{_mandir}/man1/epy3lint.1
cp -p man/pylint.1 $RPM_BUILD_ROOT%{_mandir}/man1/py3lint.1
cp -p man/pyreverse.1 $RPM_BUILD_ROOT%{_mandir}/man1/py3reverse.1
%endif

%if %{with python2}
%py_install

%py_postclean
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

cp -p examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epylint
%attr(755,root,root) %{_bindir}/pylint
%attr(755,root,root) %{_bindir}/pyreverse
%attr(755,root,root) %{_bindir}/symilar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{_mandir}/man1/epylint.1*
%{_mandir}/man1/pylint.1*
%{_mandir}/man1/pyreverse.1*
%{_mandir}/man1/symilar.1*

%files -n python-pylint
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt ChangeLog README.rst examples/*
%{py_sitescriptdir}/pylint
%{py_sitescriptdir}/pylint-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n py3lint
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/epy3lint
%attr(755,root,root) %{_bindir}/py3lint
%attr(755,root,root) %{_bindir}/py3reverse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{_mandir}/man1/epy3lint.1*
%{_mandir}/man1/py3lint.1*
%{_mandir}/man1/py3reverse.1*

%files -n python3-pylint
%defattr(644,root,root,755)
%doc CONTRIBUTORS.txt ChangeLog README.rst examples/*
%{py3_sitescriptdir}/pylint
%{py3_sitescriptdir}/pylint-%{version}-py*.egg-info
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc doc/_build/text/*
%endif
