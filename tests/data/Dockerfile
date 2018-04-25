FROM registry.fedoraproject.org/fedora:27

ENV NAME=colin-labels \
    VERSION=0.0.3

LABEL name="${NAME}" \
    summary="Colin image used for testing Dockerfile labels" \
    maintainer="Petr Hracek <phracek@redhat.com>" \
    version="${VERSION}" \
    com.redhat.component="colin-labels" \
    description="The image contains labels which are used for testing colin functionality." \
    io.k8s.description="The image contains labels which are used for testing colin functionality."

COPY ./files/usage /files/usage

CMD ["/files/usage"]