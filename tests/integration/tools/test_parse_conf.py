from textwrap import dedent
import json
import os
import shutil
import tempfile
import unittest

from pylexa.tools.parse_conf import parse_yaml


class TestParseYaml(unittest.TestCase):

    YAML = dedent('''\
        intents:
            - TestIntent:
                foo: AMAZON.NUMBER
                bar: CUSTOM_SLOT
            - OtherIntent
            - AMAZON.YesIntent

        utterances:
            TestIntent:
                - 'do something with {foo} and {bar}'
                - '{foo} {bar}'
            OtherIntent:
                - 'do something else'

        slots:
            CUSTOM_SLOT:
                - value 1
                - value 2
    ''')

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

        with tempfile.NamedTemporaryFile(dir=cls.tempdir, delete=False) as f:
            schema_filename = f.name
            f.write(cls.YAML)

        parse_yaml(schema_filename)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)

    def should_write_intent_schema(self):
        schema_filename = os.path.join(self.tempdir, 'intent_schema.json')
        self.assertTrue(os.path.exists(schema_filename))
        with open(schema_filename) as f:
            contents = f.read()

        expected_contents = {
            'intents': [{
                'intent': 'TestIntent',
                'slots': [{
                    'name': 'foo',
                    'type': 'AMAZON.NUMBER'
                },{
                    'name': 'bar',
                    'type': 'CUSTOM_SLOT'
                }]
            }, {
                'intent': 'OtherIntent',
            },{
                'intent': 'AMAZON.YesIntent'
            }]
        }
        self.assertEqual(json.loads(contents), expected_contents)

    def should_write_slots(self):
        slot_dir = os.path.join(self.tempdir, 'slots')
        self.assertTrue(os.path.exists(slot_dir))
        custom_slot_file = os.path.join(slot_dir, 'CUSTOM_SLOT')
        self.assertTrue(os.path.exists(custom_slot_file))

        with open(custom_slot_file) as f:
            contents = f.read()

        expected_contents = 'value 1\nvalue 2'
        self.assertEqual(contents, expected_contents)

    def should_write_utterances(self):
        utterances_file = os.path.join(self.tempdir, 'utterances.txt')
        self.assertTrue(os.path.exists(utterances_file))
        with open(utterances_file) as f:
            contents = f.read()

        expected_contents = '\n'.join([
            'OtherIntent do something else',
            'TestIntent do something with {foo} and {bar}',
            'TestIntent {foo} {bar}',
        ])

        self.assertEqual(contents, expected_contents)
