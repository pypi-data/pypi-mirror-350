from config_mujoco import *
import sysconfig

pysite = sysconfig.get_paths()["purelib"]
file = pysite+"/gymnasium_robotics/envs/assets/kitchen_franka/kitchen_assets/kitchen_env_model.xml"
# file = '/home/mtoussai/git/MuJoCo2Rai/kitchen_dataset/RUSTIC_ONE_WALL_SMALL.xml'

print('=====================', file)
C = Config_Mujoco(file, visualsOnly=True)
C.view(True)