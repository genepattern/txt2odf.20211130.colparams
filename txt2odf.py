import pandas as pd
from txt2odf_functions import *
import os

print(sys.argv)
#txt_file, prune_gct, gct, cls = parse_arguments(sys.argv)
print(sys.argv)
txt_file, id_col, stat_col, prune_gct, gct, cls = parse_arguments(sys.argv)

name_of_file = os.path.basename(txt_file).strip('txt')+'odf'

data_df = pd.read_table(txt_file)
#data_df.insert(1, 'Description', data_df['id'])
data_df.insert(1, 'Description', data_df[id_col])
data_df.insert(0, 'Rank', data_df.index.values+1)
#data_df.insert(3, 'Score', data_df['stat'])
data_df.insert(3, 'Score', data_df[stat_col])
#data_df.rename(columns={'id': 'Feature'}, inplace=True)
data_df.rename(columns={id_col: 'Feature'}, inplace = True)

rest_of_cols = [col for col in data_df.columns if col not in ["Rank", "Feature"]]
data_df = data_df[["Rank", "Feature"] + rest_of_cols]

classes = ['Nothing', 'class_0', 'class_1']
if cls is not None:
    print("\tHabemus CLS!")
    cls_file = open(cls)
    cls_file.readline()
    temp = cls_file.readline()
    classes = temp.strip('\n').split()

vals = dict()
vals['gct'] = txt_file
vals['cls'] = txt_file
vals['n_perm'] = 1
vals['class_0'] = classes[2]
vals['class_1'] = classes[1]
#vals['func'] = 'stat'
vals['func'] = stat_col
vals['rand_seed'] = 123456789
vals['dat_lines'] = len(data_df)

df2odf(data_df=data_df, vals=vals, file_name=name_of_file)
print('\tFile', name_of_file, "has been written!")

if prune_gct:
    original_gct = pd.read_table(gct, sep='\t', skiprows=2)
    # print(original_gct)
    #df = original_gct.loc[original_gct['Name'].isin(data_df['Feature'])]
    try:
        df = original_gct.loc[original_gct["Name"].isin(data_df["Feature"])]
    except KeyError:
        df = original_gct.loc[original_gct["NAME"].isin(data_df["Feature"])]

    pruned = open(name_of_file.strip('.odf')+'_pruned.gct', 'w')
    pruned.write("#1.2\n")
    #pruned.write("\t".join([str(df.shape[0]), str(df.shape[1])]) + "\n")
    pruned.write("\t".join([str(df.shape[0]), str(df.shape[1] - 2)]) + "\n")
    pruned.write(df.to_csv(sep='\t', index=False))
    pruned.close()

    print('\tOriginal GCT lenght=', len(original_gct))
print('\tPrunned GCT lenght=', len(data_df))
