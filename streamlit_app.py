import pandas as pd
import shutil
import os
from pathlib import Path
import streamlit as st
import functions_ed as func


st.image('title copy app.png', width=400)
st.write('Please remove QUOTATION MARKS " " from your files')
st.write("")

add_selectbox = st.sidebar.selectbox('What stage do you want to complete', ['1. Copy files', '2. Sort by size', '3. Rename chrome', '4. Final rename', '5. Album - Copy All', '6. Album - Copy By Name'])

if add_selectbox == '1. Copy files':
    
    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    source_path = st.text_input("Please copy and paste the location of the MAIN file", "")
    path_name = st.text_input("Please enter the location where you want to copy the files", "")
    
    if not file_source or not source_path or not path_name:
        st.stop()        
    else:
        pic_list = pd.read_excel(file_source)
        st.write('Here is your files excel folder')
        st.dataframe(pic_list)
        st.write('The table has {} rows and {} columns'.format(pic_list.shape[0], pic_list.shape[1]))
        func.add_file_ending_column(pic_list)

        file_names = []
        not_a_pic = []

        for dirpaths, dirnames, filenames in os.walk(source_path):
                for file in filenames:
                    file_names.append(file)

        for i, k in zip(pic_list['файл'], pic_list['File_ending']):
            
            if len(i) < 8 or k == '':
                file = i + '.JPG'
            elif len(i) > 7 and len(k) == 1:
                file = i[:len(i)-1] + '.JPG'
            else:
                file =  i[:len(i)-2] + '.JPG'
                
            if file not in file_names:
                not_a_pic.append(file)
                
        st.write('These files are not found in the folder')
        st.dataframe(not_a_pic)
        # for pic in not_a_pic:
        #     st.write(pic)

        # answer = st.text_input('Would you like to drop these files from the excel table?')
        # if not answer:
        #     st.stop()
        # elif answer.lower() == 'yes':
        #     not_pic_indexes = []
        #     for i in not_a_pic:
        #         temp = i.strip('.JPG')
        #         index = list(pic_list['файл']).index(temp)
        #         not_pic_indexes.append(index)
        #     pic_list.drop(labels=not_pic_indexes, axis=0, inplace=True)
            
        
        func.make_folder(path_name)
        
        # class_number = st.text_input('Please enter the file class number')
        seperator = st.text_input('Please enter the seperator between class and file number')


        # copied_files = []
        # duplicated_files = []
        copied_files = 0
        if st.button("Copy files", type="primary"):

            with st.spinner("Copying files...."):
                            
                for (dirpaths, dirnames, filenames) in os.walk(source_path):
            
                    for i, j, k in zip(pic_list['файл'], pic_list['формат'], pic_list['File_ending']):
                    
                        dest_path = path_name
                        
                        try:
                            temp = func.split_file(i, seperator)[1]
                            class_number = func.split_file(i, seperator)[0]
                            if len(temp) <= 4:
                                file = class_number + seperator + temp + '.JPG'
                            elif len(temp) > 4 and len(k) == 1:
                                file = class_number + seperator + temp[:len(temp)-1] + '.JPG'
                            else:
                                file = class_number + seperator + temp[:len(temp)-2] + '.JPG'
                        except:
                            continue
                        
                        file = file.strip()    
                        source_path = os.path.join(dirpaths, file)
                        if os.path.isfile(source_path):
                            shutil.copy(src=source_path, dst=dest_path)
                            copied_files+=1
                            # copied = os.path.basename(source_path.strip('.JPG'))
                            # file_ending  = func.extract_file_ending(copied)
                            # copied = copied + k                            
                            # if copied not in copied_files:
                            #     copied_files.append(copied)
                            # else:
                            #     duplicated_files.append(copied)

            st.success('Done !')                            
            st.write('{} unique files were copied to {}'.format(copied_files, path_name))

            num_files = func.extract_filenames(seperator, df_column=pic_list)
            df_files = pic_list.copy()
            df_files['файл'] = num_files
            dup_files = df_files[df_files['файл'].duplicated()].sort_values(by='File_ending')
            dup_files['файл'] += dup_files['File_ending']
            st.write('Here are your duplicated files')
            st.dataframe(dup_files)

            st.write('There are {} listed files'.format(len(pic_list)))
            st.write('There are {} duplicated files'.format(dup_files.shape[0]))
            st.write('There are {} non duplicated files'.format(len(pic_list) - dup_files.shape[0]))
            copied = copied_files - dup_files.shape[0]           
            st.write('{} files were copied'.format(copied))
            
            # st.write('Here are your duplicated files')
            # st.dataframe(list(set(duplicated_files)))
            # st.write('There are {} listed files'.format(len(pic_list)))
            # st.write('There are {} duplicated files'.format(len(duplicated_files)))
            # st.write('There are {} non duplicated files'.format(len(pic_list) - len(set(duplicated_files))))
            # st.write('{} files were copied'.format(len(copied_files)))


