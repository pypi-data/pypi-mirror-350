# BP Runner

BP Runner 是一个轻量级的命令行任务执行引擎，用于管理和监控长时间运行的业务流程。

## 功能特性

- ✅ 支持命令行任务执行与监控
- ✅ 自动生成执行脚本和环境配置
- ✅ 提供任务状态、PID、执行统计信息记录
- ✅ 支持任务取消和清理
- ✅ 完善的日志记录和错误输出

## 安装

```bash
pip install bp-runner
```

## 配置文件

创建配置文件 config.yaml:

```yaml

command: ls -l /etc  # 要执行的命令
env: 
  ENV1: value1       # 环境变量
  ENV2: value2
task_dir: ./task     # 任务目录
work_dir: ./work     # 工作目录
```

## 运行任务

1. 创建 Runner 实例

```python

from bp_runner import Runner

runner = Runner(config)
runner.run()
```

2. 命令行运行

```bash
bp-runner -c config.yaml
```

## 配置选项

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------| 
| command | str/list | 是 | 要执行的命令 | 
| task_dir | str | 是 | 任务输出目录 | 
| work_dir | str | 否 | 命令工作目录 | 
| env | dict | 否 | 环境变量配置 |

## 任务管理

```python

# 获取任务状态
status = runner.get_status()

# 获取执行统计
stats = runner.get_stat()

# 取消任务
runner.cancel()

# 清理任务
runner.delete()
```

## 输出文件

任务执行后会生成以下文件:

```text
status.yaml - 任务状态
pid.yaml - 进程ID
stat.yaml - 执行统计
output.log - 标准输出
err.log - 错误输出
run.sh - 生成的执行脚本
```

许可证
MIT License - 详见 LICENSE 文件