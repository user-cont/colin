import colin

result = colin.run("image")
assert result.ok
assert result.status == "passed"
print(result.logs())
