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
This script allows dynamically setting the state and attributes of an entity
in Home Assistant. It can be used to modify existing entities or create
new ones if `allow_create` is set to `true`.

Parameters:
    entity_id (str): The entity ID whose state and attributes need to be
        updated. Required.
    allow_create (bool, optional): If `true`, allows setting a new entity
        if it doesn't exist. Defaults to `false`.
    state (str, optional): The new state to be assigned to the entity.
        If omitted, the current state is preserved.

Example usage:
action: python_script.exec
data:
  entity_id: light.pantry_light
  state: 'on'
  brightness: 255
  file: /config/python_scripts/set_state.py

action: python_script.exec
data:
  entity_id: sensor.hour
  state: '14'
  file: /config/python_scripts/set_state.py

"""

input_entity = data.get("entity_id")

if not input_entity:
    raise ValueError("entity_id is required if you want to set something.")

# Retrieve the current state
input_state_object = hass.states.get(input_entity)

if input_state_object is None and not data.get("allow_create"):
    raise ValueError(f"Unknown entity_id: {input_entity}")

# Initialize state and attributes
input_state = input_state_object.state if input_state_object else None
input_attributes_object = input_state_object.attributes.copy() if input_state_object else {}

for item, attribute_value in data.items():
    if item in ["file", "allow_create", "entity_id", "cache"]:
        continue  # Skip already handled items

    elif item == "state":
        input_state = attribute_value
    else:
        input_attributes_object[item] = attribute_value

hass.states.set(input_entity, input_state, input_attributes_object)
