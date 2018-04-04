import colin

result = colin.run("colin-test")

def test_colin_test_latest():
    assert result.all_results

def test_colin_test_maintainer():
    for res in result._dict_of_results['labels']:
        assert res['name']
        assert res['name'] == 'maintainer_label_required'
        assert res['status'] == 'failed'
