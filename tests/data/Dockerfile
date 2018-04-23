FROM registry.fedoraproject.org/fedora:27

ENV NAME="colin-labels" \
    VERSION="0.0.3"

ENV SUMMARY="Colin image used for testing Dockerfile labels" \
    DESCRIPTION="The image contains labels which are used for testing colin functionality."

LABEL maintainer="Petr Hracek <phracek@redhat.com>" \
    summary="${SUMMARY}" \
    version="${VERSION}" \
    com.redhat.component="${NAME}" \
    description="${DESCRIPTION}" \
    io.k8s.description="${DESCRIPTION}" \
    io.openshift.tags="${NAME}

COPY ./files/usage /files/usage

CMD ["/files/usage"]