import colin


def get_colin_test_image():
    return colin.run("colin-test")


def test_colin_test_latest():
    assert get_colin_test_image()

def test_colin_test_maintainer():
    result = get_colin_test_image()
    for res in result._dict_of_results['labels']:
        assert res['name']
        assert res['name'] == 'maintainer_label_required'
        assert res['status'] == 'failed'