if add_selectbox == '2. Sort by size':

    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    path_name = st.text_input("Please enter the location of your files", "")

    if not file_source or not path_name:
        st.stop()
        st.success('Thanks for entering file locations')
    else:
        df_copied_files = pd.read_excel(file_source)
        st.write('Here is your files excel folder')
        st.dataframe(df_copied_files)
        st.write('The table has {} rows and {} columns'.format(df_copied_files.shape[0], df_copied_files.shape[1]))
        func.add_file_ending_column(df_copied_files)
        
        size_rank_dict = {
            'наклейка': 1,
            'наклейка-2': 1,
            'магнит': 2,
            'магнит-2': 2,
            'магнит-3': 2,
            'магнит-4': 2,
            '10x15': 3,
            '10x15-2': 3,
            '10x15-3': 3,
            '10x15-4': 3,
            '10x15-5': 3,
            '10x15-6': 3,
            '15x21': 4,
            '15x21-2': 4,
            '15x21-3': 4,
            '15x21-4': 4,
            '15x21-5': 4,
            '15x21-6': 4,
            'блок3': 4, 
            'блок5': 4,
            'блок3-2': 4,
            '21x30': 5,
            '21x30-2': 5,
            '21x30-3': 5,
            '21x30-4': 5,
            'File': 6,
            'File-2': 6,
            'File-3': 6,
            'File-4': 6,
            '30x45': 7,
            '30x45-2': 7
            }

        df_copied_files['Format_rank'] = df_copied_files['формат'].map(size_rank_dict)

        folder_list = ['_10x15', '10x15', '10x15-2', '15x21', '21x30', 'File', '30x45', 'магнит', 'наклейка']

        for folder in folder_list:
            path_names = path_name+'/'+folder
            func.make_folder(path_names)
            
        pic_copy_sorted = df_copied_files.sort_values(by='Format_rank', axis=0, ascending=False)

        seperator = st.text_input("Please enter the seperator between class and file number")
        if not seperator:
            # st.warning("Please make sure that you only enter a separator")
            st.stop()

        pic_copy_sorted['File_names'] = func.extract_filenames(seperator, df_column=pic_copy_sorted)##

        if st.button("Move files", type="primary"):

            with st.spinner("Moving files...."):

                for i, j, k in zip(pic_copy_sorted['файл'], pic_copy_sorted['формат'], pic_copy_sorted['File_ending']):

                    source_path = path_name
                    dest_path = path_name
                    seperator = seperator

                    try:        
                        temp = func.split_file(i, seperator)[1]
                        class_number = func.split_file(i, seperator)[0]
                        if len(temp) <= 4:
                            file_name = class_number + seperator + temp + '.JPG'
                        elif len(temp) > 4 and len(k) == 1:
                            file_name = class_number + seperator + temp[:len(temp)-1] + '.JPG'
                        else:
                            file_name = class_number + seperator + temp[:len(temp)-2] + '.JPG'
                    except:
                        continue
                    
                    file_name = file_name.strip()
                    format = None
                    
                    try:
                            
                        if j in ['блок3', 'блок5', '15x21', '15x21-2', '15x21-3', '15x21-4', '15x21-5', '15x21-6', 'блок3-2']:
                            format = '15x21'
                        elif j in ['21x30', '21x30-2', '21x30-3', '21x30-4']:
                            format = '21x30'
                        elif j in ['10x15', '10x15-2', '10x15-3', '10x15-4', '10x15-5', '10x15-6']:
                            format = '10x15'
                        elif j in ['магнит', 'магнит-2', 'магнит-3', 'магнит-4']:
                            format = 'магнит'
                        elif j in ['наклейка','наклейка-2']:
                            format = 'наклейка'
                        elif j in ['File', 'File-2', 'File-3', 'File-4']:
                            format = 'File'
                        elif j in ['30x45', '30x45-2']:
                            format = '30x45'
                        else:
                            format = j
                            
                        origin_path = source_path + '/'+file_name        
                        destination_path = dest_path + '/'+format                
                        shutil.move(src=origin_path, dst=destination_path)
                                                
                    except: 
                        continue

            st.success("Done !")
            st.write('Your files have been moved to the format folders')

