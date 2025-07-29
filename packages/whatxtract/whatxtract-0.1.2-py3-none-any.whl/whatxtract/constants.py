"""Constants for the whatxtract package."""

# fmt: off
from pathlib import Path

try:
    from selenium.webdriver.common.by import By
except ImportError:
    import sys
    import subprocess
    print('[ * ] Installing selenium...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
    from selenium.webdriver.common.by import By


DEFAULT_WAIT                = 20
VCF_BATCH_SIZE              = 5000

PROFILE_DIR                 = Path.cwd() / 'WAProfiles'
OUTPUT_DIR                  = Path.cwd() / 'output'
VCF_DIR                     = OUTPUT_DIR / 'vcf_contacts'
WAMS_DB_PATH                = OUTPUT_DIR / 'wams_db.json'

APP__DIV                                    = (By.ID, 'app')
INITIAL_STARTUP__DIV                        = (By.ID, 'wa_web_initial_startup')
LOGIN_QR_CODE__DIV                          = (By.CSS_SELECTOR, 'div[data-ref]')
LOG_INTO_WA_WEB__TEXT                       = (By.XPATH, '//div[contains(text(), "Log into WhatsApp Web")]')
LOGIN_QR_SCAN_ME__CANVAS                    = (By.XPATH, '//canvas[@aria-label="Scan me!"]')
MAIN_NAV_BAR__DIV                           = (By.CSS_SELECTOR, '[data-js-navbar="true"]')
MAIN_SEARCH_BAR__SEARCH_BOX                 = (By.CSS_SELECTOR, 'div[contenteditable="true"][role="textbox"]')
MAIN_SEARCH_BAR__SEARCH_ICON                = (By.CSS_SELECTOR, '#side span[data-icon="search"]')
LOADING__TEXTS                              = ('End-to-end encrypted', 'Your messages are downloading')
INVALID_NUMBER__DIV                         = (By.XPATH, "//div[contains(text(), 'number shared via url is invalid')]")
NEW_CHAT__BUTTON                            = (By.CSS_SELECTOR, 'button[role="button"][title="New chat"]')
CONTACTS_CONTAINER_PARENT__DIV              = (By.CSS_SELECTOR, 'div.copyable-area')
CONTACTS_CONTAINER__DIV                     = (By.CSS_SELECTOR, 'div[data-tab="4"]')
CONTACT_ITEM__DIV                           = (By.CSS_SELECTOR, 'div[role="listitem"]')
BUTTON_ROLE__DIV                            = (By.CSS_SELECTOR, 'div[role="button"]')
CONTACT_INFO__SPAN                          = (By.CSS_SELECTOR, 'span[dir="auto"]')
CONTACT_AVATAR__IMG                         = (By.CSS_SELECTOR, 'img[draggable="false"]')
CONTACT_AVATAR__DEFAULT                     = (By.CSS_SELECTOR, 'span[data-icon="default-user"] svg')
CHAT_LIST_PARENT = PANE_SIDE__DIV           = (By.ID, 'pane-side')
CHAT_LIST__DIV                              = (By.CSS_SELECTOR, 'div[role="grid"][aria-label="Chat list"]')


class SELECTORS:
    """Selectors for Selenium."""
    APP__DIV = APP__DIV
    INITIAL_STARTUP__DIV = INITIAL_STARTUP__DIV
    LOGIN_QR_CODE__DIV = LOGIN_QR_CODE__DIV
    LOG_INTO_WA_WEB__TEXT = LOG_INTO_WA_WEB__TEXT
    LOGIN_QR_SCAN_ME__CANVAS = LOGIN_QR_SCAN_ME__CANVAS
    MAIN_NAV_BAR__DIV = MAIN_NAV_BAR__DIV
    MAIN_SEARCH_BAR__SEARCH_BOX = MAIN_SEARCH_BAR__SEARCH_BOX
    MAIN_SEARCH_BAR__SEARCH_ICON = MAIN_SEARCH_BAR__SEARCH_ICON
    LOADING__TEXTS = LOADING__TEXTS
    INVALID_NUMBER__DIV = INVALID_NUMBER__DIV
    NEW_CHAT__BUTTON = NEW_CHAT__BUTTON
    CONTACTS_CONTAINER_PARENT__DIV = CONTACTS_CONTAINER_PARENT__DIV
    CONTACTS_CONTAINER__DIV = CONTACTS_CONTAINER__DIV
    CONTACT_ITEM__DIV = CONTACT_ITEM__DIV
    BUTTON_ROLE__DIV = BUTTON_ROLE__DIV
    CONTACT_INFO__SPAN = CONTACT_INFO__SPAN
    CONTACT_AVATAR__IMG = CONTACT_AVATAR__IMG
    CONTACT_AVATAR__DEFAULT = CONTACT_AVATAR__DEFAULT
    CHAT_LIST_PARENT = CHAT_LIST_PARENT
    PANE_SIDE__DIV = PANE_SIDE__DIV
    CHAT_LIST__DIV = CHAT_LIST__DIV


VCF_TEMPLATE = """BEGIN:VCARD
VERSION:3.0
N:{last};{first};;;
FN:{full}
TEL;TYPE=CELL:{tel}
END:VCARD"""


INDEXEDDB_HELPERS = """
function getResultFromRequest(req) {
    return new Promise((resolve, reject) => {
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}

function openDB(name) {
    return new Promise((resolve) => {
        const req = indexedDB.open(name);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
    });
}
"""

INDEXEDDB_EXPORT_SCRIPT = INDEXEDDB_HELPERS + """
const callback = arguments[arguments.length - 1];
const delay = ms => new Promise(res => setTimeout(res, ms));
(async () => {
    var dbName = arguments[0];
    await delay(200);
    
    const db = await openDB(dbName);
    if (!db || db.objectStoreNames.length === 0) {
        console.warn("Skipping DB:", dbName, "(no object stores)");
        if (db) db.close();
    }
    await delay(200);
    
    const tx = db.transaction(db.objectStoreNames, 'readonly');
    const dbDump = {};

    for (const storeName of db.objectStoreNames) {
        const store = tx.objectStore(storeName);
        dbDump[storeName] = await getResultFromRequest(store.getAll());
    }
    
    db.close();
    await delay(200);

    callback(dbDump);
})().catch(e => {
    console.error("Snapshot failed", e);
    callback(null);
});
"""
