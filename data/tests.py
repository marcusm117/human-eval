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


def main():
    test_HumanEval_32_fix()


if __name__ == "__main__":
    main()
