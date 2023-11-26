import typing
import configparser


def dnf_repos_parse_repofile(content: str) -> dict[str, typing.Any]:
    """ Parse a dnf repofile (.repo) into a dict.
    
    Args:
        content (str): The content of the repofile.

    Returns:
        dict[str, typing.Any]: The parsed repofile.
    """
    config = configparser.ConfigParser()
    config.read_string(content)
    sections: list[str] = config.sections()
    data: dict[str, typing.Any] = {'_keys': sections}
    for section in sections:
        data[section] = dict(config[section])
        data[section]['_keys'] = list(config[section].keys())
    return data


def unique_by_attribute(
    items: list[dict[str, typing.Any]],
    attribute: str,
    use_last: bool = False
    ) -> list[dict[str, typing.Any]]:
    """ Filter a list of dicts by a unique attribute.
    
    Args:
        items (list[dict[str, typing.Any]]): The list of dicts.
        attribute (str): The attribute to unique filter by.
        use_last (bool, optional): Whether to use the last item in the duplicated items.
            If False, the first item will be picked,
            otherwise (if True) the last item will be picked.
            Default is False.

    Returns:
        list[dict[str, typing.Any]]: The filtered list of dicts.
    """
    check = {}
    iterator = items.copy()
    result = []
    if use_last:
        iterator.reverse()
    for item in iterator:
        val = str(item[attribute])
        if not check.get(val):
            result.append(item)
            check[val] = True
    if use_last:
        result.reverse()
    return result


class FilterModule(object):

  def filters(self):
    return {
        'dnf_repos_parse_repofile': dnf_repos_parse_repofile,
        'unique_by_attribute': unique_by_attribute,
    }
