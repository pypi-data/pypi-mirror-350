# project('pycrmod',
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




py.extension_module('pycrmod',
                     [
                     '''my_git_version.h''',
                     '''crerror.h''',
                     '''elemmod.f90''',
                     '''alloci.f90''',
                     '''get_error.f90''',
                     '''tic_toc.f90''',
                     '''femmod.f90''',
                     '''datmod.f90''',
                     '''sigmamod.f90''',
                     '''electrmod.f90''',
                     '''modelmod.f90''',
                     '''relem.f90''',
                     '''relectr.f90''',
                     '''rdatm.f90''',
                     '''bsytop.f90''',
                     '''elem1.f90''',
                     '''elem3.f90''',
                     '''elem5.f90''',
                     '''elem8.f90''',
                     '''bessi0.f90''',
                     '''bessi1.f90''',
                     '''bessk0.f90''',
                     '''bessk1.f90''',
                     '''beta.f90''',
                     '''precal.f90''',
                     '''rrandb.f90''',
                     '''randb.f90''',
                     '''randdc.f90''',
                     '''refsig.f90''',
                     '''get_unit.f90''',
                     '''make_noise.f90''',
                     '''invmod.f90''',
                     '''rtrafo.f90''',
                     '''wkpot.f90''',
                     '''intcha.f90''',
                     '''filpat.f90''',
                     '''wpot.f90''',
                     '''bpot.f90''',
                     '''bkfak.f90''',
                     '''rsigma.f90''',
                     '''bvolt.f90''',
                     '''wavenmod.f90''',
                     '''vre.f90''',
                     '''bsens.f90''',
                     '''wsens.f90''',
                     '''randbmod.f90''',
                     '''errmod.f90''',
                     '''konvmod.f90''',
                     '''get_git_ver.f90''',
                     '''ompmod.f90''',
                     '''gammln.f90''',
                     '''gaulag.f90''',
                     '''gauleg.f90''',
                     '''kompab.f90''',
                     '''kompadc.f90''',
                     '''potana.f90''',
                     '''chold.f90''',
                     '''choldc.f90''',
                     '''chol.f90''',
                     '''rwaven.f90''',
                     '''randb2.f90''',
                     '''kompb.f90''',
                     '''wdatm.f90''',
                     '''scalab.f90''',
                     '''output_fempy.f90''',
                     '''fempy.f90''',
                     '''pycrmodmodule.c''',
                     '''pycrmod-f2pywrappers2.f90''',
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
