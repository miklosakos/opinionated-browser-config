# Opinionated browser configs

## Why?

I want to provide a helpful resource that targets Linux and macOS primarily to aid browser configuration with uBlock Origin (Lite) and other required settings in my opinion, hence the name of the repo.

## What does this do?

This disables most of the telemetry, notification permissions, AI and so on and so on in both Firefox and Chrome as much as I could find information about them.

## How to use

### `genpol`

`genpol` is a handy utility written to generate configuration files for both Apple macOS and Linux if you prefer not using Ansible nor Nix.
Usage:
```
-os / --system: provide the system's name, either linux or mac
-p / --browser: provide which browser you want the policy generated for, either chrome or firefox
-hp / --homepage: optional argument, sets the homepage, required format: http(s)://domain.tld/path/to/site
-b / --bookmarks: provide a bookmarks file, look at the example bookmarks file for an example
-s / --search: optional argument, allows you to set the default search engine, it needs to be used like this: 'Name,https://search.tld/?q='
-u / --ublock: tell the script you want uBlock Origin (Lite)
```
The generated files will go to the following path:
- `com.google.Chrome.plist`: `/Library/Managed Preferences/` or use an MDM solution or a deployment solution like JAMF
- `firefox_policies.json`:
  - on Apple macOS: `/Applications/Firefox.app/Contents/Resources/distribution/policies.json`, use an MDM solution or a deployment solution like JAMF
  - on Linux: `/etc/firefox/policies/policies.json`
- `chrome_policies.json`: `/etc/opt/chrome/policies/managed/`

Please note that Google Chrome policies can also be used with other Chromium derivatives but your mileage may vary!

---

### Ansible

You can use an inventory file, the Ansible playbook is preconfigured to handle any host matching the following inventory group: `workstation`.

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