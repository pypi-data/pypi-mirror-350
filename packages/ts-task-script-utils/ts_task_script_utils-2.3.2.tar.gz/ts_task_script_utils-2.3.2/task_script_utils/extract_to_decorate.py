"""
Derived from extract-to-decorate function from ts-task-script-file-util
"""

from __future__ import annotations

import re
from typing import Callable, Dict, List

import pydash


def process_metadata(function: Callable, metadata: Dict[str, any]) -> Dict[str, any]:
    """
    Applies a function to all values in a metadata object.
    :param function: a function that can be applied to a string
    :param metadata: an object of the following structure
        {
            "key": "value 1",
            "key2": "value 2",
        }
    """
    # Return nothing given
    if metadata:
        return {key: function(value) for key, value in metadata.items()}
    return metadata


def process_tags(function: Callable, tags: List) -> List:
    """
    Applies a function to all values in a tags list.
    :param function: a function that can be applied to a string
    :param tags: a list of stings
    """
    if tags:
        return [function(tag) for tag in tags]
    return tags


def process_labels(function: Callable, labels: List) -> List:
    """
    Applies a function to all values in a labels object.
    :param function: a function that can be applied to a string
    :param labels: a list of objects with the following structure
        [
            {
                "name": "key1",
                "value": "value 1"
            },
            {
                "name": "key2",
                "value": "value 2"
            }
        ]
    """
    if labels:
        return [
            {
                key: (function(value) if key == "value" else value)
                for key, value in label.items()
            }
            for label in labels
        ]
    return labels


def sanitize_output(text: str) -> str:
    """
    Removes characters that will cause pipeline errors if in metadata.
    Currently, the Regex for metadata values is ^[0-9a-zA-Z-_+.,/ ]+$
    Replaces with whitespace, then reduces multiple adjoining whitespace to single
    """
    illegal_char_regex = re.compile(r"[^0-9a-zA-Z-_+.,/ ]")

    replaced_text = illegal_char_regex.sub(" ", text)

    # Remove multiple adjoining spaces
    # (e.g. "A & B" becomes "A B" instead of "A   B")
    return " ".join([t for t in replaced_text.split(" ") if t != ""])


def do_mapping_extraction(
    mappings: List[Dict[str, any]], source_value: str, logger: Callable, flags=0
):
    """
    Iterates through the mapping list and conducts the regex search over the source string.

    :param mappings: (list, required) a list of dictionaries
            [
                {
                    "example": "/data/raw/Attune/EXP22000214/2022-08-12 vb serp test_experiment_6b5 hep 10k_a9.fcs",
                    "source": "fileKey",
                    "pattern": ".*(exp[0-9]{8})",
                    "targets": [{"type": "metadata", "name": "benchling_entry_id"}],
                }
            ]
    :param source_value: (str, required) string to search
    :param logger: (function, required) Logger function
    :param flags: (RegexFlag, optional) flag options to include in re.search, e.g. re.IGNORECASE
    """
    metadata = {}
    tags = []
    labels = []

    for mapping in mappings:
        pattern = mapping["pattern"]
        logger({"message": f"Using pattern: {pattern}", "level": "info"})

        match = re.search(pattern, source_value, flags)
        if match:
            targets = mapping["targets"]
            match_groups = match.groups()
            assert len(targets) <= len(match_groups), (
                f"Number of targets {len(targets)} should not exceed "
                f"number of matched groups {len(match_groups)}"
            )

            for target, value in zip(targets, match_groups):
                assert target["type"] in [
                    "metadata",
                    "tag",
                    "label",
                ], "Allowed target types are 'metadata', 'tag', 'label'"

                target_name = target.get("name")
                if target["type"] in ["metadata", "label"]:
                    assert target_name is not None, (
                        f"The target type {target['type']} requires a non-null "
                        f"'name' field"
                    )

                if target["type"] == "metadata":
                    if "value" in target:
                        metadata[target_name] = target["value"]
                        continue
                    metadata[target_name] = value

                elif target["type"] == "label":
                    if "value" in target:
                        labels.append({"name": target_name, "value": target["value"]})
                        continue
                    labels.append({"name": target_name, "value": value})

                elif target["type"] == "tag":
                    if "value" in target:
                        tags.append(target["value"])
                        continue
                    tags.append(value)

            logger(
                {
                    "message": f"Matched {pattern} and stopped iterating through patterns.",
                    "level": "info",
                }
            )
            break
        else:
            logger(
                {"message": f"Failed the extraction with {pattern}", "level": "info"}
            )

    return (
        metadata,
        pydash.uniq(tags),
        pydash.uniq_by(labels, lambda l: f"{l['name']}@{l['value']}"),
    )


# pylint: disable=too-many-arguments
def extract_to_decorate(
    mappings: List[Dict[str, any]],
    source_value: str,
    re_flags=0,
    sanitize=False,
    title_case=False,
    logger: Callable = print,
):
    """
    This function uses a user-defined regex pattern search to extract metadata, tags and labels from a filename

    :param mappings: (list, required) a list of dictionaries
            [
                {
                    "example": "/data/raw/Attune/EXP22000214/2022-08-12 vb serp test_experiment_6b5 hep 10k_a9.fcs",
                    "source": "fileKey",
                    "pattern": ".*(exp[0-9]{8})",
                    "targets": [{"type": "metadata", "name": "benchling_entry_id"}],
                }
            ]
    :param source_value: (str, required) string to search
    :param re_flags: (RegexFlag, optional) flag options to include in re.search, e.g. re.IGNORECASE
    :param sanitize: (bool, optional) Removes characters that will cause pipeline errors if in metadata
    :param title_case: (bool, optional) Transforms MTL values to title case
    :param logger: (function, optional) Logger function
    """
    # extract mappings
    metadata, tags, labels = do_mapping_extraction(
        mappings, source_value, logger, re_flags
    )

    if sanitize:
        metadata = process_metadata(sanitize_output, metadata)
        tags = process_tags(sanitize_output, tags)
        labels = process_labels(sanitize_output, labels)

    if title_case:
        norm_func = str.title

        metadata = process_metadata(norm_func, metadata)
        tags = process_tags(norm_func, tags)
        labels = process_labels(norm_func, labels)

    logger({"message": f"Metadata: {metadata}", "level": "info"})
    logger({"message": f"Tags: {tags}", "level": "info"})
    logger({"message": f"Labels: {labels}", "level": "info"})

    if not (metadata or tags or labels):
        logger({"message": "Metadata, tags and labels are empty!", "level": "error"})

    return {"metadata": metadata, "tags": tags, "labels": labels}
