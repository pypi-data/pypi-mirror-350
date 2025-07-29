{
  description = "isqtools";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs @ { flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.git-hooks.flakeModule inputs.treefmt-nix.flakeModule ];
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, lib, ... }: {
        pre-commit = {
          check.enable = true;
          settings.hooks = {
            nixpkgs-fmt.enable = true;
            isort = {
              enable = true;
              settings.profile = "black";
            };
            black.enable = true;
            shfmt = {
              enable = true;
              args = [ "-i" "2" ];
            };
            taplo.enable = true;
            prettier = {
              enable = true;
              excludes = [ "flake.lock" ];
            };
          };
        };

        treefmt = {
          projectRootFile = "flake.nix";
          programs = {
            nixpkgs-fmt.enable = true;
            shfmt.enable = true;
            taplo.enable = true;
            isort.enable = true;
            black.enable = true;
            prettier.enable = true;
            just.enable = true;
          };
          settings.global = {
            excludes = [ ];
          };
        };

        #python env override
        packages.python312 = pkgs.python312.override {
          packageOverrides = self: super: {
            isqtools = self.callPackage ./. {
              inherit (inputs.gitignore.lib) gitignoreSource;
            };
            openfermion = self.callPackage ./pkgs/openfermion.nix { };
          };
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ config.pre-commit.devShell config.treefmt.build.devShell ];
          packages = [
            (self'.packages.python312.withPackages (p: with p ; [
              isqtools
              hatchling
              openfermion
              autograd
              requests
              pytest
              pytest-cov
              pyscf
              matplotlib
              torch
              torchvision

              sphinx
              myst-parser
              sphinx-autodoc-typehints
              sphinx-copybutton
              furo
              nbsphinx
              jupyter

              build
              twine
            ]))
          ] ++ (with pkgs; [
            pandoc
            nbqa
          ]);

          shellHook = ''
            export PATH="$HOME/opt/isqc/isqc-0.2.5:$PATH"
          '';
        };
      };
      flake = { };
    };
}
