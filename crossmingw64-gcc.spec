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
Version:	4.7.1
Release:	2
Epoch:		1
License:	GPL v3+
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	933e6f15f51c031060af64a9e14149ff
# svn co https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/stable/v2.x/mingw-w64-crt mingw64-crt
%define		_rev	5377
Source1:	mingw64-crt.tar.xz
# Source1-md5:	ee609a06a5ead72f0b203495b5f76527
Patch0:		gcc-branch.diff
Patch1:		gcc-mingw-dirs.patch
URL:		http://mingw-w64.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossmingw64-binutils >= 2.22.51.0.1
%{!?with_bootstrap:BuildRequires:	crossmingw64-gcc}
BuildRequires:	crossmingw64-headers
BuildRequires:	flex
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	libmpc-devel
BuildRequires:	mpfr-devel >= 2.3.0
BuildRequires:	subversion >= 1.7
BuildRequires:	texinfo >= 4.2
Requires:	crossmingw64-binutils
Requires:	crossmingw64-headers
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-w64-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*/lib.*\\.a

# workaround bootstrap bug: http://gcc.gnu.org/bugzilla/PR25672
%define		filterout	-march=i486 -march=i686 -mtune=pentium4

%description
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the Mingw64 build libraries. This includes a binutils, gcc with g++
and libstdc++, all cross targeted to x86_64-pc-mingw32.

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
and libstdc++, all cross targeted to x86_64-pc-mingw32.

This package contains cross targeted g++ and libstdc++.

%prep
%setup -q -n gcc-%{version} -a 1
%patch0 -p0
%patch1 -p1

# override snapshot version.
echo %{version} > gcc/BASE-VER
echo "release" > gcc/DEV-PHASE

if [ "`svnversion -n mingw64-crt`" != "%{_rev}" ]; then
	exit 1
fi

%build
rm -rf BUILDDIR && install -d BUILDDIR/%{target} && cd BUILDDIR

# setup system headers for local build.
cp -ar %{arch}/include %{target}/include

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
TEXCONFIG=false \
../configure \
	--enable-checking=release \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--includedir=%{arch}/include \
	--with-gnu-as \
	--with-gnu-ld \
	--with-sysroot=%{arch} \
	--%{?with_bootstrap:dis}%{!?with_bootstrap:en}able-shared \
	--disable-win32-registry \
	--enable-threads=win32 \
	--enable-tls \
	--enable-sjlj-exceptions \
	--enable-languages="c%{!?with_bootstrap:,c++}" \
	--disable-multilib \
	--disable-nls \
	--disable-libmudflap \
	--disable-libquadmath \
	--disable-libssp \
	--disable-libitm \
	--disable-plugin \
	--disable-lto \
	--enable-c99 \
	--enable-long-long \
	--enable-decimal-float=yes \
	--enable-cmath \
	--with-mangler-in-ld \
	--with-gxx-include-dir=%{arch}/include/c++/%{version} \
	--enable-fully-dynamic-string \
	--enable-libstdcxx-allocator=new \
	--enable-symvers=gnu-versioned-namespace \
	--disable-libstdcxx-pch \
	--enable-__cxa_atexit \
	--with-pkgversion="PLD-Linux" \
	--with-bugurl="http://bugs.pld-linux.org" \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target}

%{__make}
cd ..

cd mingw64-crt
CC="$PWD/../BUILDDIR/gcc/gcc-cross -B$PWD/../BUILDDIR/gcc/" \
./configure \
	--host=%{target} \
	--prefix=%{_prefix} \
	--disable-lib32 --enable-lib64

%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cd BUILDDIR
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install gcc/specs $RPM_BUILD_ROOT%{gcclib}

cd ..

gccdir=$RPM_BUILD_ROOT%{gcclib}
mv $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
rm -r $gccdir/include-fixed
rm -r $gccdir/install-tools

%{__make} -C mingw64-crt install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{gcclib}/include/avx2intrin.h
%{gcclib}/include/avxintrin.h
%{gcclib}/include/bmi2intrin.h
%{gcclib}/include/bmiintrin.h
%{gcclib}/include/bmmintrin.h
%{gcclib}/include/cpuid.h
%{gcclib}/include/cross-stdarg.h
%{gcclib}/include/emmintrin.h
%{gcclib}/include/f16cintrin.h
%{gcclib}/include/float.h
%{gcclib}/include/fma4intrin.h
%{gcclib}/include/fmaintrin.h
%{gcclib}/include/ia32intrin.h
%{gcclib}/include/immintrin.h
%{gcclib}/include/iso646.h
%{gcclib}/include/limits.h
%{gcclib}/include/lwpintrin.h
%{gcclib}/include/lzcntintrin.h
%{gcclib}/include/mm3dnow.h
%{gcclib}/include/mm_malloc.h
%{gcclib}/include/mmintrin.h
%{gcclib}/include/nmmintrin.h
%{gcclib}/include/pmmintrin.h
%{gcclib}/include/popcntintrin.h
%{gcclib}/include/smmintrin.h
%{gcclib}/include/tbmintrin.h
%{gcclib}/include/stdalign.h
%{gcclib}/include/stdarg.h
%{gcclib}/include/stdbool.h
%{gcclib}/include/stddef.h
%{gcclib}/include/stdfix.h
%{gcclib}/include/stdint-gcc.h
%{gcclib}/include/stdint.h
%{gcclib}/include/stdnoreturn.h
%{gcclib}/include/syslimits.h
%{gcclib}/include/tgmath.h
%{gcclib}/include/tmmintrin.h
%{gcclib}/include/unwind.h
%{gcclib}/include/varargs.h
%{gcclib}/include/wmmintrin.h
%{gcclib}/include/x86intrin.h
%{gcclib}/include/xmmintrin.h
%{gcclib}/include/xopintrin.h
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%attr(755,root,root) %{gcclib}/lto-wrapper
%{gcclib}/*.o
%{gcclib}/libgcc.a
%if %{without bootstrap}
%{arch}/lib/libgcc_s_sjlj-1.dll
%{gcclib}/libgcc_eh.a
%endif
%{gcclib}/libgcov.a
%{gcclib}/specs*
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*
%{arch}/lib/*.a
%if %{without bootstrap}
%exclude %{arch}/include/c++
%exclude %{arch}/lib/libstdc++.a
%exclude %{arch}/lib/libsupc++.a
%endif
%{arch}/lib/*.o

%if %{without bootstrap}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-[cg]++
%attr(755,root,root) %{gcclib}/cc1plus
%{arch}/lib/libstdc++-7.dll
%{arch}/lib/libstdc++.a
%{arch}/lib/libstdc++.la
%{arch}/lib/libsupc++.a
%{arch}/lib/libsupc++.la
%{arch}/include/c++
%{_mandir}/man1/%{target}-g++.1*
%endif
