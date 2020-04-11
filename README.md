## python rougelike testing stuff :)

### setup

    virtualenv  env --python=python3    # make a new virtual env
    source env/bin/activate             # bash
    #source env/bin/activate.fish        # fish
    pip install -r requirements.txt


### starting

    # activate virtualenv, then:
    python main.py


### view logs

the logger is configured to log to `./log.txt`

just run tail on it, to get a live log:

    tail --follow log.txt




