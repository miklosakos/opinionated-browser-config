from .bookmarks import parse_bookmarks

def generate_policy(homepage=None, search=None, searchurl=None, bookmarks_file=None, ublock=False):
    policy = {
        "PasswordManagerEnabled": True,
        "AutofillAddressEnabled": True,
        "AutofillCreditCardEnabled": True,
        "ShowHomeButton": True,
        "DefaultBrowserSettingEnabled": False,
        "MetricsReportingEnabled": False,
        "DefaultGeolocationSetting": 2,
        "AIModeSettings": 1,
        "SafeBrowsingEnabled": True,
        "PasswordManagerEnabled": False,
        "AutofillCreditCardEnabled": False,
        "AutofillAddressEnabled": False,
        "HighEfficiencyModeEnabled": True,
        "MemorySaverModeSavings": 1,
        "AllowExperimentalAIForUsers": False,
        "BackgroundModeEnabled": False,
        "RestoreOnStartup": -1,
        "BookmarkBarEnabled": True,
        "EnableMediaRouter": False,
        "PrintingEnabled": False,
        "AutoplayAllowed": False,
        "WebAppInstallByUserEnabled": False,
        "HardwareAccelerationModeEnabled": True,
        "ChromeSuggestionsSettings": 1,
        "CreateThemesSettings": 1,
        "DevToolsGenAiSettings": 2,
        "GeminiActOnWebSettings": 1,
        "GeminiSparkSettings": 1,
        "GenAILocalFoundationalModelSettings": 1,
        "GenAiDefaultSettings": 2,
        "HelpMeWriteSettings": 2,
        "HistorySearchSettings": 2,
        "SearchContentSharingSettings": 1,
        "SmartTabSharingSettings": 1,
        "TabCompareSettings": 2,
        "DefaultNotificationsSetting": 2,
        "ScreenCaptureAllowed": True,
        "DefaultSensorsSetting": 2,
        "DefaultSerialGuardSetting": 2,
        "DefaultSmartCardConnectSetting": 2,
        "DefaultWebBluetoothGuardSetting": 2,
        "DefaultWebHidGuardSetting": 2,
        "DefaultWebUsbGuardSetting": 2,
        "DefaultWindowManagementSetting": 2,
        "AlternateErrorPagesEnabled": False,
        "AudioCaptureAllowed": True,
        "BuiltInAIAPIsEnabled": False,
        "ChromeDataRegionSetting": 2,
        "Disable3DAPIs": False,
        "CacheEncryptionEnabled": True,
        "DesktopSharingHubEnabled": False,
        "EnterpriseProfileBadgeToolbarSettings": 0,
        "BrowserGuestModeEnabled": False,
        "LocalNetworkAccessPermissionsPolicyDefaultEnabled": False,
        "AbusiveExperienceInterventionEnforce": True,
        "AdsSettingForIntrusiveAdsSites": 2,
        "AdvancedProtectionAllowed": True,
        "BrowserLabsEnabled": False,
        "FeedbackSurveysEnabled": False,
        "ForceGoogleSafeSearch": True,
        "GoogleSearchSidePanelEnabled": False,
        "MediaRecommendationsEnabled": False,
        "URLBlocklist": [
            "remotedesktop.google.com",
            "remotedesktop-pa.googleapis.com",
            "instantmessaging-pa.googleapis.com"
        ],
        "RemoteAccessHostFirewallTraversal": False,
        "BrowserSignin": 0,
        "SyncDisabled": True
    }

    if homepage:
        policy["HomepageLocation"] = homepage
        policy["HomepageIsNewTabPage"] = False
        policy["RestoreOnStartup"] = 1

    if search and searchurl:
        policy["DefaultSearchProviderEnabled"] = True
        policy["DefaultSearchProviderName"] = search
        policy["DefaultSearchProviderSearchURL"] = searchurl

    if bookmarks_file:
        foldername, items = parse_bookmarks(bookmarks_file)
        if items:
            policy["ManagedBookmarks"] = [{
                "name": foldername,
                "children": [{"name": item["name"], "url": item["url"]} for item in items]
            }]

    if ublock:
        policy["ExtensionInstallForcelist"] = [
            "ddkjiahejlhfcafbddmgiahcphecmpfh;https://clients2.google.com/service/update2/crx"
        ]

    return policy