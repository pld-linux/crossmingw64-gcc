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
Version:	4.7.2
Release:	4
Epoch:		1
License:	GPL v3+
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
# Source0-md5:	cc308a0891e778cfda7a151ab8a6e762
# svn co https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64/stable/v2.x/mingw-w64-crt mingw64-crt
%define		_rev	5515
Source1:	mingw64-crt.tar.xz
# Source1-md5:	bf9051e7e4deb445e9e8877ca68211e1
Patch0:		gcc-branch.diff
# Patch0-md5:	2add58e2b9d9874ba62e05ca9b6b513f
Patch1:		gcc-mingw-dirs.patch
Patch2:		gnu_inline-mismatch.patch
Patch3:		texinfo.patch
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

%prep
%setup -q -n gcc-%{version} -a 1
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	--with-bugurl="http://bugs.pld-linux.org" \
	--with-demangler-in-ld \
	--with-gxx-include-dir=%{arch}/include/c++/%{version} \
	--with-gnu-as \
	--with-gnu-ld \
	--with-pkgversion="PLD-Linux" \
	--with-sysroot=%{arch} \
	--enable-c99 \
	--enable-cmath \
	--enable-decimal-float=yes \
	--enable-fully-dynamic-string \
	--enable-languages="c%{!?with_bootstrap:,c++}" \
	--disable-libitm \
	--disable-libmudflap \
	--disable-libquadmath \
	--disable-libssp \
	--enable-libstdcxx-allocator=new \
	--disable-libstdcxx-pch \
	--enable-long-long \
	--disable-lto \
	--disable-multilib \
	--disable-nls \
	--disable-plugin \
	--enable-shared%{?with_bootstrap:=no} \
	--enable-symvers=gnu-versioned-namespace \
	--enable-sjlj-exceptions \
	--enable-threads=win32 \
	--enable-tls \
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

%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} -C BUILDDIR install \
	DESTDIR=$RPM_BUILD_ROOT

install BUILDDIR/gcc/specs $RPM_BUILD_ROOT%{gcclib}

gccdir=$RPM_BUILD_ROOT%{gcclib}
%{__mv} $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
%{__rm} -r $gccdir/include-fixed
%{__rm} -r $gccdir/install-tools

%{__make} -C mingw64-crt install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
find $RPM_BUILD_ROOT%{arch}/lib -type f -name '*.a' -o -name '*.o' \
        -exec %{target}-strip -g -R.note -R.comment "{}" ";"
%endif

# files common for GNU tools, packaged in some native packages
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libiberty.a \
	$RPM_BUILD_ROOT%{_mandir}/man7/{fsf-funding,gfdl,gpl}.7
# files common for all targets, packaged in native
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}
%if %{without bootstrap}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python \
	$RPM_BUILD_ROOT%{arch}/lib/libstdc++.dll.a-gdb.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-gcc-%{version}
%attr(755,root,root) %{_bindir}/%{target}-gcc-ar
%attr(755,root,root) %{_bindir}/%{target}-gcc-nm
%attr(755,root,root) %{_bindir}/%{target}-gcc-ranlib
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
%{gcclib}/crtfastmath.o
%{gcclib}/libgcc.a
%if %{without bootstrap}
%{arch}/lib/libgcc_s_sjlj-1.dll
%{arch}/lib/libgcc_s.a
%{gcclib}/libgcc_eh.a
%endif
%{gcclib}/libgcov.a
%{gcclib}/specs
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*
%{arch}/lib/CRT_*.o
%{arch}/lib/binmode.o
%{arch}/lib/crt*.o
%{arch}/lib/dllcrt*.o
%{arch}/lib/gcrt*.o
%{arch}/lib/txtmode.o

