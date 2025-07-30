from setuptools import setup, Extension
from _custom_build import BuildExt

setup(
    name='hisak-jptrans',
    packages=['hisak.jptrans'],
    package_dir={'hisak.jptrans': 'src'},
    package_data={'hisak.jptrans': ['*.pyi']},
    license='MIT and BSD-3-Clause',
    author='HiSakDev',
    author_email='sak.devac@gmail.com',
    description='CP932/CP51932/EUC-JP-MS japanese codecs with Go c-shared',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    use_scm_version={'local_scheme': 'no-local-version'},
    setup_requires=['setuptools>=59', 'setuptools_scm>=6'],
    cmdclass={'build_ext': BuildExt},
    ext_modules=[Extension(
        name="hisak.jptrans._jptrans",
        sources=["."],
        language="golang",
        extra_compile_args=["-buildmode", "c-shared", "-ldflags", "-s -w", "-trimpath"],
    )],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
