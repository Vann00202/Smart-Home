## Webserver

#### Running the webserver

1. Ensure that `angular-cli` and `nodejs` are installed
    - This can be done by installing the nix package manager and running `nix-shell shell.nix` in the project root
    - Alternatively `angular-cli` can be installed by first installing nodejs and then running `npm install -g @angular/cli`
1. Ensure that ports `3000` and `4200` are not blocked by firewall
1. `cd` into the rebuild directory at `Smart-Home/pi-src/webserver/rebuild`
1. Ensure required node packages are installed via `npm install`
1. Run the server on the address/port with ng serve --address 192.168.12.1 --port 4200
