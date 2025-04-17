with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "SmartHomeEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    linux-wifi-hotspot
    nodejs
    yarn
    nodePackages."@angular/cli"
  ];
}
