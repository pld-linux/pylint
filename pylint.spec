Summary:	Python tool that checks if a module satisfy a coding standard
Summary(pl):	Pythonowe narzêdzie sprawdzaj±ce zgodno¶æ modu³u ze standardem kodowania
Name:		pylint
Version:	0.8.1
Release:	1
License:	GPL
Group:		Development/Languages/Python
Source0:	ftp://ftp.logilab.fr/pub/pylint/%{name}-%{version}.tar.gz
# Source0-md5:	f04addb7496a2a3e26675d36026718d7
URL:		http://www.logilab.org/projects/pylint/view
BuildRequires:	python-devel
BuildRequires:	python-modules >= 2.2.1
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
Requires:	python-logilab-astng >= 0.13.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python tool that checks if a module satisfy a coding standard.

%description -l pl
Narzêdzie sprawdzaj±ce zgodno¶æ modu³ów napisanych w jêzyku Python
z regu³ami tworzenia kodu ¼ród³owego.

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir}/man1}

python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install examples/pylintrc $RPM_BUILD_ROOT%{_sysconfdir}

find $RPM_BUILD_ROOT%{py_sitescriptdir} -name \*.py -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog TODO README examples/* doc/*.txt
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pylintrc
%{py_sitescriptdir}/*
%{_mandir}/man1/*