if add_selectbox == '3. Rename chrome':

    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    path_name = st.text_input("Please enter the location of your files", "")

    if not file_source or not path_name:
        st.stop()
        st.success('Thanks for entering file locations')
    else:
        df_files = pd.read_excel(file_source)
        st.write('Here is your files excel folder')
        st.dataframe(df_files)
        st.write('The table has {} rows and {} columns'.format(df_files.shape[0], df_files.shape[1]))
        func.add_file_ending_column(df_files)

        # class_number = st.text_input("Please enter the file class number", '')
        seperator = st.text_input("Please enter the seperator between class and file number")

        if st.button("Rename files", type="primary"):

            with st.spinner("Renaming files...."):

                for i, j, k in zip(df_files['файл'], df_files['формат'], df_files['File_ending']):
    
                    ten_fifteen_list = ['10x15', '10x15-2', '10x15-3', '10x15-4', '10x15-5', '10x15-6']
                    fifteen_twentyone_list = ['блок3', 'блок5', '15x21', '15x21-2', '15x21-3', '15x21-4', '15x21-5', '15x21-6', 'блок3-2']
                    twentyone_thirty_list = ['21x30', '21x30-2', '21x30-3', '21x30-4']
                    magnit = ['магнит', 'магнит-2', 'магнит-3', 'магнит-4']
                    nakleka = ['наклейка','наклейка-2']
                    big_file = ['File', 'File-2', 'File-3', 'File-4']
                    thirty_fortyfive = ['30x45', '30x45-2']
                    
                    seperator = seperator
                    
                    try:      
                        
                        temp = func.split_file(i, seperator)[1]
                        class_number = func.split_file(i, seperator)[0]
                        if len(temp) <= 4:
                            file_name = class_number + seperator + temp + '.JPG'
                        elif len(temp) > 4 and len(k) == 1:
                            file_name = class_number + seperator + temp[:len(temp)-1] + '.JPG'
                        else:
                            file_name = class_number + seperator + temp[:len(temp)-2] + '.JPG'
                    except:
                        continue
                    
                    file_name = file_name.strip()
                    if j in ten_fifteen_list:
                        j = '10x15'
                    if j in fifteen_twentyone_list:
                        j = '15x21'
                    if j in twentyone_thirty_list:
                        j = '21x30'
                    if j in magnit:
                        j = 'магнит'
                    if j in nakleka:
                        j = 'наклейка'
                    if j in big_file:
                        j = 'File'
                    if j in thirty_fortyfive:
                        j = '30x45'
                    
                    folder = '/'+j
                    source_path = path_name
                    source_dir = source_path + folder
                        
                    
                    try:
                        
                        if j == '10x15' or j == '15x21':  
                            dest_path = source_dir + '/'+k
                            func.make_folder(dest_path)
                            source_file_dir = source_dir + '/' + file_name
                            shutil.move(src=source_file_dir, dst=dest_path)
                            old_name = dest_path+'/'+file_name
                            new_name = dest_path+'/'+ i +'.JPG'
                            os.rename(old_name, new_name)
                            
                        else:
                                
                            old_name = source_dir+'/'+file_name
                            new_name = source_dir+'/'+ i +'.JPG'
                            os.rename(old_name, new_name)
                                                    
                    except:
                        continue

            st.success("Done !")
            st.write('Your files have been renamed in their format folders')


