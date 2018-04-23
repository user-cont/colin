.PHONY: check build-test-container test-in-container exec-test check-local check-labels

TEST_IMAGE_NAME := colin-test
TEST_IMAGE_LABELS_NAME := colin-labels
TEST_TARGET = ./tests/integration/
RESULTS := colin.json
CONFIG := fedora
ARTIFACTS_DIR := ./artifacts

check: build-test-container build-labels-container test-in-container

build-test-container:
	docker build --network host --tag=$(TEST_IMAGE_NAME) -f ./Dockerfile.tests .

build-labels-container:
	cd tests/data && docker build --tag=$(TEST_IMAGE_LABELS_NAME) .

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

sdist:
	./setup.py sdist -d .

rpm: sdist
	rpmbuild ./*.spec -bb --define "_sourcedir $(CURDIR)" --define "_specdir $(CURDIR)" --define "_buildir $(CURDIR)" --define "_srcrpmdir $(CURDIR)" --define "_rpmdir $(CURDIR)"

srpm: sdist
	rpmbuild ./*.spec -bs --define "_sourcedir $(CURDIR)" --define "_specdir $(CURDIR)" --define "_buildir $(CURDIR)" --define "_srcrpmdir $(CURDIR)" --define "_rpmdir $(CURDIR)"

rpm-in-mock-f27: srpm
	mock --rebuild -r fedora-27-x86_64 ./*.src.rpm

rpm-in-mock-el7: srpm
	mock --rebuild -r epel-7-x86_64 ./*.src.rpm

check-local:
	ansible-playbook $(ANSIBLE_EXTRA_ARGS) -e config=$(CONFIG) -e subject=$(TEST_IMAGE_NAME) -e results=$(RESULTS) -e artifacts_dir=$(ARTIFACTS_DIR) ./local.yml -e setup=true

clean:
	git clean -dfx

install: clean
	pip install --user .

uninstall:
	pip uninstall .
	rm /usr/lib/python*/site-packages/colin\* -rf
