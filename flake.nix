{
  description = "Opinionated browser config for Chrome and Firefox";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }@inputs: {
    nixosModules = {
      firefox = ./modules/firefox;
      chrome = ./modules/chrome;
      default = {
        imports = [ ./modules/firefox ./modules/chrome ];
      };
    };
  };
}