if add_selectbox == '4. Final rename':

    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    path_name = st.text_input("Please enter the location of your files", "")

    if not file_source or not path_name:
        st.stop()
        st.write('Thanks for entering file locations')
    else:
        df_files = pd.read_excel(file_source)
        st.write('Here is your files excel folder')
        st.dataframe(df_files)
        st.write('The table has {} rows and {} columns'.format(df_files.shape[0], df_files.shape[1]))
        func.add_file_ending_column(df_files)

        if st.button("Move files", type="primary"):

            with st.spinner("Moving files...."):

                for folder in ['15x21-2', 'блок']:
                    dest_path = path_name + '/' + 'блок'
                    dest_path = path_name + '/' + folder
                    directory_name = Path(dest_path)
                    directory_name.mkdir(parents=True, exist_ok=True)


                 
                for i, j, k in zip(df_files['файл'], df_files['формат'], df_files['File_ending']):

                    file_dir = path_name + '/'
                    
                    file = i+'.JPG'
                    file = file.strip()
                                     
                    try:
                        if j in ['10x15-3', '10x15-4', '10x15-5', '10x15-6']:
                            format = '10x15'
                            if k == '':
                                source_file = file_dir + format + '/' + file
                            else:
                                source_file = file_dir + format + '/' + k + '/'+ file
                            dest_dir = file_dir + '_10x15'
                            shutil.move(src=source_file, dst=dest_dir)
                                                                        
                        if j == '10x15-2':
                            format = '10x15'
                            if k == '':
                                source_file = file_dir + format + '/' + file
                            else:
                                source_file = file_dir + format + '/' + k + '/'+ file
                            dest_dir = file_dir + '10x15-2'
                            shutil.move(src=source_file, dst=dest_dir)
                            
                        if j in ['15x21-2', '15x21-3', '15x21-4', '15x21-5', '15x21-6']:  
                            format = '15x21'
                            if k == '':
                                source_file = file_dir + format + '/' + file
                            else:
                                source_file = file_dir + format + '/' + k + '/'+ file
                            dest_dir = file_dir + '15x21-2'
                            shutil.move(src=source_file, dst=dest_dir)
                                                                
                        if j in ['блок3', 'блок5', 'блок3-2']:
                            format = '15x21'
                            if k == '':
                                source_file = file_dir + format + '/' + file
                            else:
                                source_file = file_dir + format + '/' + k + '/'+ file
                            dest_dir = file_dir + 'блок'
                            shutil.move(src=source_file, dst=dest_dir)
                                                
                                
                    except:
                        continue

                for i, j, k in zip(df_files['файл'], df_files['формат'], df_files['File_ending']):
        
                    file_dir = path_name
                    file = i+'.JPG'
                    file = file.strip()
                        
                    if  j in ['10x15', '15x21']:
                        format = j
                        try:
                            if k == '':
                                continue
                            else:
                                source_file_dir = file_dir + '/' + format + '/' + k + '/' + file
                                dest_path = file_dir + '/'+ format
                                shutil.move(src=source_file_dir, dst=dest_path)
                                
                        except:
                            continue
                       
                    else:
                        continue

                                        
            st.success("Done !")
            st.write('Your files have been moved in their format folders')

            
        order_number = st.text_input("Please enter an order NUMBER", "")
        if not order_number:
            st.stop()
        else:

            if st.button("Rename files", type="primary"):

                with st.spinner("Renaming files...."):
            
                    for i, j, k in zip(df_files['файл'], df_files['формат'], df_files['File_ending']):

                        file_dir = path_name
                       
                        if j == '15x21':
                            format = '15x21'
                        if j in ['15x21-2', '15x21-3', '15x21-4', '15x21-5', '15x21-6']:
                            format = '15x21-2'
                        if j in ['21x30', '21x30-2', '21x30-3', '21x30-4']:
                            format = '21x30'
                        if j in ['магнит', 'магнит-2', 'магнит-3', 'магнит-4']:
                            format = 'магнит'
                        if j in ['наклейка','наклейка-2']:
                            format = 'наклейка'
                        if j in  ['File', 'File-2', 'File-3', 'File-4']:
                            format = 'File'
                        if j in ['30x45', '30x45-2']:
                            format = '30x45'
                        if j in ['блок3', 'блок5', 'блок3-2']:
                            format = 'блок'                        
                        if j in ['10x15-3', '10x15-4', '10x15-5', '10x15-6']:
                            format = '_10x15'
                        if j == '10x15':
                            format = '10x15'
                        if j == '10x15-2':
                            format = '10x15-2'

                                        
                        if j in ['10x15', '10x15-2', '10x15-3', '10x15-4', '10x15-5', '10x15-6']:
                            file = i.strip()
                            format_ending_func = lambda x: x[-2:] if '-' in x else '-1'
                            format_ending = format_ending_func(j)
                            new_filename = order_number + file + format_ending
                            
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in ['магнит', 'магнит-2', 'магнит-3', 'магнит-4']:
                            file = i.strip()
                            new_filename = func.magnit_renamer(j, file, order_number)
                            
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in  ['15x21', '15x21-2', '15x21-3', '15x21-4', '15x21-5', '15x21-6']:
                            file = i.strip()
                            new_filename = func.non_magnit_renamer(j, file, order_number)
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in ['21x30', '21x30-2', '21x30-3', '21x30-4']:
                            file = i.strip()
                            new_filename = func.non_magnit_renamer(j, file, order_number)
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in ['наклейка','наклейка-2']:
                            file = i.strip()
                            new_filename = func.magnit_renamer(j, file, order_number)
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in  ['File', 'File-2', 'File-3', 'File-4']:
                            file = i.strip()
                            # format_ending_func = lambda x: '-1' if '-' in x else ''
                            # format_ending = format_ending_func(j)
                            new_filename = order_number + file + '-1'
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in ['30x45', '30x45-2']:
                            file = i.strip()
                            new_filename = func.non_magnit_renamer(j, file, order_number)
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            
                        elif j in ['блок3', 'блок5', 'блок3-2']:
                            file = i.strip()
                            new_filename = func.non_magnit_renamer(j, file, order_number)
                                                        
                            try:

                                old_name = file_dir + '/' + format + '/' + file + '.JPG'
                                new_name = file_dir + '/' + format + '/' + new_filename + '.JPG'
                                os.rename(src=old_name, dst=new_name)
                            except:
                                continue
                            print(format)

                st.success("Done !")
                st.write('Your files have been renamed')
                st.write('Total renamed files in folder {}: {}'.format(file_dir, func.file_count(file_dir)))

                for fmt in ['10x15', '15x21']:
                    file_dir = path_name + '/' + fmt

                    for dirpath, _, _, in os.walk(file_dir):
                            if os.path.isdir(dirpath):
                                if os.listdir(dirpath) == []:
                                    os.removedirs(dirpath)
                                else:
                                    continue


