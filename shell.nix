with import <nixpkgs> {};
stdenv.mkDerivation rec {
    name = "SmartHomeEnv";
    env = buildEnv { name = name; paths = buildInputs; };
    buildInputs = [
        arduino-ide
        python312Full
        python312Packages.aiohttp
        python312Packages.aiohttp-cors
        linux-wifi-hotspot
        nodejs
        yarn
        nodePackages."@angular/cli"
    ];
}
