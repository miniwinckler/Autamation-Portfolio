import pickle

def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

def load_cookies(driver, path="cookies.pkl"):
    with open(path, "rb") as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            pass