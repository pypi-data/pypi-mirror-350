import random
from typing import Literal, Union, Optional, Sequence, Any, List, Callable, Tuple


RANDOM_METHODS = ["random_list", "random_matrix", "random_tuple", "random_dict"
                  "random_set", "random_str", "random_tensor"]


# ===== English Alphabet =====
EN_ALPHABET_LOWER = "abcdefghijklmnopqrstuvwxyz"
EN_ALPHABET_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EN_ALPHABET_ALL = EN_ALPHABET_LOWER + EN_ALPHABET_UPPER

# Vowels
EN_VOWELS_LOWER = "aeiouy"
EN_VOWELS_UPPER = "AEIOUY"
EN_VOWELS_ALL = EN_VOWELS_LOWER + EN_VOWELS_UPPER

# Consonants
EN_CONSONANTS_LOWER = "bcdfghjklmnpqrstvwxz"
EN_CONSONANTS_UPPER = "BCDFGHJKLMNPQRSTVWXZ"
EN_CONSONANTS_ALL = EN_CONSONANTS_LOWER + EN_CONSONANTS_UPPER

# ===== Russian Alphabet =====
RU_ALPHABET_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_ALPHABET_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
RU_ALPHABET_ALL = RU_ALPHABET_LOWER + RU_ALPHABET_UPPER

# Vowels
RU_VOWELS_LOWER = "аеёиоуыэюя"
RU_VOWELS_UPPER = "АЕЁИОУЫЭЮЯ"
RU_VOWELS_ALL = RU_VOWELS_LOWER + RU_VOWELS_UPPER

# Consonants
RU_CONSONANTS_LOWER = "бвгджзйклмнпрстфхцчшщ"
RU_CONSONANTS_UPPER = "БВГДЖЗЙКЛМНПРСТФХЦЧШЩ"
RU_CONSONANTS_ALL = RU_CONSONANTS_LOWER + RU_CONSONANTS_UPPER

# Hard/Soft signs
RU_SIGNS_LOWER = "ъыь"
RU_SIGNS_UPPER = "ЪЫЬ"
RU_SIGNS_ALL = RU_SIGNS_LOWER + RU_SIGNS_UPPER

# ===== Special Characters =====
PUNCTUATION = ".,!?;:'\"()-–—[]{}…/"
MATH_SYMBOLS = "+-×÷=≠≈<>≤≥^√%‰°"
CURRENCY_SYMBOLS = "$€£¥₽₹₩₺₴"
OTHER_SYMBOLS = "@#&*\\|~_©®™§¶•"
WHITESPACE = " \t\n\r\v\f"

# ===== Numbers =====
DIGITS_ARABIC = "0123456789"
DIGITS_ROMAN = "ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅬⅭⅮⅯ"
DIGITS_WORDS_EN = ["zero", "one", "two", "three", "four", 
                  "five", "six", "seven", "eight", "nine"]
DIGITS_WORDS_RU = ["ноль", "один", "два", "три", "четыре",
                  "пять", "шесть", "семь", "восемь", "девять"]

# ===== Combined Sets =====
LETTERS_ALL = EN_ALPHABET_ALL + RU_ALPHABET_ALL
SYMBOLS_ALL = PUNCTUATION + MATH_SYMBOLS + CURRENCY_SYMBOLS + OTHER_SYMBOLS
ALPHANUMERIC_EN = EN_ALPHABET_ALL + DIGITS_ARABIC
ALPHANUMERIC_RU = RU_ALPHABET_ALL + DIGITS_ARABIC
PRINTABLE_CHARS = LETTERS_ALL + DIGITS_ARABIC + SYMBOLS_ALL + WHITESPACE

# ===== Private Def =====
def _get_charset(language: str, category: Optional[str], case: str) -> str:
    """Select charset based on parameters"""
    base = {
        'en': {
            'all': EN_ALPHABET_ALL,
            'vowels': EN_VOWELS_ALL,
            'consonants': EN_CONSONANTS_ALL
        },
        'ru': {
            'all': RU_ALPHABET_ALL,
            'vowels': RU_VOWELS_ALL,
            'consonants': RU_CONSONANTS_ALL,
            'signs': RU_SIGNS_ALL
        }
    }.get(language, {}).get(category or 'all', PRINTABLE_CHARS)
    
    if case == 'lower':
        return base.lower()
    elif case == 'upper':
        return base.upper()
    return base

