{
  description = "Reproducible defensive notebook environment for the MetaPlay incident report";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/49a4bd0573c376468dd7996ddb6f9fa31d8c4d97";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
          compilerLib = pkgs.stdenv.cc.cc.lib;
        in {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python312
              uv
              deno
              nodejs_22
              nushell
              gnumake
            ];

            UV_PYTHON = "${pkgs.python312}/bin/python";
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ compilerLib ];

            shellHook = ''
              echo "Defensive notebook shell: Python 3.12, uv, Deno, Node.js, Nushell"
              echo "Run: uv sync"
            '';
          };
        });
    };
}
