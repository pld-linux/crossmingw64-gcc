#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build (only C compiler with static runtime)
#
Summary:	Cross Mingw64 GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - Mingw64 gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - Mingw64 gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla Mingw64 - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - Mingw64 gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - Mingw64 gcc
Name:		crossmingw64-gcc
%define		_major_ver	4.4
%define		_minor_ver	0
Version:	%{_major_ver}.%{_minor_ver}
%define		_snap	20090123
Release:	0.%{_snap}.1
Epoch:		1
License:	GPL v3+
Group:		Development/Languages
#Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
Source0:	ftp://gcc.gnu.org/pub/gcc/snapshots/LATEST-%{_major_ver}/gcc-%{_major_ver}-%{_snap}.tar.bz2
Source1:	http://dl.sourceforge.net/mingw-w64/mingw-w64-snapshot-20081115.tar.bz2
# Source1-md5:	b472282419e6aea64e14763e30d5bb63
Patch100:	gcc-branch.diff.bz2
Patch0:		%{name}-no_include64.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossmingw64-binutils
%{!?with_bootstrap:BuildRequires:	crossmingw64-gcc}
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
#setup -q -n gcc-%{version} -a 1
%setup -q -n gcc-%{_major_ver}-%{_snap} -a 1
#patch100 -p0
%patch0 -p1
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
	--with-gnu-as \
	--with-gnu-ld \
	--with-sysroot=%{arch} \
	%{?with_bootstrap:--with-build-sysroot=$build_sysroot} \
	--%{?with_bootstrap:dis}%{!?with_bootstrap:en}able-shared \
	--enable-threads=win32 \
	--enable-sjlj-exceptions \
	--enable-languages="c%{!?with_bootstrap:,c++}" \
	--enable-c99 \
	--enable-long-long \
	--enable-decimal-float=yes \
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

export CC=%{?with_bootstrap:`pwd`/cross-gcc}%{!?with_bootstrap:%{_bindir}/%{target}-gcc}

cd trunk/mingw-w64-crt

./configure \
	--host=%{target} \
	--prefix=%{_prefix} \
	--with-sysroot=%{?with_bootstrap:$build_sysroot}%{!?with_bootstrap:%{arch}}

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

find $RPM_BUILD_ROOT%{_prefix}/x86_64-pc-mingw32/lib -type f \
	-exec mv "{}" "$RPM_BUILD_ROOT%{arch}/lib" ";"

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
find $RPM_BUILD_ROOT%{arch}/lib -type f -name '*.a' -o -name '*.o' \
        -exec %{target}-strip -g -R.note -R.comment "{}" ";"
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
%{gcclib}/include/avxintrin.h
%{gcclib}/include/bmmintrin.h
%{gcclib}/include/cpuid.h
%{gcclib}/include/cross-stdarg.h
%{gcclib}/include/emmintrin.h
%{gcclib}/include/float.h
%{gcclib}/include/immintrin.h
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
%{gcclib}/include/wmmintrin.h
%{gcclib}/include/x86intrin.h
%{gcclib}/include/xmmintrin.h
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/*.o
%{gcclib}/libgcc.a
%if %{without bootstrap}
%{_bindir}/libgcc_s_1.dll
%{gcclib}/libgcc_eh.a
%endif
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
