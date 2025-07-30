import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import shutil
import tabulate
import zipfile

class TCQi:
    # import tabulate
    def unpack_file(self, file_path, destination_folder='.//temp//'):
        for file in os.scandir(destination_folder):
            os.remove(file.path)
        shutil.unpack_archive(file_path, destination_folder, 'zip')
        content = os.listdir(destination_folder)
        file_name = ''
        for file in content:
            if file.endswith('.TCQCSV'):
                file_name = file
        return destination_folder + file_name

    def reformat_line(self, line):
        # line = line.replace(',,', ',"",')
        return line

    def read_and_split_TCQi_file(self, file_path, temp_path='.//temp//'):
        tmp = TCQi()
        table_files = []
        with open(file_path, mode='r', encoding="utf8") as file:
            current_table = None
            while True:
                line = file.readline()
                if not line:
                    break
                line = tmp.reformat_line(line)
                data = line.split('","')
                if len(data) == 0:
                    pass
                elif len(data[0]) == 0:
                    file_w.write(line)
                elif data[0][0] == '"':
                    table_name = data[0].replace('"', '')
                    if table_name == current_table:
                        file_w.write(line)
                    else:
                        try:
                            file_w.close()
                        except:
                            pass
                        current_table = table_name
                        i = 0
                        flag = os.path.isfile(temp_path + current_table + '.tbl')
                        while flag:
                            current_table = table_name + str(i)
                            i += 1
                            flag = os.path.isfile(temp_path + current_table + '.tbl')
                        table_files.append(temp_path + current_table + '.tbl')
                        print('Working on:', current_table)
                        file_w = open(temp_path + current_table + '.tbl', mode="w", encoding="utf8")
                        file_w.write(line)
                else:
                    file_w.write(line)
        return table_files

    def read_tbl_file(self, file):
        print('Working on:', file)
        dataframe = pd.read_csv(file, delimiter=',', header=0, quotechar='"', engine='c', encoding="utf8", dtype='string')
        return dataframe

    def read_all_tbl_file(self, table_files, verbose=True):
        tmp = TCQi()
        dataframe_vector = []
        table_names = []
        id_vector = []
        for file in table_files:
            dataframe_vector.append(tmp.read_tbl_file(file))
            table_name = os.path.basename(file)[:len(os.path.basename(file)) - 4]
            if len(table_name) > 31:  # Los nombres de las hojas de Excel no pueden tener una longitud mayor a 31
                table_names.append(table_name[:30])
            else:
                table_names.append(table_name)
        for dataframe in dataframe_vector:
            try:
                id_vector.append(np.asarray(dataframe["ID#NUMERIC"].to_numpy(), dtype=np.int32))
            except:
                pass
        if verbose:
            for dataframe in dataframe_vector:
                print(dataframe.to_markdown())
        list_1D = []
        for sub_list in id_vector:
            for item in sub_list:
                list_1D.append(item)
        max_id_value = max(list_1D)
        return dataframe_vector, table_names, max_id_value, id_vector

    def read_titol_nivel(self, table_files, verbose=True):
        dataframe = pd.DataFrame(
            columns=["titol_nivell", "ID#NUMERIC", "ID_SISQUILLO#NUMERIC", "TITOL#CHARACTER", "PROFUNDITAT#NUMERIC"])
        # cont = 0
        for file in table_files:
            filename = os.path.split(file)[1]
            if filename.startswith('titol_nivell'):
                with open(file, mode='r', encoding="utf8") as input:
                    for line in input:
                        vector = line.replace('\n', '').split(',')
                        if vector[1] != '"ID#NUMERIC"':
                            df2 = {'titol_nivell': vector[0],
                                   'ID#NUMERIC': vector[1],
                                   'ID_SISQUILLO#NUMERIC': vector[2],
                                   'TITOL#CHARACTER': vector[3],
                                   'PROFUNDITAT#NUMERIC': vector[4]}
                            dataframe = dataframe._append(df2, ignore_index=True)
                            # print(vector)
        if verbose:
            print(dataframe.to_markdown())
        return dataframe

    def read_nivel(self, table_files, verbose=True):
        columns_vector = ["nivell", "ID#NUMERIC", "ID_SISQUILLO#NUMERIC", "ID_PARE#NUMERIC", "DESCRIPCIO#CHARACTER",
                          "CPR_ID#NUMERIC",
                          "ID_TITOL_NIVELL#NUMERIC", "TNO_ID#CHARACTER", "IMPORT#NUMERIC", "SELECCIONAT#CHARACTER",
                          "CAMI_ORDINAL#CHARACTER", "ID_VISTA#NUMERIC"]
        dataframe = pd.DataFrame(
            columns=["nivell", "ID#NUMERIC", "ID_SISQUILLO#NUMERIC", "ID_PARE#NUMERIC", "DESCRIPCIO#CHARACTER",
                     "CPR_ID#NUMERIC",
                     "ID_TITOL_NIVELL#NUMERIC", "TNO_ID#CHARACTER", "IMPORT#NUMERIC", "SELECCIONAT#CHARACTER",
                     "CAMI_ORDINAL#CHARACTER", "ID_VISTA#NUMERIC"])
        for file in table_files:
            filename = os.path.split(file)[1]
            if filename.startswith('nivell'):
                with open(file, mode='r', encoding="utf8") as input:
                    for line in input:
                        vector = line.replace('\n', '').split('","')
                        if vector[1] != 'ID#NUMERIC':
                            df2 = {}
                            for cont, column in enumerate(columns_vector):
                                df2[column] = vector[cont]
                            dataframe = dataframe._append(df2, ignore_index=True)
        if verbose:
            print(dataframe.to_markdown())
        return dataframe

    def tbl_to_TCQi(self, file_list, output_file, folder='.//temp//'):
        with open(output_file, 'w', encoding="utf8") as outfile:
            for file in file_list:
                with open(folder + file, 'r', encoding="utf8") as srcfile:
                    shutil.copyfileobj(srcfile, outfile)

    def from_tbl_to_tcqcsv(self, table_files, temp_out_file='.//temp.TCQCSV'):
        with open(temp_out_file, mode='w', encoding="utf8") as file_output:
            for file in table_files:
                with open(file, mode='r', encoding="utf8") as file_input:
                    for line in file_input:
                        file_output.write(line)

    # Plots table using plotly, returns Schema of a given table
    def tbl_to_schema(self, title, fields, align="left", fill_color="#002060", color="white", line_color="#000000", col_width=40):
        columns = []
        columns.append(fields)
        fig = go.Figure(data=[go.Table(columnwidth=col_width,
                                        header=dict(values=[title],
                                                    align=align,
                                                    fill_color=fill_color,
                                                    font=dict(color=color),
                                                    line_color=line_color
                                                    ),
                                        cells=dict(values=columns,
                                                    line_color=line_color,
                                                    align=align))
                        ])
        if not os.path.exists("images"):
            os.mkdir("images")

        ext = ".png"
        file_name = title.copy().pop(0)
        if not os.path.exists("images/" + file_name + ext):
            fig.write_image("images/" + file_name + ext)

    def create_excel_file(self, list_dfs, temp_file, table_order):
        with pd.ExcelWriter(temp_file, engine="xlsxwriter") as writer:
            for idx, df in enumerate(list_dfs, start=0):
                df.to_excel(writer, sheet_name=table_order[idx])
                if table_order[idx].startswith('titol_nivell') or table_order[idx].startswith('nivell'):
                    worksheet = writer.sheets[table_order[idx]]
                    worksheet.hide()

    def apply_function_zero(self, x):
        try:
            value = int(x)
        except:
            value = 0
        return value

    def apply_function_text(self, x):
        if x == "0":
            return ""
        else:
            return x

    def apply_function_bool(self, x):
        try:
            value = int(x)
        except:
            value = 9999
        return value

    def apply_function_bool_text(self, x):
        if x == "9999":
            return ""
        else:
            return x

    def read_excel_file(self, filename, temp_out_file='.//temp//temp.TCQCSV'):
        list_dfs = pd.read_excel(filename, sheet_name=None, dtype='string')
        table_names = list_dfs.keys()
        file = open('output.TCQCSV', mode='w')
        file.close()
        for name in table_names:
            if name.startswith('titol_nivell') or name.startswith('nivell'):
                with open('output.TCQCSV', mode='a', encoding='utf8') as output_file:
                    with open('./temp/' + name + '.tbl', mode='r', encoding='utf8') as table_file:
                        for line in table_file:
                            output_file.write(line)
            else:
                columns = list_dfs[name].columns.to_numpy()[1:]
                list_dfs[name].to_csv(temp_out_file, sep=',', quotechar='"', quoting=1,
                                      index=False, encoding="utf8", mode='a', columns=columns)  #, float_format='%.9f'

    def adapt_file(self, filename_input, filename_output='output_adapted.tcqcsv'):
        with open(filename_output, mode='w', encoding="utf8") as file_output:
            with open(filename_input, mode='r', encoding="utf8") as file_input:
                for linea in file_input:
                    new_line = linea.replace('_x000D_', '')
                    # new_line = linea.replace(',""', ',')
                    file_output.write(new_line)
        return filename_output

    def repack_file(self, file_to_repack='.//temp.TCQCSV', temp_folder='./temp/', output_file='output.tcqi', adapt_file_flag=True):
        tmp = TCQi()
        if adapt_file_flag:
            file_to_include = tmp.adapt_file(file_to_repack)
        else:
            file_to_include = file_to_repack
        with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as myzip:
            content = os.listdir(temp_folder)
            for file in content:
                if file.endswith('.tbl') or file.endswith('.bkp') or file.endswith('.xlsx'):
                    pass
                elif file.endswith('.TCQCSV'):
                    myzip.write(file_to_include, file)
                else:
                    myzip.write(temp_folder + file, file)