if add_selectbox == '5. Album - Copy All':

    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    source_path = st.text_input("Please enter the file location of the MAIN file", "")
    path_name = st.text_input("Please enter the location where you want to copy your files", "")

    if not file_source or not source_path or not path_name:
        st.stop()
        st.success('Thanks for entering file locations')
    else:
        filenames = []
        files = pd.read_excel(file_source, header=None)
        st.write("Here's the pictures excel file")
        st.dataframe(files)

        for i in range(len(files)):
            x = files.iloc[i, :].tolist()
            filenames.extend(x)
        clean_filenames = [str(x).strip() for x in filenames]
        clean_filenames = [x for x in clean_filenames if x != 'nan']

        class_number = st.text_input("Does the excel file have a class number and seperator? If NO enter it HERE. If yes enter YES", "")
        if not class_number:
            st.stop()
        elif class_number.lower() == 'yes':
            class_number = ''
            # pass
        else:
            clean_filenames = [class_number + x for x in clean_filenames]
        
        # Add the option to add a class number
        dest_path = path_name
        func.make_folder(dest_path)
        destination_path = path_name

        answer = st.text_input("Is the seperator in the excel file different from the seperator in the class file? YES or NO","")
        if not answer:
            st.stop()
        elif answer.lower() == 'yes':
            file_seperator = st.text_input("Please enter seperator from excel file", "")
            pics_seperator = st.text_input("Please enter seperator from the pics class file", "")
        else:
            file_seperator = ''
            pics_seperator = ''

        copied_pics = []
        copied_files = []
        
        
        if st.button("Copy files", type="primary"):

            with st.spinner("Copying files...."):
                
                for dirpaths, dirnames, filenames in os.walk(source_path):
                    
                    for file in clean_filenames:
                        if str(file) == 'nan':
                                continue                        
                        try:
                            file_ending  = func.extract_file_ending(file)
                            file_name = file.replace(file_ending, '').strip() + '.JPG'
                        except:
                            file_ending = ''
                            file_name = file + '.JPG'

                        if file_seperator == '' or pics_seperator == '':
                            file_renamed = file_name
                        else:
                            file_renamed = file_name.replace(file_seperator, pics_seperator)   
                        
                        source_file = os.path.join(dirpaths, file_renamed)
                        if os.path.isfile(source_file): 
                            shutil.copy(src=source_file, dst=destination_path)
                            copied = os.path.basename(source_file.strip('.JPG'))
                            
                            copied_pics.append(copied)
                            files_copied = copied + file_ending
                            files_copied = files_copied.replace(pics_seperator, file_seperator)
                            copied_files.append(files_copied) 
                            
                            
                            if file_ending == None:
                                continue
                            else:
                                try:
                                    old_name =  destination_path + '/' + copied + '.JPG'
                                    new_name =  destination_path + '/' + copied + file_ending + '.JPG'
                                    # print(old_name)
                                    # print(new_name)
                                    os.rename(old_name, new_name)
                                except:
                                    continue
            st.success("Done !")
            st.write('Your files have been copied to the new folder') 
                                             
            file_names = []
            duplicated_files = []

            for file in clean_filenames:
                
                file_names.append(file.strip('JPG'))
                    
            for i in list(set(copied_pics)):
                if copied_pics.count(i) > 1:
                    duplicated_files.append(i)

            
            non_copied = [x for x in file_names if x not in copied_files]
            st.write('These files were not copied')
            st.dataframe(non_copied)
            st.write('These files duplicated')
            st.dataframe(duplicated_files)


