import os
import shutil
import subprocess
import time


def xtb_optimize_geometries(path_to_xyz, 
                            path_to_xtbopt, 
                            gfn_xtb=2,
                            opt_lvl='normal',
                            num_opt_cycles=None,
                            solvent=None,
                            unpaired_e=None,
                            verbose=False,
                            silent=False,
                            ):
    if not os.path.exists(path_to_xyz):
        print(f"Directory '{path_to_xyz}' does not exist.")
        return

    xyz_files_list = os.listdir(path_to_xyz)
    xyz_files_list = sorted(xyz_files_list)
    if not xyz_files_list:
        print(f"Directory '{path_to_xyz}' is empty.")
        return
    #check if all files in path_to_xyz directory are have xyz extensions
    for xyz_file in xyz_files_list:
        if not xyz_file.endswith('.xyz'):
            print(f"Directory '{path_to_xyz}' contains non-XYZ files.\nConsider removing these files.")
            return

    if not os.path.exists(path_to_xtbopt):
        print(f"Directory '{path_to_xtbopt}' does not exist.")
        return
    
    xtbopt_files_list = os.listdir(path_to_xtbopt)
    if xtbopt_files_list:
        print(f"Directory '{path_to_xtbopt}' is not empty. \nPlease empty the directory before starting the xtb geometry optimization.")
        return
    
    xtb_flags = []

    if gfn_xtb==2:
        pass
    elif gfn_xtb==1 or gfn_xtb==0:
        xtb_flags+=["--gfn", gfn_xtb]
    else:
        print("Invalid xTB parametrization. Choose from 2 (default), 1 or 0. Integer input.")
        return



    # check if chosen opt lvl is valid
    valid_opt_lvls=["crude", "sloppy", "loose", "lax", "normal", "tight", "vtight", "extreme"]
    if opt_lvl not in valid_opt_lvls:
        print(f'Chosen xTB geometry optimization level is not valid.\n'+
              'Please choose one from the list: ', valid_opt_lvls)
        return
    xtb_flags+=["--opt", opt_lvl]

    if num_opt_cycles is not None:
        if not isinstance(num_opt_cycles, int):
            print(f"Num_opt_cycles shall be in int format, but {type(num_opt_cycles)} was given instead.")
            return
        xtb_flags+=["--cycles", str(num_opt_cycles)]

    if solvent is not None:
        ##check if the solvent is correct
        available_solvents = ["acetone", 'acetonitrile', 'benzene', 'ch2cl2', 'chcl3', 'cs2', 
                                    'dioxane', 'dmf', 'dmso', 'ether', 'ethylacetate', 'furane', 
                                    'hexane', 'methanol', 'nitromethane', 'toluene', 'thf', 'water']
        if not isinstance(solvent, str):
            print(f"Solvent input shall be in string format, but {type(solvent)} was given instead.")
            return
        elif solvent.lower() not in available_solvents:
            print(f"Invalid solvent choice. \nPlease choose one from the list: ", available_solvents)
            return
        xtb_flags+=["--alpb", solvent]

    if unpaired_e is not None:
        ##check if the format is correct
        xtb_flags+=["--uhf", unpaired_e]
    
    if verbose is True:
        xtb_flags+=['--verbose',]
    elif silent is True:
        xtb_flags+=['--silent',]
    else:
        pass
    
    print(xyz_files_list)

    for i, xyz_file in enumerate(xyz_files_list):
        
        start = time.time()
        os.makedirs(path_to_xtbopt+f"/{i}")
        xyz_for_xtb_opt = path_to_xtbopt+f"/{i}/{xyz_file}"
        shutil.copy(path_to_xyz+f"/{xyz_file}", xyz_for_xtb_opt)
        os.chdir(path_to_xtbopt+f"/{i}")
        subprocess.run(["xtb", xyz_for_xtb_opt] + xtb_flags)
        ##
        ##add checking if xtb optimization crashed for the file or was successfull


        end = time.time()  
        print(end-start)

        ##
        ##get geometry optimization statistics including (1) elapsed time for each input, (2) num of iterations for each, (3) num successful, (4) num failed.
    return


