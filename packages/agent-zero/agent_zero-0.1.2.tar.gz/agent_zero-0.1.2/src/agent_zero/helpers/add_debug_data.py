def add_debug_data(debug_data, debug_data_list):
    if isinstance(debug_data, list):
        for debug_item in debug_data:
            if isinstance(debug_item, dict):
                debug_item["step_id"] = len(debug_data_list) + 1
                debug_data_list.append(debug_item)
    elif isinstance(debug_data, dict):
        debug_data["step_id"] = len(debug_data_list) + 1
        debug_data_list.append(debug_data)