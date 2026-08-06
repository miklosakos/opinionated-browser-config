# Opinionated browser configs

## Why?

I want to provide a helpful resource that targets Linux and macOS primarily to aid browser configuration with uBlock Origin (Lite) and other required settings in my opinion, hence the name of the repo.

## How to use

### Ansible

You can use an inventory file, the Ansible playbook is preconfigured to handle any host matching the following inventory group: `workstation`.

Change `ansible/playbook.yml` to match your requirements, i.e. bookmarks, homepage etc.

```sh
ansible-playbook -i /path/to/inventory.ini ./ansible/playbook.yml --ask-pass --ask-become-pass
```

### NixOS

On NixOS import the repository into your flake, for example:

```nix
{
  description = "Main NixOS flake config";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    browser-policies.url = "github:miklosakos/opinionated-browser-config";
  };

  outputs = { self, nixpkgs, browser-policies }: {
    nixosConfigurations.hostname = nixpkgs.lib.nixosSystem {
      modules = [
        browser-policies.nixosModules.default
        {
          nixpkgs.config.allowUnfree = true; #only needed if google-chrome is being installed

          opinionated.firefox = {
            enable = true;
            homepage = "https://google.com";
            
            search = {
              name = "Kagi";
              urlTemplate = "https://kagi.com/search?q={searchTerms}";
            };

            bookmarks = {
              folderName = "Folder";
              links = [
                { name = "Bookmark 1"; url = "https://google.com"; }
                { name = "Bookmark 2"; url = "https://drive.google.com"; }
                { name = "Bookmark 3"; url = "https://kagi.com"; }
              ];
            };
            
            ublock = true;
          };

          opinionated.chrome = {
            enable = true;
            homepage = "https://google.com";

            search = {
              name = "Kagi";
              url = "https://kagi.com/search?q={searchTerms}";
            };

            bookmarks = {
              folderName = "Folder";
              links = [
                { name = "Bookmark 1"; url = "https://google.com"; }
                { name = "Bookmark 2"; url = "https://drive.google.com"; }
                { name = "Bookmark 3"; url = "https://kagi.com"; }
              ];
            };
            
            ublock = true;
          };
        }
      ];
    };
  };
}
```