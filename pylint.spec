%include	/usr/lib/rpm/macros.python
Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl):	Pythonowe narzêdzie sprawdzaj±ce zgodno¶æ modu³u ze standardem kodowania
Name:		pylint
Version:	0.2
Release:	0.4
License:	GPL
Group:		Development/Languages/Python
Source0:	ftp://ftp.logilab.fr/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	4447725b8860416264c99d656124c94d
Patch0:		%{name}-checkers.patch
Patch1:		%{name}-rc.patch
URL:		http://www.logilab.org/projects/%{name}/view
BuildRequires:	python-modules >= 2.2.1
BuildRequires:	rpm-pythonprov
Requires:	python-logilab-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tool that checks if a module satisfy a coding standard.

%description -l pl
Pythonowe narzêdzie sprawdzaj±ce zgodno¶æ modu³u ze standardem
kodowania.

%prep
%setup -q -n logilab-pylint-0.2.0
%patch0 -p1
%patch1 -p1

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT

install examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}/

find $RPM_BUILD_ROOT%{py_sitedir} -name \*.py -exec rm -f {} \;

# see install section of python-logilab-common for explanation
rm -f $RPM_BUILD_ROOT%{py_sitedir}/logilab/__init__.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO README examples/*
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not mtime md5) %{_sysconfdir}/*
%{py_sitedir}/*
