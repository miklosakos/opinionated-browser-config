{ config, lib, pkgs, ... }:

let
  cfg = config.opinionated.chrome;
in
{
  options.opinionated.chrome = {
    enable = lib.mkEnableOption "Setup Chrome with the opinionated config";

    home = lib.mkOption {
      type = lib.types.nullOr lib.types.str;
      default = null;
      description = "Change the default homepage and startup page.";
    };

    search = lib.mkOption {
      type = lib.types.nullOr (lib.types.submodule {
        options = {
          name = lib.mkOption {
            type = lib.types.str;
            description = "Name of the search engine (e.g., Kagi).";
          };
          url = lib.mkOption {
            type = lib.types.str;
            description = "Search URL template with {searchTerms}.";
          };
        };
      });
      default = null;
      description = "Search engine configuration.";
    };

    ublock = lib.mkEnableOption "Deploy and configure uBlock Origin";

    bookmarks = lib.mkOption {
      type = lib.types.nullOr (lib.types.submodule {
        options = {
          folderName = lib.mkOption {
            type = lib.types.str;
            description = "Top-level folder name for the bookmarks.";
          };
          links = lib.mkOption {
            type = lib.types.listOf (lib.types.submodule {
              options = {
                name = lib.mkOption {
                  type = lib.types.str;
                  description = "Bookmark display name.";
                };
                url = lib.mkOption {
                  type = lib.types.str;
                  description = "Bookmark target URL.";
                };
              };
            });
            default = [];
            description = "List of bookmarks inside the folder.";
          };
        };
      });
      default = null;
      description = "Optional managed bookmarks.";
    };
  };

  config = lib.mkIf cfg.enable {
    # Ensure google-chrome package is installed system-wide
    environment.systemPackages = [ pkgs.google-chrome ];

    programs.chromium = {
      enable = true;
      policies = lib.mkMerge [
        # Base privacy/feature policies
        {
          MetricsReportingEnabled = false;
          PasswordManagerEnabled = false;
          AutofillAddressEnabled = false;
          AutofillCreditCardEnabled = false;
          TranslateEnabled = false;
          SpellcheckEnabled = true;
        }

        # Conditional Homepage & Startup URLs
        (lib.mkIf (cfg.home != null) {
          HomepageLocation = cfg.home;
          HomepageIsNewTabPage = false;
          RestoreOnStartup = 4; # Open a list of URLs
          RestoreOnStartupURLs = [ cfg.home ];
        })

        # Conditional Search Engine
        (lib.mkIf (cfg.searchEngine != null) {
          DefaultSearchProviderEnabled = true;
          DefaultSearchProviderName = cfg.search.name;
          DefaultSearchProviderSearchURL = cfg.search.url;
        })

        # Conditional Managed Bookmarks
        (lib.mkIf (cfg.managedBookmarks != null) {
          ManagedBookmarks = [
            {
              name = cfg.bookmarks.folderName;
              children = map (link: {
                name = link.name;
                url = link.url;
              }) cfg.bookmarks.links;
            }
          ];
        })

        (lib.mkIf cfg.ublock {
          ExtensionInstallForcelist = [
            "ddkjiahejlhfcafbddmgiahcphecmpfh;https://clients2.google.com/service/update2/crx"
          ];
        })
      ];
    };
  };
}