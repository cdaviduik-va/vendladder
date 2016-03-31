""" Utilities for player stuff """


def prettify_name(name):
    """
    Make the name of a user nice
    :param name: Either a single name or a first and last name separated by a space
    :return: The single name or the first and last name in the format "Firstname LastInitial"
    """
    names = name.strip().split(' ')
    formatted_name = '{first} {last}'.format(first=names[0], last=names[1][0]) if len(names) == 2 else names[0]
    return formatted_name
