#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build (only C compiler)
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
Patch1:		%{name}-no_red_zone.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossmingw64-binutils
BuildRequires:	flex
BuildRequires:	mpfr-devel
BuildRequires:	texinfo >= 4.2
Requires:	crossmingw64-binutils
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
%setup -q -n gcc-%{version} -a 1
%patch0 -p1
%patch1 -p1
mkdir -p winsup/mingw
cp -ar trunk/mingw-w64-headers/include winsup/mingw

%build
build_sysroot=`pwd`/winsup

rm -rf BUILDDIR && install -d BUILDDIR && cd BUILDDIR

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--includedir=%{arch}/include \
	--with-sysroot=%{arch} \
	--with-build-sysroot=$build_sysroot \
	--disable-shared \
	--enable-threads=win32 \
	--disable-sjlj-exceptions \
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
	--with-pkgversion="PLD-Linux" \
	--with-bugurl="http://bugs.pld-linux.org" \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target}

%{__make}

cd ..

cat <<EOF >cross-gcc
#!/bin/sh
p=`pwd`/BUILDDIR/gcc
\${p}/xgcc -B\${p} \$@
EOF
chmod 755 cross-gcc

export CC=`pwd`/cross-gcc

cd trunk/mingw-w64-crt

./configure \
	--host=%{target} \
	--prefix=%{_prefix} \
	--with-sysroot=$build_sysroot \

%{__make}

cd -

%install
build_sysroot=`pwd`/winsup

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir},%{arch}/lib,%{arch}/mingw/include}

cd BUILDDIR

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install gcc/specs $RPM_BUILD_ROOT%{gcclib}

cd ..

gccdir=$RPM_BUILD_ROOT%{gcclib}
mv $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
rm -r $gccdir/include-fixed
rm -r $gccdir/install-tools


cp -ar $build_sysroot/mingw/include $RPM_BUILD_ROOT%{arch}

make -C trunk/mingw-w64-crt install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/lib/* \
	$RPM_BUILD_ROOT%{arch}/lib

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{arch}/lib/*.{a,o}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%dir %{gcclib}/include
%{gcclib}/include/ammintrin.h
%{gcclib}/include/bmmintrin.h
%{gcclib}/include/cpuid.h
%{gcclib}/include/emmintrin.h
%{gcclib}/include/float.h
%{gcclib}/include/iso646.h
%{gcclib}/include/limits.h
%{gcclib}/include/mm3dnow.h
%{gcclib}/include/mm_malloc.h
%{gcclib}/include/mmintrin-common.h
%{gcclib}/include/mmintrin.h
%{gcclib}/include/nmmintrin.h
%{gcclib}/include/pmmintrin.h
%{gcclib}/include/smmintrin.h
%{gcclib}/include/stdarg.h
%{gcclib}/include/stdbool.h
%{gcclib}/include/stddef.h
%{gcclib}/include/stdfix.h
%{gcclib}/include/syslimits.h
%{gcclib}/include/tgmath.h
%{gcclib}/include/tmmintrin.h
%{gcclib}/include/unwind.h
%{gcclib}/include/varargs.h
%{gcclib}/include/xmmintrin.h
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/libgcc.a
%{gcclib}/libgcov.a
%{gcclib}/specs*
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*
%{arch}/include
%{arch}/lib/*.a
%if %{without bootstrap}
%exclude %{arch}/include/c++
%exclude %{arch}/lib/libstdc++.a
%exclude %{arch}/lib/libsupc++.a
%endif
%{arch}/lib/*.o
%dir %{arch}/mingw
%{arch}/mingw/include

%if %{without bootstrap}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-[cg]++
%attr(755,root,root) %{gcclib}/cc1plus
%{arch}/lib/libstdc++.a
%{arch}/lib/libstdc++.la
%{arch}/lib/libsupc++.a
%{arch}/lib/libsupc++.la
%{arch}/include/c++
%{_mandir}/man1/%{target}-g++.1*
%endif
