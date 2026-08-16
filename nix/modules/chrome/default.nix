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
    environment.systemPackages = [ pkgs.google-chrome ];

    programs.chromium = {
      enable = true;
      policies = lib.mkMerge [
        {
          ShowHomeButton = true;
          DefaultBrowserSettingEnabled = false;
          MetricsReportingEnabled = false;
          DefaultGeolocationSetting = 2;
          AIModeSettings = 1;
          SafeBrowsingEnabled = true;
          PasswordManagerEnabled = false;
          AutofillCreditCardEnabled = false;
          AutofillAddressEnabled = false;
          HighEfficiencyModeEnabled = true;
          MemorySaverModeSavings = 1;
          AllowExperimentalAIForUsers = false;
          BackgroundModeEnabled = false;
          RestoreOnStartup = -1;
          BookmarkBarEnabled = true;
          EnableMediaRouter = false;
          PrintingEnabled = false;
          AutoplayAllowed = false;
          WebAppInstallByUserEnabled = false;
          HardwareAccelerationModeEnabled = true;
          ChromeSuggestionsSettings = 1;
          CreateThemesSettings = 1;
          DevToolsGenAiSettings = 2;
          GeminiActOnWebSettings = 1;
          GeminiSparkSettings = 1;
          GenAILocalFoundationalModelSettings = 1;
          GenAiDefaultSettings = 2;
          HelpMeWriteSettings = 2;
          HistorySearchSettings = 2;
          SearchContentSharingSettings = 1;
          SmartTabSharingSettings = 1;
          TabCompareSettings = 2;
          DefaultNotificationsSetting = 2;
          ScreenCaptureAllowed = true;
          DefaultSensorsSetting = 2;
          DefaultSerialGuardSetting = 2;
          DefaultSmartCardConnectSetting = 2;
          DefaultWebBluetoothGuardSetting = 2;
          DefaultWebHidGuardSetting = 2;
          DefaultWebUsbGuardSetting = 2;
          DefaultWindowManagementSetting = 2;
          AlternateErrorPagesEnabled = false;
          AudioCaptureAllowed = true;
          BuiltInAIAPIsEnabled = false;
          ChromeDataRegionSetting = 2;
          Disable3DAPIs = false;
          CacheEncryptionEnabled = true;
          DesktopSharingHubEnabled = false;
          EnterpriseProfileBadgeToolbarSettings = 0;
          BrowserGuestModeEnabled = false;
          LocalNetworkAccessPermissionsPolicyDefaultEnabled = false;
          AbusiveExperienceInterventionEnforce = true;
          AdsSettingForIntrusiveAdsSites = 2;
          AdvancedProtectionAllowed = true;
          BrowserLabsEnabled = false;
          FeedbackSurveysEnabled = false;
          ForceGoogleSafeSearch = true;
          GoogleSearchSidePanelEnabled = false;
          MediaRecommendationsEnabled = false;
          URLBlocklist = [
            "remotedesktop.google.com"
            "remotedesktop-pa.googleapis.com"
            "instantmessaging-pa.googleapis.com"
          ];
          RemoteAccessHostFirewallTraversal = false;
          BrowserSignIn = 0;
          SyncDisabled = true;
        }

        # Conditional Homepage & Startup URLs
        (lib.mkIf (cfg.home != null) {
          HomepageLocation = cfg.home;
          HomepageIsNewTabPage = false;
          RestoreOnStartup = -1; # Open a list of URLs
          RestoreOnStartupURLs = [ cfg.home ];
        })

        # Conditional Search Engine
        (lib.mkIf (cfg.search != null) {
          DefaultSearchProviderEnabled = true;
          DefaultSearchProviderName = cfg.search.name;
          DefaultSearchProviderSearchURL = cfg.search.url;
        })

        # Conditional Managed Bookmarks
        (lib.mkIf (cfg.bookmarks != null) {
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