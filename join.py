"""Join two csv files using a specified column and write the result to the standard output.

Program should be executed with a command: "join.py file_path1 file_path2 column_name join_type".

The available join types are inner, left and right. The default join type is inner.
"""

import sys
from copy import deepcopy
import tabulate


def read_csv(path):
    """Read a csv file.

    Parameters:
    path (str): A path to the csv file.

    Returns:
    list: A list of dictionaries which correspond to csv file's rows, where keys are column headers.

    """

    results = []
    with open(path, 'r+') as f:
        lines = f.read().split('\n')
        keys = tuple(lines[0].split(','))
        for i in range(1, len(lines)):
            row = tuple(lines[i].split(','))
            dict_csv = {keys[k]: row[k] for k in range(len(keys))}
            results.append(dict_csv)
        return results


def inner_join(list1, list2, column):
    """Inner join two lists of dictionaries.

    Parameters:
    list1 (list): A list of dictionaries.
    list2 (list): A list of dictionaries.
    column: A column name by which the lists are joined.

    Returns:
    list: A list of merged dictionaries where keys are column headers.

    """

    merged_list = []
    for d1 in list1:
        col_id = d1[column]
        for d2 in list2:
            if d2[column] == col_id:
                merged_dict = {**d1, **d2}
                merged_list.append(merged_dict)
                break
    return merged_list


def outer_join(list1, list2, column):
    """Left outer join two lists of dictionaries.

    Parameters:
    list1 (list): A list of dictionaries treated as the left table.
    list2 (list): A list of dictionaries treated as the right table.
    column: A column name by which the lists are joined.

    Returns:
    list: A list of merged dictionaries where keys are column headers.

    """

    merged_list = []
    for d1 in list1:
        col_id = d1[column]
        for d2 in list2:
            found = False
            if d2[column] == col_id:
                merged_dict = {**d1, **d2}
                found = True
                break
        if not found:
            d = deepcopy(d2)
            d.update((key, None) for key in d)
            d.update(d1)
            merged_dict = d
        merged_list.append(merged_dict)
    return merged_list


def display(data):
    """Display a list of dictionaries as a table in standard output.

    Parameters:
    data (list): A list of dictionaries to display.

    Returns:
    None

    """

    header = data[0].keys()
    rows = [[x[column] for column in header] for x in data]
    print(tabulate.tabulate(rows, header, tablefmt='rst'))


if __name__ == "__main__":
    try:
        file1 = read_csv(sys.argv[1])
        file2 = read_csv(sys.argv[2])
        column_name = sys.argv[3]
        if len(sys.argv) == 5:
            join_type = sys.argv[4]
        else:
            join_type = 'inner'
    except IndexError:
        print("Program should be executed with a command: join.py file_path1 file_path2 column_name join_type")
        sys.exit(1)

    if join_type == 'left':
        display(outer_join(file1, file2, column_name))
    elif join_type == 'right':
        display(outer_join(file2, file1, column_name))
    elif join_type == 'inner':
        display(inner_join(file1, file2, column_name))
