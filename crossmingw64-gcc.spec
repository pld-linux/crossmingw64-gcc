#
# Conditional build:
%bcond_with	bootstrap	# bootstrap build (only C compiler with static runtime)
#
Summary:	Cross MinGW-W64 GNU binary utility development utilities - gcc
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - MinGW-W64 gcc
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - MinGW-W64 gcc
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla MinGW-W64 - gcc
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - MinGW-W64 gcc
Summary(tr.UTF-8):	GNU geliştirme araçları - MinGW-W64 gcc
Name:		crossmingw64-gcc
Version:	11.5.0
Release:	1
Epoch:		1
License:	GPL v3+
Group:		Development/Languages
Source0:	https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
# Source0-md5:	03473f26c87e05e789a32208f1fe4491
# svn co https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/stable/v2.x/mingw-w64-crt mingw64-crt
%define		_rev	5515
Source1:	mingw64-crt.tar.xz
# Source1-md5:	bf9051e7e4deb445e9e8877ca68211e1
#Patch0:		gcc-branch.diff
Patch1:		gcc-mingw-dirs.patch
Patch2:		gcc-mingw64.patch
URL:		https://www.mingw-w64.org/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	bison
BuildRequires:	crossmingw64-binutils >= 2.30
%{!?with_bootstrap:BuildRequires:	crossmingw64-gcc}
BuildRequires:	crossmingw64-headers
BuildRequires:	flex >= 2.5.4
BuildRequires:	gettext-tools >= 0.14.5
BuildRequires:	gmp-devel >= 4.3.2
BuildRequires:	isl-devel >= 0.15
BuildRequires:	libmpc-devel >= 0.8.1
BuildRequires:	libstdc++-devel
BuildRequires:	mpfr-devel >= 3.1.0
BuildRequires:	perl-tools-pod
BuildRequires:	subversion >= 1.7
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo >= 4.7
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	crossmingw64-binutils >= 2.30
Requires:	crossmingw64-headers
Requires:	gcc-dirs
Requires:	gmp >= 4.3.2
Requires:	isl >= 0.15
Requires:	libmpc >= 0.8.1
Requires:	mpfr >= 3.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-w64-mingw32
%define		sysprefix	/usr
%define		archprefix	%{sysprefix}/%{target}
%define		archbindir	%{archprefix}/bin
%define		archincludedir	%{archprefix}/include
%define		archlibdir	%{archprefix}/lib
%define		gccarchdir	%{_libdir}/gcc/%{target}
%define		gcclibdir	%{gccarchdir}/%{version}
# TODO: wine 64-bit dir, similarly to crossmingw32?
%define		_dll64dir	%{archlibdir}

%define		_noautostrip	.*/lib.*\\.a

%define		Werror_cflags	%{nil}
%define		_ssp_cflags		%{nil}

# workaround bootstrap bug: http://gcc.gnu.org/bugzilla/PR25672
%define		filterout	-march=i486 -march=i586 -march=i686 -mtune=pentium4

%description
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the MinGW-W64 build libraries. This includes a binutils, gcc with g++
and libstdc++, all cross targeted to x86_64-pc-mingw32.

This package contains cross targeted gcc.

%description -l pl.UTF-8
crossmingw64 jest kompletnym systemem do kroskompilacji, pozwalającym
budować aplikacje MS Windows pod Linuksem używając bibliotek mingw64.
System składa się z binutils, gcc z g++ i libstdc++ - wszystkie
generujące kod dla platformy x86_64-w64-mingw32.

Ten pakiet zawiera skrośny kompilator gcc.

%package -n crossmingw64-libgcc-dll
Summary:	libgcc 64-bit DLL library for Windows
Summary(pl.UTF-8):	64-bitowa biblioteka DLL libgcc dla Windows
Group:		Applications/Emulators
#Requires:	wine64 ?

%description -n crossmingw64-libgcc-dll
libgcc 64-bit DLL library for Windows.

%description -n crossmingw64-libgcc-dll -l pl.UTF-8
64-bitowa biblioteka DLL libgcc dla Windows.

%package -n crossmingw64-libatomic
Summary:	The GNU Atomic library - cross MinGW-W64 version
Summary(pl.UTF-8):	Biblioteka GNU Atomic - wersja skrośna MinGW-W64
License:	GPL v3+ with GCC Runtime Library Exception v3.1
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n crossmingw64-libatomic
This package contains cross MinGW-W64 version of the GNU Atomic
library which is a GCC support library for atomic operations not
supported by hardware.

%description -n crossmingw64-libatomic -l pl.UTF-8
Ten pakiet zawiera wersję skrośną MinGW-W64 biblioteki GNU Atomic,
będącej biblioteką GCC, wspierającej operacje atomowe na sprzęcie ich
nie obsługującym.

%package -n crossmingw64-libatomic-static
Summary:	The GNU Atomic static library - cross MinGW-W64 version
Summary(pl.UTF-8):	Statyczna biblioteka GNU Atomic - wersja skrośna MinGW-W64
License:	GPL v3+ with GCC Runtime Library Exception v3.1
Group:		Development/Libraries
Requires:	crossmingw64-libatomic = %{epoch}:%{version}-%{release}

%description -n crossmingw64-libatomic-static
The GNU Atomic static library - cross MinGW-W64 version.

%description -n crossmingw64-libatomic-static -l pl.UTF-8
Statyczna biblioteka GNU Atomic - wersja skrośna MinGW-W64.

%package -n crossmingw64-libatomic-dll
Summary:	64-bit DLL GNU Atomic library for Windows
Summary(pl.UTF-8):	64-bitowa biblioteka DLL GNU Atomic dla Windows
License:	GPL v3+ with GCC Runtime Library Exception v3.1
Group:		Applications/Emulators
#Requires:	wine64 ?

%description -n crossmingw64-libatomic-dll
64-bit DLL GNU Atomic library for Windows.

%description -n crossmingw64-libatomic-dll -l pl.UTF-8
64-bitowa biblioteka DLL GNU Atomic dla Windows.

%package c++
Summary:	MinGW-W64 binary utility development utilities - g++
Summary(pl.UTF-8):	Zestaw narzędzi MinGW-W64 - g++
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
crossmingw64 is a complete cross-compiling development system for
building stand-alone Microsoft Windows applications under Linux using
the MinGW-W64 build libraries. This includes a binutils, gcc with g++
and libstdc++, all cross targeted to x86_64-pc-mingw32.

This package contains cross targeted g++ and libstdc++.

%description c++ -l pl.UTF-8
crossmingw64 jest kompletnym systemem do kroskompilacji, pozwalającym
budować aplikacje MS Windows pod Linuksem używając bibliotek mingw64.
System składa się z binutils, gcc z g++ i libstdc++ - wszystkie
generujące kod dla platformy x86_64-w64-mingw32.

Ten pakiet zawiera skrośny kompilator g++ oraz libstdc++.

%package -n crossmingw64-libstdc++-static
Summary:	Static standard C++ library - cross MinGW32 version
Summary(pl.UTF-8):	Statyczna biblioteka standardowa C++ - wersja skrośna MinGW32
Group:		Development/Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}

%description -n crossmingw64-libstdc++-static
Static standard C++ library - cross MinGW32 version.

%description -n crossmingw64-libstdc++-static -l pl.UTF-8
Statyczna biblioteka standardowa C++ - wersja skrośna MinGW32.

%package -n crossmingw64-libstdc++-dll
Summary:	libstdc++ 64-bit DLL library for Windows
Summary(pl.UTF-8):	64-bitowa biblioteka DLL libstdc++ dla Windows
Group:		Applications/Emulators
Requires:	crossmingw64-libgcc-dll = %{epoch}:%{version}-%{release}
#Requires:	wine64 ?

%description -n crossmingw64-libstdc++-dll
libstdc++ 64-bit DLL library for Windows.

%description -n crossmingw64-libstdc++-dll -l pl.UTF-8
64-bitowa biblioteka DLL libstdc++ dla Windows.

%prep
%setup -q -n gcc-%{version} -a 1
#patch -P0 -p0
%patch -P1 -p1
%patch -P2 -p1

# override snapshot version.
echo %{version} > gcc/BASE-VER
echo "release" > gcc/DEV-PHASE

svn upgrade mingw64-crt
if [ "`svnversion -n mingw64-crt`" != "%{_rev}" ]; then
	exit 1
fi

%build
rm -rf BUILDDIR && install -d BUILDDIR/%{target} && cd BUILDDIR

