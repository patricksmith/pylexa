import argparse
import json
import os

import yaml


parser = argparse.ArgumentParser(description='Convert YAML to Alexa conf files')
parser.add_argument('filename', help='path to input YAML file')


def parse_yaml(filename):
    with open(filename) as f:
        data = yaml.safe_load(f.read())

    path = os.path.dirname(filename)
    write_intents(
        data.get('intents', {}), os.path.join(path, 'intent_schema.json'))
    write_slots(data.get('slots', {}), os.path.join(path, 'slots'))
    write_utterances(
        data.get('utterances', {}), os.path.join(path, 'utterances.txt'))


def format_intents(intents):
    for intent in intents:
        if not isinstance(intent, dict):
            yield {
                'intent': intent
            }
            continue
        for intent_name in intent:
            slots = intent[intent_name]
            yield {
                'intent': intent_name,
                'slots': [{
                    'name': slot_name,
                    'type': slot_type
                } for slot_name, slot_type in slots.iteritems()]
            }


def write_intents(intents, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps({
            'intents': list(format_intents(intents))
        }, indent=2, sort_keys=True, separators=(',', ': ')))


def write_slots(slots, dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    for name, values in slots.iteritems():
        with open(os.path.join(dirname, name), 'w') as f:
            f.write('\n'.join(values))


def format_utterances(utterances):
    return '\n'.join([
        '{} {}'.format(intent, line)
        for intent, lines in sorted(utterances.iteritems())
        for line in lines
    ])


def write_utterances(utterances, filename):
    with open(filename, 'w') as f:
        f.write(format_utterances(utterances))


def main():
    args = parser.parse_args()
    parse_yaml(args.filename)


if __name__ == '__main__':
    main()
