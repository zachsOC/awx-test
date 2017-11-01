import yaml

from demo import Run

if __name__ == '__main__':
    # load yaml input
    with open('scenario.yml', 'r') as fh:
        config = yaml.load(fh)

    # create run object
    run = Run(config)

    # start
    run.go()
