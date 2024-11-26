{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {pkgs = import nixpkgs {inherit system;};});
  in {
    devShells = forEachSupportedSystem ({pkgs}: {
      default = pkgs.mkShell {
        # venvDir = "./.venv";
        packages = with pkgs; [
          (pkgs.python312.withPackages (python-pkgs:
            with python-pkgs; [
              # venvShellHook
              pip

              pandas
              numpy
              scipy
              sympy
              scikit-learn
              matplotlib
              seaborn
            ]))

          ruff
        ];
      };
    });
  };
}
