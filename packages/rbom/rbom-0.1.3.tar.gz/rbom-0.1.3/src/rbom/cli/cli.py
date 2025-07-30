import os
import sys
from typing import NamedTuple
import json
import click

from parsers.rbom_parser import MetaData, RBOMParser
from policies.policy_handler import PolicyHandler

# from parsers.rbom_parser import MetaData, RBOMParser

# from rbom_parser import RBOMParser, MetaData
# from ..policies.policy_handler import PolicyHandler


######################
# consts 
######################

FILE_PATH = "rbom_content_cli.json"


######################
# helpers 
######################
def k_echo(text: str, color:str):
    click.echo(click.style(text, fg=color, bold=True))


def get_file_content():
    with open(FILE_PATH, 'r') as file:
        data = json.load(file)
        return data

def write_file_content(rbom_content:dict):
    file = open(FILE_PATH, "w")
    file.write(json.dumps(rbom_content))

######################
# click
######################

class Colors(NamedTuple):
    red = "red"
    cyan = "cyan"
    bright_blue = "bright_blue"
    bright_green = "bright_green"


@click.group()
def group():
    pass


@click.command()
@click.argument('path', type=click.types.STRING)
def load(path):
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
    k_echo(text=f"Loading {path}", color=Colors.bright_blue)
    rbom = RBOMParser.load_rbom(path)
    write_file_content(rbom)
    k_echo(text=f"Loaded {path}", color=Colors.bright_green)



@click.command()
@click.option('--name', default="unknown", help='The name of the attribute', type=click.types.STRING)
@click.option('--value', default="unknown", help='The value of the attribute')
def set_attribute(name, value):
    if name not in MetaData.items:
        raise InterruptedError(f"{name} is not a valid attribute name")


    is_policies, is_sbom, is_distribution = False, False, False
    if name == MetaData.policies:
        is_policies = True
    elif name == MetaData.distribution:
        is_distribution = True
    elif name == MetaData.sbom:
        is_sbom = True


    k_echo(text=f"Setting attribute {name} to {value}", color=Colors.bright_blue)

    rbom_content = get_file_content()
    rbom_content = RBOMParser.embed_attribute(
        rbom_content,
        name, 
        value, 
        is_policies=is_policies, 
        is_distribution=is_distribution, 
        is_sbom=is_sbom,)

    write_file_content(rbom_content)
    k_echo(text=f"Attribute {name} has been set", color=Colors.bright_green)
    

@click.command()
@click.option('--public-key-path', default="unknown", help='Path to public_key.pem', type=click.types.STRING)
@click.option('--repository', default="unknown", help='Full repository name org/repo', type=click.types.STRING)
@click.option('--commit-sha', default="unknown", help='Git commit sha', type=click.types.STRING)
@click.option('--github-token', default="unknown", help='GitHub access token', type=click.types.STRING)
@click.argument('path')
def sign(path, public_key_path, repository, commit_sha, github_token):
    """
    path: path to private key
    """
    if 'unknown' in [public_key_path, repository, commit_sha, github_token]:
        raise Exception("These signing parameters are required: --public-key-path, --repository, --commit-sha, --github-token")

    rbom_content = get_file_content()


    #################
    # policiies
    #################
    k_echo(text=f"Processing policies...", color=Colors.cyan)
    policies = PolicyHandler.parse_policies(
        rbom_content=rbom_content,
        repo_full_name=repository,
        commit_sha=commit_sha,
        github_token=github_token,
    )
    rbom_content = RBOMParser.embed_attribute(rbom_content, MetaData.policies, policies, is_policies=True)
    k_echo(text=f"Policies complete", color=Colors.bright_green)
    #################
    # signing
    #################
    k_echo(text=f"Signing...", color=Colors.bright_blue)
    signature = RBOMParser.sign_rbom_secure(rbom_content, path)
    rbom_content = RBOMParser.embed_signature(rbom_content, signature=signature)
    k_echo(text=f"Signing complete", color=Colors.bright_green)
    #################
    # saving
    #################
    k_echo(text=f"Saving...", color=Colors.bright_blue)
    RBOMParser.save_rbom(rbom_content, 'signed.rbom.yaml')
    k_echo(text=f"RBOM signed and saved ✅ to 'signed.rbom.yaml'", color=Colors.bright_green)
    #################
    # verify
    #################
    k_echo(text=f"Verifying signiture...", color=Colors.bright_blue)
    is_valid = RBOMParser.verify_rbom_signature(rbom_content, signature, public_key_path)
    if is_valid:
        k_echo(text=f"RBOM signature verified ✅", color=Colors.bright_green)
    else:
        k_echo(text=f"Invalid RBOM signature ❌", color=Colors.red)
        sys.exit()


# group.add_command(hello)
group.add_command(load)
group.add_command(set_attribute)
group.add_command(sign)

if __name__ == '__main__':
    try:
        group()
    except Exception as e:
        k_echo(text=f"#################################", color=Colors.red)
        k_echo(text=f"An exception occured: ", color=Colors.red)
        k_echo(text=str(e), color=Colors.red)
        k_echo(text=f"#################################", color=Colors.red)



'''
LOCAL DEV


# load rbom
python src/rbom/cli/cli.py load "src/rbom/example.rbom.yaml"

# set attribute
```bash
python src/rbom/cli/cli.py set-attribute --name=actor --value=prof
```

# sign and save
```bash
python src/rbom/cli/cli.py sign "keys/private_rbom_key.pem" --public-key-path="keys/public_rbom_key.pem" --repository="spockops/rbom" --commit-sha="214124412214" --github-token="ghyp21214412412" 

```

HATCH 
```bash
hatch env prune
hatch run xcli load "src/rbom/example.rbom.yaml"

```
'''