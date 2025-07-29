
py = import('python').find_installation()
py_dep = py.dependency()

python_sources = [
  '__init__.py',
  'crmod.py',
  'crtomo.py',
  'cutmckee.py',
]

py.install_sources(
  python_sources,
  pure: true,             # Will be installed next to binaries
  subdir: 'crtomo_wrapper'  # Folder relative to site-packages to install to
)
