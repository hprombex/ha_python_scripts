# Copyright (c) 2025 hprombex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#
# Author: hprombex

"""
Home Assistant Python Script to save and restore entity last_changed status.

Parameters:
    action (str): 'save' or 'restore'.
    states_location (str): File path for saving/restoring states, default: /config/python_scripts.
    entities (str): Comma-separated entity IDs to save/restore.
                     Use 'all' to save all entities.
                     Use wildcard '*' to match multiple entities (e.g., binary_sensor.pir_*, binary_sensor.pir_*_occupancy).
"""

import os
import json
import fnmatch
from datetime import datetime as dt

dump_json_dict = {}

action = data.get("action", "save").lower()  # Expected values: 'save' or 'restore'

# Define the location of the JSON file to store entity states
entity_states_location = data.get("states_location", "/config/python_scripts")
entity_states_json_file = os.path.join(
    entity_states_location, "entity_states.json"
)

# Retrieve entities to process
entities = data.get("entities", "")  # eg.: binary_sensor.sms_host,switch.switch_test


def expand_wildcard(entity_pattern: str) -> list[str]:
    """
    Expands entity pattern with '*' wildcard to match multiple entities.

    :param entity_pattern: Entity ID pattern, which may contain '*' as a wildcard.
    :return: A list of matching entity IDs from Home Assistant state objects.
    """
    matched_entities = [
        e.entity_id for e in hass.states.all() if
        fnmatch.fnmatch(e.entity_id, entity_pattern)
    ]
    return matched_entities if matched_entities else []  # Return the empty list if no matches found


if action == "save":
    if entities.lower() == "all":
        entities_ids = [e.entity_id for e in hass.states.all()]
    else:
        entities_ids = []
        for entity in entities.split(","):
            if "*" in entity:
                entities_ids.extend(expand_wildcard(entity))
            else:
                entities_ids.append(entity)

    if not entities_ids:
        raise ValueError("No entities found to save.")

    for entity_id in entities_ids:
        entity_state_object = hass.states.get(entity_id)
        if entity_state_object:
            dump_json_dict[entity_id] = str(entity_state_object.last_changed)

    with open(entity_states_json_file, "w", encoding="utf-8") as json_file:
        json.dump(dump_json_dict, json_file, indent=4)

elif action == "restore":
    try:
        with open(entity_states_json_file, "r") as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"State file {entity_states_json_file} not found."
        )

    entities_ids = []
    for entity in entities.split(","):
        if "*" in entity:
            entities_ids.extend(expand_wildcard(entity))
        else:
            entities_ids.append(entity)

    for entity_id in entities_ids:
        entity_last_changed = json_data.get(entity_id)
        if not entity_last_changed:
            logger.warning(f"Entity {entity_id} not found in saved states.")
            continue

        entity_state_object = hass.states.get(entity_id)
        entity_state_object.last_changed = dt.strptime(
            entity_last_changed, "%Y-%m-%d %H:%M:%S.%f%z"
        )  # convert to datetime.datetime
else:
    raise ValueError("Invalid action specified. Use 'save' or 'restore'.")
