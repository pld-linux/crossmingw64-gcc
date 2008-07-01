#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build (only pure C compiler w/o startfiles)
#
Summary:	Cross Mingw64 GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - Mingw64 gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - Mingw64 gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla Mingw64 - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - Mingw64 gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - Mingw64 gcc
Name:		crossmingw64-gcc
Version:	4.3.1
Release:	0.1
Epoch:		1
License:	GPL v3+
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	4afa0290cc3a41ac8822666f1110de98
Source1:	http://dl.sourceforge.net/mingw-w64/mingw-w64-snapshot-20080424.tar.bz2
# Source1-md5:	e2eea49233efd0be3a40fc774abeb1a2
Patch0:		%{name}-no_include64.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossmingw64-binutils
BuildRequires:	flex
BuildRequires:	mpfr-devel
BuildRequires:	texinfo >= 4.2
Requires:	crossmingw64-binutils
Requires:	gcc-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*/lib.*\\.a

%description
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw64 build libraries. This includes a binutils, gcc with g++
and libstdc++, all cross targeted to x86_64-mingw32.

This package contains cross targeted gcc.

%package c++
Summary:	Mingw64 binary utility development utilities - g++
Summary(pl.UTF-8):	Zestaw narzędzi mingw64 - g++
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw64 build libraries. This includes a binutils, gcc with g++
and libstdc++, all cross targeted to x86_64-mingw32.

This package contains cross targeted g++ and (static) libstdc++.

%prep
%setup -q -n gcc-%{version}
%patch0 -p1
mkdir winsup
tar -xjf %{SOURCE1} -C winsup
ln -s mingw-w64-headers winsup/trunk/mingw

%build
build_sysroot=`pwd`/winsup/trunk

rm -rf BUILDDIR && install -d BUILDDIR && cd BUILDDIR

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{arch}/bin \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--includedir=%{arch}/include \
	--with-sysroot=%{arch} \
	--with-build-sysroot=$build_sysroot \
	--disable-shared \
	--enable-threads=win32 \
	--enable-languages="c%{!?with_bootstrap:,c++}" \
	--enable-c99 \
	--enable-long-long \
	--enable-cmath \
	--disable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-mangler-in-ld \
	--with-gxx-include-dir=%{arch}/include/c++/%{version} \
	--disable-libstdcxx-pch \
	--enable-__cxa_atexit \
	--disable-libmudflap \
	--disable-libssp \
	--target=%{target}

%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}}

cd BUILDDIR

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install gcc/specs $RPM_BUILD_ROOT%{gcclib}

cd ..

mv -f $RPM_BUILD_ROOT%{arch}/bin/%{target}-* $RPM_BUILD_ROOT%{_bindir}

# already in arch/lib, shouldn't be here
rm $RPM_BUILD_ROOT%{_libdir}/libiberty.a

gccdir=$RPM_BUILD_ROOT%{gcclib}
mv $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
rm -r $gccdir/include-fixed
rm -r $gccdir/install-tools

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

#if %{without bootstrap}
# restore hardlinks
#ln -f $RPM_BUILD_ROOT%{_bindir}/%{target}-{g++,c++}
#ln -f $RPM_BUILD_ROOT%{arch}/bin/{g++,c++}
#endif

# the same... make hardlink
ln -f $RPM_BUILD_ROOT%{arch}/bin/gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcov
%attr(755,root,root) %{arch}/bin/gcc
#{arch}/lib/libiberty.a
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/libgcc.a
%{gcclib}/libgcov.a
%{gcclib}/specs*
%dir %{gcclib}/include

%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*

%if 0
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-[cg]++
%attr(755,root,root) %{arch}/bin/[cg]++
%attr(755,root,root) %{gcclib}/cc1plus
%{arch}/lib/libstdc++.a
%{arch}/lib/libstdc++.la
%{arch}/lib/libsupc++.a
%{arch}/lib/libsupc++.la
%{arch}/include/g++
%{_mandir}/man1/%{target}-g++.1*
%endif
