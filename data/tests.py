# The tests can be run as a Script, use the Command "python tests.py",
# alternatively, they can be run as a Module using pytest
# If you wish to use pytest, you can install it by "pip3 install pytest",
# uncomment the import pytest line below, and use the Command "python -m pytest -v tests.py"

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


def test_HumanEval_38_fix():
    # the original prompt doesn't have examples in the docstring
    # which causes inconsistency in the Data Set
    with jsonlines.open("human-eval-v2-20210705.jsonl") as reader:
        reader_list = list(reader)
        original_prompt = reader_list[38]["prompt"]
        assert ">>> encode_cyclic" not in original_prompt
        assert ">>> decode_cyclic" not in original_prompt

    # the fixed prompt has 2 examples each for encode_cyclic and decode_cyclic
    with jsonlines.open("human-eval-enhanced-202305.jsonl") as reader:
        reader_list = list(reader)
        fixed_prompt = reader_list[38]["prompt"]
        assert ">>> encode_cyclic('abc')\n    'bca'\n" in fixed_prompt
        assert ">>> encode_cyclic('ab')\n    'ab'\n" in fixed_prompt
        assert ">>> decode_cyclic('bca')\n    'abc'\n" in fixed_prompt
        assert ">>> decode_cyclic('ab')\n    'ab'\n" in fixed_prompt

        # make sure the added examples are correct
        solution = reader_list[38]["canonical_solution"]
        func_def_code = fixed_prompt + solution
        exec(func_def_code + "\n\nassert encode_cyclic('abc') == 'bca'")
        exec(func_def_code + "\n\nassert encode_cyclic('ab') == 'ab'")

        # decode_cyclic(string) is equivalent to encode_cyclic(encode_cyclics(string))
        exec(func_def_code + "\n\nassert encode_cyclic(encode_cyclic('bca')) == 'abc'")
        exec(func_def_code + "\n\nassert encode_cyclic(encode_cyclic('ab')) == 'ab'")


def main():
    test_HumanEval_32_fix()
    test_HumanEval_38_fix()


if __name__ == "__main__":
    main()
