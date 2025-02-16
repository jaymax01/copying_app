# Splitter function

def split_file(file_name, splitter='_'):

    if splitter not in file_name:
        return file_name.split(file_name[3])
    elif splitter in file_name:
        return file_name.split(splitter)
    else:
        return file_name.split('n')
    
# File ending extractor

def extract_file_ending(file_name=None):
    import re
    
    name = file_name
    reg_pattern = r"[a-z]+"
    pattern = re.compile(reg_pattern)
    pattern_match = pattern.search(name, 7, 10)
    
    return pattern_match.group()

# File ending column function

def add_file_ending_column(df=None):
    
    file_ending_list = []
    
    for x in df['файл']:
        try:
            temp = extract_file_ending(x)
            file_ending_list.append(temp)
        except:
            file_ending_list.append('')    
    df['File_ending'] = file_ending_list
    
    return df

# File name extraction function

def extract_filenames(seperator, df_column=None):
    
    file_list = []
    
    for i, k in zip(df_column['файл'], df_column['File_ending']):
        try:
            temp = split_file(i, seperator)[1]
            class_number = split_file(i, seperator)[0]
            if len(temp) <= 4:
               file = class_number + seperator + temp
            elif len(temp) > 4 and len(k) == 1:
               file = class_number + seperator + temp[:len(temp)-1]
            else:
               file = class_number + seperator + temp[:len(temp)-2]
            file_list.append(file)
        except:
            continue
        
    return file_list

# Folder creation function

def make_folder(dest_path=None):
    from pathlib import Path
    directory_name = Path(dest_path)
    directory_name.mkdir(parents=True, exist_ok=True)


# Magnit format ending extractor

def magnit_renamer(format, filename, order_no):
    
    if '-2' in format:
        return order_no + filename + '-1'
    elif '-3' in format or '-4' in format:
        return '_' + order_no + filename + '-2'
    else:
        return order_no + filename + '-1'
    
# Non magnit format ending extractor

def non_magnit_renamer(format, filename, order_no):

    for i in range(2, 7):
        if format == '15x21-2':
            return order_no + filename + '-2'
        elif '-'+ str(i) in format:
            return '_' + order_no + filename + '-'+ str(i)
    return order_no + filename + '-1'


# Count number of files in a directory

def file_count(dir_path):
    import os
    return sum([len(file) for _, _, file in os.walk(dir_path)])