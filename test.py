# from src.tools.cli_tools import run_str

# result = run_str("ping localhost")

# print(result)

result = "hei jeg sitter på kontoret"
expect = ["hei", "jeg", "kontoret"]

if all(item in result for item in expect):
    print("success")
else:
    print("error")