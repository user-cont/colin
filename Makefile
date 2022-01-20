.PHONY: check build-test-image test-in-container exec-test check-local check-code-style check-pylint check-bandit setup-ci

TEST_IMAGE_NAME := colin-test
TEST_TARGET = ./tests

check: build-test-image test-in-container

build-test-image:
	docker build --network host --tag=$(TEST_IMAGE_NAME) -f ./Dockerfile.tests .

test-in-container: build-test-image test-in-container-now

test-in-container-now:
	@# use it like this: `make test-in-container TEST_TARGET=./tests/integration/test_utils.py`
	docker run --rm --privileged --security-opt label=disable \
		--name=colin \
		--cap-add SYS_ADMIN -ti \
		-v /var/tmp/ \
		-v $(CURDIR):/src \
		$(TEST_IMAGE_NAME) \
		make exec-test TEST_TARGET="$(TEST_TARGET)"

test-in-ci: test-in-container

exec-test:
	PYTHONPATH=$(CURDIR) py.test-3 --cov=colin $(TEST_TARGET)

check-code-style: check-pylint check-bandit

check-pylint:
	pylint colin || true

clean:
	python3 setup.py clean
	rm -rf build/* dist/*
	git clean -fx

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

install: uninstall clean
	pip3 install --user .

uninstall:
	pip3 show colin && pip3 uninstall -y colin || true
	rm /usr/lib/python*/site-packages/colin\* -rf
