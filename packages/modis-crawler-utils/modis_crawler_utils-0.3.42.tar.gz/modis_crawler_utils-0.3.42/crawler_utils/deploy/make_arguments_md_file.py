import argparse
import json
import re

common_header = '_common'
args_header = 'args'
settings_header = 'settings'
description_header = 'description'


def main():
    cmd_args = parse_cmd_args()
    with open(cmd_args.input, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        with open(cmd_args.output, 'w') as result_file:
            if cmd_args.single:
                add_part(result_file, json_data)
            else:
                for item in json_data:
                    item_data = json_data[item]
                    part_name = 'Общие настройки и аргументы' if item == common_header else item
                    heading = '#' * cmd_args.level + ' ' + part_name + '\n\n'
                    add_part(result_file, item_data, heading)
        print('Successfully generated arguments.md file')


def parse_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default='args_and_settings.json', metavar='args_and_settings.json',
                        help='Input JSON file with settings and arguments')
    parser.add_argument('-o', '--output', type=str, default='arguments.md', metavar='arguments.md',
                        help='Output markdown file')
    parser.add_argument('-l', '--level', type=int, default=4, help='Section heading level')
    parser.add_argument('-s', '--single', default=False, action='store_true',
                        help='If set, expects input JSON to have args and settings for single crawler on top level')
    return parser.parse_args()


def add_part(file, data, heading=None):
    description = data.get(description_header)
    settings = data.get(settings_header)
    args = data.get(args_header)
    if heading and (description or settings or args):
        file.write(heading)
    if description:
        file.write(description + '\n\n')
    if settings:
        fill_args_settings_table(data[settings_header], file, 'Настройка')
    if args:
        fill_args_settings_table(data[args_header], file, 'Аргумент')


def fill_args_settings_table(data, file, table_type):
    header = ('№', table_type, 'Название', 'Тип', 'Описание', 'Обязателен', 'Значение по умолчанию')
    write_table_header(header, file)

    for index, table_data in enumerate(data, start=1):
        file.write('|' + '|'.join((
            str(index),
            table_data['name'].replace('_', '_\u200b'),  # allows break on underscore for long names
            table_data['short_description'],
            table_data['type'],
            table_data['long_description'],
            'Да' if table_data.get('required') else 'Нет',
            re.sub(r',(?=\S)', ',\u200b', str(table_data.get('default', '-'))),  # allows break on comma for list-like settings
        )) + '|\n')
    file.write('\n\n')


def write_table_header(header, file):
    file.write('| ' + ' | '.join(header) + ' |\n')
    file.write('|-' + '-|-'.join('-' * len(c) for c in header) + '-|\n')


if __name__ == '__main__':
    main()
