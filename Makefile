.PHONY: check build-test-container test-in-container exec-test

TEST_IMAGE_NAME = colin-test
TEST_TARGET = ./tests/integration/colin_tests.py

check: build-test-container test-in-container

build-test-container:
	docker build --network host --tag=$(TEST_IMAGE_NAME) -f ./Dockerfile.tests .

test-in-container: build-test-container
	@# use it like this: `make test-in-container TEST_TARGET=./tests/integration/test_utils.py`
	docker run --net=host --rm -v /dev:/dev:ro --security-opt label=disable --cap-add SYS_ADMIN -ti -v /var/run/docker.sock:/var/run/docker.sock:Z -v $(CURDIR):/src $(TEST_IMAGE_NAME) make exec-test TEST_TARGET=$(TEST_TARGET)

exec-test:
	PYTHONPATH=$(CURDIR) py.test-3 $(TEST_TARGET)

clean:
	python3 setup.py clean
	rm -rf build/* dist/*

html:
	make -f Makefile.docs html
