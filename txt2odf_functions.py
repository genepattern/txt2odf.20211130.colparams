import sys


def parse_arguments(args=sys.argv):
    txt_file = None
    id_col = None
    stat_col = None
    prune_gct = False
    gct = None
    cls = None

    arg_n = len(args)
    #if arg_n == 1:
    if arg_n < 4:
        sys.exit("Error message: No files were provided. This module needs a GCT and a CLS file to work.")
    #elif arg_n == 2:
    elif arg_n == 4:
        txt_file = args[1]
        id_col = args[2]
        stat_col = args[3]
        prune_gct = False
        gct = None
        cls = None

        print("Using txt_file=", txt_file)
        print("Using id_col=", id_col)
        print("Using stat_col=", stat_col)
        print("Using prune_gct=", prune_gct, '(default)')
        print("Using gct=", gct, '(default)')
        print("Using cls=", cls, '(default)')
    #elif arg_n == 3:
    elif arg_n == 5:
        txt_file = args[1]
        id_col = args[2]
        stat_col = args[3]
        #prune_gct = eval(args[2])
        prune_gct = eval(args[4])
        gct = None
        cls = None
        print("Using txt_file=", txt_file)
        print("Using id_col=", id_col)
        print("Using stat_col=", stat_col)
        print("Using prune_gct=", prune_gct)
        print("Using gct=", gct, '(default)')
        print("Using cls=", cls, '(default)')
    #elif arg_n == 4:
    elif arg_n == 6:
        txt_file = args[1]
        id_col = args[2]
        stat_col = args[3]
        #prune_gct = eval(args[2])
        prune_gct = eval(args[4])
        #gct = args[3]
        gct = args[5]
        cls = None
        print("Using txt_file=", txt_file)
        print("Using id_col=", id_col)
        print("Using stat_col=", stat_col)
        print("Using prune_gct=", prune_gct)
        print("Using gct=", gct)
        print("Using cls=", cls, '(default)')
    #elif arg_n == 5:
    elif arg_n == 7:
        txt_file = args[1]
        id_col = args[2]
        stat_col = args[3]
        #prune_gct = eval(args[2])
        prune_gct = eval(args[4])
        #gct = args[3]
        gct = args[5]
        #cls = args[4]
        cls = args[6]
        print("Using txt_file=", txt_file)
        print("Using id_col=", id_col)
        print("Using stat_col=", stat_col)
        print("Using prune_gct=", prune_gct)
        print("Using gct=", gct)
        print("Using cls=", cls)

    #return txt_file, prune_gct, gct, cls
    return txt_file, id_col, stat_col, prune_gct, gct, cls 

def dtype_to_odftype(dtypes):
    dtypes = dtypes.astype(str)
    
    return dtypes.map(
        ## This is probably awful
        lambda dt: "String" if dt == "object" else "double"
    )

def df2odf(data_df, vals, file_name='noname.odf'):
    new_dt = dtype_to_odftype(data_df.dtypes)

    colnames_no_colon = [
        colname.replace(":", "_")
        for colname in data_df.columns
    ]

    f = open(file_name, 'w')
    f.write("ODF 1.0\n")  # Hard-coding spance, not tab here.
    f.write("HeaderLines=19\n")  # hard-coding lines here. Needs to change.
    #f.write("COLUMN_NAMES:"+"\t".join(list(data_df))+"\n")
    f.write("COLUMN_NAMES:"+"\t".join(colnames_no_colon)+"\n")
    #f.write("COLUMN_TYPES:"+"\t".join(['int', 'String', 'String', 'double', 'double', 'double', 'double', 'double', 'double', 'double'])+"\n")  # TODO: automate this.
    f.write("COLUMN_TYPES:"+"\t".join(list(new_dt))+"\n")
    f.write("Model=Comparative Marker Selection\n")
    f.write("Dataset File="+vals['gct']+"\n")
    f.write("Class File="+vals['cls']+"\n")
    f.write("Permutations="+str(vals['n_perm'])+"\n")
    f.write("Balanced=false\n")
    f.write("Complete=false\n")
    f.write("Test Direction=2 Sided\n")
    f.write("Class 0="+vals['class_0']+"\n")
    f.write("Class 1="+vals['class_1']+"\n")
    f.write("Test Statistic="+vals['func']+"\n")
    f.write("pi0=TBD\n")
    f.write("lambda=TBD\n")
    f.write("pi0(lambda)=TBD\n")
    f.write("cubic spline(lambda)=TBD\n")
    f.write("Random Seed="+str(vals['rand_seed'])+"\n")
    f.write("Smooth p-values=true\n")
    f.write("DataLines="+str(vals['dat_lines'])+"\n")
    # f.write("RowNamesColumn=1\n")
    # f.write("RowDescriptionsColumn=2\n")
    f.write(data_df.to_csv(sep='\t', index=False, header=False))
