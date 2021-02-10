"""
Test different target types.
"""

import pytest

import colin
from tests.conftest import (
    LABELS_IMAGE,
    convert_image_to_oci,
    get_skopeo_oci_target,
)


@pytest.fixture()
def ruleset():
    """ simple ruleset as a pytest fixture """
    return {
        "version": "1",
        "name": "Laughing out loud ruleset",
        "description": "This set of checks is required to pass because we said it",
        "contact_email": "forgot-to-reply@example.nope",
        "checks": [
            {
                "name": "com.redhat.component_label",
            },
            {
                "name": "name_label",
            },
            {
                "name": "version_label",
            },
            {
                "name": "description_label",
            },
            {
                "name": "io.k8s.description_label",
            },
            {
                "name": "vcs-ref_label",
            },
            {
                "name": "vcs-type_label",
            },
            {
                "name": "architecture_label",
            },
            {
                "name": "com.redhat.build-host_label",
            },
            {
                "name": "authoritative_source-url_label",
            },
            {
                "name": "vendor_label",
            },
            {
                "name": "release_label",
            },
            {"name": "url_label", "usable_targets": ["image"]},
            {
                "name": "build-date_label",
            },
            {
                "name": "distribution-scope_label",
            },
            {
                "name": "run_or_usage_label",
            },
            {
                "name": "help_file_or_readme",
            },
            {
                "name": "maintainer_label",
            },
            {
                "name": "summary_label",
            },
            {
                "name": "install_label_capital_deprecated",
            },
            {
                "name": "architecture_label_capital_deprecated",
            },
            {
                "name": "bzcomponent_deprecated",
            },
            {
                "name": "name_label_capital_deprecated",
            },
            {
                "name": "release_label_capital_deprecated",
            },
            {
                "name": "uninstall_label_capital_deprecated",
            },
            {
                "name": "version_label_capital_deprecated",
            },
        ],
    }


def test_podman_image_target(ruleset):
    results = colin.run(
        LABELS_IMAGE, "image", ruleset=ruleset, logging_level=10, pull=False
    )
    assert results.ok
    assert results.results_per_check["url_label"].ok


def test_oci_target(ruleset):
    image_name = "colin-labels"
    oci_path = convert_image_to_oci(image_name=image_name)
    skopeo_target = get_skopeo_oci_target(image_name=image_name, oci_path=oci_path)
    results = colin.run(
        skopeo_target, "oci", ruleset=ruleset, logging_level=10, pull=False
    )
    assert results.ok
    assert results.results_per_check["url_label"].ok
