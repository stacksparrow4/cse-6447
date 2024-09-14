import sys
if 'pwn' in sys.modules:
  print("You must import cse BEFORE importing pwntools for the patcher to work.")
  print("Eg.")
  print("\timport cse")
  print("\tfrom pwn import *")
  exit(1)

import pwn
import os.path

from unittest.mock import patch

pwn.context.arch = 'amd64'
pwn.context.terminal = ["/opt/pwntools-fake-term.sh"]

HOMEDIR_FOLDER = "comp6447-binaries"

global_ssh = None
def get_ssh():
  global global_ssh
  if global_ssh is None:
    with open(".connection/zid", "r") as f:
      zid = f.read().strip()
    global_ssh = pwn.ssh(zid, 'cse.unsw.edu.au', keyfile='.connection/id_cse')
    assert run_remote_cmd(f'mkdir -p {HOMEDIR_FOLDER}') == 0
    global_ssh.set_working_directory(os.path.join(global_ssh.pwd().decode(),  HOMEDIR_FOLDER))
  return global_ssh

def run_remote_cmd(x):
  c = get_ssh().system(x)
  res = c.poll()
  while res is None:
    pwn.sleep(0.01)
    res = c.poll()
  return res

def upload_executable_file(file_location):
  filename = os.path.basename(file_location)
  get_ssh().upload_file(file_location, filename)
  assert run_remote_cmd(f'chmod +x {filename}') == 0

def retrieve_file_path_from_argv(argv, executable):
  if executable is not None:
    return executable
  elif type(argv) is list:
    return argv[0]
  elif type(argv) is str:
    return argv
  else:
    raise RuntimeError("Could not understand argv to cse_process")

def cse_process(argv, executable=None, *args, **kwargs):
  file_path = retrieve_file_path_from_argv(argv, executable)  
  upload_executable_file(file_path)

  return get_ssh().process(argv, executable, *args, **kwargs)

def cse_gdb_debug(argv, *args, **kwargs):
  print("Please do not use gdb.debug() as it is not supported yet.")
  print("Instead, use:")
  print("\tp = process(...)")
  print("\tgdb.attach(p, ...)")
  exit(1)

orig_gdb_attach = pwn.gdb.attach
def cse_gdb_attach(target, gdbscript='', exe=None, gdb_args=None, sysroot=None, api=False):
  if not os.path.exists("/tmp/pwntoolscode-waiting"):
    print("Tried to spawn terminal but VSCode did not have the terminal waiting.")
    print("Perhaps you forgot to run using the Play button in VSCode?")
    exit(1)

  return orig_gdb_attach(target, gdbscript=gdbscript, exe=exe, gdb_args=gdb_args, ssh=global_ssh, sysroot=sysroot, api=api)

def create_callable_constructor(callable):
  def const(*args, **kwargs):
    return callable
  return const

patch('pwn.process', new_callable=create_callable_constructor(cse_process)).start()
patch('pwn.gdb.debug', new_callable=create_callable_constructor(cse_gdb_debug)).start()
patch('pwn.gdb.attach', new_callable=create_callable_constructor(cse_gdb_attach)).start()
