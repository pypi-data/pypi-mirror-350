import io
import json
import zipfile
import tarfile
import platform
from urllib.request import urlopen
from pathlib import Path
from tempfile import TemporaryDirectory
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from subprocess import check_call, DEVNULL


class BuildExt(build_ext):
    cmd_golang = 'go'
    temp_golang = None
    version = None
    os = None
    arch = None

    def initialize_options(self):
        super().initialize_options()
        self.version = self.distribution.get_version()
        self.os = platform.system().lower()
        self.arch = platform.machine().lower()
        if self.arch == 'x86_64':
            self.arch = 'amd64'
        elif self.arch == 'aarch64':
            self.arch = 'arm64'

    def build_extensions(self):
        for ext in self.extensions:
            if ext.language in ('go', 'golang'):
                if not self._check_golang_sdk():
                    if self._download_golang_sdk():
                        self.cmd_golang = '{}/go/bin/go'.format(self.temp_golang.name)
                self._build_c_shared_golang(ext)
            else:
                super().build_extension(ext)

    def _check_golang_sdk(self) -> bool:
        try:
            check_call([self.cmd_golang, 'version'], stdout=DEVNULL)
        except FileNotFoundError:
            if self.temp_golang is None:
                self.temp_golang = TemporaryDirectory()
            return False
        return True

    def _download_golang_sdk(self) -> bool:
        if self.temp_golang is None:
            return False

        filename = None
        with urlopen('https://go.dev/dl/?mode=json') as res:
            if res.status == 200:
                for v in json.load(res):
                    if v['stable']:
                        for f in v['files']:
                            if f['os'] == self.os and f['arch'] == self.arch and f['kind'] == 'archive':
                                filename = Path(f['filename'])
                                break
                        else:
                            continue
                        break
        if filename:
            print('downloading Go SDK {}'.format(filename))
            with urlopen('https://go.dev/dl/{}'.format(filename)) as res:
                if res.status == 200:
                    if filename.suffix == '.zip':
                        with zipfile.ZipFile(io.BytesIO(res.read())) as z:
                            z.extractall(path=self.temp_golang.name)
                            return True
                    elif filename.suffix:
                        with tarfile.open(fileobj=res, mode='r:{}'.format(filename.suffix[1:])) as tar:
                            tar.extractall(path=self.temp_golang.name)
                            return True
        return False

    def _build_c_shared_golang(self, ext: Extension):
        out = Path(self.get_ext_fullpath(ext.name)).absolute()
        cmd = [self.cmd_golang, 'build']
        ok_version = False
        next_arg = ''
        for arg in ext.extra_compile_args:
            if next_arg:
                arg += ' {}'.format(next_arg)
                next_arg = ''
            cmd.append(arg)
            if arg == '-ldflags' and self.version:
                next_arg = '-X main.version={}'.format(self.version)
                ok_version = True
        if not ok_version and self.version:
            cmd.append('-ldflags')
            cmd.append('-X main.version={}'.format(self.version))
        cmd.append('-o')
        cmd.append(str(out))
        if len(ext.sources) == 1 and Path(ext.sources[0]).is_dir():
            cmd.append('.')
            check_call(cmd, cwd=Path(ext.sources[0]).absolute())
        else:
            for source in ext.sources:
                cmd.append(source)
            check_call(cmd)
        if out.exists():
            out.chmod(0o755)
        hout = out.with_suffix('.h')
        if hout.exists():
            hout.unlink()
