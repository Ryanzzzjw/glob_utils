
def visualise(d:dict,lvl:int=0, disp_val:bool=False)-> None:
    """print tree of the passed dict and nested dict

    Args:
        d (dict): dictionary to display
        lvl (int, optional): start level. Defaults to 0.
        disp_val (bool, optional): if `True` values will be displayed on top. Defaults to False.
    
    Example: of output 
            KEY                       LEVEL           TYPE
        -------------------------------------------------------------------------------
        eit_dataset               0               <class 'dict'>
        FMDL_GEN                1               <class 'int'>
        dir_path                1               <class 'str'>
        name                    1               <class 'str'>
        samples_filenames       1               <class 'NoneType'>
        samples_folder          1               <class 'str'>
        samples_indx            1               <class 'NoneType'>
        src_filenames           1               <class 'NoneType'>
        src_folder              1               <class 'str'>
        src_indx                1               <class 'NoneType'>
        time_computation        1               <class 'NoneType'>
        type                    1               <class 'str'>
        fwd_model                 0               <class 'dict'>
        boundary                1               <class 'numpy.ndarray'>
        boundary_numbers        1               <class 'numpy.ndarray'>
        electrode               1               <class 'dict'>
            000                   2               <class 'dict'>
            nodes               3               <class 'numpy.ndarray'>
            obj                 3               <class 'str'>
            pos                 3               <class 'numpy.ndarray'>
            shape               3               <class 'float'>
            z_contact           3               <class 'float'>
            001                   2               <class 'dict'>
            nodes               3               <class 'numpy.ndarray'>

    """


    # go through the dictionary alphabetically 
    for k in sorted(d):

        indent = '  '*lvl # indent the table to visualise hierarchy
        t = str(type(d[k]))
        
        if disp_val:
            val= str(d[k])
            header= '{:<25} {:<15} {:<10} {:30}'.format('KEY','LEVEL','TYPE', 'VAL')
            line= "{:<25} {:<15} {:<10} {:30}".format(indent+str(k),lvl,t, val)
        else:
            header= '{:<25} {:<15} {:<10}'.format('KEY','LEVEL','TYPE')
            line="{:<25} {:<15} {:<10}".format(indent+str(k),lvl,t)

        # print the table header if we're at the beginning
        if lvl == 0 and k == sorted(d)[0]:
            print(header)
            print('-'*79)

        # print details of each entry
        print(line)

        # if the entry is a dictionary
        
        if type(d[k])==dict:
            # visualise THAT dictionary with +1 indent
            visualise(d[k],lvl+1)