# setup system headers for local build.
#cp -ar %{archincludedir} %{target}/include

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{sysprefix} \
	--bindir=%{archbindir} \
	--libdir=%{_libdir} \
	--includedir=%{archincludedir} \
	--libexecdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--with-bugurl="http://bugs.pld-linux.org" \
	--with-build-time-tools=%{archbindir} \
	--with-demangler-in-ld \
	--with-dwarf2 \
	--with-gnu-as \
	--with-gnu-ld \
	--with-gxx-include-dir=%{archincludedir}/c++/%{version} \
	--with-long-double-128 \
	--with-pkgversion="PLD-Linux" \
	--with-sysroot=%{archprefix} \
	--enable-c99 \
	--enable-checking=release \
	--enable-cmath \
	--enable-decimal-float=yes \
	--enable-fully-dynamic-string \
	--disable-isl-version-check \
	--enable-languages="c%{!?with_bootstrap:,c++}" \
	%{?with_bootstrap:--disable-libatomic} \
	--disable-libcc1 \
	--disable-libitm \
	--disable-libquadmath \
	--disable-libssp \
	--enable-libstdcxx-allocator=new \
	--disable-libstdcxx-pch \
	--enable-linker-build-id \
	--enable-long-long \
	--disable-lto \
	--disable-multilib \
	--disable-nls \
	--disable-plugin \
	--enable-sjlj-exceptions \
	--enable-shared%{?with_bootstrap:=no} \
	--enable-symvers=gnu-versioned-namespace \
	--enable-threads=win32 \
	--enable-tls \
	--disable-werror \
	--disable-win32-registry \
	--enable-__cxa_atexit \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=%{target}

%{__make}
cd ..

cd mingw64-crt
CC="$PWD/../BUILDDIR/gcc/gcc-cross -B$PWD/../BUILDDIR/gcc/" \
./configure \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	--host=%{target} \
	--prefix=%{_prefix} \
	--disable-lib32 \
	--enable-lib64

%{__make} -j1
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} -C BUILDDIR install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p BUILDDIR/gcc/specs $RPM_BUILD_ROOT%{gcclibdir}

gccdir=$RPM_BUILD_ROOT%{gcclibdir}
%{__mv} $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
%{__rm} -r $gccdir/include-fixed
%{__rm} -r $gccdir/install-tools

# these must be symlinks: gcclibdir is calculated relatively to real binary path
ln -sf %{archbindir}/%{target}-gcc $RPM_BUILD_ROOT%{_bindir}/%{target}-gcc
ln -sf %{archbindir}/%{target}-g++ $RPM_BUILD_ROOT%{_bindir}/%{target}-g++
ln -sf %{archbindir}/%{target}-cpp $RPM_BUILD_ROOT%{_bindir}/%{target}-cpp
ln -sf %{archbindir}/%{target}-gcov $RPM_BUILD_ROOT%{_bindir}/%{target}-gcov
ln -sf %{archbindir}/%{target}-gcov-dump $RPM_BUILD_ROOT%{_bindir}/%{target}-gcov-dump
ln -sf %{archbindir}/%{target}-gcov-tool $RPM_BUILD_ROOT%{_bindir}/%{target}-gcov-tool

%{__make} -C mingw64-crt -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{archprefix}/libsrc

# DLLs
# same path currently, so disable for now
#install -d $RPM_BUILD_ROOT%{_dll64dir}
#%{__mv} $RPM_BUILD_ROOT%{archlibdir} $RPM_BUILD_ROOT%{_dll64dir}

