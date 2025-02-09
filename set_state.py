# TODO

"""
entity_id: todo
allow_create: todo
state: todo

example usage:

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


if input_state_object is not None:
    input_state = input_state_object.state
    input_attributes_object = input_state_object.attributes.copy()
else:
    input_attributes_object = {}

for item in data:
    new_attribute = data.get(item)
    logger.warning(f"item = {item} / value = {new_attribute}"
    )

    if item in ["file", "allow_create", "entity_id", "cache"]:
        continue  # already handled
    elif item == "state":
        input_state = new_attribute
    else:
        input_attributes_object[item] = new_attribute

hass.states.set(input_entity, input_state, input_attributes_object)
