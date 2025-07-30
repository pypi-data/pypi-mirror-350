import click
import bp_config
import bp_runner

@click.command(
    name="bp-runner",
    context_settings={"help_option_names": ["--help", "-h"]}
)
@click.option('--config', '-c', default='config.yaml', help='配置文件路径')
def main(config):
    config_handler = bp_config.ConfigHandler()
    data = config_handler.read_config(config)
    runner = bp_runner.Runner(data)
    runner.run()
    pass

if __name__ == '__main__':
    main()