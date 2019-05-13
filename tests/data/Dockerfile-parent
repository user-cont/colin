FROM scratch

ENV NAME=colin-labels-parent \
    VERSION=0.0.4

LABEL name="${NAME}" \
    summary="Colin image used for testing Dockerfile labels for parent" \
    maintainer="Petr Hracek <phracek@redhat.com>" \
    version="${VERSION}" \
    com.redhat.component="colin-labels" \
    description="The image contains labels which are used for testing colin functionality for parent." \
    io.k8s.description="The image contains labels which are used for testing colin functionality for parent." \
    run="docker run <application image>" \
    url="https://project.example.com/"

COPY files/usage /files/usage

CMD ["/files/usage"]
