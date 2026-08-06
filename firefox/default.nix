{ config, lib, pkgs, ... }:

let
  cfg = config.opinionated.firefox;
in
{
  options.opinionated.firefox = {
    enable = lib.mkEnableOption "Setup Firefox with the opinionated config";

    home = lib.mkOption {
      type = lib.types.nullOr lib.types.str;
      default = null;
      description = "Change the default homepage";
    };

    search = lib.mkOption {
      type = lib.types.nullOr (lib.types.submodule {
        options = {
          name = lib.mkOption {
            type = lib.types.str;
            description = "Name of the search engine (e.g., Kagi).";
          };
          urlTemplate = lib.mkOption {
            type = lib.types.str;
            description = "URL template with {searchTerms}.";
          };
        };
      });
      default = null;
      description = "Default search engine configuration.";
    };
    ublock = lib.mkEnableOption "Deploy and configure uBlock Origin";
    bookmarks = lib.mkOption {
      type = lib.types.nullOr (lib.types.submodule {
        options = {
          folder = lib.mkOption {
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
            description = "List of managed bookmarks.";
          };
        };
      });
      default = null;
      description = "Configure bookmarks management.";
    };
  };

config = lib.mkIf cfg.enable {
    programs.firefox = {
      enable = true;
      policies = lib.mkMerge [
        # Base policies
        {
          DisableTelemetry = true;
          DisableFirefoxStudies = true;
          DisablePocket = true;
          PasswordManagerEnabled = false;
          HardwareAcceleration = true;
          NewTabPage = false;
          Permissions = {
            Notifications = { BlockNewRequests = true; };
          };
          FirefoxHome = {
            Search = true;
            TopSites = false;
            SponsoredTopSites = false;
            Highlights = false;
            Pocket = false;
            Snippets = false;
            SponsoredPocket = false;
          };
        }

        # Conditional Homepage
        (lib.mkIf (cfg.homepage != null) {
          Homepage = {
            URL = cfg.homepage;
            Locked = true;
          };
        })

        # Conditional Search Engine
        (lib.mkIf (cfg.search != null) {
          SearchEngines = {
            Default = cfg.search.name;
            PreventInstalls = false;
            Add = [
              {
                Name = cfg.search.name;
                URLTemplate = cfg.search.url;
                Method = "GET";
              }
            ];
          };
        })

        # Conditional Managed Bookmarks (Transforms submodule structure into Firefox's expected format)
        (lib.mkIf (cfg.bookmarks != null) {
          ManagedBookmarks = [
            { toplevel_name = cfg.bookmarks.folder; }
          ] ++ map (link: {
            name = link.name;
            url = link.url;
          }) cfg.bookmarks.links;
        })

        # Conditional Extensions
        (lib.mkIf cfg.ublock {
          ExtensionSettings = {
            "uBlock0@raymondhill.net" = {
              installation_mode = "force_installed";
              install_url = "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi";
            };
          };
          "3rdparty" = {
            Extensions = {
              "uBlock0@raymondhill.net" = {
                adminSettings = {
                  selectedFilterLists = [
                    "user-filters",
                    "ublock-filters",
                    "ublock-badware",
                    "ublock-privacy",
                    "ublock-quick-fixes",
                    "ublock-unbreak",
                    "ublock-experimental",
                    "easylist",
                    "adguard-generic",
                    "adguard-mobile",
                    "easyprivacy",
                    "adguard-spyware-url",
                    "block-lan",
                    "urlhaus-1",
                    "curben-phishing",
                    "plowe-0",
                    "dpollock-0",
                    "fanboy-cookiemonster",
                    "ublock-cookies-easylist",
                    "adguard-cookies",
                    "ublock-cookies-adguard",
                    "fanboy-social",
                    "adguard-social",
                    "fanboy-thirdparty_social",
                    "fanboy-ai-suggestions",
                    "easylist-chat",
                    "easylist-newsletters",
                    "easylist-notifications",
                    "easylist-annoyances",
                    "adguard-mobile-app-banners",
                    "adguard-other-annoyances",
                    "adguard-popup-overlays",
                    "adguard-widgets",
                    "ublock-annoyances",
                    "ALB-0",
                    "BGR-0",
                    "CHN-0",
                    "CZE-0",
                    "DEU-0",
                    "EST-0",
                    "ara-0",
                    "spa-1",
                    "spa-0",
                    "FIN-0",
                    "FRA-0",
                    "GRC-0",
                    "HRV-0",
                    "HUN-0",
                    "IDN-0",
                    "ISR-0",
                    "IND-0",
                    "IRN-0",
                    "ISL-0",
                    "ITA-0",
                    "JPN-1",
                    "KOR-1",
                    "LTU-0",
                    "LVA-0",
                    "MKD-0",
                    "NLD-0",
                    "NOR-0",
                    "POL-3",
                    "POL-0",
                    "ROU-1",
                    "RUS-0",
                    "RUS-1",
                    "SWE-1",
                    "SVN-0",
                    "THA-0",
                    "TUR-0",
                    "UKR-0",
                    "VIE-1"
                  ];
                };
              };
            };
          };
        })
      ];
    };
  };
}