%if 0%{!?debug:1}
%if %{without bootstrap}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dll64dir}/*.dll
%endif
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclibdir}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclibdir}/libgcov.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{archlibdir}/*.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{archlibdir}/*.o
%endif

# files common for GNU tools, packaged in some native packages
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man7/{fsf-funding,gfdl,gpl}.7
# files common for all targets, packaged in native
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}
%if %{without bootstrap}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python \
	$RPM_BUILD_ROOT%{archlibdir}/libstdc++.dll.a-gdb.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcov
%attr(755,root,root) %{_bindir}/%{target}-gcov-dump
%attr(755,root,root) %{_bindir}/%{target}-gcov-tool
%attr(755,root,root) %{archbindir}/%{target}-cpp
%attr(755,root,root) %{archbindir}/%{target}-gcc
%attr(755,root,root) %{archbindir}/%{target}-gcc-%{version}
%attr(755,root,root) %{archbindir}/%{target}-gcc-ar
%attr(755,root,root) %{archbindir}/%{target}-gcc-nm
%attr(755,root,root) %{archbindir}/%{target}-gcc-ranlib
%attr(755,root,root) %{archbindir}/%{target}-gcov
%attr(755,root,root) %{archbindir}/%{target}-gcov-dump
%attr(755,root,root) %{archbindir}/%{target}-gcov-tool
%if %{without bootstrap}
%{archlibdir}/libgcc_s.a
%endif
%dir %{gccarchdir}
%dir %{gcclibdir}
%attr(755,root,root) %{gcclibdir}/cc1
%attr(755,root,root) %{gcclibdir}/collect2
%attr(755,root,root) %{gcclibdir}/lto-wrapper
%{gcclibdir}/libgcc.a
%if %{without bootstrap}
%{gcclibdir}/libgcc_eh.a
%endif
%{gcclibdir}/libgcov.a
%{gcclibdir}/crtbegin.o
%{gcclibdir}/crtend.o
%{gcclibdir}/crtfastmath.o
%{gcclibdir}/specs
%dir %{gcclibdir}/include
%{gcclibdir}/include/adxintrin.h
%{gcclibdir}/include/ammintrin.h
%{gcclibdir}/include/amxbf16intrin.h
%{gcclibdir}/include/amxint8intrin.h
%{gcclibdir}/include/amxtileintrin.h
%{gcclibdir}/include/avx2intrin.h
%{gcclibdir}/include/avx5124fmapsintrin.h
%{gcclibdir}/include/avx5124vnniwintrin.h
%{gcclibdir}/include/avx512bf16intrin.h
%{gcclibdir}/include/avx512bf16vlintrin.h
%{gcclibdir}/include/avx512bitalgintrin.h
%{gcclibdir}/include/avx512bwintrin.h
%{gcclibdir}/include/avx512cdintrin.h
%{gcclibdir}/include/avx512dqintrin.h
%{gcclibdir}/include/avx512erintrin.h
%{gcclibdir}/include/avx512fintrin.h
%{gcclibdir}/include/avx512ifmaintrin.h
%{gcclibdir}/include/avx512ifmavlintrin.h
%{gcclibdir}/include/avx512pfintrin.h
%{gcclibdir}/include/avx512vbmi2intrin.h
%{gcclibdir}/include/avx512vbmi2vlintrin.h
%{gcclibdir}/include/avx512vbmiintrin.h
%{gcclibdir}/include/avx512vbmivlintrin.h
%{gcclibdir}/include/avx512vlbwintrin.h
%{gcclibdir}/include/avx512vldqintrin.h
%{gcclibdir}/include/avx512vlintrin.h
%{gcclibdir}/include/avx512vnniintrin.h
%{gcclibdir}/include/avx512vnnivlintrin.h
%{gcclibdir}/include/avx512vp2intersectintrin.h
%{gcclibdir}/include/avx512vp2intersectvlintrin.h
%{gcclibdir}/include/avx512vpopcntdqintrin.h
%{gcclibdir}/include/avx512vpopcntdqvlintrin.h
%{gcclibdir}/include/avxintrin.h
%{gcclibdir}/include/avxvnniintrin.h
%{gcclibdir}/include/bmi2intrin.h
%{gcclibdir}/include/bmiintrin.h
%{gcclibdir}/include/bmmintrin.h
%{gcclibdir}/include/cet.h
%{gcclibdir}/include/cetintrin.h
%{gcclibdir}/include/cldemoteintrin.h
%{gcclibdir}/include/clflushoptintrin.h
%{gcclibdir}/include/clwbintrin.h
%{gcclibdir}/include/clzerointrin.h
%{gcclibdir}/include/cpuid.h
%{gcclibdir}/include/cross-stdarg.h
%{gcclibdir}/include/emmintrin.h
%{gcclibdir}/include/enqcmdintrin.h
%{gcclibdir}/include/f16cintrin.h
%{gcclibdir}/include/float.h
%{gcclibdir}/include/fma4intrin.h
%{gcclibdir}/include/fmaintrin.h
%{gcclibdir}/include/fxsrintrin.h
%{gcclibdir}/include/gcov.h
%{gcclibdir}/include/gfniintrin.h
%{gcclibdir}/include/hresetintrin.h
%{gcclibdir}/include/ia32intrin.h
%{gcclibdir}/include/immintrin.h
%{gcclibdir}/include/iso646.h
%{gcclibdir}/include/keylockerintrin.h
%{gcclibdir}/include/limits.h
%{gcclibdir}/include/lwpintrin.h
%{gcclibdir}/include/lzcntintrin.h
%{gcclibdir}/include/mm3dnow.h
%{gcclibdir}/include/mm_malloc.h
%{gcclibdir}/include/mmintrin.h
%{gcclibdir}/include/movdirintrin.h
%{gcclibdir}/include/mwaitintrin.h
%{gcclibdir}/include/mwaitxintrin.h
%{gcclibdir}/include/nmmintrin.h
%{gcclibdir}/include/pconfigintrin.h
%{gcclibdir}/include/pkuintrin.h
%{gcclibdir}/include/pmmintrin.h
%{gcclibdir}/include/popcntintrin.h
%{gcclibdir}/include/prfchwintrin.h
%{gcclibdir}/include/rdseedintrin.h
%{gcclibdir}/include/rtmintrin.h
%{gcclibdir}/include/serializeintrin.h
%{gcclibdir}/include/sgxintrin.h
%{gcclibdir}/include/shaintrin.h
%{gcclibdir}/include/smmintrin.h
%{gcclibdir}/include/stdalign.h
%{gcclibdir}/include/stdarg.h
%{gcclibdir}/include/stdatomic.h
%{gcclibdir}/include/stdbool.h
%{gcclibdir}/include/stddef.h
%{gcclibdir}/include/stdfix.h
%{gcclibdir}/include/stdint-gcc.h
%{gcclibdir}/include/stdint.h
%{gcclibdir}/include/stdnoreturn.h
%{gcclibdir}/include/syslimits.h
%{gcclibdir}/include/tbmintrin.h
%{gcclibdir}/include/tgmath.h
%{gcclibdir}/include/tmmintrin.h
%{gcclibdir}/include/tsxldtrkintrin.h
%{gcclibdir}/include/uintrintrin.h
%{gcclibdir}/include/unwind.h
%{gcclibdir}/include/vaesintrin.h
%{gcclibdir}/include/varargs.h
%{gcclibdir}/include/vpclmulqdqintrin.h
%{gcclibdir}/include/waitpkgintrin.h
%{gcclibdir}/include/wbnoinvdintrin.h
%{gcclibdir}/include/wmmintrin.h
%{gcclibdir}/include/x86gprintrin.h
%{gcclibdir}/include/x86intrin.h
%{gcclibdir}/include/xmmintrin.h
%{gcclibdir}/include/xopintrin.h
%{gcclibdir}/include/xsavecintrin.h
%{gcclibdir}/include/xsaveintrin.h
%{gcclibdir}/include/xsaveoptintrin.h
%{gcclibdir}/include/xsavesintrin.h
%{gcclibdir}/include/xtestintrin.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*
%{_mandir}/man1/%{target}-gcov-dump.1*
%{_mandir}/man1/%{target}-gcov-tool.1*

# mingw-w64 runtime
%{archlibdir}/CRT_*.o
%{archlibdir}/binmode.o
%{archlibdir}/crt*.o
%{archlibdir}/dllcrt*.o
%{archlibdir}/gcrt*.o
%{archlibdir}/txtmode.o

# Win64 API+mingw-w64 runtime
%{archlibdir}/lib6to4svc.a
%{archlibdir}/libCINTIME.a
%{archlibdir}/libPS5UI.a
%{archlibdir}/libPSCRIPT5.a
%{archlibdir}/libUNIDRV.a
%{archlibdir}/libUNIDRVUI.a
%{archlibdir}/libaaaamon.a
%{archlibdir}/libacledit.a
%{archlibdir}/libaclui.a
%{archlibdir}/libactiveds.a
%{archlibdir}/libactxprxy.a
%{archlibdir}/libadmparse.a
%{archlibdir}/libadmwprox.a
%{archlibdir}/libadptif.a
%{archlibdir}/libadrot.a
%{archlibdir}/libadsiis.a
%{archlibdir}/libadsiisex.a
%{archlibdir}/libadsldp.a
%{archlibdir}/libadsldpc.a
%{archlibdir}/libadsmsext.a
%{archlibdir}/libadsnt.a
%{archlibdir}/libadvapi32.a
%{archlibdir}/libadvpack.a
%{archlibdir}/libaelupsvc.a
%{archlibdir}/libagentanm.a
%{archlibdir}/libagentctl.a
%{archlibdir}/libagentdp2.a
%{archlibdir}/libagentdpv.a
%{archlibdir}/libagentmpx.a
%{archlibdir}/libagentpsh.a
%{archlibdir}/libagentsr.a
%{archlibdir}/libagrmco64.a
%{archlibdir}/libagtintl.a
%{archlibdir}/libakscoinst.a
%{archlibdir}/libalrsvc.a
%{archlibdir}/libamstream.a
%{archlibdir}/libapcups.a
%{archlibdir}/libapphelp.a
%{archlibdir}/libappmgmts.a
%{archlibdir}/libappmgr.a
%{archlibdir}/libaqadmin.a
%{archlibdir}/libaqueue.a
%{archlibdir}/libasp.a
%{archlibdir}/libaspperf.a
%{archlibdir}/libasycfilt.a
%{archlibdir}/libatkctrs.a
%{archlibdir}/libatl.a
%{archlibdir}/libatmlib.a
%{archlibdir}/libatmpvcno.a
%{archlibdir}/libatrace.a
%{archlibdir}/libaudiosrv.a
%{archlibdir}/libauthz.a
%{archlibdir}/libautodisc.a
%{archlibdir}/libavicap32.a
%{archlibdir}/libavifil32.a
%{archlibdir}/libazroles.a
%{archlibdir}/libazroleui.a
%{archlibdir}/libbasesrv.a
%{archlibdir}/libbatmeter.a
%{archlibdir}/libbatt.a
%{archlibdir}/libbcrypt.a
%{archlibdir}/libbidispl.a
%{archlibdir}/libbitsprx2.a
%{archlibdir}/libbitsprx3.a
%{archlibdir}/libbnts.a
%{archlibdir}/libbootvid.a
%{archlibdir}/libbrowscap.a
%{archlibdir}/libbrowser.a
%{archlibdir}/libbrowseui.a
%{archlibdir}/libbrpinfo.a
%{archlibdir}/libbthci.a
%{archlibdir}/libbthprops.a
%{archlibdir}/libbthserv.a
%{archlibdir}/libbtpanui.a
%{archlibdir}/libc_g18030.a
%{archlibdir}/libc_is2022.a
%{archlibdir}/libc_iscii.a
%{archlibdir}/libcabinet.a
%{archlibdir}/libcabview.a
%{archlibdir}/libcamocx.a
%{archlibdir}/libcards.a
%{archlibdir}/libcatsrv.a
%{archlibdir}/libcatsrvps.a
%{archlibdir}/libcatsrvut.a
%{archlibdir}/libccfgnt.a
%{archlibdir}/libcdfview.a
%{archlibdir}/libcdm.a
%{archlibdir}/libcdosys.a
%{archlibdir}/libcertcli.a
%{archlibdir}/libcertmgr.a
%{archlibdir}/libcertobj.a
%{archlibdir}/libcfgbkend.a
%{archlibdir}/libcfgmgr32.a
%{archlibdir}/libchsbrkr.a
%{archlibdir}/libchtbrkr.a
%{archlibdir}/libchtskdic.a
%{archlibdir}/libciadmin.a
%{archlibdir}/libcic.a
%{archlibdir}/libcimwin32.a
%{archlibdir}/libciodm.a
%{archlibdir}/libclasspnp.a
%{archlibdir}/libclb.a
%{archlibdir}/libclbcatex.a
%{archlibdir}/libclbcatq.a
%{archlibdir}/libclfsw32.a
%{archlibdir}/libcliconfg.a
%{archlibdir}/libclusapi.a
%{archlibdir}/libcmcfg32.a
%{archlibdir}/libcmdial32.a
%{archlibdir}/libcmpbk32.a
%{archlibdir}/libcmprops.a
%{archlibdir}/libcmsetacl.a
%{archlibdir}/libcmutil.a
%{archlibdir}/libcnbjmon.a
%{archlibdir}/libcnetcfg.a
%{archlibdir}/libcnvfat.a
%{archlibdir}/libcoadmin.a
%{archlibdir}/libcolbact.a
%{archlibdir}/libcomaddin.a
%{archlibdir}/libcomadmin.a
%{archlibdir}/libcomcat.a
%{archlibdir}/libcomctl32.a
%{archlibdir}/libcomdlg32.a
%{archlibdir}/libcompatui.a
%{archlibdir}/libcompstui.a
%{archlibdir}/libcomrepl.a
%{archlibdir}/libcomres.a
%{archlibdir}/libcomsetup.a
%{archlibdir}/libcomsnap.a
%{archlibdir}/libcomsvcs.a
%{archlibdir}/libcomuid.a
%{archlibdir}/libconfmsp.a
%{archlibdir}/libconnect.a
%{archlibdir}/libconsole.a
%{archlibdir}/libcontrot.a
%{archlibdir}/libcorpol.a
%{archlibdir}/libcredui.a
%{archlibdir}/libcrtdll.a
%{archlibdir}/libcrypt32.a
%{archlibdir}/libcryptdlg.a
%{archlibdir}/libcryptdll.a
%{archlibdir}/libcryptext.a
%{archlibdir}/libcryptnet.a
%{archlibdir}/libcryptsp.a
%{archlibdir}/libcryptsvc.a
%{archlibdir}/libcryptui.a
%{archlibdir}/libcryptxml.a
%{archlibdir}/libcscapi.a
%{archlibdir}/libcscdll.a
%{archlibdir}/libcscui.a
%{archlibdir}/libcsrsrv.a
%{archlibdir}/libd2d1.a
%{archlibdir}/libd3d8thk.a
%{archlibdir}/libd3d9.a
%{archlibdir}/libd3dcompiler*.a
%{archlibdir}/libd3dcsxd*.a
%{archlibdir}/libd3dx10*.a
%{archlibdir}/libd3dx11*.a
%{archlibdir}/libd3dx9*.a
%{archlibdir}/libd3dxof.a
%{archlibdir}/libdanim.a
%{archlibdir}/libdataclen.a
%{archlibdir}/libdatime.a
%{archlibdir}/libdavclnt.a
%{archlibdir}/libdavcprox.a
%{archlibdir}/libdbgeng.a
%{archlibdir}/libdbghelp.a
%{archlibdir}/libdbnetlib.a
%{archlibdir}/libdbnmpntw.a
%{archlibdir}/libdciman32.a
%{archlibdir}/libddraw.a
%{archlibdir}/libddrawex.a
%{archlibdir}/libdelayimp.a
%{archlibdir}/libdeskadp.a
%{archlibdir}/libdeskmon.a
%{archlibdir}/libdeskperf.a
%{archlibdir}/libdevenum.a
%{archlibdir}/libdevmgr.a
%{archlibdir}/libdfrgifps.a
%{archlibdir}/libdfrgsnap.a
%{archlibdir}/libdfrgui.a
%{archlibdir}/libdfsshlex.a
%{archlibdir}/libdgnet.a
%{archlibdir}/libdhcpcsvc.a
%{archlibdir}/libdhcpcsvc6.a
%{archlibdir}/libdhcpmon.a
%{archlibdir}/libdhcpsapi.a
%{archlibdir}/libdiactfrm.a
%{archlibdir}/libdigest.a
%{archlibdir}/libdimap.a
%{archlibdir}/libdimsntfy.a
%{archlibdir}/libdimsroam.a
%{archlibdir}/libdinput.a
%{archlibdir}/libdinput8.a
%{archlibdir}/libdirectdb.a
%{archlibdir}/libdiskcopy.a
%{archlibdir}/libdispex.a
%{archlibdir}/libdmconfig.a
%{archlibdir}/libdmdlgs.a
%{archlibdir}/libdmdskmgr.a
%{archlibdir}/libdmintf.a
%{archlibdir}/libdmivcitf.a
%{archlibdir}/libdmocx.a
%{archlibdir}/libdmoguids.a
%{archlibdir}/libdmserver.a
%{archlibdir}/libdmutil.a
%{archlibdir}/libdmvdsitf.a
%{archlibdir}/libdnsapi.a
%{archlibdir}/libdnsrslvr.a
%{archlibdir}/libdocprop.a
%{archlibdir}/libdocprop2.a
%{archlibdir}/libdpnaddr.a
%{archlibdir}/libdpnet.a
%{archlibdir}/libdpnhpast.a
%{archlibdir}/libdpnhupnp.a
%{archlibdir}/libdpnlobby.a
%{archlibdir}/libdpvacm.a
%{archlibdir}/libdpvoice.a
%{archlibdir}/libdpvvox.a
%{archlibdir}/libdrprov.a
%{archlibdir}/libds32gt.a
%{archlibdir}/libdsauth.a
%{archlibdir}/libdsdmo.a
%{archlibdir}/libdsdmoprp.a
%{archlibdir}/libdskquota.a
%{archlibdir}/libdskquoui.a
%{archlibdir}/libdsound.a
%{archlibdir}/libdsound3d.a
%{archlibdir}/libdsprop.a
%{archlibdir}/libdsprov.a
%{archlibdir}/libdsquery.a
%{archlibdir}/libdssec.a
%{archlibdir}/libdssenh.a
%{archlibdir}/libdsuiext.a
%{archlibdir}/libduser.a
%{archlibdir}/libdwmapi.a
%{archlibdir}/libdwrite.a
%{archlibdir}/libdxdiagn.a
%{archlibdir}/libdxerr8.a
%{archlibdir}/libdxerr9.a
%{archlibdir}/libdxgi.a
%{archlibdir}/libdxguid.a
%{archlibdir}/libdxtmsft.a
%{archlibdir}/libdxtrans.a
%{archlibdir}/libdxva2.a
%{archlibdir}/libeappcfg.a
%{archlibdir}/libeappgnui.a
%{archlibdir}/libeapphost.a
%{archlibdir}/libeappprxy.a
%{archlibdir}/libefsadu.a
%{archlibdir}/libels.a
%{archlibdir}/libencapi.a
%{archlibdir}/libersvc.a
%{archlibdir}/libes.a
%{archlibdir}/libesent.a
%{archlibdir}/libesentprf.a
%{archlibdir}/libesscli.a
%{archlibdir}/libeventcls.a
%{archlibdir}/libeventlog.a
%{archlibdir}/libevntagnt.a
%{archlibdir}/libevntrprv.a
%{archlibdir}/libevr.a
%{archlibdir}/libevtgprov.a
%{archlibdir}/libexstrace.a
%{archlibdir}/libextmgr.a
%{archlibdir}/libf3ahvoas.a
%{archlibdir}/libfastprox.a
%{archlibdir}/libfaultrep.a
%{archlibdir}/libfcachdll.a
%{archlibdir}/libfde.a
%{archlibdir}/libfdeploy.a
%{archlibdir}/libfeclient.a
%{archlibdir}/libfilemgmt.a
%{archlibdir}/libfldrclnr.a
%{archlibdir}/libfltlib.a
%{archlibdir}/libfmifs.a
%{archlibdir}/libfontext.a
%{archlibdir}/libfontsub.a
%{archlibdir}/libframedyn.a
%{archlibdir}/libfsusd.a
%{archlibdir}/libftpctrs2.a
%{archlibdir}/libftpmib.a
%{archlibdir}/libftpsvc2.a
%{archlibdir}/libfwcfg.a
%{archlibdir}/libfwpuclnt.a
%{archlibdir}/libfxsapi.a
%{archlibdir}/libfxscfgwz.a
%{archlibdir}/libfxscom.a
%{archlibdir}/libfxscomex.a
%{archlibdir}/libfxsdrv.a
%{archlibdir}/libfxsmon.a
%{archlibdir}/libfxsocm.a
%{archlibdir}/libfxsperf.a
%{archlibdir}/libfxsroute.a
%{archlibdir}/libfxsst.a
%{archlibdir}/libfxst30.a
%{archlibdir}/libfxstiff.a
%{archlibdir}/libfxsui.a
%{archlibdir}/libfxswzrd.a
%{archlibdir}/libgcdef.a
%{archlibdir}/libgdi32.a
%{archlibdir}/libgdiplus.a
%{archlibdir}/libgetuname.a
%{archlibdir}/libglmf32.a
%{archlibdir}/libglu32.a
%{archlibdir}/libgmon.a
%{archlibdir}/libgpedit.a
%{archlibdir}/libgpkcsp.a
%{archlibdir}/libgptext.a
%{archlibdir}/libguitrn.a
%{archlibdir}/libgzip.a
%{archlibdir}/libh323msp.a
%{archlibdir}/libhal.a
%{archlibdir}/libhbaapi.a
%{archlibdir}/libhgfs.a
%{archlibdir}/libhhsetup.a
%{archlibdir}/libhid.a
%{archlibdir}/libhidclass.a
%{archlibdir}/libhidparse.a
%{archlibdir}/libhlink.a
%{archlibdir}/libhmmapi.a
%{archlibdir}/libhnetcfg.a
%{archlibdir}/libhnetmon.a
%{archlibdir}/libhnetwiz.a
%{archlibdir}/libhostmib.a
%{archlibdir}/libhotplug.a
%{archlibdir}/libhticons.a
%{archlibdir}/libhtrn_jis.a
%{archlibdir}/libhttpapi.a
%{archlibdir}/libhttpext.a
%{archlibdir}/libhttpmib.a
%{archlibdir}/libhttpodbc.a
%{archlibdir}/libhtui.a
%{archlibdir}/libhypertrm.a
%{archlibdir}/libiasacct.a
%{archlibdir}/libiasads.a
%{archlibdir}/libiashlpr.a
%{archlibdir}/libiasnap.a
%{archlibdir}/libiaspolcy.a
%{archlibdir}/libiasrad.a
%{archlibdir}/libiassam.a
%{archlibdir}/libiassdo.a
%{archlibdir}/libiassvcs.a
%{archlibdir}/libicaapi.a
%{archlibdir}/libicfgnt5.a
%{archlibdir}/libicm32.a
%{archlibdir}/libicmp.a
%{archlibdir}/libicmui.a
%{archlibdir}/libicwconn.a
%{archlibdir}/libicwdial.a
%{archlibdir}/libicwdl.a
%{archlibdir}/libicwhelp.a
%{archlibdir}/libicwphbk.a
%{archlibdir}/libicwutil.a
%{archlibdir}/libidq.a
%{archlibdir}/libieakeng.a
%{archlibdir}/libieaksie.a
%{archlibdir}/libiedkcs32.a
%{archlibdir}/libieencode.a
%{archlibdir}/libiepeers.a
%{archlibdir}/libiernonce.a
%{archlibdir}/libiesetup.a
%{archlibdir}/libifmon.a
%{archlibdir}/libifsutil.a
%{archlibdir}/libigmpagnt.a
%{archlibdir}/libiis.a
%{archlibdir}/libiisadmin.a
%{archlibdir}/libiiscfg.a
%{archlibdir}/libiisclex4.a
%{archlibdir}/libiisext.a
%{archlibdir}/libiislog.a
%{archlibdir}/libiismap.a
%{archlibdir}/libiisrstap.a
%{archlibdir}/libiisrtl.a
%{archlibdir}/libiissuba.a
%{archlibdir}/libiisui.a
%{archlibdir}/libiisuiobj.a
%{archlibdir}/libiisutil.a
%{archlibdir}/libiisw3adm.a
%{archlibdir}/libiiswmi.a
%{archlibdir}/libimagehlp.a
%{archlibdir}/libimekrcic.a
%{archlibdir}/libimeshare.a
%{archlibdir}/libimgutil.a
%{archlibdir}/libimjp81k.a
%{archlibdir}/libimjpcic.a
%{archlibdir}/libimjpcus.a
%{archlibdir}/libimjpdct.a
%{archlibdir}/libimjputyc.a
%{archlibdir}/libimm32.a
%{archlibdir}/libimsinsnt.a
%{archlibdir}/libimskdic.a
%{archlibdir}/libinetcfg.a
%{archlibdir}/libinetcomm.a
%{archlibdir}/libinetmgr.a
%{archlibdir}/libinetmib1.a
%{archlibdir}/libinetpp.a
%{archlibdir}/libinetppui.a
%{archlibdir}/libinfoadmn.a
%{archlibdir}/libinfocomm.a
%{archlibdir}/libinfoctrs.a
%{archlibdir}/libinfosoft.a
%{archlibdir}/libinitpki.a
%{archlibdir}/libinput.a
%{archlibdir}/libinseng.a
%{archlibdir}/libiphlpapi.a
%{archlibdir}/libipmontr.a
%{archlibdir}/libipnathlp.a
%{archlibdir}/libippromon.a
%{archlibdir}/libiprip.a
%{archlibdir}/libiprop.a
%{archlibdir}/libiprtprio.a
%{archlibdir}/libiprtrmgr.a
%{archlibdir}/libipsecsnp.a
%{archlibdir}/libipsecsvc.a
%{archlibdir}/libipsmsnap.a
%{archlibdir}/libipv6mon.a
%{archlibdir}/libipxsap.a
%{archlibdir}/libirclass.a
%{archlibdir}/libisapips.a
%{archlibdir}/libisatq.a
%{archlibdir}/libiscomlog.a
%{archlibdir}/libiscsidsc.a
%{archlibdir}/libisign32.a
%{archlibdir}/libitircl.a
%{archlibdir}/libitss.a
%{archlibdir}/libixsso.a
%{archlibdir}/libiyuv_32.a
%{archlibdir}/libjet500.a
%{archlibdir}/libjscript.a
%{archlibdir}/libjsproxy.a
%{archlibdir}/libkbd*.a
%{archlibdir}/libkd1394.a
%{archlibdir}/libkdcom.a
%{archlibdir}/libkerberos.a
%{archlibdir}/libkernel32.a
%{archlibdir}/libkeymgr.a
%{archlibdir}/libkorwbrkr.a
%{archlibdir}/libkrnlprov.a
%{archlibdir}/libks.a
%{archlibdir}/libksuser.a
%{archlibdir}/libktmw32.a
%{archlibdir}/liblangwrbk.a
%{archlibdir}/liblargeint.a
%{archlibdir}/liblicdll.a
%{archlibdir}/liblicmgr10.a
%{archlibdir}/liblicwmi.a
%{archlibdir}/liblinkinfo.a
%{archlibdir}/liblmhsvc.a
%{archlibdir}/liblmmib2.a
%{archlibdir}/liblmrt.a
%{archlibdir}/libloadperf.a
%{archlibdir}/liblocalsec.a
%{archlibdir}/liblocalspl.a
%{archlibdir}/liblocalui.a
%{archlibdir}/liblog.a
%{archlibdir}/libloghours.a
%{archlibdir}/liblogscrpt.a
%{archlibdir}/liblonsint.a
%{archlibdir}/liblpdsvc.a
%{archlibdir}/liblpk.a
%{archlibdir}/liblprhelp.a
%{archlibdir}/liblprmon.a
%{archlibdir}/liblprmonui.a
%{archlibdir}/liblsasrv.a
%{archlibdir}/liblz32.a
%{archlibdir}/libm.a
%{archlibdir}/libmag_hook.a
%{archlibdir}/libmailmsg.a
%{archlibdir}/libmapi32.a
%{archlibdir}/libmapistub.a
%{archlibdir}/libmcastmib.a
%{archlibdir}/libmcd32.a
%{archlibdir}/libmcdsrv32.a
%{archlibdir}/libmchgrcoi.a
%{archlibdir}/libmciavi32.a
%{archlibdir}/libmcicda.a
%{archlibdir}/libmciole32.a
%{archlibdir}/libmciqtz32.a
%{archlibdir}/libmciseq.a
%{archlibdir}/libmciwave.a
%{archlibdir}/libmdhcp.a
%{archlibdir}/libmdminst.a
%{archlibdir}/libmetadata.a
%{archlibdir}/libmf.a
%{archlibdir}/libmf3216.a
%{archlibdir}/libmfc42.a
%{archlibdir}/libmfc42u.a
%{archlibdir}/libmfcsubs.a
%{archlibdir}/libmfplat.a
%{archlibdir}/libmgmtapi.a
%{archlibdir}/libmidimap.a
%{archlibdir}/libmigism.a
%{archlibdir}/libmiglibnt.a
%{archlibdir}/libmimefilt.a
%{archlibdir}/libmingw32.a
%{archlibdir}/libmingwex.a
%{archlibdir}/libmingwthrd.a
%{archlibdir}/libmlang.a
%{archlibdir}/libmll_hp.a
%{archlibdir}/libmll_mtf.a
%{archlibdir}/libmll_qic.a
%{archlibdir}/libmmcbase.a
%{archlibdir}/libmmcndmgr.a
%{archlibdir}/libmmcshext.a
%{archlibdir}/libmmfutil.a
%{archlibdir}/libmmutilse.a
%{archlibdir}/libmobsync.a
%{archlibdir}/libmodemui.a
%{archlibdir}/libmofd.a
%{archlibdir}/libmoldname.a
%{archlibdir}/libmpr.a
%{archlibdir}/libmprapi.a
%{archlibdir}/libmprddm.a
%{archlibdir}/libmprdim.a
%{archlibdir}/libmprmsg.a
%{archlibdir}/libmprui.a
%{archlibdir}/libmqad.a
%{archlibdir}/libmqcertui.a
%{archlibdir}/libmqdscli.a
%{archlibdir}/libmqgentr.a
%{archlibdir}/libmqise.a
%{archlibdir}/libmqlogmgr.a
%{archlibdir}/libmqoa.a
%{archlibdir}/libmqperf.a
%{archlibdir}/libmqqm.a
%{archlibdir}/libmqrt.a
%{archlibdir}/libmqrtdep.a
%{archlibdir}/libmqsec.a
%{archlibdir}/libmqsnap.a
%{archlibdir}/libmqtrig.a
%{archlibdir}/libmqupgrd.a
%{archlibdir}/libmqutil.a
%{archlibdir}/libmsaatext.a
%{archlibdir}/libmsacm32.a
%{archlibdir}/libmsadce.a
%{archlibdir}/libmsadcf.a
%{archlibdir}/libmsadco.a
%{archlibdir}/libmsadcs.a
%{archlibdir}/libmsadds.a
%{archlibdir}/libmsado15.a
%{archlibdir}/libmsadomd.a
%{archlibdir}/libmsador15.a
%{archlibdir}/libmsadox.a
%{archlibdir}/libmsadrh15.a
%{archlibdir}/libmsafd.a
%{archlibdir}/libmsasn1.a
%{archlibdir}/libmscandui.a
%{archlibdir}/libmscat32.a
%{archlibdir}/libmscms.a
%{archlibdir}/libmsctfmonitor.a
%{archlibdir}/libmsctfp.a
%{archlibdir}/libmsdadiag.a
%{archlibdir}/libmsdaosp.a
%{archlibdir}/libmsdaprst.a
%{archlibdir}/libmsdaps.a
%{archlibdir}/libmsdarem.a
%{archlibdir}/libmsdart.a
%{archlibdir}/libmsdatl3.a
%{archlibdir}/libmsdfmap.a
%{archlibdir}/libmsdmo.a
%{archlibdir}/libmsdrm.a
%{archlibdir}/libmsdtclog.a
%{archlibdir}/libmsdtcprx.a
%{archlibdir}/libmsdtcstp.a
%{archlibdir}/libmsdtctm.a
%{archlibdir}/libmsdtcuiu.a
%{archlibdir}/libmsftedit.a
%{archlibdir}/libmsgina.a
%{archlibdir}/libmsgr3en.a
%{archlibdir}/libmsgrocm.a
%{archlibdir}/libmsgsvc.a
%{archlibdir}/libmshtml.a
%{archlibdir}/libmshtmled.a
%{archlibdir}/libmsi.a
%{archlibdir}/libmsident.a
%{archlibdir}/libmsieftp.a
%{archlibdir}/libmsihnd.a
%{archlibdir}/libmsimg32.a
%{archlibdir}/libmsimtf.a
%{archlibdir}/libmsinfo.a
%{archlibdir}/libmsiprov.a
%{archlibdir}/libmsir3jp.a
%{archlibdir}/libmsisip.a
%{archlibdir}/libmslbui.a
%{archlibdir}/libmsls31.a
%{archlibdir}/libmslwvtts.a
%{archlibdir}/libmsmqocm.a
%{archlibdir}/libmsobcomm.a
%{archlibdir}/libmsobdl.a
%{archlibdir}/libmsobmain.a
%{archlibdir}/libmsobshel.a
%{archlibdir}/libmsobweb.a
%{archlibdir}/libmsoe.a
%{archlibdir}/libmsoeacct.a
%{archlibdir}/libmsoert2.a
%{archlibdir}/libmspatcha.a
%{archlibdir}/libmspmsnsv.a
%{archlibdir}/libmsports.a
%{archlibdir}/libmsrating.a
%{archlibdir}/libmsrle32.a
%{archlibdir}/libmssign32.a
%{archlibdir}/libmssip32.a
%{archlibdir}/libmstask.a
%{archlibdir}/libmstime.a
%{archlibdir}/libmstlsapi.a
%{archlibdir}/libmstscax.a
%{archlibdir}/libmsutb.a
%{archlibdir}/libmsv1_0.a
%{archlibdir}/libmsvcirt.a
%{archlibdir}/libmsvcp60.a
%{archlibdir}/libmsvcr100.a
%{archlibdir}/libmsvcr110.a
%{archlibdir}/libmsvcr80.a
%{archlibdir}/libmsvcr90.a
%{archlibdir}/libmsvcr90d.a
%{archlibdir}/libmsvcrt.a
%{archlibdir}/libmsvfw32.a
%{archlibdir}/libmsvidc32.a
%{archlibdir}/libmsvidctl.a
%{archlibdir}/libmsw3prt.a
%{archlibdir}/libmswsock.a
%{archlibdir}/libmsxactps.a
%{archlibdir}/libmsxml3.a
%{archlibdir}/libmsxs64.a
%{archlibdir}/libmsyuv.a
%{archlibdir}/libmtxclu.a
%{archlibdir}/libmtxdm.a
%{archlibdir}/libmtxex.a
%{archlibdir}/libmtxoci.a
%{archlibdir}/libmycomput.a
%{archlibdir}/libmydocs.a
%{archlibdir}/libnarrhook.a
%{archlibdir}/libncobjapi.a
%{archlibdir}/libncprov.a
%{archlibdir}/libncrypt.a
%{archlibdir}/libncxpnt.a
%{archlibdir}/libnddeapi.a
%{archlibdir}/libnddenb32.a
%{archlibdir}/libndfapi.a
%{archlibdir}/libndis.a
%{archlibdir}/libndisnpp.a
%{archlibdir}/libnetapi32.a
%{archlibdir}/libnetcfgx.a
%{archlibdir}/libnetid.a
%{archlibdir}/libnetlogon.a
%{archlibdir}/libnetman.a
%{archlibdir}/libnetoc.a
%{archlibdir}/libnetplwiz.a
%{archlibdir}/libnetrap.a
%{archlibdir}/libnetshell.a
%{archlibdir}/libnetui0.a
%{archlibdir}/libnetui1.a
%{archlibdir}/libnetui2.a
%{archlibdir}/libnewdev.a
%{archlibdir}/libnextlink.a
%{archlibdir}/libnlhtml.a
%{archlibdir}/libnntpadm.a
%{archlibdir}/libnntpapi.a
%{archlibdir}/libnntpsnap.a
%{archlibdir}/libnormaliz.a
%{archlibdir}/libnpptools.a
%{archlibdir}/libnshipsec.a
%{archlibdir}/libntdll.a
%{archlibdir}/libntdsapi.a
%{archlibdir}/libntdsbcli.a
%{archlibdir}/libntevt.a
%{archlibdir}/libntfsdrv.a
%{archlibdir}/libntlanman.a
%{archlibdir}/libntlanui.a
%{archlibdir}/libntlanui2.a
%{archlibdir}/libntlsapi.a
%{archlibdir}/libntmarta.a
%{archlibdir}/libntmsapi.a
%{archlibdir}/libntmsdba.a
%{archlibdir}/libntmsevt.a
%{archlibdir}/libntmsmgr.a
%{archlibdir}/libntmssvc.a
%{archlibdir}/libntoc.a
%{archlibdir}/libntoskrnl.a
%{archlibdir}/libntprint.a
%{archlibdir}/libntshrui.a
%{archlibdir}/libntvdm64.a
%{archlibdir}/libnwprovau.a
%{archlibdir}/liboakley.a
%{archlibdir}/libobjsel.a
%{archlibdir}/liboccache.a
%{archlibdir}/libocgen.a
%{archlibdir}/libocmanage.a
%{archlibdir}/libocmsn.a
%{archlibdir}/libodbc32.a
%{archlibdir}/libodbc32gt.a
%{archlibdir}/libodbcbcp.a
%{archlibdir}/libodbcconf.a
%{archlibdir}/libodbccp32.a
%{archlibdir}/libodbccr32.a
%{archlibdir}/libodbccu32.a
%{archlibdir}/libodbctrac.a
%{archlibdir}/liboeimport.a
%{archlibdir}/liboemiglib.a
%{archlibdir}/libofffilt.a
%{archlibdir}/libole32.a
%{archlibdir}/liboleacc.a
%{archlibdir}/liboleaut32.a
%{archlibdir}/libolecli32.a
%{archlibdir}/libolecnv32.a
%{archlibdir}/liboledb32.a
%{archlibdir}/liboledb32r.a
%{archlibdir}/liboledlg.a
%{archlibdir}/liboleprn.a
%{archlibdir}/libolesvr32.a
%{archlibdir}/libopengl32.a
%{archlibdir}/libosuninst.a
%{archlibdir}/libovprintmondll.a
%{archlibdir}/libp2p.a
%{archlibdir}/libp2pcollab.a
%{archlibdir}/libp2pgraph.a
%{archlibdir}/libpanmap.a
%{archlibdir}/libpautoenr.a
%{archlibdir}/libpchshell.a
%{archlibdir}/libpchsvc.a
%{archlibdir}/libpcwum.a
%{archlibdir}/libpdh.a
%{archlibdir}/libperfctrs.a
%{archlibdir}/libperfdisk.a
%{archlibdir}/libperfnet.a
%{archlibdir}/libperfos.a
%{archlibdir}/libperfproc.a
%{archlibdir}/libperfts.a
%{archlibdir}/libphotowiz.a
%{archlibdir}/libpid.a
%{archlibdir}/libpidgen.a
%{archlibdir}/libpintlcsa.a
%{archlibdir}/libpintlcsd.a
%{archlibdir}/libpjlmon.a
%{archlibdir}/libpngfilt.a
%{archlibdir}/libpolicman.a
%{archlibdir}/libpolstore.a
%{archlibdir}/libpowrprof.a
%{archlibdir}/libprintui.a
%{archlibdir}/libprofmap.a
%{archlibdir}/libprovthrd.a
%{archlibdir}/libpsapi.a
%{archlibdir}/libpsbase.a
%{archlibdir}/libpschdprf.a
%{archlibdir}/libpsnppagn.a
%{archlibdir}/libpstorec.a
%{archlibdir}/libpstorsvc.a
%{archlibdir}/libqasf.a
%{archlibdir}/libqcap.a
%{archlibdir}/libqdv.a
%{archlibdir}/libqdvd.a
%{archlibdir}/libqedit.a
%{archlibdir}/libqmgr.a
%{archlibdir}/libqmgrprxy.a
%{archlibdir}/libqosname.a
%{archlibdir}/libquartz.a
%{archlibdir}/libquery.a
%{archlibdir}/libqutil.a
%{archlibdir}/libqwave.a
%{archlibdir}/libracpldlg.a
%{archlibdir}/librasadhlp.a
%{archlibdir}/librasapi32.a
%{archlibdir}/librasauto.a
%{archlibdir}/libraschap.a
%{archlibdir}/librasctrs.a
%{archlibdir}/librasdlg.a
%{archlibdir}/librasman.a
%{archlibdir}/librasmans.a
%{archlibdir}/librasmontr.a
%{archlibdir}/librasmxs.a
%{archlibdir}/librasppp.a
%{archlibdir}/librasrad.a
%{archlibdir}/librassapi.a
%{archlibdir}/librasser.a
%{archlibdir}/librastapi.a
%{archlibdir}/librastls.a
%{archlibdir}/librcbdyctl.a
%{archlibdir}/librdchost.a
%{archlibdir}/librdpcfgex.a
%{archlibdir}/librdpsnd.a
%{archlibdir}/librdpwsx.a
%{archlibdir}/libregapi.a
%{archlibdir}/libregsvc.a
%{archlibdir}/libregwizc.a
%{archlibdir}/libremotepg.a
%{archlibdir}/librend.a
%{archlibdir}/librepdrvfs.a
%{archlibdir}/libresutil.a
%{archlibdir}/libresutils.a
%{archlibdir}/libriched20.a
%{archlibdir}/librnr20.a
%{archlibdir}/libroutetab.a
%{archlibdir}/librpcdiag.a
%{archlibdir}/librpchttp.a
%{archlibdir}/librpcns4.a
%{archlibdir}/librpcnsh.a
%{archlibdir}/librpcref.a
%{archlibdir}/librpcrt4.a
%{archlibdir}/librpcss.a
%{archlibdir}/librsaenh.a
%{archlibdir}/librsfsaps.a
%{archlibdir}/librshx32.a
%{archlibdir}/librsmps.a
%{archlibdir}/librstrmgr.a
%{archlibdir}/librtm.a
%{archlibdir}/librtutils.a
%{archlibdir}/librwnh.a
%{archlibdir}/libsafrcdlg.a
%{archlibdir}/libsafrdm.a
%{archlibdir}/libsafrslv.a
%{archlibdir}/libsamlib.a
%{archlibdir}/libsamsrv.a
%{archlibdir}/libsapi.a
%{archlibdir}/libscarddlg.a
%{archlibdir}/libsccbase.a
%{archlibdir}/libsccsccp.a
%{archlibdir}/libscecli.a
%{archlibdir}/libscesrv.a
%{archlibdir}/libschannel.a
%{archlibdir}/libschedsvc.a
%{archlibdir}/libsclgntfy.a
%{archlibdir}/libscredir.a
%{archlibdir}/libscript.a
%{archlibdir}/libscripto.a
%{archlibdir}/libscriptpw.a
%{archlibdir}/libscrnsave.a
%{archlibdir}/libscrnsavw.a
%{archlibdir}/libscrobj.a
%{archlibdir}/libscrptutl.a
%{archlibdir}/libscrrun.a
%{archlibdir}/libsdhcinst.a
%{archlibdir}/libsdpblb.a
%{archlibdir}/libseclogon.a
%{archlibdir}/libsecur32.a
%{archlibdir}/libsecurity.a
%{archlibdir}/libsendcmsg.a
%{archlibdir}/libsendmail.a
%{archlibdir}/libsens.a
%{archlibdir}/libsensapi.a
%{archlibdir}/libsenscfg.a
%{archlibdir}/libseo.a
%{archlibdir}/libseos.a
%{archlibdir}/libserialui.a
%{archlibdir}/libservdeps.a
%{archlibdir}/libserwvdrv.a
%{archlibdir}/libsetupapi.a
%{archlibdir}/libsetupqry.a
%{archlibdir}/libsfc.a
%{archlibdir}/libsfc_os.a
%{archlibdir}/libsfcfiles.a
%{archlibdir}/libsfmapi.a
%{archlibdir}/libshdocvw.a
%{archlibdir}/libshell32.a
%{archlibdir}/libshfolder.a
%{archlibdir}/libshgina.a
%{archlibdir}/libshimeng.a
%{archlibdir}/libshimgvw.a
%{archlibdir}/libshlwapi.a
%{archlibdir}/libshmedia.a
%{archlibdir}/libshscrap.a
%{archlibdir}/libshsvcs.a
%{archlibdir}/libsigtab.a
%{archlibdir}/libsimptcp.a
%{archlibdir}/libsisbkup.a
%{archlibdir}/libskdll.a
%{archlibdir}/libslayerxp.a
%{archlibdir}/libslbcsp.a
%{archlibdir}/libslbiop.a
%{archlibdir}/libslc.a
%{archlibdir}/libslcext.a
%{archlibdir}/libslwga.a
%{archlibdir}/libsmlogcfg.a
%{archlibdir}/libsmtpadm.a
%{archlibdir}/libsmtpapi.a
%{archlibdir}/libsmtpcons.a
%{archlibdir}/libsmtpctrs.a
%{archlibdir}/libsmtpsnap.a
%{archlibdir}/libsmtpsvc.a
%{archlibdir}/libsniffpol.a
%{archlibdir}/libsnmpapi.a
%{archlibdir}/libsnmpcl.a
%{archlibdir}/libsnmpincl.a
%{archlibdir}/libsnmpmib.a
%{archlibdir}/libsnmpsmir.a
%{archlibdir}/libsnmpsnap.a
%{archlibdir}/libsnmpstup.a
%{archlibdir}/libsnmpthrd.a
%{archlibdir}/libsnprfdll.a
%{archlibdir}/libsoftkbd.a
%{archlibdir}/libsoftpub.a
%{archlibdir}/libspcommon.a
%{archlibdir}/libspoolss.a
%{archlibdir}/libsptip.a
%{archlibdir}/libspttseng.a
%{archlibdir}/libsqlsrv32.a
%{archlibdir}/libsqlxmlx.a
%{archlibdir}/libsrchctls.a
%{archlibdir}/libsrchui.a
%{archlibdir}/libsrclient.a
%{archlibdir}/libsrrstr.a
%{archlibdir}/libsrsvc.a
%{archlibdir}/libsrvsvc.a
%{archlibdir}/libssdpapi.a
%{archlibdir}/libssdpsrv.a
%{archlibdir}/libssinc.a
%{archlibdir}/libsspicli.a
%{archlibdir}/libsstub.a
%{archlibdir}/libstaxmem.a
%{archlibdir}/libstclient.a
%{archlibdir}/libstdprov.a
%{archlibdir}/libsti.a
%{archlibdir}/libsti_ci.a
%{archlibdir}/libstobject.a
%{archlibdir}/libstorprop.a
%{archlibdir}/libstreamci.a
%{archlibdir}/libstrmfilt.a
%{archlibdir}/libstrmiids.a
%{archlibdir}/libsvcext.a
%{archlibdir}/libsvcpack.a
%{archlibdir}/libswprv.a
%{archlibdir}/libsxs.a
%{archlibdir}/libsynceng.a
%{archlibdir}/libsyncui.a
%{archlibdir}/libsysinv.a
%{archlibdir}/libsysmod.a
%{archlibdir}/libsyssetup.a
%{archlibdir}/libt2embed.a
%{archlibdir}/libtapi3.a
%{archlibdir}/libtapi32.a
%{archlibdir}/libtapiperf.a
%{archlibdir}/libtapisrv.a
%{archlibdir}/libtbs.a
%{archlibdir}/libtcpmib.a
%{archlibdir}/libtcpmon.a
%{archlibdir}/libtcpmonui.a
%{archlibdir}/libtdh.a
%{archlibdir}/libtermmgr.a
%{archlibdir}/libtermsrv.a
%{archlibdir}/libthawbrkr.a
%{archlibdir}/libthemeui.a
%{archlibdir}/libtlntsvrp.a
%{archlibdir}/libtraffic.a
%{archlibdir}/libtrialoc.a
%{archlibdir}/libtrkwks.a
%{archlibdir}/libtsappcmp.a
%{archlibdir}/libtsbyuv.a
%{archlibdir}/libtscfgwmi.a
%{archlibdir}/libtsd32.a
%{archlibdir}/libtshoot.a
%{archlibdir}/libtsoc.a
%{archlibdir}/libtwext.a
%{archlibdir}/libtxflog.a
%{archlibdir}/libtxfw32.a
%{archlibdir}/libudhisapi.a
%{archlibdir}/libufat.a
%{archlibdir}/libuihelper.a
%{archlibdir}/libulib.a
%{archlibdir}/libumandlg.a
%{archlibdir}/libumdmxfrm.a
%{archlibdir}/libumpnpmgr.a
%{archlibdir}/libuniime.a
%{archlibdir}/libunimdmat.a
%{archlibdir}/libuniplat.a
%{archlibdir}/libuntfs.a
%{archlibdir}/libupnp.a
%{archlibdir}/libupnphost.a
%{archlibdir}/libupnpui.a
%{archlibdir}/libureg.a
%{archlibdir}/liburl.a
%{archlibdir}/liburlauth.a
%{archlibdir}/liburlmon.a
%{archlibdir}/libusbcamd2.a
%{archlibdir}/libusbd.a
%{archlibdir}/libusbmon.a
%{archlibdir}/libusbport.a
%{archlibdir}/libuser32.a
%{archlibdir}/libuserenv.a
%{archlibdir}/libusp10.a
%{archlibdir}/libutildll.a
%{archlibdir}/libuuid.a
%{archlibdir}/libuxtheme.a
%{archlibdir}/libvbscript.a
%{archlibdir}/libvds_ps.a
%{archlibdir}/libvdsbas.a
%{archlibdir}/libvdsdyndr.a
%{archlibdir}/libvdsutil.a
%{archlibdir}/libvdswmi.a
%{archlibdir}/libverifier.a
%{archlibdir}/libversion.a
%{archlibdir}/libvfw32.a
%{archlibdir}/libvgx.a
%{archlibdir}/libviewprov.a
%{archlibdir}/libvmx_mode.a
%{archlibdir}/libvss_ps.a
%{archlibdir}/libvssapi.a
%{archlibdir}/libvsstrace.a
%{archlibdir}/libvsswmi.a
%{archlibdir}/libw32time.a
%{archlibdir}/libw32topl.a
%{archlibdir}/libw3cache.a
%{archlibdir}/libw3comlog.a
%{archlibdir}/libw3core.a
%{archlibdir}/libw3ctrlps.a
%{archlibdir}/libw3ctrs.a
%{archlibdir}/libw3dt.a
%{archlibdir}/libw3ext.a
%{archlibdir}/libw3isapi.a
%{archlibdir}/libw3ssl.a
%{archlibdir}/libw3tp.a
%{archlibdir}/libwab32.a
%{archlibdir}/libwabimp.a
%{archlibdir}/libwamreg.a
%{archlibdir}/libwamregps.a
%{archlibdir}/libwbemcore.a
%{archlibdir}/libwbemupgd.a
%{archlibdir}/libwdigest.a
%{archlibdir}/libwdmaud.a
%{archlibdir}/libwdsclient.a
%{archlibdir}/libwdsclientapi.a
%{archlibdir}/libwdscore.a
%{archlibdir}/libwdscsl.a
%{archlibdir}/libwdsimage.a
%{archlibdir}/libwdstptc.a
%{archlibdir}/libwdsupgcompl.a
%{archlibdir}/libwdsutil.a
%{archlibdir}/libwebcheck.a
%{archlibdir}/libwebclnt.a
%{archlibdir}/libwebhits.a
%{archlibdir}/libwecapi.a
%{archlibdir}/libwer.a
%{archlibdir}/libwevtapi.a
%{archlibdir}/libwevtfwd.a
%{archlibdir}/libwiadss.a
%{archlibdir}/libwiarpc.a
%{archlibdir}/libwiaservc.a
%{archlibdir}/libwiashext.a
%{archlibdir}/libwin32spl.a
%{archlibdir}/libwinfax.a
%{archlibdir}/libwininet.a
%{archlibdir}/libwinipsec.a
%{archlibdir}/libwinmm.a
%{archlibdir}/libwinrnr.a
%{archlibdir}/libwinscard.a
%{archlibdir}/libwinspool.a
%{archlibdir}/libwinsrv.a
%{archlibdir}/libwinsta.a
%{archlibdir}/libwintrust.a
%{archlibdir}/libwinusb.a
%{archlibdir}/libwkssvc.a
%{archlibdir}/libwlanapi.a
%{archlibdir}/libwlanui.a
%{archlibdir}/libwlanutil.a
%{archlibdir}/libwldap32.a
%{archlibdir}/libwlnotify.a
%{archlibdir}/libwlstore.a
%{archlibdir}/libwmi.a
%{archlibdir}/libwmi2xml.a
%{archlibdir}/libwmiaprpl.a
%{archlibdir}/libwmiprop.a
%{archlibdir}/libwmisvc.a
%{archlibdir}/libwow64.a
%{archlibdir}/libwow64cpu.a
%{archlibdir}/libwow64mib.a
%{archlibdir}/libwow64win.a
%{archlibdir}/libwpd_ci.a
%{archlibdir}/libws2_32.a
%{archlibdir}/libws2help.a
%{archlibdir}/libwscsvc.a
%{archlibdir}/libwsdapi.a
%{archlibdir}/libwshatm.a
%{archlibdir}/libwshbth.a
%{archlibdir}/libwshcon.a
%{archlibdir}/libwsock32.a
%{archlibdir}/libwtsapi32.a
%{archlibdir}/libx3daudio.a
%{archlibdir}/libx3daudio1_*.a
%{archlibdir}/libx3daudiod1_7.a
%{archlibdir}/libxapofx.a
%{archlibdir}/libxapofx1_*.a
%{archlibdir}/libxapofxd1_5.a
%{archlibdir}/libxaudio.a
%{archlibdir}/libxaudio2_*.a
%{archlibdir}/libxaudiod.a
%{archlibdir}/libxaudiod2_7.a
%{archlibdir}/libxinput.a
%{archlibdir}/libxinput1_*.a
%{archlibdir}/libzoneoc.a

%if %{without bootstrap}
%files -n crossmingw64-libgcc-dll
%defattr(644,root,root,755)
%{_dll64dir}/libgcc_s_sjlj-1.dll

%files -n crossmingw64-libatomic
%defattr(644,root,root,755)
%{archlibdir}/libatomic.dll.a
%{archlibdir}/libatomic.la

%files -n crossmingw64-libatomic-static
%defattr(644,root,root,755)
%{archlibdir}/libatomic.a

%files -n crossmingw64-libatomic-dll
%defattr(644,root,root,755)
%{_dll64dir}/libatomic-1.dll
%endif

%if %{without bootstrap}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{archbindir}/%{target}-c++
%attr(755,root,root) %{archbindir}/%{target}-g++
%attr(755,root,root) %{gcclibdir}/cc1plus
%attr(755,root,root) %{gcclibdir}/g++-mapper-server
%{archlibdir}/libstdc++.dll.a
%{archlibdir}/libstdc++.la
%{archlibdir}/libstdc++fs.la
%{archlibdir}/libstdc++fs.a
%{archlibdir}/libsupc++.la
%{archlibdir}/libsupc++.a
%{archincludedir}/c++
%{_mandir}/man1/%{target}-g++.1*

%files -n crossmingw64-libstdc++-static
%defattr(644,root,root,755)
%{archlibdir}/libstdc++.a

%files -n crossmingw64-libstdc++-dll
%defattr(644,root,root,755)
%{_dll64dir}/libstdc++-8.dll
%endif
