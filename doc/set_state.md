# Home Assistant Python Script: set_state.py

This Python script allows dynamically setting the state and attributes of an entity in Home Assistant. It can be used to modify existing entities or create new ones if `allow_create` is set to `true`.

## Requirements
This script requires:
- [PythonScriptsPro](https://github.com/AlexxIT/PythonScriptsPro) - A Home Assistant integration that extends the functionality of Python scripts, enabling file operations and better script execution.

## Features
- Modify the state of an existing Home Assistant entity.
- Add or update attributes for the specified entity.
- Optionally create a new entity if it does not exist.

## Parameters

| Parameter        | Type    | Required | Description                                                                             |
|------------------|---------|----------|-----------------------------------------------------------------------------------------|
| `entity_id`      | string  | ✅ True   | The entity ID whose state and attributes need to be updated.                            |
| `allow_create`   | boolean | ❌ False  | If `true`, allows setting a new entity if it doesn't exist. Defaults to `false`.        |
| `state`          | string  | ❌ False  | The new state to be assigned to the entity. If omitted, the current state is preserved. |
| Other attributes | any     | ❌ False  | Additional key-value pairs will be added as attributes to the entity.                   |

## Example Usage

### Set Light State and Brightness
```yaml
action: python_script.exec
data:
  entity_id: light.pantry_light
  state: 'on'
  brightness: 255
  file: /config/python_scripts/set_state.py
```

### Set Sensor Value
```yaml
action: python_script.exec
data:
  entity_id: sensor.hour
  state: '14'
  file: /config/python_scripts/set_state.py
```

## Installation
1. Copy the script to the `python_scripts` directory in your Home Assistant configuration folder.
2. Ensure `python_script:` is enabled in your `configuration.yaml`.
3. Reload Home Assistant or restart the system.

---

