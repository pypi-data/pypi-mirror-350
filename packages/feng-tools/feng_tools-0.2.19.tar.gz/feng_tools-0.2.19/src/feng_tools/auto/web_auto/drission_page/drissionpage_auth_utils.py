import json
import os.path
default_cookies_file = 'cookies.json'
default_local_storage_file = 'local_storage.json'
default_session_storage_file = 'session_storage.json'


def save_auth(browser, auth_save_path:str,
              cookies_file:str = None,
              storage_file:str = None,
              session_file:str = None,
              is_save_session:bool=True):
    """保存认证信息"""
    if not cookies_file:
        cookies_file = os.path.join(auth_save_path, default_cookies_file)
    if not storage_file:
        storage_file = os.path.join(auth_save_path, default_local_storage_file)
    if not session_file:
        session_file = os.path.join(auth_save_path, default_session_storage_file)
    # 保存cookies
    save_cookies(browser, cookies_file)
    # 保存本地存储
    save_local_storage(browser, storage_file)
    if is_save_session:
        # 保存会话存储（可选，根据需求决定是否保存）
        save_session_storage(browser, session_file)

def restore_auth(browser, auth_save_path:str,
              cookies_file:str = None,
              storage_file:str = None,
              session_file:str = None,
              is_save_session:bool=True):
    """恢复Cookie、本地存储和会话存储"""
    load_auth(browser, auth_save_path, cookies_file, storage_file, session_file, is_save_session)

def load_auth(browser, auth_save_path:str,
              cookies_file:str = None,
              storage_file:str = None,
              session_file:str = None,
              is_save_session:bool=True):
    """加载Cookie、本地存储和会话存储"""
    if not cookies_file:
        cookies_file = os.path.join(auth_save_path, default_cookies_file)
    if not storage_file:
        storage_file = os.path.join(auth_save_path, default_local_storage_file)
    if not session_file:
        session_file = os.path.join(auth_save_path, default_session_storage_file)
    # 加载cookies
    load_cookies(browser, cookies_file)
    # 加载本地存储
    load_local_storage(browser, storage_file)
    if is_save_session:
        # 加载会话存储（可选，根据需求决定是否保存）
        load_session_storage(browser, session_file)
    # 刷新页面使认证信息生效
    browser.refresh()


def save_cookies(browser, cookies_file:str = None):
    cookies_file = cookies_file if cookies_file else default_cookies_file
    cookies = browser.get_cookies()
    with open(cookies_file, 'w') as f:
        json.dump(cookies, f)

def load_cookies(browser, cookies_file:str = None) -> bool:
    cookies_file = cookies_file if cookies_file else default_cookies_file
    if os.path.exists(cookies_file):
        try:
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
                # 设置Cookie
                for cookie in cookies:
                    browser.set_cookie(cookie)
                return True
        except Exception as e:
            return False
    return False


def save_local_storage(browser, storage_file:str=None):
    """保存本地存储到文件"""
    storage_file = storage_file if storage_file else default_local_storage_file
    storage = browser.evaluate('''() => {
        const result = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            result[key] = localStorage.getItem(key);
        }
        return result;
    }''')
    with open(storage_file, 'w') as f:
        json.dump(storage, f)

def load_local_storage(browser, storage_file:str=None):
    """从文件加载本地存储"""
    storage_file = storage_file if storage_file else default_local_storage_file
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            storage = json.load(f)
        for key, value in storage.items():
            browser.evaluate(f'''localStorage.setItem('{key}', '{value}');''')



def save_session_storage(browser,  session_file:str=None):
    """保存会话存储到文件"""
    session_file = session_file if session_file else default_session_storage_file
    storage = browser.evaluate('''() => {
        const result = {};
        for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            result[key] = sessionStorage.getItem(key);
        }
        return result;
    }''')
    with open(session_file, 'w') as f:
        json.dump(storage, f)

def load_session_storage(browser, session_file:str=None):
    """从文件加载会话存储"""
    session_file = session_file if session_file else default_session_storage_file
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            storage = json.load(f)
        for key, value in storage.items():
            browser.evaluate(f'''sessionStorage.setItem('{key}', '{value}');''')


def save_indexed_db(browser, db_name, indexed_db_file='indexed_db.json'):
    """保存IndexedDB"""
    data = browser.evaluate('''async (dbName) => {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(dbName);
            const result = {};

            request.onsuccess = function(event) {
                const db = event.target.result;
                const transaction = db.transaction(db.objectStoreNames, 'readonly');

                db.objectStoreNames.forEach(storeName => {
                    const store = transaction.objectStore(storeName);
                    const getAllRequest = store.getAll();

                    getAllRequest.onsuccess = function() {
                        result[storeName] = getAllRequest.result;
                        // 所有数据都获取后resolve
                        if (Object.keys(result).length === db.objectStoreNames.length) {
                            resolve(result);
                            db.close();
                        }
                    };
                    getAllRequest.onerror = function() {
                        reject(new Error(`获取存储对象 ${storeName} 失败`));
                        db.close();
                    };
                });
            };

            request.onerror = function() {
                reject(new Error('打开数据库失败'));
            };
        });
    }''', db_name)

    with open(indexed_db_file, 'w') as f:
        json.dump(data, f)