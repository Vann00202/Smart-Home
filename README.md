# Smart Home

## Required Dependencies

There are a couple ways to install all the necessary packages. Either through a nix shell or by manually installing via the distributions package manager (likely apt)

#### Nix Shell Method

This is mostly recommended for getting a reproducible testing environment. The steps are as follows:

1. Install the nix package manager either for the entire system or just one user:
    - Local user: `sh <(curl -L https://nixos.org/nix/install) --no-daemon`
    - Local user: `sh <(curl -L https://nixos.org/nix/install) --daemon`
1. Update the channels via `nix-channel --update`
1. Enter the build environment by running `nix-shell shell.nix`
    - The build environment can be exited at any time by running `exit`
1. This should install the main dependencies. However some of the python/node libraries still need to be installed
1. For node run `cd pi-src/webserver/rebuild && npm install`
1. For python do the following:
    - run `python -m venv ./venv`
    - run `source ./venv/bin/activate`
    - run `python -m pip install -r requirements.txt`
    - Note: If adding any pip packages while in the env run `pip freeze > requirements.txt`


#### Manual method

This assumes you are using apt as the package manager. The steps are as follows:
NOTE: This uses a PPA for installing linux-wifi-hotspot. The tool can alternatively be built from source if needed.

1. Run `sudo apt update`
1. Make sure we can install PPAs by running `sudo apt install software-properties-common`
1. Add required PPA `sudo add-apt-repository ppa:lakinduakash/lwh`
1. Run `sudo apt update` again
1. Run sudo apt install `nodejs npm python3 python3-pip arduino linux-wifi-hotspot`
1. Install the necessary python packages `python3 -m pip install aiohttp aiohttp-cors`
1. Make sure angular-cli is installed `npm install -g @angular/cli`

