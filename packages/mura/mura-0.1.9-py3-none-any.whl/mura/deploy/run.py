import os, importlib, logging
import torch
from lightning.pytorch.loggers import WandbLogger

from mura.repo.git_utils import understand_env
from mura.deploy.util import cprint, class_to_dict_update, check_wifi
from mura.deploy.set_gpu import set_gpu
import time

class Run:
    def __init__(self, args):
        self.args = args
        
    def __enter__(self):
        # _time = time.time()
        version, action_number, action_id, task_id, run_id, paramfile, logfile = self.args[1:]
        action_number = int(action_number)
        action_id = int(action_id)
        task_id = int(task_id)
        run_id = int(run_id)
        
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        py_logger = logging.getLogger('auto')
        py_logger.setLevel(logging.INFO)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        py_logger.addHandler(consoleHandler)

        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(logFormatter)
        py_logger.addHandler(fileHandler)
            
        # load class 'param' from inside from paramfile.
        module_name = 'param'
        module_path = os.path.join(os.getcwd(), paramfile)
        
        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Now you can use the module
        else:
            py_logger.warn(f"File not found: {module_path}")
        _config = module
        # py_logger.info(f'elapsed time: {time.time() -_time:.2f}s')
        
        if hasattr(_config, 'config'):
            config = _config.config
            param = config.actions[action_id].tasks[task_id].runs[run_id]
            action = config.actions[action_id]
            task = action.tasks[task_id]
            action_name = action.action_name
            task_name = task.task_name
            run_name = param.name if hasattr(param, 'name') else ''
            ngpu = action.ngpu
            project_name = config.project_name
        else:
            print(_config)
            param = _config.param
            action_name = ''
            task_name = ''
            run_name = param.name if hasattr(param, 'name') else ''
            ngpu = 1
            project_name = param.project_name
            
        # py_logger.info(f'elapsed time: {(time.time() - _time):.2f}s')
        param.gpus, self.lock_gpu_commands = set_gpu(ngpu)
        
        version, task, save_path = understand_env()
        fname = version + f'.{action_number}.' + '.'.join([str(action_id), str(task_id), str(run_id)])
        if action_name:
            fname += '-' + action_name
        if task_name:
            fname += '-' + task_name
        if run_name:
            fname += '-' + run_name

        # os.makedirs(os.path.join(save_path,"wandb/"), exist_ok=True)
        param_dict = class_to_dict_update(param)
        py_logger.info(str(param_dict))
        offline = not check_wifi()
        py_logger.info(f'wandb offline: {offline}')
        wandb_logger = WandbLogger(project=project_name, name=fname,
                        version=fname, config=param_dict,# log_model='all',
                        offline = offline)
                        # save_dir=save_path) # has issues with sync.
                        
                        
        # TODO add watch stuff from train.py
                        
        return param, wandb_logger, py_logger, version, save_path

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, 'lock_gpu_commands'):
            self.unlock_gpu()
        
    def unlock_gpu(self):
        for cmd in self.lock_gpu_commands:
            os.system(cmd)