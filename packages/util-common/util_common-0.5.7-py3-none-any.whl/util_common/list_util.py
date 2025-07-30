from typing import Any


def in_batches(data: list[Any], batch_size: int) -> list[list[Any]]:
    """
    Splits the data into batches of a specified size.

    :param data: The list of data to be split into batches.
    :param batch_size: The size of each batch.
    :return: A list of batches, where each batch is a list of data items.
    """
    return [data[i : i + batch_size] for i in range(0, len(data), batch_size)]


def flatten(data: list[Any]) -> list:
    """
    Flatten a nested list using a generator expression.

    :param nested_list: A list that may contain other lists.
    :return: A flat list with all the elements from the nested lists.
    """

    def _flatten(data: list[Any]):
        for item in data:
            if isinstance(item, list):
                yield from flatten(item)
            else:
                yield item

    return list(_flatten(data))
