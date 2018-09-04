import colin

result = colin.run(target="my-image",
                   target_type="image")

assert result.ok
print(result.results)
print(result.get_pretty_string(stat=True,
                               verbose=True))
print(result.json())