if add_selectbox == '6. Album - Copy By Name':

    file_source = st.text_input("Please copy and paste the file location of your class EXCEL file", "")
    source_path = st.text_input("Please enter the file location of the MAIN file", "")
    path_name = st.text_input("Please enter the location where you want to copy your files", "")

    if not file_source or not source_path or not path_name:
        st.stop()
        st.success('Thanks for entering file locations')
    else:
        data_file = pd.read_excel(file_source)
        data_file.dropna(axis=1, how='all', inplace=True)
        data_file.fillna(0, inplace=True)
        #data_file[data_file.columns[1:]].astype('int32')
        data_file = data_file.convert_dtypes(convert_integer=True)        
        st.write("Here's the pictures excel file")
        st.dataframe(data_file)
        func.make_folder(path_name)

        class_number = st.text_input("Does the excel file have a class number and seperator? If NO enter it HERE. If yes enter YES", "")
        if not class_number:
            st.stop()
        elif class_number.lower() == 'yes':
            class_number = ''
            # pass
                
        answer = st.text_input("Is the seperator in the excel file different from the seperator in the class file? Enter YES or NO","")
        if not answer:
            st.stop()            
        elif answer.lower() == 'yes':
            file_seperator = st.text_input("Please enter seperator from excel file", "")
            pics_seperator = st.text_input("Please enter seperator from the pics class file", "")
        else:
            file_seperator = ''
            pics_seperator = ''

        copied_files = []
        clean_filenames = []
        copied_pics = []
        
        if st.button("Copy By Name", type="primary"):

            with st.spinner("Copying files...."):
        
        
                for dirpaths, dirnames, filenames in os.walk(source_path):

                    for row in data_file.itertuples():
                        #temp_list = [x for x in list(row)[1:] if x != 'NA']
                        temp_list = [str(x).strip() for x in list(row)[1:]]
                        
                        clean_filenames.extend(temp_list[1:])
                        folder_name = temp_list[0]
                        name_folder_path = path_name + '/' + folder_name
                        func.make_folder(name_folder_path)
                        temp_list.remove(folder_name)
                        if class_number != 'yes':
                            temp_list = [class_number + x for x in temp_list]
                        # Add the option to add a class number
                        
                        for file in temp_list:   
                            if str(file) == 'nan':
                               continue
                            try:
                                file_ending = func.extract_file_ending(file)
                                file_no_ending = file.replace(file_ending, '').strip() + '.JPG'
                            except:
                                file_ending = ''
                                file_no_ending = file + '.JPG'
                            file_renamed = file_no_ending.replace(file_seperator, pics_seperator)
                            
                            source_file = os.path.join(dirpaths, file_renamed)            
                            if os.path.isfile(source_file):
                                shutil.copy(src=source_file, dst=name_folder_path)
                                copied = os.path.basename(source_file.strip('.JPG'))

                                copied_pics.append(copied)
                                files_copied = copied + file_ending
                                files_copied = files_copied.replace(pics_seperator, file_seperator)
                                copied_files.append(files_copied) 
                                
                                # print(file_seperator)
                                # print(pics_seperator)
                                
                                try:
                                    copied = os.path.basename(source_file)
                                    old_name =  name_folder_path + '/' + copied
                                    new_name =  name_folder_path + '/' + copied.strip('.JPG') + file_ending + '.JPG'
                                    os.rename(old_name, new_name)
                                except:
                                    continue
                            
            st.success("Done !")
            st.write("The students' files have been copied to their folders") 

            file_names = []
            duplicated_files = []

            for file in clean_filenames:
                
                if class_number != '' and pics_seperator != '':
                    file = class_number + pics_seperator + file                
                    file_names.append(file)
                    
            for i in list(set(copied_pics)):
                if copied_pics.count(i) > 1:
                    duplicated_files.append(i)
            
            non_copied = [x for x in file_names if x not in copied_files]
            st.write('These files were not copied')
            st.dataframe(non_copied)
            st.write('These files are duplicated')
            st.dataframe(duplicated_files)