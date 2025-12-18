{
  description = "Small backend application";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonModule =
        with pkgs;
        (python313.withPackages (
          python-pkgs: with python-pkgs; [
            pyjwt
            passlib
            alembic
            fastapi
            fastapi-cli
            sqlalchemy
            asyncpg
            pytest
            httpx
            bcrypt
            passlib
            pyjwt
            python-multipart
            email-validator
            pydantic-settings
          ]
        ));
    in
    {
      shellHook = pkgs.mkShell {
        shellHook = ''
          exec fish
        '';
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = [ pythonModule ];
      };
    };
}
