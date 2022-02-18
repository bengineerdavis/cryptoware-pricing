# cryptoware-pricing

[cryptoware-pricing](https://github.com/bengineerdavis/cryptoware-pricing) is a project aimed at making it easier to predict the future price of PC hardware for hardware enthusiasts by determining a relationship to cryptocurrency prices.

## Motivation
As a frustrated PC hardware enthusiast that is also facinated by data analysis, I want a better way of knowing how to read the cryptocurrency markets and their stranglehold on the outrageous pricing for PC components, so I know when I can finally afford to make more custom PCs again.

Maybe you feel the same way :(

## Important!
I ```gitignore```'d some local files such as ```requirements.txt``` and ```schema.sql```. 

I've set up the project with the expectation that you will generate those files locally as part of installation, setup, and usage.

## Installation

1. Download the [repository](https://github.com/bengineerdavis/cryptoware-pricing) to use locally. Pick and/or create the local directory where you want the repository to live!

Learn more about using [remote repositories](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories)

### Using HTTPS
```bash
git clone https://github.com/bengineerdavis/cryptoware-pricing.git
```

### Using [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
```bash
git clone git@github.com:bengineerdavis/cryptoware-pricing.git
```

2. Set your virtual environment.

```python
# for this example, we'll name our virtual environment "venv"
python3 -m venv venv
```

3. Launch our newly created virtual environment from the root direcotry of the repository we just cloned.

```bash
# We'll need to do this each time we want to use the virtual environment
source venv/bin/activate

# to exit the virtual environment when we're done:
deactivate
```

4. Go to this link and click the Download button.

```http
https://www.kaggle.com/raczeq/ethereum-effect-pc-parts/metadata
```

5. From the root of downloaded repository, unzip the archive into our ```data``` directory.

```bash
unzip Downloads/archive.zip -d data/
```

6. Finally, install your dependencies in the virtual environment you just made.

```bash
# update pip
python -m pip install --upgrade pip

# install our dependency manager, pip-tools
python -m pip intall pip-tools

# run pip-tools to install our dependencies from requirements.in
pip-compile && pip-sync
```

## Setup

Once you have your installation done, there's several more steps to do to get started. Keep in mind, I am using a Linux machine--make sure you have a ```bash``` terminal installed on your machine. Mac should run this code with relatively few issues.

```bash
#Make all the scripts in the ```scripts``` directory executable.
chmod +x scripts/*

# then, run the sqlstamp.sql to generate our boilerplate SQL script, named "schema.sql"
python scripts/sqlstamp.py
```

After generating ```schema.sql```, we'll make some edits to it to match the schema outlined in the kaggle site of the original dataset creator.

This code represents my initial exploration of existing data.

## Usage
COMING SOON?

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)