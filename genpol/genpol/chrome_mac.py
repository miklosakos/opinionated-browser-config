import plistlib
from .bookmarks import parse_bookmarks

def generate_policy(homepage=None, search=None, searchurl=None, bookmarks_file=None, ublock=False):
    policy = {
        "PasswordManagerEnabled": True,
        "AutofillAddressEnabled": True,
        "AutofillCreditCardEnabled": True
    }

    if homepage:
        policy["HomepageLocation"] = homepage
        policy["HomepageIsNewTabPage"] = False
        policy["RestoreOnStartup"] = 1
        policy["ShowHomeButton"] = True,
        policy["DefaultBrowserSettingEnabled"] = False,
        policy["MetricsReportingEnabled"] = False,
        policy["DefaultGeolocationSetting"] = 2,
        policy["AIModeSettings"] = 1,
        policy["SafeBrowsingEnabled"] = True,
        policy["PasswordManagerEnabled"] = False,
        policy["AutofillCreditCardEnabled"] = False,
        policy["AutofillAddressEnabled"] = False,
        policy["HighEfficiencyModeEnabled"] = True,
        policy["MemorySaverModeSavings"] = 1,
        policy["AllowExperimentalAIForUsers"] = False,
        policy["BackgroundModeEnabled"] = False,
        policy["RestoreOnStartup"] = -1,
        policy["BookmarkBarEnabled"] = True,
        policy["EnableMediaRouter"] = False,
        policy["PrintingEnabled"] = False,
        policy["AutoplayAllowed"] = False,
        policy["WebAppInstallByUserEnabled"] = False,
        policy["HardwareAccelerationModeEnabled"] =  True,
        policy["ChromeSuggestionsSettings"] = 1,
        policy["CreateThemesSettings"] = 1,
        policy["DevToolsGenAiSettings"] =  2,
        policy["GeminiActOnWebSettings"] = 1,
        policy["GeminiSparkSettings"] = 1,
        policy["GenAILocalFoundationalModelSettings"] = 1,
        policy["GenAiDefaultSettings"] = 2,
        policy["HelpMeWriteSettings"] = 2,
        policy["HistorySearchSettings"] = 2,
        policy["SearchContentSharingSettings"] = 1,
        policy["SmartTabSharingSettings"] = 1,
        policy["TabCompareSettings"] = 2,
        policy["DefaultNotificationsSetting"] = 2,
        policy["ScreenCaptureAllowed"] = True,
        policy["DefaultSensorsSetting"] = 2,
        policy["DefaultSerialGuardSetting"] = 2,
        policy["DefaultSmartCardConnectSetting"] = 2,
        policy["DefaultWebBluetoothGuardSetting"] = 2,
        policy["DefaultWebHidGuardSetting"] = 2,
        policy["DefaultWebUsbGuardSetting"] = 2,
        policy["DefaultWindowManagementSetting"] = 2,
        policy["AlternateErrorPagesEnabled"] = False,
        policy["AudioCaptureAllowed"] = True,
        policy["BuiltInAIAPIsEnabled"] = False,
        policy["ChromeDataRegionSetting"] = 2,
        policy["Disable3DAPIs"] = False,
        policy["CacheEncryptionEnabled"] = True,
        policy["DesktopSharingHubEnabled"] = False,
        policy["EnterpriseProfileBadgeToolbarSettings"] = 0,
        policy["BrowserGuestModeEnabled"] = False,
        policy["LocalNetworkAccessPermissionsPolicyDefaultEnabled"] = False,
        policy["AbusiveExperienceInterventionEnforce"] = True,
        policy["AdsSettingForIntrusiveAdsSites"] = 2,
        policy["AdvancedProtectionAllowed"] = True,
        policy["BrowserLabsEnabled"] = False,
        policy["FeedbackSurveysEnabled"] = False,
        policy["ForceGoogleSafeSearch"] = True,
        policy["GoogleSearchSidePanelEnabled"] = False,
        policy["MediaRecommendationsEnabled"] = False,
        policy["BrowserSignin"] = 0,
        policy["SyncDisabled"] = True,


    if search and searchurl:
        policy["DefaultSearchProviderEnabled"] = True
        policy["DefaultSearchProviderName"] = search
        policy["DefaultSearchProviderSearchURL"] = searchurl

    if bookmarks_file:
        folder_name, items = parse_bookmarks(bookmarks_file)
        if items:
            policy["ManagedBookmarks"] = [{
                "name": folder_name,
                "children": [{"name": item["name"], "url": item["url"]} for item in items]
            }]

    if ublock:
        policy["ExtensionInstallForcelist"] = [
            "ddkjiahejlhfcafbddmgiahcphecmpfh;https://clients2.google.com/service/update2/crx"
        ]

    # Convert dictionary to binary/xml plist bytes using standard library
    return plistlib.dumps(policy, fmt=plistlib.FMT_XML)