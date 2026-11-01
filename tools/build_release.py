"""Build the MO2 install archive; developer files are deliberately excluded."""
from pathlib import Path
import hashlib

import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(destination=None):
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    if not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful():
        raise RuntimeError('Release checks failed; no archive was built')
    version = ET.fromstring((ROOT / 'fomod/info.xml').read_bytes()).findtext('Version')
    if not version:
        raise ValueError('FOMOD version is missing')
    filename = 'Absolute_RPG_v' + version.replace(' ', '_') + '.zip'
    destination = Path(destination) if destination else ROOT / 'dist'
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / filename
    files = []
    for name in ['gamedata', 'variants', 'fomod', 'licenses']:
        files.extend(p for p in (ROOT / name).rglob('*') if p.is_file())
    files.extend(ROOT / name for name in ['README_RU.txt', 'CREDITS.txt'])
    if any(p.suffix in ['.py', '.pyc', '.log', '.dmp'] for p in files):
        raise ValueError('Developer files found in the install tree')
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for p in sorted(files):
            info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Archive CRC verification failed')
        if len(archive.namelist()) != len(files):
            raise RuntimeError('Archive entry count mismatch')
    print(output)
    print(f'{len(files)} files, {output.stat().st_size} bytes')
    print('SHA256 ' + hashlib.sha256(output.read_bytes()).hexdigest())
    return output


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else None)
