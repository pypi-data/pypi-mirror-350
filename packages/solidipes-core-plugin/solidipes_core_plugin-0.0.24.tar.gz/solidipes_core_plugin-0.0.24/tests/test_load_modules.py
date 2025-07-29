import importlib
import pkgutil

import pytest

PACKAGE_NAME = "solidipes_core_plugin"
SUBPACKAGE_NAMES = ["downloaders", "loaders", "mounters", "reports", "scanners", "uploaders", "validators", "viewers"]


module_paths = []


for subpackage_name in SUBPACKAGE_NAMES:
    try:
        subpackage = importlib.import_module(f"{PACKAGE_NAME}.{subpackage_name}")

    except ImportError:
        continue

    new_module_paths = [
        f"{subpackage_name}.{module.name}"
        for module in pkgutil.iter_modules(subpackage.__path__)
        if module.ispkg is False
    ]

    module_paths.extend(new_module_paths)


@pytest.mark.parametrize("module_path", module_paths)
def test_load_module(
    module_path: str,
) -> None:
    """Test that each module can be imported."""

    module = importlib.import_module(f"{PACKAGE_NAME}.{module_path}")
    assert module is not None