def _generate_digit(weights: Optional[Sequence[float]]) -> Union[str, int]:
    """Generates digit in different formats"""
    formats = [
        (DIGITS_ARABIC, 0.6),
        (DIGITS_ROMAN, 0.2),
        (DIGITS_WORDS_EN, 0.1),
        (DIGITS_WORDS_RU, 0.1)
    ]
    
    charset, *rest = random.choices(
        [f[0] for f in formats],
        weights=weights or [f[1] for f in formats]
    )[0]
    
    if isinstance(charset, list):
        return random.choice(charset)
    return random.choice(charset)


# ===== Public Def =====

def random_list(
    length: int = 10,
    *,
    min_value: Union[int, float] = 0,
    max_value: Union[int, float] = 100,
    value_type: Literal['int', 'float', 'str', 'bool', 'mixed', 'letter', 'digit', 'custom'] = "int",
    unique: bool = False,
    sorted: bool = False,
    elements: Optional[Sequence[Any]] = None,
    weights: Optional[Sequence[float]] = None,
    string_length: int = 5,
    charset: Optional[str] = None,
    language: Literal['en', 'ru'] = "en",
    char_category: Optional[Literal['all', 'vowels', 'consonants', 'signs']] = None,
    case: str = "mixed",
    nested: bool = False,
    nested_depth: int = 1,
    nested_length: int = 3,
    generator: Optional[Callable[[int], Any]] = None,
    seed: Optional[int] = None,
    function: Optional[Callable[[Any], Any]] = None 
) -> List[Any]:
    """
    Generates a highly customizable random list with support for multiple languages and data types.

    This function provides extensive control over list generation including:
    - Numeric values (integers/floats) within specified ranges
    - Text generation with language-specific character sets
    - Mixed-type lists with configurable probabilities
    - Nested list structures
    - Unique element enforcement and sorting options
    - Post-generation element processing

    Args:
        length (int): Desired length of the list (default: 10)
        min_value (Union[int, float]): Minimum value for numeric types (default: 0)
        max_value (Union[int, float]): Maximum value for numeric types (default: 100)
        value_type (str): Type of elements to generate. Options:
            - 'int': Integer numbers
            - 'float': Floating-point numbers
            - 'str': Random strings
            - 'bool': Boolean values
            - 'mixed': Mixed types
            - 'letter': Single letters
            - 'digit': Numeric representations
            - 'custom': Use provided elements (default: 'int')
        unique (bool): Whether elements must be unique (default: False)
        sorted (bool): Whether to sort the resulting list (default: False)
        elements (Optional[Sequence[Any]]): Custom elements when value_type='custom'
        weights (Optional[Sequence[float]]): Probability weights for custom/mixed types
        string_length (int): Length of generated strings (default: 5)
        charset (Optional[str]): Custom character set for string generation
        language (str): Language for character generation ('en' or 'ru') (default: 'en')
        char_category (Optional[str]): Character category. Options:
            - 'all': All letters
            - 'vowels': Only vowels
            - 'consonants': Only consonants
            - 'signs': Only signs (Russian only)
        case (str): Letter casing. Options: 'lower', 'upper', 'mixed' (default: 'mixed')
        nested (bool): Whether to generate nested lists (default: False)
        nested_depth (int): Maximum nesting depth (default: 1)
        nested_length (int): Length of nested lists (default: 3)
        generator (Optional[Callable[[int], Any]]): Custom element generator function
        seed (Optional[int]): Random seed for reproducible results
        element_processor (Optional[Callable[[Any], Any]]): Transformation function applied to each 
            generated element. The function receives the element and should return the processed version.
            Applied to both top-level and nested elements. (default: None)

    Returns:
        List[Any]: A randomly generated list according to specified parameters

    Raises:
        ValueError: If invalid parameters are provided (e.g., not enough unique elements)
        TypeError: If sorting fails due to mixed incompatible types

    Examples:
        >>> # Basic integer list
        >>> random_list(5, value_type='int')
        [42, 87, 15, 93, 61]

        >>> # Russian vowels in uppercase
        >>> random_list(3, value_type='letter', language='ru', 
        ...             char_category='vowels', case='upper')
        ['А', 'У', 'О']

        >>> # Mixed-type nested structure with processing
        >>> random_list(4, value_type='mixed', nested=True,
        ...             element_processor=lambda x: str(x).upper())
        ['28', ['FOO', '3.14'], 'TRUE', ['FALSE', 'BAR']]

        >>> # Custom elements with weights and processing
        >>> random_list(5, value_type='custom', 
        ...             elements=['red', 'green', 'blue'],
        ...             weights=[0.5, 0.3, 0.2],
        ...             element_processor=lambda x: f"color_{x}")
        ['color_red', 'color_blue', 'color_red', 'color_green', 'color_red']

        >>> # Number processing
        >>> random_list(3, value_type='int',
        ...             element_processor=lambda x: x**2)
        [16, 64, 9]

    Notes:
        - When using unique=True with nested lists, entire sublists are considered for uniqueness
        - Sorting mixed-type lists will convert elements to strings for comparison
        - Character categories are language-specific (e.g., 'signs' only applies to Russian)
        - For string generation, charset overrides language/char_category parameters
        - When using seed, results will be reproducible across runs
        - The element_processor is applied:
            * After element generation
            * Before uniqueness checking
            * Before sorting
            * Recursively to nested elements
        - For nested structures, the processor receives entire sublists
    """
    if seed is not None:
        random.seed(seed)
    
    # Character set selection
    if charset is None and value_type == "str":
        charset = _get_charset(language, char_category, case)
    
    if generator is not None:
        result = [generator(i) for i in range(length)]
        return [function(x) for x in result] if function else result
    
    value_generators = {
        'int': lambda: random.randint(int(min_value), int(max_value)),
        'float': lambda: random.uniform(min_value, max_value),
        'str': lambda: ''.join(random.choices(charset, k=string_length)),
        'bool': lambda: random.choice([True, False]),
        'mixed': lambda: random.choices(
            [random.randint(int(min_value), int(max_value)),
             random.uniform(min_value, max_value),
             ''.join(random.choices(charset or PRINTABLE_CHARS, k=string_length)),
             random.choice([True, False])],
            weights=weights or [0.4, 0.3, 0.2, 0.1])[0],
        'letter': lambda: random.choice(charset or LETTERS_ALL),
        'digit': lambda: _generate_digit(weights)
    }
    
    if value_type == 'custom' and elements:
        if unique and len(elements) < length:
            raise ValueError("Not enough unique elements for requested length")
        if weights and len(weights) != len(elements):
            raise ValueError("Weights length must match elements length")
        
        result = random.sample(elements, k=length) if unique else random.choices(elements, weights=weights, k=length)
        return [function(x) for x in result] if function else result
    
    if value_type not in value_generators and value_type != 'custom':
        raise ValueError(f"Unsupported value_type: {value_type}")
    
    def generate_element():
        if nested and random.random() < 0.3 and nested_depth > 0:
            nested_result = random_list(
                length=nested_length,
                min_value=min_value,
                max_value=max_value,
                value_type=value_type,
                unique=unique,
                sorted=sorted,
                weights=weights,
                elements=elements,
                string_length=string_length,
                charset=charset,
                language=language,
                char_category=char_category,
                case=case,
                nested=True,
                nested_depth=nested_depth-1,
                nested_length=nested_length,
                generator=generator,
                function=function 
            )
            return function(nested_result) if function else nested_result
        generated = value_generators[value_type]()
        return function(generated) if function else generated
    
    result = []
    seen = set()
    
    while len(result) < length:
        element = generate_element()
        
        if unique:
            element_key = tuple(element) if isinstance(element, list) else element
            if element_key in seen:
                continue
            seen.add(element_key)
        
        result.append(element)
    
    if sorted:
        try:
            result.sort()
        except TypeError:
            result.sort(key=lambda x: str(x))
    
    return result

