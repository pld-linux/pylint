# TODO:
# - include examples in package

# Conditional build:
%bcond_without  python2 # Python 2.x version
%bcond_without  python3 # Python 3.x version (available as 'py3lint')
%bcond_without	doc # Documentation

Summary:	Python 2 tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Narzędzie Pythona 2 sprawdzające zgodność modułu ze standardem kodowania
Name:		pylint
Version:	2.2.0
Release:	1
License:	GPL v2+
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/pypi/pylint
Source0:	https://github.com/PyCQA/pylint/archive/%{name}-%{version}.tar.gz
# Source0-md5:	32908fa8ddc2cf1db69d66413fab8db7
URL:		http://www.pylint.org/
%if %{with python2}
BuildRequires:	python-astroid >= 1.5.3
BuildRequires:	python-certifi >= 2017.4.17
BuildRequires:	python-chardet >= 3.0.2
BuildRequires:	python-devel
BuildRequires:	python-idna >= 2.5
BuildRequires:	python-isort
BuildRequires:	python-lazy-object-proxy
BuildRequires:	python-mccabe
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools >= 7.0
BuildRequires:	python-wrapt
#BuildConflicts:	python-chardet >= 3.1.0
#BuildConflicts:	python-idna >= 2.7
%endif
%if %{with python3}
BuildRequires:	python3-2to3
BuildRequires:	python3-astroid >= 1.5.3
BuildRequires:	python3-certifi >= 2017.4.17
BuildRequires:	python3-chardet >= 3.0.2
BuildRequires:	python3-devel
BuildRequires:	python3-idna >= 2.5
BuildRequires:	python3-isort
BuildRequires:	python3-lazy-object-proxy
BuildRequires:	python3-mccabe
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 7.0
BuildRequires:	python3-wrapt
#BuildConflicts:	python3-chardet >= 3.1.0
#BuildConflicts:	python3-idna >= 2.7
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg
Requires:	python-pylint = %{version}-%{release}
Suggests:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# /etc/pylintrc is deliberately packaged to both packages with same name
%define		_duplicate_files_terminate_build	0

# current Python 3.x provides all these
%define		_noautoreq	python3egg.backports.functools-lru-cache python3egg.configparser python3egg.singledispatch

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
%doc ChangeLog README.rst examples/*
%{?with_doc:%doc doc/_build/text/*.txt}
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
%{py_sitescriptdir}/pylint
%{py_sitescriptdir}/pylint-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n py3lint
%defattr(644,root,root,755)
%doc ChangeLog README.rst examples/*
%{?with_doc:%doc doc/_build/text/*.txt}
%attr(755,root,root) %{_bindir}/epy3lint
%attr(755,root,root) %{_bindir}/py3lint
%attr(755,root,root) %{_bindir}/py3reverse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{_mandir}/man1/epy3lint.1*
%{_mandir}/man1/py3lint.1*
%{_mandir}/man1/py3reverse.1*

%files -n python3-pylint
%defattr(644,root,root,755)
%{py3_sitescriptdir}/pylint
%{py3_sitescriptdir}/pylint-%{version}-py*.egg-info
%endif
