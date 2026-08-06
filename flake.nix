{
  description = "Opinionated browser config for Chrome and Firefox";
  outputs = inputs: {
    nixosModules = rec {
      firefox = ./nix/modules/firefox;
      chrome = ./nix/modules/chrome;
      default = {
        imports = [ firefox chrome ];
      };
    };
  };
}