{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    packages = with pkgs; [
        arduino-ide
        python311Full
        linux-wifi-hotspot
        nodejs
        yarn
        nodePackages."@angular/cli"
    ];

    env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
        pkgs.stdenv.cc.cc.lib
        pkgs.libz
    ];
}
