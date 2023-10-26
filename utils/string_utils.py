def extract_value_in_brackets(input_string):  # извлекает название группы из []
    start_index = input_string.find('[')
    end_index = input_string.find(']')

    if start_index != -1 and end_index != -1 and start_index < end_index:
        value_in_brackets = input_string[start_index + 1:end_index]
        return value_in_brackets
    else:
        return None
