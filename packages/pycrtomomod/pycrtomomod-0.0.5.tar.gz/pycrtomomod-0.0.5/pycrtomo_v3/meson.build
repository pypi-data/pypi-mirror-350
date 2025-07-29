# project('pycrtomo',
#         ['c', 'fortran'],
#         version : '0.1',
#         meson_version: '>= 1.1.0',
#         default_options : [
#                             'warning_level=1',
#                             'buildtype=release'
#                           ])
fc = meson.get_compiler('fortran')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
np_dep = declare_dependency(include_directories: inc_np)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

inc_np = include_directories(incdir_numpy, incdir_f2py)
# gh-25000
quadmath_dep = fc.find_library('quadmath', required: false)




py.extension_module('pycrtomo',
                     [
                     '''crerror.h''',
                     '''my_git_version.h''',
                     '''alloci.f90''',
                     '''datmod.f90''',
                     '''electrmod.f90''',
                     '''elemmod.f90''',
                     '''errmod.f90''',
                     '''femmod.f90''',
                     '''invmod.f90''',
                     '''konvmod.f90''',
                     '''modelmod.f90''',
                     '''pathmod.f90''',
                     '''randbmod.f90''',
                     '''sigmamod.f90''',
                     '''wavenmod.f90''',
                     '''bbsens.f90''',
                     '''bessi0.f90''',
                     '''beta.f90''',
                     '''bessi1.f90''',
                     '''bessk0.f90''',
                     '''bessk1.f90''',
                     '''bkfak.f90''',
                     '''bsytop.f90''',
                     '''chareal.f90''',
                     '''chkpol.f90''',
                     '''chol.f90''',
                     '''elem1.f90''',
                     '''elem3.f90''',
                     '''elem4.f90''',
                     '''elem5.f90''',
                     '''elem8.f90''',
                     '''filpat.f90''',
                     '''gammln.f90''',
                     '''gaulag.f90''',
                     '''gauleg.f90''',
                     '''get_error.f90''',
                     '''get_git_ver.f90''',
                     '''ompmod.f90''',
                     '''get_unit.f90''',
                     '''intcha.f90''',
                     '''kompab.f90''',
                     '''kompb.f90''',
                     '''make_noise.f90''',
                     '''potana.f90''',
                     '''precal.f90''',
                     '''randb.f90''',
                     '''randb2.f90''',
                     '''rdatm.f90''',
                     '''relectr.f90''',
                     '''relem.f90''',
                     '''rrandb.f90''',
                     '''rsigma.f90''',
                     '''refsig.f90''',
                     '''rtrafo.f90''',
                     '''rwaven.f90''',
                     '''scalab.f90''',
                     '''sort.f90''',
                     '''tic_toc.f90''',
                     '''vre.f90''',
                     '''wkpot.f90''',
                     '''wout.f90''',
                     '''cjgmod.f90''',
                     '''invhpmod.f90''',
                     '''variomodel.f90''',
                     '''besp_elem.f90''',
                     '''blam0.f90''',
                     '''bnachbar.f90''',
                     '''bmcm_mod.f90''',
                     '''bpar.f90''',
                     '''brough_mod.f90''',
                     '''bsendc.f90''',
                     '''bsensi.f90''',
                     '''bsigm0.f90''',
                     '''bsigma.f90''',
                     '''bsmatm_mod.f90''',
                     '''bvariogram.f90''',
                     '''bvolti.f90''',
                     '''bvariogram_s.f90''',
                     '''cg_mod.f90''',
                     '''chold.f90''',
                     '''choldc.f90''',
                     '''cholz.f90''',
                     '''dmisft.f90''',
                     '''gauss_dble.f90''',
                     '''gauss_cmplx.f90''',
                     '''kont1.f90''',
                     '''kont2.f90''',
                     '''kompadc.f90''',
                     '''kompbdc.f90''',
                     '''linvd.f90''',
                     '''linvz.f90''',
                     '''mdian1.f90''',
                     '''parfit.f90''',
                     '''randdc.f90''',
                     '''randbdc2.f90''',
                     '''rall.f90''',
                     '''rdati.f90''',
                     '''scaldc.f90''',
                     '''update.f90''',
                     '''vredc.f90''',
                     '''wout_up.f90''',
                     '''invpy.f90''',
                     '''pycrtomomodule.c''',
                     '''pycrtomo-f2pywrappers2.f90''',
                     fortranobject_c
                     ],
                     include_directories: [
                     inc_np,

                     ],
                     dependencies : [
                     py_dep,
                     quadmath_dep,
                     dependency('openmp'),


                     ],

                     install : true)