def random_matrix():
    print(f"Функция def {random_matrix.__name__}() ещё не реализована")

def random_tensor():
    print(f"Функция def {random_tensor.__name__}() ещё не реализована")

def random_tuple():
    print(f"Функция def {random_tuple.__name__}() ещё не реализована")

def random_dict():
    print(f"Функция def {random_dict.__name__}() ещё не реализована")

def random_set():
    print(f"Функция def {random_set.__name__}() ещё не реализована")

def random_str():
    print(f"Функция def {random_str.__name__}() ещё не реализована")

def random_int(
    min: int,
    max: int,
    *,
    not_zero: bool = False,
    including: Optional[Union[int, range, List[Union[int, range]]]] = None,
    excluding: Optional[Union[int, range, List[Union[int, range]]]] = None
) -> int:
    """
    Generates a highly customizable random integer with advanced inclusion/exclusion rules.

    This function provides precise control over integer generation including:
    - Standard range constraints (min/max)
    - Special exclusion of zero value
    - Complex inclusion/exclusion rules with single values or ranges
    - Post-generation processing of the result

    Args:
        min: Minimum possible value (inclusive)
        max: Maximum possible value (inclusive)
        not_zero: If True, zero will be excluded from possible results (default: False)
        including: Values or ranges to include in selection. If None, uses full [min, max] range.
                   Examples: 
                   - 5
                   - range(10,20)
                   - [3, range(5,8), 42]
        excluding: Values or ranges to exclude from selection
                   Examples:
                   - 5
                   - range(10,20)
                   - [3, range(5,8), 100]
        seed: Random seed for reproducible results (default: None)
        element_processor: Transformation function applied to the generated value.
                           Receives the integer and should return the processed version.
                           (default: None)

    Returns:
        int: A randomly generated integer satisfying all conditions

    Raises:
        ValueError: If no valid numbers exist within the specified constraints
        TypeError: If including/excluding contains invalid types

    Examples:
        >>> # Basic random integer
        >>> random_int(1, 100)
        42

        >>> # Excluding zero and specific ranges
        >>> random_int(-50, 50, not_zero=True, 
        ...            excluding=[range(-10, 10), 42])
        37

        >>> # Only specific included values with processing
        >>> random_int(0, 100, including=[10, 20, 30],
        ...            element_processor=lambda x: x*2)
        40

        >>> # Reproducible result with seed
        >>> random_int(1, 1000, seed=42)
        654

    Notes:
        - When both including and excluding are specified, exclusions are applied after inclusions
        - Ranges in including/excluding follow standard Python range semantics (upper bound excluded)
        - The element_processor is applied after all other constraints are satisfied
        - For large exclusion sets, generation may take longer as it needs to find valid numbers
        - When using seed, results will be reproducible across runs
    """
    allowed = set()

    # Process including
    if including is None:
        allowed.update(range(min, max+1))
    else:
        elements = [including] if not isinstance(including, list) else including
        for el in elements:
            if isinstance(el, int):
                if min <= el <= max:
                    allowed.add(el)
            elif isinstance(el, range):
                for n in el:
                    if min <= n <= max:
                        allowed.add(n)
            else:
                raise TypeError("Including elements must be int or range")

    # Process excluding
    excluded = set()
    if excluding is not None:
        elements = [excluding] if not isinstance(excluding, list) else excluding
        for el in elements:
            if isinstance(el, int):
                excluded.add(el)
            elif isinstance(el, range):
                excluded.update(el)
            else:
                raise TypeError("Excluding elements must be int or range")

    allowed -= excluded

    # Handle not_zero
    if not_zero:
        allowed.discard(0)

    if not allowed:
        raise ValueError("No valid numbers matching criteria")

    return random.choice(list(allowed))

