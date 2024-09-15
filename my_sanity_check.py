import pandas as pd
import re
import os

entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'maximum_weight_recommendation': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre',
        'cubic foot',
        'cubic inch',
        'cup',
        'decilitre',
        'fluid ounce',
        'gallon',
        'imperial gallon',
        'litre',
        'microlitre',
        'millilitre',
        'pint',
        'quart'}
}

allowed_units = {unit for entity in entity_unit_map for unit in entity_unit_map[entity]}



##Wrong-True key value dictionary
wrong_true_dict = {
    'pounds': 'pound',
    'ter': 'tre',
    'feet': 'foot',
    'inches': 'inch',
    'mm': 'millimetre',
    'cm': 'centimetre',
    'ounces': 'ounce',
    'ml': 'millilitre',
    'millimeters': 'millilitre',
    'meters': 'metre',
    'V': 'volt',
    'v': 'volt',
    'volts': 'volt',
    'watts': 'watt',
    'grams': 'gram',
    'volts': 'volt',
    'VAC': 'volt',
    'lb': 'pound',
    'lbs': 'pound',
    'kg': 'kilogram',
    'amps': 'null',
    'cc': 'null',
    'fl': 'fluid ounce',
    'microns': 'null',
    'oz': 'ounce',
    'ft': 'foot',
    'in': 'inch',
    'g': 'gram',
    'mg': 'milligram',
    'ug': 'microgram',
    'cans': 'null',
    'pixels': 'inch',
    'W': 'watt',
    'x': 'null',
    'liters': 'litre',
    'RPM': 'null',
    'gallons': 'gallon',
    'BTU': 'null',
    'packs': 'null'
}


def common_mistake(unit):
    # First, check if the unit is directly in allowed_units
    if unit in allowed_units:
        return unit
    
    # Check for common mistakes and replacements based on the wrong_true_dict
    for wrong, correct in wrong_true_dict.items():
        # print(f'wrong is: {wrong}, and unit is: {unit}')
        if wrong == unit:
            # corrected_unit = unit.replace(wrong, correct)
            corrected_unit = correct
            # if corrected_unit in allowed_units:
            return corrected_unit

    # If no correction is found, return the original unit
    return unit


def insert_space_between_number_and_letters(s):
    # Regular expression to match a number followed directly by letters
    pattern = re.compile(r'(\d+(\.\d+)?)([a-zA-Z])')
    
    # Replace the matched pattern with number followed by a space and the letters
    return pattern.sub(r'\1 \3', s)

### Here is the main code 
info_file = "info.txt"

# Read the content of the text file
with open(info_file, 'r') as file:
    lines = file.readlines()

# Extract the values
start_index = int(lines[0].strip())  # First value is the last_index where unit not matched
file_path = lines[1].strip()  # Second line is raw csv file
output_file_path = lines[2].strip()  # Third line is post_processed csv file


output_df = pd.read_csv(file_path)

collected_data = []

# Iterating through the DataFrame
for i, record in output_df.iloc[start_index:].iterrows():
    try:
        s = record['prediction']
        index = record['index']
        image_link = record['image_link']
        
        # Stripping and validating the prediction
        s_stripped = "" if s is None or str(s) == 'nan' else s.strip()
        if s_stripped == "":
            continue
        
        # Regex to match the format 'number unit'
        pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
        s_stripped = insert_space_between_number_and_letters(s_stripped)
    
        if not pattern.match(s_stripped):
            collected_data.append({
                'index': index,
                'image_link': image_link,
                'prediction': f""
            })
            continue
            # raise ValueError(f"Invalid format in {s}, at index {index}")
        
        # Split the string into number and unit
        parts = s_stripped.split(maxsplit=1)
        number = float(parts[0])
        unit = common_mistake(parts[1])
        # print(f"number: {number}, and unit: {unit}")
        if unit == 'null':
            collected_data.append({
                'index': index,
                'image_link': image_link,
                'prediction': f""
            })
            continue

        # Check if the rectified unit is in allowed_units
        if unit not in allowed_units:
            raise ValueError(f"Invalid unit [{unit}] found in {s_stripped} at index {index}. Allowed units: {allowed_units}")
        
        # Append valid data to the list
        collected_data.append({
            'index': index,
            'image_link': image_link,
            'prediction': f"{number} {unit}"
        })
    
    except ValueError as ve:
        print(f"Error: {ve}. Saving collected data...")
        # Creating a DataFrame from the collected data
        old_df = pd.read_csv(output_file_path)
        collected_df = pd.DataFrame(collected_data)
        collected_df = pd.concat([old_df, collected_df], ignore_index=False)
        if collected_df.empty:
            start = 0
            end = 0
        else:
            start = collected_df.iloc[0]['index']
            end = collected_df.iloc[-1]['index']
        new_file_name = f'Test_out/post_processed/test_out-{start}-{end}.csv'
        collected_df.to_csv(new_file_name, index=False)
        if new_file_name != output_file_path:
            os.remove(output_file_path)
        with open(info_file, 'w') as file:
            file.write(f"{i}\n")
            file.write(f"{file_path}\n")
            file.write(f"{new_file_name}\n")
        break

# If no error occurred and all rows are processed, save the data
else:
    old_df = pd.read_csv(output_file_path)
    collected_df = pd.DataFrame(collected_data)
    collected_df = pd.concat([old_df, collected_df], ignore_index=False)
    if collected_df.empty:
        start = 0
        end = 0
    else:
        start = collected_df.iloc[0]['index']
        end = collected_df.iloc[-1]['index']
    new_file_name = f'Test_out/post_processed/test_out-{start}-{end}.csv'
    collected_df.to_csv(new_file_name, index=False)
    if new_file_name != output_file_path:
        os.remove(output_file_path)
    with open(info_file, 'w') as file:
        file.write(f"{i}\n")
        file.write(f"{file_path}\n")
        file.write(f"{new_file_name}\n")
    print("All data processed and saved successfully.")