# Win64 API+mingw-w64 runtime
%{arch}/lib/lib6to4svc.a
%{arch}/lib/libCINTIME.a
%{arch}/lib/libPS5UI.a
%{arch}/lib/libPSCRIPT5.a
%{arch}/lib/libUNIDRV.a
%{arch}/lib/libUNIDRVUI.a
%{arch}/lib/libaaaamon.a
%{arch}/lib/libacledit.a
%{arch}/lib/libaclui.a
%{arch}/lib/libactiveds.a
%{arch}/lib/libactxprxy.a
%{arch}/lib/libadmparse.a
%{arch}/lib/libadmwprox.a
%{arch}/lib/libadptif.a
%{arch}/lib/libadrot.a
%{arch}/lib/libadsiis.a
%{arch}/lib/libadsiisex.a
%{arch}/lib/libadsldp.a
%{arch}/lib/libadsldpc.a
%{arch}/lib/libadsmsext.a
%{arch}/lib/libadsnt.a
%{arch}/lib/libadvapi32.a
%{arch}/lib/libadvpack.a
%{arch}/lib/libaelupsvc.a
%{arch}/lib/libagentanm.a
%{arch}/lib/libagentctl.a
%{arch}/lib/libagentdp2.a
%{arch}/lib/libagentdpv.a
%{arch}/lib/libagentmpx.a
%{arch}/lib/libagentpsh.a
%{arch}/lib/libagentsr.a
%{arch}/lib/libagrmco64.a
%{arch}/lib/libagtintl.a
%{arch}/lib/libakscoinst.a
%{arch}/lib/libalrsvc.a
%{arch}/lib/libamstream.a
%{arch}/lib/libapcups.a
%{arch}/lib/libapphelp.a
%{arch}/lib/libappmgmts.a
%{arch}/lib/libappmgr.a
%{arch}/lib/libaqadmin.a
%{arch}/lib/libaqueue.a
%{arch}/lib/libasp.a
%{arch}/lib/libaspperf.a
%{arch}/lib/libasycfilt.a
%{arch}/lib/libatkctrs.a
%{arch}/lib/libatl.a
%{arch}/lib/libatmlib.a
%{arch}/lib/libatmpvcno.a
%{arch}/lib/libatrace.a
%{arch}/lib/libaudiosrv.a
%{arch}/lib/libauthz.a
%{arch}/lib/libautodisc.a
%{arch}/lib/libavicap32.a
%{arch}/lib/libavifil32.a
%{arch}/lib/libazroles.a
%{arch}/lib/libazroleui.a
%{arch}/lib/libbasesrv.a
%{arch}/lib/libbatmeter.a
%{arch}/lib/libbatt.a
%{arch}/lib/libbcrypt.a
%{arch}/lib/libbidispl.a
%{arch}/lib/libbitsprx2.a
%{arch}/lib/libbitsprx3.a
%{arch}/lib/libbnts.a
%{arch}/lib/libbootvid.a
%{arch}/lib/libbrowscap.a
%{arch}/lib/libbrowser.a
%{arch}/lib/libbrowseui.a
%{arch}/lib/libbrpinfo.a
%{arch}/lib/libbthci.a
%{arch}/lib/libbthprops.a
%{arch}/lib/libbthserv.a
%{arch}/lib/libbtpanui.a
%{arch}/lib/libc_g18030.a
%{arch}/lib/libc_is2022.a
%{arch}/lib/libc_iscii.a
%{arch}/lib/libcabinet.a
%{arch}/lib/libcabview.a
%{arch}/lib/libcamocx.a
%{arch}/lib/libcards.a
%{arch}/lib/libcatsrv.a
%{arch}/lib/libcatsrvps.a
%{arch}/lib/libcatsrvut.a
%{arch}/lib/libccfgnt.a
%{arch}/lib/libcdfview.a
%{arch}/lib/libcdm.a
%{arch}/lib/libcdosys.a
%{arch}/lib/libcertcli.a
%{arch}/lib/libcertmgr.a
%{arch}/lib/libcertobj.a
%{arch}/lib/libcfgbkend.a
%{arch}/lib/libcfgmgr32.a
%{arch}/lib/libchsbrkr.a
%{arch}/lib/libchtbrkr.a
%{arch}/lib/libchtskdic.a
%{arch}/lib/libciadmin.a
%{arch}/lib/libcic.a
%{arch}/lib/libcimwin32.a
%{arch}/lib/libciodm.a
%{arch}/lib/libclasspnp.a
%{arch}/lib/libclb.a
%{arch}/lib/libclbcatex.a
%{arch}/lib/libclbcatq.a
%{arch}/lib/libclfsw32.a
%{arch}/lib/libcliconfg.a
%{arch}/lib/libclusapi.a
%{arch}/lib/libcmcfg32.a
%{arch}/lib/libcmdial32.a
%{arch}/lib/libcmpbk32.a
%{arch}/lib/libcmprops.a
%{arch}/lib/libcmsetacl.a
%{arch}/lib/libcmutil.a
%{arch}/lib/libcnbjmon.a
%{arch}/lib/libcnetcfg.a
%{arch}/lib/libcnvfat.a
%{arch}/lib/libcoadmin.a
%{arch}/lib/libcolbact.a
%{arch}/lib/libcomaddin.a
%{arch}/lib/libcomadmin.a
%{arch}/lib/libcomcat.a
%{arch}/lib/libcomctl32.a
%{arch}/lib/libcomdlg32.a
%{arch}/lib/libcompatui.a
%{arch}/lib/libcompstui.a
%{arch}/lib/libcomrepl.a
%{arch}/lib/libcomres.a
%{arch}/lib/libcomsetup.a
%{arch}/lib/libcomsnap.a
%{arch}/lib/libcomsvcs.a
%{arch}/lib/libcomuid.a
%{arch}/lib/libconfmsp.a
%{arch}/lib/libconnect.a
%{arch}/lib/libconsole.a
%{arch}/lib/libcontrot.a
%{arch}/lib/libcorpol.a
%{arch}/lib/libcredui.a
%{arch}/lib/libcrtdll.a
%{arch}/lib/libcrypt32.a
%{arch}/lib/libcryptdlg.a
%{arch}/lib/libcryptdll.a
%{arch}/lib/libcryptext.a
%{arch}/lib/libcryptnet.a
%{arch}/lib/libcryptsp.a
%{arch}/lib/libcryptsvc.a
%{arch}/lib/libcryptui.a
%{arch}/lib/libcryptxml.a
%{arch}/lib/libcscapi.a
%{arch}/lib/libcscdll.a
%{arch}/lib/libcscui.a
%{arch}/lib/libcsrsrv.a
%{arch}/lib/libd2d1.a
%{arch}/lib/libd3d8thk.a
%{arch}/lib/libd3d9.a
%{arch}/lib/libd3dcompiler*.a
%{arch}/lib/libd3dcsxd*.a
%{arch}/lib/libd3dx10*.a
%{arch}/lib/libd3dx11*.a
%{arch}/lib/libd3dx9*.a
%{arch}/lib/libd3dxof.a
%{arch}/lib/libdanim.a
%{arch}/lib/libdataclen.a
%{arch}/lib/libdatime.a
%{arch}/lib/libdavclnt.a
%{arch}/lib/libdavcprox.a
%{arch}/lib/libdbgeng.a
%{arch}/lib/libdbghelp.a
%{arch}/lib/libdbnetlib.a
%{arch}/lib/libdbnmpntw.a
%{arch}/lib/libdciman32.a
%{arch}/lib/libddraw.a
%{arch}/lib/libddrawex.a
%{arch}/lib/libdelayimp.a
%{arch}/lib/libdeskadp.a
%{arch}/lib/libdeskmon.a
%{arch}/lib/libdeskperf.a
%{arch}/lib/libdevenum.a
%{arch}/lib/libdevmgr.a
%{arch}/lib/libdfrgifps.a
%{arch}/lib/libdfrgsnap.a
%{arch}/lib/libdfrgui.a
%{arch}/lib/libdfsshlex.a
%{arch}/lib/libdgnet.a
%{arch}/lib/libdhcpcsvc.a
%{arch}/lib/libdhcpcsvc6.a
%{arch}/lib/libdhcpmon.a
%{arch}/lib/libdhcpsapi.a
%{arch}/lib/libdiactfrm.a
%{arch}/lib/libdigest.a
%{arch}/lib/libdimap.a
%{arch}/lib/libdimsntfy.a
%{arch}/lib/libdimsroam.a
%{arch}/lib/libdinput.a
%{arch}/lib/libdinput8.a
%{arch}/lib/libdirectdb.a
%{arch}/lib/libdiskcopy.a
%{arch}/lib/libdispex.a
%{arch}/lib/libdmconfig.a
%{arch}/lib/libdmdlgs.a
%{arch}/lib/libdmdskmgr.a
%{arch}/lib/libdmintf.a
%{arch}/lib/libdmivcitf.a
%{arch}/lib/libdmocx.a
%{arch}/lib/libdmoguids.a
%{arch}/lib/libdmserver.a
%{arch}/lib/libdmutil.a
%{arch}/lib/libdmvdsitf.a
%{arch}/lib/libdnsapi.a
%{arch}/lib/libdnsrslvr.a
%{arch}/lib/libdocprop.a
%{arch}/lib/libdocprop2.a
%{arch}/lib/libdpnaddr.a
%{arch}/lib/libdpnet.a
%{arch}/lib/libdpnhpast.a
%{arch}/lib/libdpnhupnp.a
%{arch}/lib/libdpnlobby.a
%{arch}/lib/libdpvacm.a
%{arch}/lib/libdpvoice.a
%{arch}/lib/libdpvvox.a
%{arch}/lib/libdrprov.a
%{arch}/lib/libds32gt.a
%{arch}/lib/libdsauth.a
%{arch}/lib/libdsdmo.a
%{arch}/lib/libdsdmoprp.a
%{arch}/lib/libdskquota.a
%{arch}/lib/libdskquoui.a
%{arch}/lib/libdsound.a
%{arch}/lib/libdsound3d.a
%{arch}/lib/libdsprop.a
%{arch}/lib/libdsprov.a
%{arch}/lib/libdsquery.a
%{arch}/lib/libdssec.a
%{arch}/lib/libdssenh.a
%{arch}/lib/libdsuiext.a
%{arch}/lib/libduser.a
%{arch}/lib/libdwmapi.a
%{arch}/lib/libdwrite.a
%{arch}/lib/libdxdiagn.a
%{arch}/lib/libdxerr8.a
%{arch}/lib/libdxerr9.a
%{arch}/lib/libdxgi.a
%{arch}/lib/libdxguid.a
%{arch}/lib/libdxtmsft.a
%{arch}/lib/libdxtrans.a
%{arch}/lib/libdxva2.a
%{arch}/lib/libeappcfg.a
%{arch}/lib/libeappgnui.a
%{arch}/lib/libeapphost.a
%{arch}/lib/libeappprxy.a
%{arch}/lib/libefsadu.a
%{arch}/lib/libels.a
%{arch}/lib/libencapi.a
%{arch}/lib/libersvc.a
%{arch}/lib/libes.a
%{arch}/lib/libesent.a
%{arch}/lib/libesentprf.a
%{arch}/lib/libesscli.a
%{arch}/lib/libeventcls.a
%{arch}/lib/libeventlog.a
%{arch}/lib/libevntagnt.a
%{arch}/lib/libevntrprv.a
%{arch}/lib/libevr.a
%{arch}/lib/libevtgprov.a
%{arch}/lib/libexstrace.a
%{arch}/lib/libextmgr.a
%{arch}/lib/libf3ahvoas.a
%{arch}/lib/libfastprox.a
%{arch}/lib/libfaultrep.a
%{arch}/lib/libfcachdll.a
%{arch}/lib/libfde.a
%{arch}/lib/libfdeploy.a
%{arch}/lib/libfeclient.a
%{arch}/lib/libfilemgmt.a
%{arch}/lib/libfldrclnr.a
%{arch}/lib/libfltlib.a
%{arch}/lib/libfmifs.a
%{arch}/lib/libfontext.a
%{arch}/lib/libfontsub.a
%{arch}/lib/libframedyn.a
%{arch}/lib/libfsusd.a
%{arch}/lib/libftpctrs2.a
%{arch}/lib/libftpmib.a
%{arch}/lib/libftpsvc2.a
%{arch}/lib/libfwcfg.a
%{arch}/lib/libfwpuclnt.a
%{arch}/lib/libfxsapi.a
%{arch}/lib/libfxscfgwz.a
%{arch}/lib/libfxscom.a
%{arch}/lib/libfxscomex.a
%{arch}/lib/libfxsdrv.a
%{arch}/lib/libfxsmon.a
%{arch}/lib/libfxsocm.a
%{arch}/lib/libfxsperf.a
%{arch}/lib/libfxsroute.a
%{arch}/lib/libfxsst.a
%{arch}/lib/libfxst30.a
%{arch}/lib/libfxstiff.a
%{arch}/lib/libfxsui.a
%{arch}/lib/libfxswzrd.a
%{arch}/lib/libgcdef.a
%{arch}/lib/libgdi32.a
%{arch}/lib/libgdiplus.a
%{arch}/lib/libgetuname.a
%{arch}/lib/libglmf32.a
%{arch}/lib/libglu32.a
%{arch}/lib/libgmon.a
%{arch}/lib/libgpedit.a
%{arch}/lib/libgpkcsp.a
%{arch}/lib/libgptext.a
%{arch}/lib/libguitrn.a
%{arch}/lib/libgzip.a
%{arch}/lib/libh323msp.a
%{arch}/lib/libhal.a
%{arch}/lib/libhbaapi.a
%{arch}/lib/libhgfs.a
%{arch}/lib/libhhsetup.a
%{arch}/lib/libhid.a
%{arch}/lib/libhidclass.a
%{arch}/lib/libhidparse.a
%{arch}/lib/libhlink.a
%{arch}/lib/libhmmapi.a
%{arch}/lib/libhnetcfg.a
%{arch}/lib/libhnetmon.a
%{arch}/lib/libhnetwiz.a
%{arch}/lib/libhostmib.a
%{arch}/lib/libhotplug.a
%{arch}/lib/libhticons.a
%{arch}/lib/libhtrn_jis.a
%{arch}/lib/libhttpapi.a
%{arch}/lib/libhttpext.a
%{arch}/lib/libhttpmib.a
%{arch}/lib/libhttpodbc.a
%{arch}/lib/libhtui.a
%{arch}/lib/libhypertrm.a
%{arch}/lib/libiasacct.a
%{arch}/lib/libiasads.a
%{arch}/lib/libiashlpr.a
%{arch}/lib/libiasnap.a
%{arch}/lib/libiaspolcy.a
%{arch}/lib/libiasrad.a
%{arch}/lib/libiassam.a
%{arch}/lib/libiassdo.a
%{arch}/lib/libiassvcs.a
%{arch}/lib/libicaapi.a
%{arch}/lib/libicfgnt5.a
%{arch}/lib/libicm32.a
%{arch}/lib/libicmp.a
%{arch}/lib/libicmui.a
%{arch}/lib/libicwconn.a
%{arch}/lib/libicwdial.a
%{arch}/lib/libicwdl.a
%{arch}/lib/libicwhelp.a
%{arch}/lib/libicwphbk.a
%{arch}/lib/libicwutil.a
%{arch}/lib/libidq.a
%{arch}/lib/libieakeng.a
%{arch}/lib/libieaksie.a
%{arch}/lib/libiedkcs32.a
%{arch}/lib/libieencode.a
%{arch}/lib/libiepeers.a
%{arch}/lib/libiernonce.a
%{arch}/lib/libiesetup.a
%{arch}/lib/libifmon.a
%{arch}/lib/libifsutil.a
%{arch}/lib/libigmpagnt.a
%{arch}/lib/libiis.a
%{arch}/lib/libiisadmin.a
%{arch}/lib/libiiscfg.a
%{arch}/lib/libiisclex4.a
%{arch}/lib/libiisext.a
%{arch}/lib/libiislog.a
%{arch}/lib/libiismap.a
%{arch}/lib/libiisrstap.a
%{arch}/lib/libiisrtl.a
%{arch}/lib/libiissuba.a
%{arch}/lib/libiisui.a
%{arch}/lib/libiisuiobj.a
%{arch}/lib/libiisutil.a
%{arch}/lib/libiisw3adm.a
%{arch}/lib/libiiswmi.a
%{arch}/lib/libimagehlp.a
%{arch}/lib/libimekrcic.a
%{arch}/lib/libimeshare.a
%{arch}/lib/libimgutil.a
%{arch}/lib/libimjp81k.a
%{arch}/lib/libimjpcic.a
%{arch}/lib/libimjpcus.a
%{arch}/lib/libimjpdct.a
%{arch}/lib/libimjputyc.a
%{arch}/lib/libimm32.a
%{arch}/lib/libimsinsnt.a
%{arch}/lib/libimskdic.a
%{arch}/lib/libinetcfg.a
%{arch}/lib/libinetcomm.a
%{arch}/lib/libinetmgr.a
%{arch}/lib/libinetmib1.a
%{arch}/lib/libinetpp.a
%{arch}/lib/libinetppui.a
%{arch}/lib/libinfoadmn.a
%{arch}/lib/libinfocomm.a
%{arch}/lib/libinfoctrs.a
%{arch}/lib/libinfosoft.a
%{arch}/lib/libinitpki.a
%{arch}/lib/libinput.a
%{arch}/lib/libinseng.a
%{arch}/lib/libiphlpapi.a
%{arch}/lib/libipmontr.a
%{arch}/lib/libipnathlp.a
%{arch}/lib/libippromon.a
%{arch}/lib/libiprip.a
%{arch}/lib/libiprop.a
%{arch}/lib/libiprtprio.a
%{arch}/lib/libiprtrmgr.a
%{arch}/lib/libipsecsnp.a
%{arch}/lib/libipsecsvc.a
%{arch}/lib/libipsmsnap.a
%{arch}/lib/libipv6mon.a
%{arch}/lib/libipxsap.a
%{arch}/lib/libirclass.a
%{arch}/lib/libisapips.a
%{arch}/lib/libisatq.a
%{arch}/lib/libiscomlog.a
%{arch}/lib/libiscsidsc.a
%{arch}/lib/libisign32.a
%{arch}/lib/libitircl.a
%{arch}/lib/libitss.a
%{arch}/lib/libixsso.a
%{arch}/lib/libiyuv_32.a
%{arch}/lib/libjet500.a
%{arch}/lib/libjscript.a
%{arch}/lib/libjsproxy.a
%{arch}/lib/libkbd*.a
%{arch}/lib/libkd1394.a
%{arch}/lib/libkdcom.a
%{arch}/lib/libkerberos.a
%{arch}/lib/libkernel32.a
%{arch}/lib/libkeymgr.a
%{arch}/lib/libkorwbrkr.a
%{arch}/lib/libkrnlprov.a
%{arch}/lib/libks.a
%{arch}/lib/libksuser.a
%{arch}/lib/libktmw32.a
%{arch}/lib/liblangwrbk.a
%{arch}/lib/liblargeint.a
%{arch}/lib/liblicdll.a
%{arch}/lib/liblicmgr10.a
%{arch}/lib/liblicwmi.a
%{arch}/lib/liblinkinfo.a
%{arch}/lib/liblmhsvc.a
%{arch}/lib/liblmmib2.a
%{arch}/lib/liblmrt.a
%{arch}/lib/libloadperf.a
%{arch}/lib/liblocalsec.a
%{arch}/lib/liblocalspl.a
%{arch}/lib/liblocalui.a
%{arch}/lib/liblog.a
%{arch}/lib/libloghours.a
%{arch}/lib/liblogscrpt.a
%{arch}/lib/liblonsint.a
%{arch}/lib/liblpdsvc.a
%{arch}/lib/liblpk.a
%{arch}/lib/liblprhelp.a
%{arch}/lib/liblprmon.a
%{arch}/lib/liblprmonui.a
%{arch}/lib/liblsasrv.a
%{arch}/lib/liblz32.a
%{arch}/lib/libm.a
%{arch}/lib/libmag_hook.a
%{arch}/lib/libmailmsg.a
%{arch}/lib/libmapi32.a
%{arch}/lib/libmapistub.a
%{arch}/lib/libmcastmib.a
%{arch}/lib/libmcd32.a
%{arch}/lib/libmcdsrv32.a
%{arch}/lib/libmchgrcoi.a
%{arch}/lib/libmciavi32.a
%{arch}/lib/libmcicda.a
%{arch}/lib/libmciole32.a
%{arch}/lib/libmciqtz32.a
%{arch}/lib/libmciseq.a
%{arch}/lib/libmciwave.a
%{arch}/lib/libmdhcp.a
%{arch}/lib/libmdminst.a
%{arch}/lib/libmetadata.a
%{arch}/lib/libmf.a
%{arch}/lib/libmf3216.a
%{arch}/lib/libmfc42.a
%{arch}/lib/libmfc42u.a
%{arch}/lib/libmfcsubs.a
%{arch}/lib/libmfplat.a
%{arch}/lib/libmgmtapi.a
%{arch}/lib/libmidimap.a
%{arch}/lib/libmigism.a
%{arch}/lib/libmiglibnt.a
%{arch}/lib/libmimefilt.a
%{arch}/lib/libmingw32.a
%{arch}/lib/libmingwex.a
%{arch}/lib/libmingwthrd.a
%{arch}/lib/libmlang.a
%{arch}/lib/libmll_hp.a
%{arch}/lib/libmll_mtf.a
%{arch}/lib/libmll_qic.a
%{arch}/lib/libmmcbase.a
%{arch}/lib/libmmcndmgr.a
%{arch}/lib/libmmcshext.a
%{arch}/lib/libmmfutil.a
%{arch}/lib/libmmutilse.a
%{arch}/lib/libmobsync.a
%{arch}/lib/libmodemui.a
%{arch}/lib/libmofd.a
%{arch}/lib/libmoldname.a
%{arch}/lib/libmpr.a
%{arch}/lib/libmprapi.a
%{arch}/lib/libmprddm.a
%{arch}/lib/libmprdim.a
%{arch}/lib/libmprmsg.a
%{arch}/lib/libmprui.a
%{arch}/lib/libmqad.a
%{arch}/lib/libmqcertui.a
%{arch}/lib/libmqdscli.a
%{arch}/lib/libmqgentr.a
%{arch}/lib/libmqise.a
%{arch}/lib/libmqlogmgr.a
%{arch}/lib/libmqoa.a
%{arch}/lib/libmqperf.a
%{arch}/lib/libmqqm.a
%{arch}/lib/libmqrt.a
%{arch}/lib/libmqrtdep.a
%{arch}/lib/libmqsec.a
%{arch}/lib/libmqsnap.a
%{arch}/lib/libmqtrig.a
%{arch}/lib/libmqupgrd.a
%{arch}/lib/libmqutil.a
%{arch}/lib/libmsaatext.a
%{arch}/lib/libmsacm32.a
%{arch}/lib/libmsadce.a
%{arch}/lib/libmsadcf.a
%{arch}/lib/libmsadco.a
%{arch}/lib/libmsadcs.a
%{arch}/lib/libmsadds.a
%{arch}/lib/libmsado15.a
%{arch}/lib/libmsadomd.a
%{arch}/lib/libmsador15.a
%{arch}/lib/libmsadox.a
%{arch}/lib/libmsadrh15.a
%{arch}/lib/libmsafd.a
%{arch}/lib/libmsasn1.a
%{arch}/lib/libmscandui.a
%{arch}/lib/libmscat32.a
%{arch}/lib/libmscms.a
%{arch}/lib/libmsctfmonitor.a
%{arch}/lib/libmsctfp.a
%{arch}/lib/libmsdadiag.a
%{arch}/lib/libmsdaosp.a
%{arch}/lib/libmsdaprst.a
%{arch}/lib/libmsdaps.a
%{arch}/lib/libmsdarem.a
%{arch}/lib/libmsdart.a
%{arch}/lib/libmsdatl3.a
%{arch}/lib/libmsdfmap.a
%{arch}/lib/libmsdmo.a
%{arch}/lib/libmsdrm.a
%{arch}/lib/libmsdtclog.a
%{arch}/lib/libmsdtcprx.a
%{arch}/lib/libmsdtcstp.a
%{arch}/lib/libmsdtctm.a
%{arch}/lib/libmsdtcuiu.a
%{arch}/lib/libmsftedit.a
%{arch}/lib/libmsgina.a
%{arch}/lib/libmsgr3en.a
%{arch}/lib/libmsgrocm.a
%{arch}/lib/libmsgsvc.a
%{arch}/lib/libmshtml.a
%{arch}/lib/libmshtmled.a
%{arch}/lib/libmsi.a
%{arch}/lib/libmsident.a
%{arch}/lib/libmsieftp.a
%{arch}/lib/libmsihnd.a
%{arch}/lib/libmsimg32.a
%{arch}/lib/libmsimtf.a
%{arch}/lib/libmsinfo.a
%{arch}/lib/libmsiprov.a
%{arch}/lib/libmsir3jp.a
%{arch}/lib/libmsisip.a
%{arch}/lib/libmslbui.a
%{arch}/lib/libmsls31.a
%{arch}/lib/libmslwvtts.a
%{arch}/lib/libmsmqocm.a
%{arch}/lib/libmsobcomm.a
%{arch}/lib/libmsobdl.a
%{arch}/lib/libmsobmain.a
%{arch}/lib/libmsobshel.a
%{arch}/lib/libmsobweb.a
%{arch}/lib/libmsoe.a
%{arch}/lib/libmsoeacct.a
%{arch}/lib/libmsoert2.a
%{arch}/lib/libmspatcha.a
%{arch}/lib/libmspmsnsv.a
%{arch}/lib/libmsports.a
%{arch}/lib/libmsrating.a
%{arch}/lib/libmsrle32.a
%{arch}/lib/libmssign32.a
%{arch}/lib/libmssip32.a
%{arch}/lib/libmstask.a
%{arch}/lib/libmstime.a
%{arch}/lib/libmstlsapi.a
%{arch}/lib/libmstscax.a
%{arch}/lib/libmsutb.a
%{arch}/lib/libmsv1_0.a
%{arch}/lib/libmsvcirt.a
%{arch}/lib/libmsvcp60.a
%{arch}/lib/libmsvcr100.a
%{arch}/lib/libmsvcr110.a
%{arch}/lib/libmsvcr80.a
%{arch}/lib/libmsvcr90.a
%{arch}/lib/libmsvcr90d.a
%{arch}/lib/libmsvcrt.a
%{arch}/lib/libmsvfw32.a
%{arch}/lib/libmsvidc32.a
%{arch}/lib/libmsvidctl.a
%{arch}/lib/libmsw3prt.a
%{arch}/lib/libmswsock.a
%{arch}/lib/libmsxactps.a
%{arch}/lib/libmsxml3.a
%{arch}/lib/libmsxs64.a
%{arch}/lib/libmsyuv.a
%{arch}/lib/libmtxclu.a
%{arch}/lib/libmtxdm.a
%{arch}/lib/libmtxex.a
%{arch}/lib/libmtxoci.a
%{arch}/lib/libmycomput.a
%{arch}/lib/libmydocs.a
%{arch}/lib/libnarrhook.a
%{arch}/lib/libncobjapi.a
%{arch}/lib/libncprov.a
%{arch}/lib/libncrypt.a
%{arch}/lib/libncxpnt.a
%{arch}/lib/libnddeapi.a
%{arch}/lib/libnddenb32.a
%{arch}/lib/libndfapi.a
%{arch}/lib/libndis.a
%{arch}/lib/libndisnpp.a
%{arch}/lib/libnetapi32.a
%{arch}/lib/libnetcfgx.a
%{arch}/lib/libnetid.a
%{arch}/lib/libnetlogon.a
%{arch}/lib/libnetman.a
%{arch}/lib/libnetoc.a
%{arch}/lib/libnetplwiz.a
%{arch}/lib/libnetrap.a
%{arch}/lib/libnetshell.a
%{arch}/lib/libnetui0.a
%{arch}/lib/libnetui1.a
%{arch}/lib/libnetui2.a
%{arch}/lib/libnewdev.a
%{arch}/lib/libnextlink.a
%{arch}/lib/libnlhtml.a
%{arch}/lib/libnntpadm.a
%{arch}/lib/libnntpapi.a
%{arch}/lib/libnntpsnap.a
%{arch}/lib/libnormaliz.a
%{arch}/lib/libnpptools.a
%{arch}/lib/libnshipsec.a
%{arch}/lib/libntdll.a
%{arch}/lib/libntdsapi.a
%{arch}/lib/libntdsbcli.a
%{arch}/lib/libntevt.a
%{arch}/lib/libntfsdrv.a
%{arch}/lib/libntlanman.a
%{arch}/lib/libntlanui.a
%{arch}/lib/libntlanui2.a
%{arch}/lib/libntlsapi.a
%{arch}/lib/libntmarta.a
%{arch}/lib/libntmsapi.a
%{arch}/lib/libntmsdba.a
%{arch}/lib/libntmsevt.a
%{arch}/lib/libntmsmgr.a
%{arch}/lib/libntmssvc.a
%{arch}/lib/libntoc.a
%{arch}/lib/libntoskrnl.a
%{arch}/lib/libntprint.a
%{arch}/lib/libntshrui.a
%{arch}/lib/libntvdm64.a
%{arch}/lib/libnwprovau.a
%{arch}/lib/liboakley.a
%{arch}/lib/libobjsel.a
%{arch}/lib/liboccache.a
%{arch}/lib/libocgen.a
%{arch}/lib/libocmanage.a
%{arch}/lib/libocmsn.a
%{arch}/lib/libodbc32.a
%{arch}/lib/libodbc32gt.a
%{arch}/lib/libodbcbcp.a
%{arch}/lib/libodbcconf.a
%{arch}/lib/libodbccp32.a
%{arch}/lib/libodbccr32.a
%{arch}/lib/libodbccu32.a
%{arch}/lib/libodbctrac.a
%{arch}/lib/liboeimport.a
%{arch}/lib/liboemiglib.a
%{arch}/lib/libofffilt.a
%{arch}/lib/libole32.a
%{arch}/lib/liboleacc.a
%{arch}/lib/liboleaut32.a
%{arch}/lib/libolecli32.a
%{arch}/lib/libolecnv32.a
%{arch}/lib/liboledb32.a
%{arch}/lib/liboledb32r.a
%{arch}/lib/liboledlg.a
%{arch}/lib/liboleprn.a
%{arch}/lib/libolesvr32.a
%{arch}/lib/libopengl32.a
%{arch}/lib/libosuninst.a
%{arch}/lib/libovprintmondll.a
%{arch}/lib/libp2p.a
%{arch}/lib/libp2pcollab.a
%{arch}/lib/libp2pgraph.a
%{arch}/lib/libpanmap.a
%{arch}/lib/libpautoenr.a
%{arch}/lib/libpchshell.a
%{arch}/lib/libpchsvc.a
%{arch}/lib/libpcwum.a
%{arch}/lib/libpdh.a
%{arch}/lib/libperfctrs.a
%{arch}/lib/libperfdisk.a
%{arch}/lib/libperfnet.a
%{arch}/lib/libperfos.a
%{arch}/lib/libperfproc.a
%{arch}/lib/libperfts.a
%{arch}/lib/libphotowiz.a
%{arch}/lib/libpid.a
%{arch}/lib/libpidgen.a
%{arch}/lib/libpintlcsa.a
%{arch}/lib/libpintlcsd.a
%{arch}/lib/libpjlmon.a
%{arch}/lib/libpngfilt.a
%{arch}/lib/libpolicman.a
%{arch}/lib/libpolstore.a
%{arch}/lib/libpowrprof.a
%{arch}/lib/libprintui.a
%{arch}/lib/libprofmap.a
%{arch}/lib/libprovthrd.a
%{arch}/lib/libpsapi.a
%{arch}/lib/libpsbase.a
%{arch}/lib/libpschdprf.a
%{arch}/lib/libpsnppagn.a
%{arch}/lib/libpstorec.a
%{arch}/lib/libpstorsvc.a
%{arch}/lib/libqasf.a
%{arch}/lib/libqcap.a
%{arch}/lib/libqdv.a
%{arch}/lib/libqdvd.a
%{arch}/lib/libqedit.a
%{arch}/lib/libqmgr.a
%{arch}/lib/libqmgrprxy.a
%{arch}/lib/libqosname.a
%{arch}/lib/libquartz.a
%{arch}/lib/libquery.a
%{arch}/lib/libqutil.a
%{arch}/lib/libqwave.a
%{arch}/lib/libracpldlg.a
%{arch}/lib/librasadhlp.a
%{arch}/lib/librasapi32.a
%{arch}/lib/librasauto.a
%{arch}/lib/libraschap.a
%{arch}/lib/librasctrs.a
%{arch}/lib/librasdlg.a
%{arch}/lib/librasman.a
%{arch}/lib/librasmans.a
%{arch}/lib/librasmontr.a
%{arch}/lib/librasmxs.a
%{arch}/lib/librasppp.a
%{arch}/lib/librasrad.a
%{arch}/lib/librassapi.a
%{arch}/lib/librasser.a
%{arch}/lib/librastapi.a
%{arch}/lib/librastls.a
%{arch}/lib/librcbdyctl.a
%{arch}/lib/librdchost.a
%{arch}/lib/librdpcfgex.a
%{arch}/lib/librdpsnd.a
%{arch}/lib/librdpwsx.a
%{arch}/lib/libregapi.a
%{arch}/lib/libregsvc.a
%{arch}/lib/libregwizc.a
%{arch}/lib/libremotepg.a
%{arch}/lib/librend.a
%{arch}/lib/librepdrvfs.a
%{arch}/lib/libresutil.a
%{arch}/lib/libresutils.a
%{arch}/lib/libriched20.a
%{arch}/lib/librnr20.a
%{arch}/lib/libroutetab.a
%{arch}/lib/librpcdiag.a
%{arch}/lib/librpchttp.a
%{arch}/lib/librpcns4.a
%{arch}/lib/librpcnsh.a
%{arch}/lib/librpcref.a
%{arch}/lib/librpcrt4.a
%{arch}/lib/librpcss.a
%{arch}/lib/librsaenh.a
%{arch}/lib/librsfsaps.a
%{arch}/lib/librshx32.a
%{arch}/lib/librsmps.a
%{arch}/lib/librstrmgr.a
%{arch}/lib/librtm.a
%{arch}/lib/librtutils.a
%{arch}/lib/librwnh.a
%{arch}/lib/libsafrcdlg.a
%{arch}/lib/libsafrdm.a
%{arch}/lib/libsafrslv.a
%{arch}/lib/libsamlib.a
%{arch}/lib/libsamsrv.a
%{arch}/lib/libsapi.a
%{arch}/lib/libscarddlg.a
%{arch}/lib/libsccbase.a
%{arch}/lib/libsccsccp.a
%{arch}/lib/libscecli.a
%{arch}/lib/libscesrv.a
%{arch}/lib/libschannel.a
%{arch}/lib/libschedsvc.a
%{arch}/lib/libsclgntfy.a
%{arch}/lib/libscredir.a
%{arch}/lib/libscript.a
%{arch}/lib/libscripto.a
%{arch}/lib/libscriptpw.a
%{arch}/lib/libscrnsave.a
%{arch}/lib/libscrnsavw.a
%{arch}/lib/libscrobj.a
%{arch}/lib/libscrptutl.a
%{arch}/lib/libscrrun.a
%{arch}/lib/libsdhcinst.a
%{arch}/lib/libsdpblb.a
%{arch}/lib/libseclogon.a
%{arch}/lib/libsecur32.a
%{arch}/lib/libsecurity.a
%{arch}/lib/libsendcmsg.a
%{arch}/lib/libsendmail.a
%{arch}/lib/libsens.a
%{arch}/lib/libsensapi.a
%{arch}/lib/libsenscfg.a
%{arch}/lib/libseo.a
%{arch}/lib/libseos.a
%{arch}/lib/libserialui.a
%{arch}/lib/libservdeps.a
%{arch}/lib/libserwvdrv.a
%{arch}/lib/libsetupapi.a
%{arch}/lib/libsetupqry.a
%{arch}/lib/libsfc.a
%{arch}/lib/libsfc_os.a
%{arch}/lib/libsfcfiles.a
%{arch}/lib/libsfmapi.a
%{arch}/lib/libshdocvw.a
%{arch}/lib/libshell32.a
%{arch}/lib/libshfolder.a
%{arch}/lib/libshgina.a
%{arch}/lib/libshimeng.a
%{arch}/lib/libshimgvw.a
%{arch}/lib/libshlwapi.a
%{arch}/lib/libshmedia.a
%{arch}/lib/libshscrap.a
%{arch}/lib/libshsvcs.a
%{arch}/lib/libsigtab.a
%{arch}/lib/libsimptcp.a
%{arch}/lib/libsisbkup.a
%{arch}/lib/libskdll.a
%{arch}/lib/libslayerxp.a
%{arch}/lib/libslbcsp.a
%{arch}/lib/libslbiop.a
%{arch}/lib/libslc.a
%{arch}/lib/libslcext.a
%{arch}/lib/libslwga.a
%{arch}/lib/libsmlogcfg.a
%{arch}/lib/libsmtpadm.a
%{arch}/lib/libsmtpapi.a
%{arch}/lib/libsmtpcons.a
%{arch}/lib/libsmtpctrs.a
%{arch}/lib/libsmtpsnap.a
%{arch}/lib/libsmtpsvc.a
%{arch}/lib/libsniffpol.a
%{arch}/lib/libsnmpapi.a
%{arch}/lib/libsnmpcl.a
%{arch}/lib/libsnmpincl.a
%{arch}/lib/libsnmpmib.a
%{arch}/lib/libsnmpsmir.a
%{arch}/lib/libsnmpsnap.a
%{arch}/lib/libsnmpstup.a
%{arch}/lib/libsnmpthrd.a
%{arch}/lib/libsnprfdll.a
%{arch}/lib/libsoftkbd.a
%{arch}/lib/libsoftpub.a
%{arch}/lib/libspcommon.a
%{arch}/lib/libspoolss.a
%{arch}/lib/libsptip.a
%{arch}/lib/libspttseng.a
%{arch}/lib/libsqlsrv32.a
%{arch}/lib/libsqlxmlx.a
%{arch}/lib/libsrchctls.a
%{arch}/lib/libsrchui.a
%{arch}/lib/libsrclient.a
%{arch}/lib/libsrrstr.a
%{arch}/lib/libsrsvc.a
%{arch}/lib/libsrvsvc.a
%{arch}/lib/libssdpapi.a
%{arch}/lib/libssdpsrv.a
%{arch}/lib/libssinc.a
%{arch}/lib/libsspicli.a
%{arch}/lib/libsstub.a
%{arch}/lib/libstaxmem.a
%{arch}/lib/libstclient.a
%{arch}/lib/libstdprov.a
%{arch}/lib/libsti.a
%{arch}/lib/libsti_ci.a
%{arch}/lib/libstobject.a
%{arch}/lib/libstorprop.a
%{arch}/lib/libstreamci.a
%{arch}/lib/libstrmfilt.a
%{arch}/lib/libstrmiids.a
%{arch}/lib/libsvcext.a
%{arch}/lib/libsvcpack.a
%{arch}/lib/libswprv.a
%{arch}/lib/libsxs.a
%{arch}/lib/libsynceng.a
%{arch}/lib/libsyncui.a
%{arch}/lib/libsysinv.a
%{arch}/lib/libsysmod.a
%{arch}/lib/libsyssetup.a
%{arch}/lib/libt2embed.a
%{arch}/lib/libtapi3.a
%{arch}/lib/libtapi32.a
%{arch}/lib/libtapiperf.a
%{arch}/lib/libtapisrv.a
%{arch}/lib/libtbs.a
%{arch}/lib/libtcpmib.a
%{arch}/lib/libtcpmon.a
%{arch}/lib/libtcpmonui.a
%{arch}/lib/libtdh.a
%{arch}/lib/libtermmgr.a
%{arch}/lib/libtermsrv.a
%{arch}/lib/libthawbrkr.a
%{arch}/lib/libthemeui.a
%{arch}/lib/libtlntsvrp.a
%{arch}/lib/libtraffic.a
%{arch}/lib/libtrialoc.a
%{arch}/lib/libtrkwks.a
%{arch}/lib/libtsappcmp.a
%{arch}/lib/libtsbyuv.a
%{arch}/lib/libtscfgwmi.a
%{arch}/lib/libtsd32.a
%{arch}/lib/libtshoot.a
%{arch}/lib/libtsoc.a
%{arch}/lib/libtwext.a
%{arch}/lib/libtxflog.a
%{arch}/lib/libtxfw32.a
%{arch}/lib/libudhisapi.a
%{arch}/lib/libufat.a
%{arch}/lib/libuihelper.a
%{arch}/lib/libulib.a
%{arch}/lib/libumandlg.a
%{arch}/lib/libumdmxfrm.a
%{arch}/lib/libumpnpmgr.a
%{arch}/lib/libuniime.a
%{arch}/lib/libunimdmat.a
%{arch}/lib/libuniplat.a
%{arch}/lib/libuntfs.a
%{arch}/lib/libupnp.a
%{arch}/lib/libupnphost.a
%{arch}/lib/libupnpui.a
%{arch}/lib/libureg.a
%{arch}/lib/liburl.a
%{arch}/lib/liburlauth.a
%{arch}/lib/liburlmon.a
%{arch}/lib/libusbcamd2.a
%{arch}/lib/libusbd.a
%{arch}/lib/libusbmon.a
%{arch}/lib/libusbport.a
%{arch}/lib/libuser32.a
%{arch}/lib/libuserenv.a
%{arch}/lib/libusp10.a
%{arch}/lib/libutildll.a
%{arch}/lib/libuuid.a
%{arch}/lib/libuxtheme.a
%{arch}/lib/libvbscript.a
%{arch}/lib/libvds_ps.a
%{arch}/lib/libvdsbas.a
%{arch}/lib/libvdsdyndr.a
%{arch}/lib/libvdsutil.a
%{arch}/lib/libvdswmi.a
%{arch}/lib/libverifier.a
%{arch}/lib/libversion.a
%{arch}/lib/libvfw32.a
%{arch}/lib/libvgx.a
%{arch}/lib/libviewprov.a
%{arch}/lib/libvmx_mode.a
%{arch}/lib/libvss_ps.a
%{arch}/lib/libvssapi.a
%{arch}/lib/libvsstrace.a
%{arch}/lib/libvsswmi.a
%{arch}/lib/libw32time.a
%{arch}/lib/libw32topl.a
%{arch}/lib/libw3cache.a
%{arch}/lib/libw3comlog.a
%{arch}/lib/libw3core.a
%{arch}/lib/libw3ctrlps.a
%{arch}/lib/libw3ctrs.a
%{arch}/lib/libw3dt.a
%{arch}/lib/libw3ext.a
%{arch}/lib/libw3isapi.a
%{arch}/lib/libw3ssl.a
%{arch}/lib/libw3tp.a
%{arch}/lib/libwab32.a
%{arch}/lib/libwabimp.a
%{arch}/lib/libwamreg.a
%{arch}/lib/libwamregps.a
%{arch}/lib/libwbemcore.a
%{arch}/lib/libwbemupgd.a
%{arch}/lib/libwdigest.a
%{arch}/lib/libwdmaud.a
%{arch}/lib/libwdsclient.a
%{arch}/lib/libwdsclientapi.a
%{arch}/lib/libwdscore.a
%{arch}/lib/libwdscsl.a
%{arch}/lib/libwdsimage.a
%{arch}/lib/libwdstptc.a
%{arch}/lib/libwdsupgcompl.a
%{arch}/lib/libwdsutil.a
%{arch}/lib/libwebcheck.a
%{arch}/lib/libwebclnt.a
%{arch}/lib/libwebhits.a
%{arch}/lib/libwecapi.a
%{arch}/lib/libwer.a
%{arch}/lib/libwevtapi.a
%{arch}/lib/libwevtfwd.a
%{arch}/lib/libwiadss.a
%{arch}/lib/libwiarpc.a
%{arch}/lib/libwiaservc.a
%{arch}/lib/libwiashext.a
%{arch}/lib/libwin32spl.a
%{arch}/lib/libwinfax.a
%{arch}/lib/libwininet.a
%{arch}/lib/libwinipsec.a
%{arch}/lib/libwinmm.a
%{arch}/lib/libwinrnr.a
%{arch}/lib/libwinscard.a
%{arch}/lib/libwinspool.a
%{arch}/lib/libwinsrv.a
%{arch}/lib/libwinsta.a
%{arch}/lib/libwintrust.a
%{arch}/lib/libwinusb.a
%{arch}/lib/libwkssvc.a
%{arch}/lib/libwlanapi.a
%{arch}/lib/libwlanui.a
%{arch}/lib/libwlanutil.a
%{arch}/lib/libwldap32.a
%{arch}/lib/libwlnotify.a
%{arch}/lib/libwlstore.a
%{arch}/lib/libwmi.a
%{arch}/lib/libwmi2xml.a
%{arch}/lib/libwmiaprpl.a
%{arch}/lib/libwmiprop.a
%{arch}/lib/libwmisvc.a
%{arch}/lib/libwow64.a
%{arch}/lib/libwow64cpu.a
%{arch}/lib/libwow64mib.a
%{arch}/lib/libwow64win.a
%{arch}/lib/libwpd_ci.a
%{arch}/lib/libws2_32.a
%{arch}/lib/libws2help.a
%{arch}/lib/libwscsvc.a
%{arch}/lib/libwsdapi.a
%{arch}/lib/libwshatm.a
%{arch}/lib/libwshbth.a
%{arch}/lib/libwshcon.a
%{arch}/lib/libwsock32.a
%{arch}/lib/libwtsapi32.a
%{arch}/lib/libx3daudio.a
%{arch}/lib/libx3daudio1_*.a
%{arch}/lib/libx3daudiod1_7.a
%{arch}/lib/libxapofx.a
%{arch}/lib/libxapofx1_*.a
%{arch}/lib/libxapofxd1_5.a
%{arch}/lib/libxaudio.a
%{arch}/lib/libxaudio2_*.a
%{arch}/lib/libxaudiod.a
%{arch}/lib/libxaudiod2_7.a
%{arch}/lib/libxinput.a
%{arch}/lib/libxinput1_*.a
%{arch}/lib/libzoneoc.a

%if %{without bootstrap}
%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-c++
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{arch}/lib/libstdc++-7.dll
%{arch}/lib/libstdc++.a
%{arch}/lib/libstdc++.dll.a
%{arch}/lib/libstdc++.la
%{arch}/lib/libsupc++.a
%{arch}/lib/libsupc++.la
%{arch}/include/c++
%{_mandir}/man1/%{target}-g++.1*
%endif
