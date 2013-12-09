# TODO:
# - include examples in package

# Conditional build:
%bcond_without  python2 # Python 2.x version
%bcond_without  python3 # Python 3.x version (available as 'py3lint')

Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Pythonowe narzędzie sprawdzające zgodność modułu ze standardem kodowania
Name:		pylint
Version:	1.0.0
Release:	2
License:	GPL
Group:		Development/Languages/Python
Source0:	https://bitbucket.org/logilab/pylint/get/%{name}-version-%{version}.tar.bz2
# Source0-md5:	9a83c079c2c608a9156feecf909b7b8a
Patch0:		%{name}-type_error.patch
URL:		http://www.pylint.org/
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-modules >= 2.2.1
%endif
%if %{with python3}
BuildRequires:	python3-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules >= 1:3.2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sphinx-pdg
Requires:	python-logilab-astroid >= 0.24.3
Requires:	python-logilab-common >= 0.53.0
Requires:	python-modules
Suggests:	python-devel-src
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tool that checks if a module satisfy a coding standard.

%description -l pl.UTF-8
Narzędzie sprawdzające zgodność modułów napisanych w języku Python z
regułami tworzenia kodu źródłowego.

%package gui
Summary:	GUI for pylint
Summary(pl.UTF-8):	Graficzny interfejs użytkownika dla pylinta
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-tkinter

%description gui
Tk based GUI for pylint.

%description gui -l pl.UTF-8
Oparty na bibliotece Tk graficzny interfejs użytkownika dla pylinta.

%package -n py3lint
Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl.UTF-8):	Pythonowe narzędzie sprawdzające zgodność modułu ze standardem kodowania
Group:		Development/Languages/Python
Requires:	python3-logilab-astroid >= 0.24.3
Requires:	python3-logilab-common >= 0.53.0
Obsoletes:	pylint-python3 < 1.0.0-2

%description -n py3lint
Python tool that checks if a module satisfy a coding standard.

Python 3.x version, available via the 'py3lint' command.

%description -n py3lint -l pl.UTF-8
Narzędzie sprawdzające zgodność modułów napisanych w języku Python z
regułami tworzenia kodu źródłowego.

Wersja dla Pythona 3.x, dostępna przez polecenie 'py3lint'.

%package -n py3lint-gui
Summary:	GUI for pylint
Summary(pl.UTF-8):	Graficzny interfejs użytkownika dla pylinta
Group:		Development/Languages/Python
Requires:	py3lint = %{version}-%{release}
Requires:	python3-tkinter
Obsoletes:	pylint-python3-gui < 1.0.0-2

%description -n py3lint-gui
Tk based GUI for pylint.

%description -n py3lint-gui -l pl.UTF-8
Oparty na bibliotece Tk graficzny interfejs użytkownika dla pylinta.

%prep
%setup -qc
mv logilab-pylint-*/* .
%patch0 -p1

%build
%if %{with python2}
%{__python} setup.py build
%endif

%if %{with python3}
export NO_SETUPTOOLS=1
%{__python3} setup.py build --build-base=build3
unset NO_SETUPTOOLS
%endif

%{__make} -C doc text

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1}

%if %{with python3}
export NO_SETUPTOOLS=1
%{__python3} setup.py build --build-base=build3 install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

unset NO_SETUPTOOLS
mv $RPM_BUILD_ROOT%{_bindir}/epylint $RPM_BUILD_ROOT%{_bindir}/epy3lint
mv $RPM_BUILD_ROOT%{_bindir}/pylint $RPM_BUILD_ROOT%{_bindir}/py3lint
mv $RPM_BUILD_ROOT%{_bindir}/pylint-gui $RPM_BUILD_ROOT%{_bindir}/py3lint-gui
mv $RPM_BUILD_ROOT%{_bindir}/pyreverse $RPM_BUILD_ROOT%{_bindir}/py3reverse
cp -p man/epylint.1 $RPM_BUILD_ROOT%{_mandir}/man1/epy3lint.1
cp -p man/pylint.1 $RPM_BUILD_ROOT%{_mandir}/man1/py3lint.1
cp -p man/pylint-gui.1 $RPM_BUILD_ROOT%{_mandir}/man1/py3lint-gui.1
cp -p man/pyreverse.1 $RPM_BUILD_ROOT%{_mandir}/man1/py3reverse.1
%endif

%if %{with python2}
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
%endif

cp -p examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/pylintrc

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc logilab-pylint-*/{ChangeLog,README,examples/*,doc/_build/text/*.txt}
%attr(755,root,root) %{_bindir}/epylint
%attr(755,root,root) %{_bindir}/pylint
%attr(755,root,root) %{_bindir}/pyreverse
%attr(755,root,root) %{_bindir}/symilar
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{py_sitescriptdir}/pylint
%{py_sitescriptdir}/pylint-%{version}-py*.egg-info
%{_mandir}/man1/epylint.1*
%{_mandir}/man1/pylint.1*
%{_mandir}/man1/pyreverse.1*
%{_mandir}/man1/symilar.1*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pylint-gui
%{_mandir}/man1/pylint-gui.1*
%endif

%if %{with python3}
%files -n py3lint
%defattr(644,root,root,755)
%doc logilab-pylint-*/{ChangeLog,README,examples/*,doc/_build/text/*.txt}
%attr(755,root,root) %{_bindir}/epy3lint
%attr(755,root,root) %{_bindir}/py3lint
%attr(755,root,root) %{_bindir}/py3reverse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{py3_sitescriptdir}/pylint
%{py3_sitescriptdir}/pylint-%{version}-py*.egg-info
%{_mandir}/man1/epy3lint.1*
%{_mandir}/man1/py3lint.1*
%{_mandir}/man1/py3reverse.1*

%files -n py3lint-gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/py3lint-gui
%{_mandir}/man1/py3lint-gui.1*
%endif
