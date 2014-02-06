Name:           python-cython
Version:        0.20
Release:        0
Url:            http://www.cython.org
Summary:        The Cython compiler for writing C extensions for the Python language
License:        Apache-2.0
Group:          Development/Languages/Python

Source:         %{name}-%{version}.tar.gz
BuildRequires:  fdupes
BuildRequires:  python-devel
Provides:       python-cython = %{version}
Obsoletes:      python-cython < %{version}
Requires:       python-xml
Requires:       python-libxml2
Requires:       python-lxml
Requires(post): update-alternatives
Requires(postun): update-alternatives


%description
The Cython language makes writing C extensions for the Python language as
easy as Python itself.  Cython is a source code translator based on the
well-known Pyrex, but supports more cutting edge functionality and
optimizations.

The Cython language is very close to the Python language (and most Python
code is also valid Cython code), but Cython additionally supports calling C
functions and declaring C types on variables and class attributes. This
allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for writing glue code for external C
libraries, and for fast C modules that speed up the execution of Python
code.

%prep
%setup -q -n Cython-%{version}
sed -i "s|^#!.*||" Cython/Debugger/{libpython,Cygdb}.py cython.py # Fix non-executable scripts
sed -i "s|\r||" Demos/callback/{README.txt,cheesefinder.h} Demos/embed/Makefile.{unix,msc.static} Doc/primes.c # Fix EOL encoding
mv bin/cython bin/cython-%{py_ver}
mv bin/cygdb bin/cygdb-%{py_ver}
sed -i "s|bin/cython|bin/cython-%{py_ver}|" setup.py
sed -i "s|bin/cygdb|bin/cygdb-%{py_ver}|" setup.py

%build
CFLAGS="%{optflags}" python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
ln -s  %{_bindir}/cython-%{py_ver} %{buildroot}%{_bindir}/cython
ln -s  %{_bindir}/cygdb-%{py_ver} %{buildroot}%{_bindir}/cygdb
%fdupes -s %{buildroot}%{python_sitearch} %{buildroot}%{_docdir}

%pre
# Since /usr/bin/cython and /usr/bin/cygdb became ghosted to be used with update-alternatives, we have to get rid
# of the old binary resulting from the non-update-alternativies-ified package:
[[ ! -L %{_bindir}/cygdb ]] && rm -f %{_bindir}/cygdb
[[ ! -L %{_bindir}/cython ]] && rm -f %{_bindir}/cython
exit 0

%post
update-alternatives \
   --install %{_bindir}/cython cython %{_bindir}/cython-%{py_ver} 30 \
   --slave %{_bindir}/cygdb cygdb %{_bindir}/cygdb-%{py_ver}

%preun
if [ $1 -eq 0 ] ; then
    update-alternatives --remove cython %{_bindir}/cython-%{py_ver}
fi

# Disabled testsuite as it takes a long time:
#%%check
#python runtests.py

%files
%defattr(-,root,root,-)
%license COPYING.txt LICENSE.txt
%doc README.txt ToDo.txt USAGE.txt Doc Demos
%ghost %{_bindir}/cygdb
%{_bindir}/cygdb-%{py_ver}
%ghost %{_bindir}/cython
%{_bindir}/cython-%{py_ver}
%{python_sitearch}/Cython/
%{python_sitearch}/Cython-%{version}-py%{py_ver}.egg-info
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport/
