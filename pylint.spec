%include	/usr/lib/rpm/macros.python
Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl):	Pythonowe narzêdzie sprawdzaj±ce zgodno¶æ modu³u ze standardem kodowania
Name:		pylint
Version:	0.1.2
Release:	0.1
License:	GPL
Group:		Development/Languages/Python
Source0:	ftp://ftp.logilab.fr/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	ac8e90069fefa7fb35b003507856cf34
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
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --optimize=2 --root=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{py_sitedir} -name \*.py -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO
%attr(755,root,root) %{_bindir}/*
%{py_sitedir}/*
