# The tests can be run as a Script, use the Command "python tests.py",
# alternatively, they can be run as a Module using pytest
# If you wish to use pytest, you can install it by "pip3 install pytest",
# uncomment the import pytest line below, and use the Command "python -m pytest -vv tests.py"

# import pytest
import jsonlines


def test_HumanEval_32_fix():
    # the original prompt has a typo in "find_zero returns only only zero point"
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[32]["prompt"]
        assert "only only zero point" in original_prompt

    # the fixed prompt is "find_zero returns only one zero point"
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[32]["prompt"]
        assert "only only zero point" not in fixed_prompt
        assert "only one zero point" in fixed_prompt

        # make sure the function definition is correct
        solution = reader_list[38]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code)


def test_HumanEval_38_fix():
    # the original prompt doesn't have examples in the docstring
    # which causes inconsistency in the Data Set
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[38]["prompt"]
        assert ">>> decode_cyclic" not in original_prompt

    # the fixed prompt has 2 examples in the docstring of decode_cyclic
    # we didn't add examples for encode_cyclic to maintain consistency with other tasks like 32
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[38]["prompt"]
        assert ">>> decode_cyclic('bca')\n    'abc'\n" in fixed_prompt
        assert ">>> decode_cyclic('ab')\n    'ab'\n" in fixed_prompt
        assert ">>> encode_cyclic" not in fixed_prompt

        # make sure the added examples are correct
        solution = reader_list[38]["canonical_solution"]
        func_def_code = fixed_prompt + solution

        # decode_cyclic(string) is equivalent to encode_cyclic(encode_cyclics(string))
        exec(func_def_code + "\n\nassert encode_cyclic(encode_cyclic('bca')) == 'abc'")
        exec(func_def_code + "\n\nassert encode_cyclic(encode_cyclic('ab')) == 'ab'")


def test_HumanEval_41_fix():
    # the original prompt doesn't have examples in the docstring
    # which causes inconsistency in the Data Set
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[41]["prompt"]
        assert ">>> car_race_collision" not in original_prompt

    # the fixed prompt has 1 example
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[41]["prompt"]
        assert ">>> car_race_collision(3)\n    9\n" in fixed_prompt

        # make sure the added example is correct
        solution = reader_list[41]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code + "\n\nassert car_race_collision(3) == 9")


def test_HumanEval_47_fix():
    # the original prompt has a wrong example, median([-10, 4, 6, 1000, 10, 20]) should be 8.0 instead of 15.0
    # also see https://github.com/openai/human-eval/issues/6
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[47]["prompt"]
        assert ">>> median([-10, 4, 6, 1000, 10, 20])\n    15.0\n" in original_prompt

    # the fixed prompt has the correct example
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[47]["prompt"]
        assert ">>> median([-10, 4, 6, 1000, 10, 20])\n    8.0\n" in fixed_prompt

        # make sure the added example is correct
        solution = reader_list[47]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code + "\n\nassert median([-10, 4, 6, 1000, 10, 20]) == 8.0")


def test_HumanEval_50_fix():
    # the original prompt doesn't have examples in the docstring
    # also the prompt is ambiguous in "encode_shift", not explicitly specifying lowercase or uppercase for input string
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[50]["prompt"]
        assert ">>> encode_shift" not in original_prompt

    # the fixed prompt has 1 exmaple in the docstring of decode_shift
    # we didn't add examples for encode_shift to maintain consistency with other tasks like 32 and 38
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[50]["prompt"]
        assert ">>> decode_shift('abc')\n    'vwx'\n" in fixed_prompt
        assert ">>> encode_shift" not in fixed_prompt

        # make sure the added example is correct
        solution = reader_list[50]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code + "\n\nassert decode_shift('abc') == 'vwx'")


def test_HumanEval_57_fix():
    # the original prompt is ambiguous, not explicitly specifying how to handle non-strictly increasing or decreasing input
    # also the prompt a typo in "Return True is list elements are monotonically increasing or decreasing."
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[57]["prompt"]
        assert "Return True is list elements are monotonically increasing or decreasing." in original_prompt

    # the fixed prompt is
    # "Return True if list elements are monotonically increasing or decreasing.
    # Still return True when list elements are non-strictly monotonically increasing or decreasing."
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[57]["prompt"]
        assert "Return True if list elements are monotonically increasing or decreasing." in fixed_prompt
        assert "Still return True when list elements are non-strictly monotonically increasing or decreasing." in fixed_prompt

        # make sure the function definition is correct
        solution = reader_list[57]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code + "\n\nassert monotonic([1, 2, 3]) is True")


def main():
    test_HumanEval_32_fix()
    test_HumanEval_38_fix()
    test_HumanEval_41_fix()
    test_HumanEval_47_fix()
    test_HumanEval_50_fix()


if __name__ == "__main__":
    main()
