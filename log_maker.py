import pandas as pd
import datetime




class stats():
    def __init__(self,i_p,o_p,csv):
        self.input_file = i_p
        self.output_file = o_p
        self.csv_path = csv


    def lcount(self):
        df = pd.DataFrame()
        main_line = ''
        with open(self.input_file) as infile:
            for line in infile:
                if 'Exe_file ' in line:
                    df[line] = ""
                    main_line = line
                    print(main_line)
                else:
                    df = df.append({main_line: line}, ignore_index=True)
        return df


    def make_stats(self):
        # input_file = 'C:/Users/kir/Desktop/actions/log.txt'
        output_file = open(self.output_file,'w')
        df = self.lcount()
        df_splited = df
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(df)
        df_splited.to_excel(self.csv_path)
        res = list(zip(df_splited.columns, df_splited.columns[1:] + df_splited.columns[:1]))
        print(res)
        for i in res:
            output_file.write('TIME SPEND' + i[0].split('.')[1] + ' ' +
                              str(datetime.datetime.strptime(i[1].split('.')[0],'%Y-%m-%d %H:%M:%S,%f') -
                              datetime.datetime.strptime(i[0].split('.')[0],'%Y-%m-%d %H:%M:%S,%f')) + '\n')


        for i in df_splited.columns:
            df_splited[i] = df_splited[i].str.split('.').str[1]


        for i in df_splited.columns:
            output_file.write('ACTION\n' + str(i) + str(df_splited[i].value_counts().to_dict()) + '\n')



