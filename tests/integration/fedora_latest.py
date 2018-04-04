import colin

result = colin.run("fedora")
for r in result.all_results:
    print(r)
print(result.logs())
