import argparse,json, os
from abacustest.lib_prepare.abacus import WriteKpt, WriteInput, gen_stru
from pathlib import Path
from abacustest.lib_model.model_012_band import PrepBand

def gen_abacus_inputs(stru_files, stru_type, pp_path, orb_path, input_param=None, kpoint=None):
    """
    Generate the abacus input files.
    
    Parameters
    ----------
    stru_files : list
        The structure files, should be a list of cif or dpdata supported data
    stru_type : str
        The structure type, cif or dpdata supported format
    pp_path : str
        The pseudopotential path
    orb_path : str
        The orbital path
    input_param : dict
        The specified input parameter, which will used in INPUT
    kpoint : list
        The kpoint setting, should be a list of three int, will generate a KPT file
    
    Returns
    -------
    job_path : dict
        The job path, which is a dict, key is the job path, value is {"element": element, "pp": pp, "orb": orb}
    """
    job_path = gen_stru(stru_files, stru_type, pp_path, orb_path, tpath=".")
    # job_path is dict: key is the job path, value is {"element": element, "pp": pp, "orb": orb}
    # the pp and orb file has been linked to the job path
    
    if job_path is None or len(job_path) == 0:
        raise ValueError("No valid structure file found.")
    
    # write INPUT file and KPT file
    
    default_input = {
        "ecutwfc": 100,
        "calculation": "scf",
        "basis_type": "pw"
    }
    # will find the recommand ecutwfc from ecutwfc.json file, and if this file is not found, 100 will be used
    if os.path.isfile(os.path.join(pp_path, "ecutwfc.json")):
        recommand_ecutwfc = json.load(open(os.path.join(pp_path, "ecutwfc.json"), "r"))
    else:
        recommand_ecutwfc = None
    ecutwfc_set = False
    if input_param is not None:
        default_input.update(input_param)
        if "ecutwfc" in input_param:
            ecutwfc_set = True
        
    for path, job in job_path.items():
        element = job["element"]
        if not ecutwfc_set and recommand_ecutwfc is not None:
            default_input["ecutwfc"] = max([recommand_ecutwfc[i] for i in element])
        # write the input file
        WriteInput(default_input, os.path.join(path, "INPUT"))
        
        if kpoint is not None:
            WriteKpt(kpoint, os.path.join(path, "KPT"))
        
    return job_path
            


def EasyRun(input_param):
    """
    Easy run an abacus job by simply providing a parameter file and structure files.
    """
    default_param = {
        "stru_file": None, # structure file should be a list of cif or dpdata supported data
        "stru_type": None, # structure type, cif or dpdata supportted format
        "job_type": "scf", # the job type
        "pp_path": None, # the pseudopotential path
        "orb_path": None, # the pseudopotential type
        "input_param": None, # the specified input parameter, which will used in INPUT
        "kpoint": None, # the kpoint setting, should be a list of threee int, will generate a KPT file
        "machine": None, # the machine type
        "command": None, # the command to run abacus
        "image": None, # the image to run ABACUS
    }
    
    param = {k: v if k not in input_param else input_param[k] for k,v in default_param.items()}
    if param["stru_file"] is None:
        raise ValueError("The structure file should be specified.")
    if param["stru_type"] is None:
        raise ValueError("The structure type should be specified.")
    if param["pp_path"] is None:
        raise ValueError("The pseudopotential path should be specified.")
    if param["machine"] is None:
        raise ValueError("The machine type should be specified.")
    if param["command"] is None:
        raise ValueError("The command to run abacus should be specified.")
    
    supported_job_type = ["scf", "band"]
    if param["job_type"] not in supported_job_type:
        raise ValueError(f"The job type should be one of {supported_job_type}, but got {param['job_type']}.")
    
    jobs = gen_abacus_inputs(param["stru_file"], param["stru_type"], 
                                 param["pp_path"], param["orb_path"], 
                                 param["input_param"], param["kpoint"])
    job_path = list(jobs.keys())
    # modify the INPUT for different job type, and gen the run.sh script
    if param["job_type"] == "scf":
        for ijob in job_path:
            Path(os.path.join(ijob, "run.sh")).write_text(param['command'])
        run_script = "bash run.sh"
    elif param["job_type"] == "band":
        prep_band = PrepBand(job_path, run_command=param['command'])
        _, run_script = prep_band.run()
    else:
        raise ValueError(f"Unsupported job type: {param['job_type']}.")
    
    # generate the parameter setting for abacustest submit
    setting = {
        "save_path": "results",
        "run_dft": {
            "example": job_path,
            "command": run_script,
            "image": param["image"],
            "bohrium": {
                "scass_type": param["machine"],
                "job_type": "container",
                "platform": "ali"
            }
        }
    }
    json.dump(setting, open("setting.json", "w"), indent=4)
    print("The inputs are generated in", ", ".join(job_path))
    # run the abacustest submit
    # read the user input to ask if the user want to run the abacustest submit
    #run = input("Do you want to run the abacustest submit? (y/n): ")
    #if run.lower().strip() in ["y","yes"]:
    #    os.system("abacustest submit -p setting.json")
    #else:
    print("You can execute the command 'abacustest submit -p setting.json' to run the abacustest to submit all jobs to remote.")
    print(f"Or you can 'cd' to each job path and execute '{run_script}' to run the job.")

def EasyRunArgs(parser):  
    parser.description = "Easy run an ABACUS job by simply providing a parameter file and structure file."
    parser.add_argument('-p', '--paramfile', type=str,  help='The parameter file, should be .json type', required=True)
    return parser

def main():
    parser = argparse.ArgumentParser()
    param = EasyRunArgs(parser).parse_args()
    EasyRun(param)
    
if __name__ == "__main__":
    main()