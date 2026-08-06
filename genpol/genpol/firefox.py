from .bookmarks import parse_bookmarks
def generate_policy(homepage=None, search=None, searchurl=None, bookmarks_file=None, ublock=False):
    policies = {
        "DisableTelemetry": True,
        "DisablePocket": True,
        "PasswordManagerEnabled": True
    }
    if homepage:
        policies["Homepage"] = {
            "URL": homepage,
            "Locked": True
        }
    
    if search and searchurl:
        policies["SearchEngines"] = {
            "Default": search,
            "PreventInstalls": True,
            "Add": [{
                "Name": search,
                "URLTemplate": searchurl,
                "Method": "GET"
            }]
        }
    if bookmarks_file:
        folder_name, items = parse_bookmarks(bookmarks_file)
        if items:
            bookmark = [{"toplevel_name": folder_name}]
            for item in items:
                bookmark.append({"name": item["name"], "url": item["url"]})
            policies["ManagedBookmarks"] = bookmark
    if ublock:
        policies["ExtensionSettings"] = {
            "uBlock0@raymondhill.net": {
                "installation_mode": "force_installed",
                "install_url": "https://addons.mozilla.org/firefox/downloads/latest/ublock-origin/latest.xpi"
            }
        }
        policies["3rdparty"] = {
            "Extensions": {
                "uBlock0@raymondhill.net": {
                    "adminSettings": {
                        "selectedFilterLists": [
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
                        ]
                    }
                }
            }
        }
    return {"policies": policies}