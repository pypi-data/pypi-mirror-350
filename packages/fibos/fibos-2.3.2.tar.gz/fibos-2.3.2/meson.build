project('fibos', 
        ['c', 'fortran'],
        version: '2.3.2',
	license: 'MIT',
        default_options: [
            'buildtype=release',
            'warning_level=2',
        ])

py = import('python').find_installation('python3', pure: false)
py_dep = py.dependency()
numpy_dep = dependency('numpy')

# Define common arguments for all modules
common_args = {
    'name_prefix': '',
    'install': true,
    'install_dir': py.get_install_dir() / 'fibos',
    'dependencies': [py_dep, numpy_dep],
}

if host_machine.system() == 'windows'
    extension = '.dll'
elif host_machine.system() == 'darwin'
    extension = '.dylib'
else
    extension = '.so'
endif

# Build each module with explicit names
modules = [
    'main75',
    'ds75',
    'occsurf75',
    'renum75',
    'surfcal76',
    'respak75'
]

foreach module : modules
    shared_module(
        module,
        [f'fibos/fortran/@module@.f'],
        override_options: [f'name_suffix=@extension@'],
        kwargs: common_args,
    )
endforeach

# Install all Python package files
python_sources = [
    'fibos/__init__.py',
    'fibos/cleaner.py',
    'fibos/folders_manipulate.py',
    'fibos/main_intermediary.py',
    'fibos/manage_os.py',
    'fibos/read_Disp.py',
    'fibos/read_os.py',
    'fibos/read_prot.py',
    'fibos/respak.py',
    'fibos/utils.py',
    'fibos/set_parameters.py',
]

# Install Python files
py.install_sources(
    python_sources,
    subdir: 'fibos'
)

# Install Fortran header files
fortran_headers = [
    'fibos/fortran/assign_qr.h',
    'fibos/fortran/input_sims.h',
    'fibos/fortran/params.h',
    'fibos/fortran/surf-sims.h'
]

install_data(
    fortran_headers,
    install_dir: py.get_install_dir() / 'fibos/fortran'
)

# Install additional data files
install_data(['fibos/radii', 'fibos/pattern'],
    install_dir: py.get_install_dir() / 'fibos')
