import collections
from functools import lru_cache



@lru_cache
def occur_once(text: str) -> int:
    if not isinstance(text, str):
        raise TypeError('Argument is non Str-type')
    list_occurs_letter = collections.Counter(text).most_common()
    count_occurs_once = sum(map(lambda value: value[1] if value[1] == 1 else 0, list_occurs_letter))
    return count_occurs_once

def load_from_file(file: str) -> str:
    with open(file, 'r') as f:
        text = f.read()
    return text



