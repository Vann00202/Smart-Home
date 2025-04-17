with import <nixpkgs> {};
stdenv.mkDerivation rec {
    name = "SmartHomeEnv";
    env = buildEnv { name = name; paths = buildInputs; };
    buildInputs = [
        arduino-ide
        python312Full
        python312Packages.flask
        python312Packages.flask-cors
        linux-wifi-hotspot
        nodejs
        yarn
        nodePackages."@angular/cli"
    ];
}
