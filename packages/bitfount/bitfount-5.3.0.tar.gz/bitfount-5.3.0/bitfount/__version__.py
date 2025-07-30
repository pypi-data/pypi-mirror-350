"""Version information for `setup.py`."""

# ruff: noqa: E501
#   ____  _ _    __                   _
#  | __ )(_) |_ / _| ___  _   _ _ __ | |_
#  |  _ \| | __| |_ / _ \| | | | '_ \| __|
#  | |_) | | |_|  _| (_) | |_| | | | | |_
#  |____/|_|\__|_|  \___/ \__,_|_| |_|\__|
from __future__ import annotations

__author__ = "Bitfount"
__author_email__ = "info@bitfount.com"
__copyright__ = "Copyright 2021 Bitfount Ltd"
__description__ = "Machine Learning and Federated Learning Library."
__title__ = "bitfount"
__url__ = "https://github.com/bitfount/bitfount"
__version__ = "5.3.0"

# Legacy combined version list - maintained for backward compatibility
# YAML versions must be all on one line for the breaking changes script to work
__yaml_versions__ = ["2.0.0", "3.0.0", "4.0.0", "4.0.1", "4.1.0", "5.0.0", "6.0.0", "6.1.0", "6.2.0", "6.2.1", "6.3.0", "6.4.0", "6.5.0", "6.6.0"]  # fmt: off

# Role-specific version lists - starting fresh with 7.0.0
__modeller_yaml_versions__ = ["7.0.0", "7.1.0", "7.2.0", "7.3.0", "7.4.0", "7.5.0", "7.6.0", "7.7.0", "7.8.0"]  # fmt: off

# Use semver conventions for the YAML versions
# YAML Version Changes
__changelog__ = """
- 7.8.0:
    - Adds support for boolean as task template variables.
- 7.7.0:
  - Added InferenceAndImageOutput protocol
- 7.6.0:
  - Introduced new bscan image and mask generation algorithm.
- 7.5.0:
  - Add largest lesion upper size bound and patient age bounds to trial inclusion algorithms.
- 7.4.0:
   - Added post-processing to ModelInference Algorithm.
- 7.3.0:
  - Amethyst to use Amethyst Trial Calculation
  - Addition of Charcoal Trial Calculation
- 7.2.0:
  - Adding Image Source
- 7.1.0:
    Modeller:
        - Introduced new pre-filtering algorithm.
- 7.0.0:
  - Complete redesign of YAML versioning system
  - Introduced role-specific version lists (__pod_yaml_versions__ and __modeller_yaml_versions__)
  - Decoupled pod and modeller configuration schemas
  - Maintained backward compatibility with __yaml_versions__ for legacy code
  - Reset version numbering for role-specific schemas to provide a clean starting point
- 6.6.0:
  - Add specifications for datasource and datasplitter (kw)arg dictionaries,
    to provide tighter specification of these items.
  - Fix typing of "save path", etc., instances to correctly be specced as string/null
    rather than types inferred from fields.Function()
  - Fix Optional[Union[X, Y]] specs to correctly allow None/null
  - Change Union parsing to export to anyOf instead of oneOf, to better match
    the expected Marshmallow behaviour.
  - Fix issue with Union[dict[...],...] fields not being correctly written to
    the spec if they didn't contain enums.
  - Fix enum dicts to ensure they are valid JSON Schema components.
  - Introduce typing for template elements to ensure that those are also adhered to.
- 6.5.0:
  - Added NextGenSearchProtocol protocol
  - Fix incorrect args config for _SimpleCSVAlgorithm
- 6.4.0:
  - Added NextGenPatientQuery algorithm
"""