class TCQiTools:
    def extract_TCQi_info(self, file):
        tcqi = TCQi()
        # 1). Set file to be analyzed
        tcqi_file = file

        # 2). Extract TCQi infor with TCQi object's functions
        table_files = tcqi.read_and_split_TCQi_file(
            tcqi.unpack_file(tcqi_file)
        )

        # 3). Arrange the info in tables
        df_vector, table_names, id_max, id_vector = tcqi.read_all_tbl_file(table_files, False)

        # 4). Output a DataFrame object with the info
        return df_vector

    def get_table(self, tables, table):
        # 1). Copy input info into local variable
        df = tables.copy()

        # 2). Output specified table

        return df[table]

    def get_table_column(self, table, column):
        # 1). Copy input info into local variable
        col = table.copy()

        # 2). Output specified table column
        return col[column]

    def get_column_cell(self, column, row):
        # 1). Copy input info into local variable
        cell = column.copy()

        # 3). Output specified column cell
        return cell.iloc[row]

    def merge_tables(self, table_1, columns_1, id_1, table_2, columns_2, id_2):
        return table_1.copy()[columns_1].join(table_2[columns_2].set_index(id_2), on=id_1, lsuffix='_caller',
                                              rsuffix='_other')

    def get_kpi_first(self, table, kpi_name, kpis=[], phases=[], element=[]):
        # 1). Filter origin columns
        result = table.copy()[
            ['ID_ELEMENT#NUMERIC', 'ID_FASE#CHARACTER', 'ID_INDICADOR#SMALLINT', 'VALOR#NUMERIC',
             'CODI_ITEC#CHARACTER']]

        # 2). Filter by kpis selected
        result = result[(result['ID_INDICADOR#SMALLINT'].isin(kpis))]
        # 2.1). Delete kpi column
        result = result.drop(columns='ID_INDICADOR#SMALLINT')

        # 3). Filter by phases selected
        if phases != []:
            result = result[(result['ID_FASE#CHARACTER'].isin(phases))]
        # 3.1). Delete phase column
        result = result.drop(columns='ID_FASE#CHARACTER')
        # 3.2). Add up values for kpi and phase
        result['VALOR#NUMERIC'] = result['VALOR#NUMERIC'].astype(float)
        result = result.groupby(['ID_ELEMENT#NUMERIC', 'CODI_ITEC#CHARACTER'],
                                                              as_index=False).sum()
        result['VALOR#NUMERIC'] = result['VALOR#NUMERIC'].astype(str)

        # 4) Filter by elements selected
        if element != []:
            result = result[(result['CODI_ITEC#CHARACTER'].isin(element))]
        # 4.1). Delete element code column
        result = result.drop(columns='CODI_ITEC#CHARACTER')

        # 5). Rename result column to avoid data clashing
        # 5.1). Assign calculated value to the new column
        result[kpi_name] = result['VALOR#NUMERIC']

        # 6). Delete value column
        result = result.drop(columns='VALOR#NUMERIC')

        # 7). Output the value by: kpi, phase and element selected
        return result

    def get_kpi_second(self, table, kpi_name, kpis=[], phases=[], element=[]):
        # 1). Filter origin columns
        result = table.copy()[
            ['ID_ELEMENT#NUMERIC', 'ID_FASE#CHARACTER', 'ID_INDICADOR#SMALLINT', 'VALOR2#NUMERIC',
             'CODI_ITEC#CHARACTER']]

        # 2). Filter by kpis selected
        result = result[(result['ID_INDICADOR#SMALLINT'].isin(kpis))]
        # 2.1). Delete kpi column
        result = result.drop(columns='ID_INDICADOR#SMALLINT')

        # 3). Filter by phases selected
        if phases != []:
            result = result[(result['ID_FASE#CHARACTER'].isin(phases))]
        # 3.1). Delete phase column
        result = result.drop(columns='ID_FASE#CHARACTER')
        # 3.2). Add up values for kpi and phase
        result['VALOR2#NUMERIC'] = result['VALOR2#NUMERIC'].astype(float)
        result = result.groupby(['ID_ELEMENT#NUMERIC', 'CODI_ITEC#CHARACTER'],
                                as_index=False).sum()
        result['VALOR2#NUMERIC'] = result['VALOR2#NUMERIC'].astype(str)

        # 4) Filter by elements selected
        if element != []:
            result = result[(result['CODI_ITEC#CHARACTER'].isin(element))]
        # 4.1). Delete element code column
        result = result.drop(columns='CODI_ITEC#CHARACTER')

        # 5). Rename result column to avoid data clashing
        # 5.1). Assign calculated value to the new column
        result[kpi_name] = result['VALOR2#NUMERIC']

        # 6). Delete value column
        result = result.drop(columns='VALOR2#NUMERIC')

        # 7). Output the value by: kpi, phase and element selected
        return result

    def get_kpi_third(self, table, kpi_name, kpis=[], phases=[], element=[]):
        # 1). Filter origin columns
        result = table.copy()[
            ['ID_ELEMENT#NUMERIC', 'ID_FASE#CHARACTER', 'ID_INDICADOR#SMALLINT', 'VALOR3#NUMERIC',
             'CODI_ITEC#CHARACTER']]

        # 2). Filter by kpis selected
        result = result[(result['ID_INDICADOR#SMALLINT'].isin(kpis))]
        # 2.1). Delete kpi column
        result = result.drop(columns='ID_INDICADOR#SMALLINT')

        # 3). Filter by phases selected
        if phases != []:
            result = result[(result['ID_FASE#CHARACTER'].isin(phases))]
        # 3.1). Delete phase column
        result = result.drop(columns='ID_FASE#CHARACTER')
        # 3.2). Add up values for kpi and phase
        result['VALOR3#NUMERIC'] = result['VALOR3#NUMERIC'].astype(float)
        result = result.groupby(['ID_ELEMENT#NUMERIC', 'CODI_ITEC#CHARACTER'],
                                as_index=False).sum()
        result['VALOR3#NUMERIC'] = result['VALOR3#NUMERIC'].astype(str)

        # 4) Filter by elements selected
        if element != []:
            result = result[(result['CODI_ITEC#CHARACTER'].isin(element))]
        # 4.1). Delete element code column
        result = result.drop(columns='CODI_ITEC#CHARACTER')

        # 5). Rename result column to avoid data clashing
        # 5.1). Assign calculated value to the new column
        result[kpi_name] = result['VALOR3#NUMERIC']

        # 6). Delete value column
        result = result.drop(columns='VALOR3#NUMERIC')

        # 7). Output the value by: kpi, phase and element selected
        return result

    def get_sum_total(self, table):
        result = 0
        for i in table.values:
            result += float(i[1])
        return result

    def excel_export(self, table, filename):
        table.to_excel("Output/" + filename, index=False)



if __name__ == '__main__':
    tcqi = TCQi()
    file = 'filename.tcqi'
    table_files = tcqi.read_and_split_TCQi_file(
        tcqi.unpack_file('.//Data//' + file))
    df_vector, table_names, id_max, id_vector = tcqi.read_all_tbl_file(table_files, False)
    tcqi.create_excel_file(df_vector, './' + file[:len(file)-5] + '.xlsx', table_names)
    tcqi.read_excel_file('./' + file[:len(file)-5] + '.xlsx')
    tcqi.repack_file()

    tcqi_tools = TCQiTools()
    # ...