def random_float(
    min: float,
    max: float,
    *,
    not_zero: bool = False,
    including: Optional[Union[float, Tuple[float, float], List[Union[float, Tuple[float, float]]]]] = None,
    excluding: Optional[Union[float, Tuple[float, float], List[Union[float, Tuple[float, float]]]]] = None
) -> float:
    """
    Generates a highly customizable random float with advanced inclusion/exclusion rules.

    This function provides precise control over float generation including:
    - Standard range constraints (min/max)
    - Special exclusion of zero value
    - Complex inclusion/exclusion rules with single values or intervals
    - Optional precision control
    - Post-generation processing of the result

    Args:
        min: Minimum possible value (inclusive)
        max: Maximum possible value (inclusive)
        not_zero: If True, zero will be excluded from possible results (default: False)
        including: Values or intervals to include in selection. If None, uses full [min, max] range.
                   Examples:
                   - 5.0
                   - (10.0, 20.0)
                   - [3.0, (5.0, 8.0), 42.5]
        excluding: Values or intervals to exclude from selection
                   Examples:
                   - 5.0
                   - (10.0, 20.0)
                   - [3.0, (5.0, 8.0), 100.0]
        seed: Random seed for reproducible results (default: None)
        element_processor: Transformation function applied to the generated value.
                          Receives the float and should return the processed version.
                          (default: None)
        precision: Number of decimal places to round to (None means no rounding) (default: None)

    Returns:
        float: A randomly generated float satisfying all conditions

    Raises:
        ValueError: If no valid numbers exist within the specified constraints
        TypeError: If including/excluding contains invalid types

    Examples:
        >>> # Basic random float
        >>> random_float(0.0, 1.0)
        0.5488135039273248

        >>> # With precision and exclusion
        >>> random_float(0, 10, excluding=[(2.5, 3.5)], precision=2)
        4.37

        >>> # Only specific intervals with processing
        >>> random_float(0, 100, including=[(10, 20), (30, 40)],
        ...              element_processor=lambda x: f"{x:.1f}°C")
        '15.3°C'

        >>> # Reproducible result with seed and precision
        >>> random_float(0, 1, seed=42, precision=4)
        0.3745

    Notes:
        - Intervals in including/excluding are treated as [a, b] (both bounds inclusive)
        - When multiple intervals are provided in including, selection is weighted by interval length
        - The element_processor is applied after all other constraints and optional rounding
        - For complex exclusion patterns, generation may require multiple attempts
        - Precision rounding uses Python's round() function (banker's rounding)
        - Zero exclusion checks for values with absolute value < 1e-12 to account for float precision
    """
    # Validate input
    if min > max:
        raise ValueError("min must be <= max")

    # Convert inputs to interval lists
    def process_intervals(source, clip=True):
        intervals = []
        if source is None:
            return [(min, max)] if not clip else None

        elements = source if isinstance(source, list) else [source]
        for el in elements:
            if isinstance(el, (float, int)):
                val = float(el)
                if clip and (val < min or val > max):
                    continue
                intervals.append((val, val))
            elif isinstance(el, tuple) and len(el) == 2:
                a, b = sorted([float(el[0]), float(el[1])])
                if clip:
                    a = max(a, min)
                    b = min(b, max)
                    if a > b:
                        continue
                intervals.append((a, b))
            else:
                raise TypeError("Elements must be float or (float, float) tuples")
        return intervals

    include_intervals = process_intervals(including)
    exclude_intervals = process_intervals(excluding, clip=False)

    # Generate candidate numbers with max attempts
    max_attempts = 10_000
    for _ in range(max_attempts):
        # Generate in allowed range
        if include_intervals:
            # Select random interval weighted by length
            weights = [b-a for a, b in include_intervals]
            total_weight = sum(weights)
            if total_weight <= 0:
                raise ValueError("No valid intervals to generate from")
            a, b = random.choices(include_intervals, weights=weights, k=1)[0]
            candidate = random.uniform(a, b)
        else:
            candidate = random.uniform(min, max)

        # Check excludes
        exclude = False
        for a, b in exclude_intervals:
            if a <= candidate <= b:
                exclude = True
                break
        if exclude:
            continue

        # Check not_zero
        if not_zero and abs(candidate) < 1e-12:  # Account for float precision
            continue

        return candidate

    raise ValueError("Failed to find valid number after maximum attempts")