
py = import('python').find_installation()
py_dep = py.dependency()

python_sources = [
  '__init__.py',
  'pycrtomo.py',
  'extract_pyinv_examples.py',
]

py.install_sources(
  python_sources,
  pure: true,
  subdir: 'crtomo_tests'
)

install_data(
    [
      'data/example_modeling_01.zip',
      'data/example_inversion_01.zip',
    ],
    install_dir: py.get_install_dir() / 'crtomo_tests/data',
)
