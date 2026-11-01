"""Release checks for the installable mod; run: python -m unittest discover -s tests."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def skills(root):
    result = {}
    for p in sorted((root / 'configs/experience_framework/skills').glob('*.ltx')):
        current = None
        for line in p.read_text(encoding='utf-8-sig').splitlines():
            line = line.split(';', 1)[0].strip()
            m = re.match(r'\[([^]]+)\]', line)
            if m:
                current = result.setdefault(m[1], {})
            elif current is not None and '=' in line:
                k, v = map(str.strip, line.split('=', 1))
                current[k] = v
    return {k: v for k, v in result.items() if k.startswith('perk_')}


def strings(root, lang):
    result = {}
    for p in sorted((root / f'configs/text/{lang}').glob('*.xml')):
        for e in ET.fromstring(p.read_bytes()).findall('string'):
            key = e.get('id')
            if key in result:
                raise AssertionError(f'Duplicate string ID {key} in {p}')
            result[key] = e.findtext('text') or ''
    return result


def installed(profile):
    data = {}
    for folder in [ROOT / 'gamedata', ROOT / f'variants/{profile}/gamedata']:
        if folder.is_dir():
            for p in folder.rglob('*'):
                if p.is_file():
                    data[p.relative_to(folder).as_posix()] = p
    return data


class ReleaseChecks(unittest.TestCase):
    def test_preset_has_current_name_and_no_unused_options(self):
        text = (ROOT / 'gamedata/scripts/x_cxv_experience_perks_mcm.script').read_text(encoding='utf-8-sig')
        self.assertIn('add_preset("Absolute RPG Preset", ilrath_preset)', text)
        self.assertNotIn('local options =', text)
        self.assertNotIn('--experience_mcm.add_option(options)', text)

    def test_xml_is_valid(self):
        for p in ROOT.rglob('*.xml'):
            if '.git' not in p.parts:
                with self.subTest(path=p.relative_to(ROOT)):
                    ET.fromstring(p.read_bytes())

    def test_skill_set_and_rank_budget(self):
        base = skills(ROOT / 'gamedata')
        self.assertEqual(len(base), 66)
        self.assertEqual(sum(int(s['max_level']) for s in base.values()), 224)
        for profile in ['clikrad', 'clikrad_aml']:
            merged = base | skills(ROOT / f'variants/{profile}/gamedata')
            self.assertEqual(set(merged), set(base))
            self.assertEqual(sum(int(s['max_level']) for s in merged.values()), 224)

    def test_every_description_has_player_facing_format(self):
        base = skills(ROOT / 'gamedata')
        checked = 0
        forbidden = re.compile(r'health_restore_speed|UIWorkshopCraft|liz_fdda|lam2|callback|monkeypatch|healthThreshold|enable=false|компонент интеграции|integration component|engine limitation|ограничение движка|скрипт|script API', re.I)
        for profile in ['', 'clikrad', 'clikrad_aml']:
            for lang in ['rus', 'eng']:
                st = strings(ROOT / 'gamedata', lang)
                if profile:
                    st.update(strings(ROOT / f'variants/{profile}/gamedata', lang))
                header = '%c[ui_gray_3]' + ('Эффекты:' if lang == 'rus' else 'Effects:')
                for skill_id, data in base.items():
                    for suffix in [''] + ['_' + str(n) for n in range(1, int(data['max_level']) + 1)]:
                        key = data['description'] + suffix
                        with self.subTest(profile=profile or 'gamma', lang=lang, skill=skill_id, rank=suffix):
                            self.assertIn(key, st)
                            value = st[key]
                            self.assertEqual(value.count(header), 1, key)
                            self.assertIn('\\n\\n' + header + '\\n%c[ui_gray_2]- ', value, key)
                            self.assertFalse(forbidden.search(value), key)
                            self.assertNotIn('\ufffd', value)
                            self.assertNotIn('\n', value, 'Use literal X-Ray newline escapes')
                            self.assertTrue(value.endswith('%c[ui_gray_2]'), key)
                            if '%c[d_red]' in value:
                                warning = value.split('%c[d_red]', 1)[1]
                                self.assertNotIn('%c[', warning.removesuffix('%c[ui_gray_2]'))
                            checked += 1
        self.assertEqual(checked, 1740)

    def test_required_warnings_are_red(self):
        required = ['perk_rapid_reload', 'perk_observer', 'perk_field_dresser', 'perk_symbiosis', 'perk_milspec_engineer', 'perk_lockpick_mastery', 'perk_mag_loader', 'perk_museum_exhibit']
        sk = skills(ROOT / 'gamedata')
        for lang in ['rus', 'eng']:
            st = strings(ROOT / 'gamedata', lang)
            for skill_id in required:
                for n in range(1, int(sk[skill_id]['max_level']) + 1):
                    value = st[sk[skill_id]['description'] + '_' + str(n)]
                    self.assertIn('%c[d_red]', value, (lang, skill_id, n))

    def test_no_obsolete_visible_branding(self):
        for lang in ['rus', 'eng']:
            for key, value in strings(ROOT / 'gamedata', lang).items():
                # Mags Redux is a different, still required magazine addon.
                clean = re.sub(r'Mags Redux', '', value, flags=re.I)
                self.assertNotRegex(clean, r'(?i)\bredux\b|stage7[igh]?', (lang, key))

    def test_localisations_agree_on_numeric_effects(self):
        from collections import Counter
        sk = skills(ROOT / 'gamedata')
        for profile in ['', 'clikrad', 'clikrad_aml']:
            tables = {}
            for lang in ['rus', 'eng']:
                tables[lang] = strings(ROOT / 'gamedata', lang)
                if profile:
                    tables[lang].update(strings(ROOT / f'variants/{profile}/gamedata', lang))
            for skill_id, data in sk.items():
                for rank in range(1, int(data['max_level']) + 1):
                    key = data['description'] + '_' + str(rank)
                    numbers = []
                    for lang in ['rus', 'eng']:
                        value = re.sub(r'%c\[[^]]+\]', '', tables[lang][key])
                        effects = re.split(r'(?:Эффекты|Effects):', value)[1]
                        numbers.append(Counter(re.findall(r'\d+(?:\.\d+)?', effects.replace(',', '.'))))
                    with self.subTest(profile=profile, skill=skill_id, rank=rank):
                        self.assertEqual(*numbers)

    def test_fomod_profiles_and_sources(self):
        doc = ET.fromstring((ROOT / 'fomod/ModuleConfig.xml').read_bytes())
        group = doc.find('.//group')
        assert group is not None
        self.assertEqual(group.get('type'), 'SelectExactlyOne')
        self.assertEqual(len(group.findall('./plugins/plugin')), 3)
        for e in doc.iter():
            if e.tag in ['folder', 'file'] and 'source' in e.attrib:
                self.assertTrue((ROOT / e.attrib['source']).exists(), e.attrib['source'])
        for profile in ['', 'clikrad', 'clikrad_aml']:
            files = installed(profile)
            self.assertEqual('scripts/magazines_aml.script' in files, profile == 'clikrad_aml')


if __name__ == '__main__':
    unittest.main()
