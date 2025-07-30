configure_file(
    input: '_util.py',
    output: '_util.py',
    configuration: configuration_data({'VERSION': meson.project_version()}),
    install: true,
    install_dir: python.get_install_dir() / 'ozi_build',
    install_tag: 'python-runtime',
)
sources = [
    '__init__.py',
    '_at.py',
    '_branch.py',
    '_categories.py',
    '_char.py',
    '_files.py',
    '_groupref.py',
    '_ranges.py',
    '_redos.py',
    '_regexploit.py',
    '_repeat.py',
    '_sequence.py',
    '_sre.py',
    '_text.py',
    'buildapi.py',
    'config.py',
    'metadata.py',
    'pep425tags.py',
    'schema.py',
    '_pyc_wheel.py',
]
foreach source: sources
    fs.copyfile(source)
    python.install_sources(
        source,
        pure : true,
        subdir : 'ozi_build'
    )
endforeach
subdir('jwt')