from json_parse import json_parse
from pprint import pprint
from collections import defaultdict
from titlecase import titlecase
import spell_correct


def insert_space(model, phrase):
    return model[0:(len(phrase))] + ' ' + model[len(phrase):]


def standardize(data, phrase):
    phrase = phrase.upper()
    model = data["model"]
    model = "".join(model.split()).upper()
    if model.startswith(phrase):
        model = insert_space(model, phrase).strip()
        print(model)


def standardize_manufacturer(data, d, abbr):
    manufacturer = str(data["manufacturer"])
    model = str(data["model"])
    remove_hyphen = model.replace("-", "").lower()
    # Split the string into individual words. split() returns a list.
    split_model = remove_hyphen.split()

    # Combine model number
    if len(split_model[0]) < 4:
        split_model[0] += split_model[1]
        del split_model[1]

    # Spell check the model name. If it is an abbreviation, replace it with its full form.
    for i in range(1, len(split_model)):
        if split_model[i] in abbr:
            split_model[i] = titlecase(abbr[split_model[i]])
        else:
            split_model[i] = titlecase(spell_correct.correct(split_model[i]))

    # Convert the model number to upper case.
    split_model[0] = split_model[0].upper()

    # Join the list with a single space to give the model string.
    model = " ".join(split_model)

    # Add the manufacturer and model to a dictionary of lists.
    if manufacturer not in d:
        d[manufacturer].append(model)
    elif model not in d[manufacturer]:
        d[manufacturer].append(model)


def main():
    case_dict = defaultdict(list)
    abbreviations = {'std': 'standard', 'cut': 'cutter'}
    with open('machine_model-Case.json', 'r') as record:
        for data in json_parse(record, "\n"):
            standardize_manufacturer(data, case_dict, abbreviations)

    pprint(dict(case_dict))

    with open('machine_model-Caterpillar.json', 'r') as record:
        for data in json_parse(record, "\n"):
            standardize(data, "140h")


if __name__ == '__main__':
    main()
