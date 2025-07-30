import os
import yaml
import bp_config


COMMAND_SHELL_TEMPLATE = """
#!/bin/env bash

set -ue

{env_string}

if [ ! -d "{work_dir}" ]; then
    mkdir -p {work_dir}
fi
cd {work_dir}

START_TIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "status: start" > {status_filename}

/usr/bin/time -q -o {stat_filename} \
--format="\\ncode: %x\\ntime: %e\\ncpu: %P\\nmemory: %K\\ncputime: %S" \
{command_string} 1>{log_filename} 2>{err_filename} &
pid=$!
echo "status: runing" > {status_filename}
echo "pid: $pid" > {pid_filename}
wait $!

END_TIME=$(date +"%Y-%m-%d %H:%M:%S")

echo -e "start_time: $START_TIME\\nend_time: $END_TIME" >> {stat_filename}

echo "status: finish" > {status_filename}

"""


class Runner:
    def __init__(self, config):
        self.handler = bp_config.ConfigHandler()
        self._runner_config = config
        task_dir = self._runner_config.get("task_dir")
        if task_dir is None:
            raise ValueError("task_dir is empty")
        task_dir = os.path.abspath(task_dir)
        self._runner_config.update({"task_dir": task_dir})
        filenames = {
            "log_filename": f"{task_dir}/out.log",
            "err_filename": f"{task_dir}/err.log",
            "stat_filename": f"{task_dir}/stat.yaml",
            "status_filename": f"{task_dir}/status.yaml",
            "pid_filename": f"{task_dir}/pid.yaml",
            "run_shell_filename": f"{task_dir}/run.sh",
        }
        self._runner_config.update(filenames)
        self._init_status()
        self.init()

    def init(self):
        env_string = self._get_env_vars()
        command = self._runner_config.get("command", "")
        if command == "":
            raise ValueError("command is empty")
        if isinstance(command, list):
            command_string = " ".join(command)
        elif isinstance(command, str):
            command_string = command
        else:
            raise ValueError("command is not list or string")
        config = {
            "env_string": env_string, 
            "command_string": command_string
        }
        config.update(self._runner_config)
        content = COMMAND_SHELL_TEMPLATE.format(**config)
        self.run_shell_filename = self._runner_config.get(
            "run_shell_filename", "run.sh"
        )
        with open(self.run_shell_filename, "w") as f:
            f.write(content)
        self._command = f"bash {self.run_shell_filename}"


    def run(self):
        os.system(self._command)
        status = self.get_stat()
        if status.get("code") != 0:
            self._save_status("error")
        

    def cancel(self):
        pid = self.get_pid()
        if pid is not None:
            os.system(f"kill -9 {pid}")
        pass

    def delete(self):
        self.cancel()
        os.system(f"rm -rf '{self.task_dir}'")
        pass

    def _get_env_vars(self):
        res = ""
        n = 0
        env = self._runner_config.get("env", {})
        for k, v in env.items():
            res += f"export {k}='{v}'\n"
            n += 1
        env_flag = ""
        if n > 0:
            env_flag = "1"
        self._runner_config.update({"env_flag": env_flag})
        return res

    def get_pid(self):
        pid_filename = self._runner_config.get("pid_filename")
        info = self.handler.read_config(pid_filename)
        return info.get("pid", None)

    def get_status(self):
        status_filename = self._runner_config.get("status_filename")
        info = self.handler.read_config(status_filename)
        return info

    def get_stat(self):
        stat_filename = self._runner_config.get("stat_filename")
        info = self.handler.read_config(stat_filename)
        return info

    def get_log(self):
        log_filename = self._runner_config.get("log_filename")
        info = open(log_filename, encoding="UTF-8").read()
        return info

    def get_output(self):
        output_filename = self._runner_config.get("output_filename")
        info = open(output_filename, encoding="UTF-8").read()
        return info

    def _init_status(self):
        task_dir = self._runner_config.get("task_dir")
        if not os.path.exists(task_dir):
            os.makedirs(task_dir, exist_ok=True)
        self._save_status("init")

    def _save_status(self, status):
        status_filename = self._runner_config.get("status_filename")
        self.handler.write_config(status_filename, {"status": status})
