from .str_utils import *

count_occurrences = many_count 
STR_METHODS_ALTS = STR_METHODS + ["count_occurences"]

from .random_utils import *

random_dictionary = random_dict
random_string = random_str
RANDOM_METHODS_ALTS = RANDOM_METHODS + ["random_dictionary", "random_string"]

__all__ = [STR_METHODS_ALTS + RANDOM_METHODS_ALTS]
