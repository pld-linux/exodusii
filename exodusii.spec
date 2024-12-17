Summary:	Finite Element Data Model
Summary(pl.UTF-8):	Model danych elementów skończonych (FE)
Name:		exodusii
Version:	6.09.0
%define	gitref	f7b697abda26c05a5177c9ecf75c782f0b0f31e6
%define	snap	20150604
%define	rel	3
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Libraries
Source0:	https://github.com/certik/exodus/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	959f785e18f57aa999f637d4198e0047
Patch0:		%{name}-libdir.patch
# mirror; original project URL, sf.net/p/exodusii returns 403
URL:		https://github.com/certik/exodus
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel
BuildRequires:	hdf5-devel
BuildRequires:	netcdf-devel >= 4.2.1.1
BuildRequires:	python >= 1:2.5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	zlib-devel
Requires:	netcdf >= 4.2.1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Finite Element data model.

%description -l pl.UTF-8
Model danych elementów skończonych (FE).

%package devel
Summary:	Header files for Exodus II libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Exodus II
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	netcdf-devel >= 4.2.1.1

%description devel
Header files for Exodus II libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Exodus II.

%package -n python-exodus
Summary:	Python wrapper of some of the Exodus II library
Summary(pl.UTF-8):	Pythonowy interfejs do części biblioteki Exodus II
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
# requires ctypes module; python 2 only for now
Requires:	python-modules >= 1:2.5

%description -n python-exodus
Python wrapper of some of the Exodus II library.

%description -n python-exodus -l pl.UTF-8
Pythonowy interfejs do części biblioteki Exodus II.

%package doc
Summary:	Documentation for Exodus II libraries
Summary(pl.UTF-8):	Dokumentacja do bibliotek Exodus II
Group:		Documentation
BuildArch:	noarch

%description doc
Documentation for Exodus II libraries.

%description doc -l pl.UTF-8
Dokumentacja do bibliotek Exodus II.

%prep
%setup -q -n exodus-%{gitref}
%patch -P0 -p1

# expected by nemesis
%{__mv} exodus exodusii

%build
TOPDIR="$(pwd)"
install -d build/{exodusii,nemesis}
cd build/exodusii
%cmake ../../exodusii \
	-DHDF5_LIBRARY=%{_libdir}/libhdf5.so \
	-DHDF5HL_LIBRARY=%{_libdir}/libhdf5_hl.so \
	-DNETCDF_INCLUDE_DIR=%{_includedir} \
	-DNETCDF_LIBRARY=%{_libdir}/libnetcdf.so \
	-DNETCDF_NCDUMP=%{_bindir}/ncdump \
	-DPYTHON_INSTALL=%{py_sitescriptdir}

%{__make}

cd ../nemesis
%cmake ../../nemesis \
	-DEXODUS_LIBRARY="$TOPDIR/build/exodusii/cbind/libexodus.so" \
	-DHDF5_LIBRARY=%{_libdir}/libhdf5.so \
	-DHDF5HL_LIBRARY=%{_libdir}/libhdf5_hl.so \
	-DMATH_LIBRARY=%{_libdir}/libm.so \
	-DNETCDF_INCLUDE_DIR=%{_includedir} \
	-DNETCDF_LIBRARY=%{_libdir}/libnetcdf.so \
	-DNETCDF_NCDUMP=%{_bindir}/ncdump \
	-DZ_LIBRARY=%{_libdir}/libz.so

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/exodusii install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C build/nemesis install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.NEMESIS exodusii/{COPYRIGHT,README}
%attr(755,root,root) %{_libdir}/libexodus.so
%attr(755,root,root) %{_libdir}/libexoIIv2for.so
%attr(755,root,root) %{_libdir}/libnemesis.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/exodusII*.h
%{_includedir}/exodusII*.inc
%{_includedir}/ne_nemesisI.h

%files -n python-exodus
%defattr(644,root,root,755)
%doc exodusii/README.PYTHON
# uses sys.dont_write_bytecode = True, so just .py packaged
%{py_sitescriptdir}/exodus.py

%files doc
%defattr(644,root,root,755)
%doc exodusii/doc/*.{txt,pdf}
