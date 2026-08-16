# Opinionated browser configs

## Why?

I want to provide a helpful resource that targets Linux and macOS primarily to aid browser configuration with uBlock Origin (Lite) and other required settings in my opinion, hence the name of the repo.

## What does this do?

This disables most of the telemetry, notification permissions, AI and so on and so on  in both Firefox and Chrome as much as I could find information about them plus enables uBlock Origin (Firefox) / uBlock Origin Lite (Chrome).

## How to use

### Ansible

You can use an inventory file, the Ansible playbook is preconfigured to handle all hosts presents in the inventory file.

Change `ansible/playbook.yml` to match your requirements, i.e. bookmarks, homepage etc.

```sh
ansible-playbook -i /path/to/inventory.ini ./ansible/playbook.yml --ask-pass --ask-become-pass
```

---
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
    nixosConfigurations.hostname = nixpkgs.lib.
     
    nixosSystem {
      modules = [
        nixpkgs.config.allowUnfree = true; #only needed if chrome is being used
        browser-policies.nixosModules.default
        {
          opinionated.firefox = {
            enable = true;
            homepage = "https://google.com";
            
            search = {
              name = "Kagi";
              url = "https://kagi.com/search?q={searchTerms}";
            };

            bookmarks = {
              folder = "Folder";
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
            home = "https://google.com";

            search = {
              name = "Kagi";
              url = "https://kagi.com/search?q={searchTerms}";
            };

            bookmarks = {
              folder = "Folder";
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