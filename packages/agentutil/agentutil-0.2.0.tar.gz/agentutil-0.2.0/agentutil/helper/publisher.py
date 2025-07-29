from agentutil.models.news import NewsStatus, NewsORM, News as NewsSchema
from agentutil.helper.sql_client import get_db


from tenacity import retry, stop_after_attempt, wait_random_exponential
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from time import sleep
import urllib.parse
import requests
import shutil
import os

load_dotenv(override=True)

HEADLESS = bool(os.getenv("HEADLESS"))
SELENIUM_URL = os.getenv("SELENIUM_URL")

# ============================================================================================================================

def extract_image_links(content: str) -> list:
    soup = BeautifulSoup(content, "html.parser")
    image_tags = soup.find_all("img")
    image_links = [img.get("src") for img in image_tags if img.get("src")]
    return image_links

# ============================================================================================================================

def download_images(image_urls, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    allowed_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    images_data = []

    for idx, url in enumerate(image_urls):
        image_info = {
            "source_url": url,
            "downloaded_path": None,
            "success_download": False
        }

        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path.lower()

        if not path.endswith(allowed_extensions):
            print(f"⛔️ رد شد (پسوند نامعتبر): {url}")
            images_data.append(image_info)
            continue

        def try_download(target_url, referer=None):
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "DNT": "1",
                "Upgrade-Insecure-Requests": "1"
            }
            if referer:
                headers["Referer"] = referer

            try:
                response = requests.get(target_url, timeout=30, headers=headers)
                if response.status_code == 200:
                    return response
                else:
                    print(f"❌ خطا در دانلود {target_url}: وضعیت {response.status_code}")
            except Exception as e:
                print(f"❌ استثناء در دانلود {target_url}: {e}")
            return None

        # تلاش اول با URL کامل
        response = try_download(url)

        # تلاش دوم با حذف query string و افزودن referer
        if not response:
            stripped_url = urllib.parse.urlunparse(parsed_url._replace(query=""))
            referer = f"{parsed_url.scheme}://{parsed_url.netloc}"
            response = try_download(stripped_url, referer=referer)
            if response:
                print(f"✅ موفق با URL ساده‌شده و شبیه‌سازی مرورگر: {stripped_url}")

        if response:
            file_ext = os.path.splitext(parsed_url.path)[1]
            filename = f"{idx + 1}{file_ext}"
            filepath = os.path.join(save_folder, filename)

            try:
                with open(filepath, 'wb') as f:
                    f.write(response.content)

                image_info["downloaded_path"] = os.path.abspath(filepath)
                image_info["success_download"] = True
            except Exception as e:
                print(f"❌ خطا در ذخیره فایل {filepath}: {e}")

        images_data.append(image_info)

    return images_data

# ============================================================================================================================

def create_driver(headless=False, remote=False):

    options = webdriver.ChromeOptions()

    options.add_argument('--disable-hang-monitor')

    if headless:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
    })

    options.page_load_strategy = 'none'
    
    if remote:
        return webdriver.Remote(command_executor=SELENIUM_URL, options=options)
    
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ============================================================================================================================

def login_to_admin_panel(driver, username: str, password: str, cms_login_url: str):
    try:
        cms_url = f"{cms_login_url}/admin/fa"
        driver.get(cms_url)
        driver.maximize_window()
        sleep(1)

        captcha_check = driver.find_elements(By.XPATH, "//label[@for='sec_code' and contains(text(), 'کد امنیت')]")
        if captcha_check:
            return False, "صفحه لاگین با کپچا مواجه شده است."

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "enter"))).click()
        
        if "/admin/index.php" in driver.current_url:
            return False, "نام کاربری و رمزعبور اشتباه است."
        
        return True, None
    
    except Exception as e:
        return False, str(e)

# ============================================================================================================================

def open_submit_news_page(driver):
    send_news_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='ارسال خبر']"))).get_attribute("href")
    driver.get(send_news_link)

    # رفتن به iframe مربوط به فرم ارسال خبر
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    iframe_src = iframe.get_attribute("src")
    driver.get(iframe_src)

# ============================================================================================================================

def submit_new_news(driver, news: NewsSchema):
    # وارد کردن عنوان خبر
    title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "title")))
    title_input.send_keys(news.title)

    # وارد کردن خلاصه خبر
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='subtitle']"))).send_keys(news.summary)

    # وارد کردن متن خبر
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='کد منبع']"))).click()

    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tox-textarea")))
    body.send_keys(news.content)

    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='ذخيره' and contains(@class, 'tox-button')]")))
    save_button.click()
    sleep(1)
    
    driver.switch_to.default_content()

    sleep(1)

    status_select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "status")))
    status_select = Select(status_select_element)
    status_select.select_by_value("N")

    sleep(1)

    edit_after_send_checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "edit_after_send")))
    edit_after_send_checkbox.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "send_news_button"))).click()

    sleep(3)

    news_id_span = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "news-info-bar")))
    news_id = int(news_id_span.text)

    return True, news_id

# ============================================================================================================================

def upload_images_in_csm(driver, abs_downloaded_image_path):
    for image in abs_downloaded_image_path:

        upload_input = driver.find_element(By.CSS_SELECTOR, "#multi_upload_container input[type='file']")
        driver.execute_script("arguments[0].removeAttribute('multiple');", upload_input)

        upload_input.send_keys(image)

        submit_button = driver.find_element(By.NAME, "submit")
        submit_button.click()
        sleep(1)    

# ============================================================================================================================

def open_album_page(driver):
    album_page_link = driver.find_element(By.XPATH, "//a[text()='لیست عکس های ارسالی']")
    album_page_link.click()
    sleep(1)

# ============================================================================================================================

def get_uploaded_image_links(driver):
    album_images = driver.find_elements(By.TAG_NAME, "img")
    cms_images_urls = [image.find_element(By.XPATH, "parent::a").get_attribute("href") for image in album_images[::-1]]
    return cms_images_urls

# ============================================================================================================================

def replace_image_URLs(driver, zipped_image_urls):
    # وارد کردن متن خبر
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='کد منبع']"))).click()

    sleep(1)
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tox-textarea")))

    old_textarea_data = body.get_attribute("value")

    for key, value in zipped_image_urls.items():
        old_textarea_data = old_textarea_data.replace(key, value)

        key_encoded = key.replace("&", "&amp;")
        old_textarea_data = old_textarea_data.replace(key_encoded, value)

    body.clear()
    body.send_keys(old_textarea_data)

    sleep(1)

    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='ذخيره' and contains(@class, 'tox-button')]")))
    save_button.click()
    sleep(1)

    driver.switch_to.default_content()

    edit_news_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "edit_news_btn")))
    edit_news_button.click()

# ============================================================================================================================

def delete_downloaded_images(news_id):
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    images_folder_path = os.path.join(APP_DIR, "temp", str(news_id))

    if os.path.exists(images_folder_path) and os.path.isdir(images_folder_path):
        try:
            shutil.rmtree(images_folder_path)
            print(f"پوشه {images_folder_path} با موفقیت حذف شد.")
        except Exception as e:
            print(f"خطا در حذف پوشه: {e}")
    else:
        print(f"پوشه {images_folder_path} پیدا نشد.")

# ============================================================================================================================

def change_status_to_published(driver):

    # رفتن به صفحه وضعیت خبر
    status_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='وضعیت خبر']"))).get_attribute("href")
    driver.get(status_link)
    sleep(1)

    # تغییر وضعیت به منتشره
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "status")))
    select = Select(select_element)
    select.select_by_value("P")
    sleep(1)

    # ذخیره تغییرات
    submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "submit")))
    submit_button.click()
    sleep(1)

    # !بعد از این با خطا مواجه خواهید شد

# ============================================================================================================================

def add_images_to_news(driver, image_links, news_id):

    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    save_folder = os.path.join(APP_DIR, "temp", str(news_id))

    # دانلود عکس‌ها
    images_data = download_images(image_links, save_folder)
    downloaded_paths = [img["downloaded_path"] for img in images_data if img["success_download"]]
    sleep(1)

    if not downloaded_paths:
        print("⛔ هیچ عکسی با موفقیت دانلود نشد. عملیات متوقف شد.")
        return

    # آپلود عکس‌ها
    send_image_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[text()='ارسال عکس']"))).get_attribute("href")
    driver.get(send_image_link)
    sleep(1)

    upload_images_in_csm(driver, downloaded_paths)
    sleep(1)

    # رفتن به صفحه آلبوم
    open_album_page(driver)
    sleep(1)

    # دریافت لینک‌های آپلودشده
    cms_image_urls = get_uploaded_image_links(driver)
    sleep(1)

    # فیلتر عکس‌هایی که موفق بودن
    successful_image_sources = [img["source_url"] for img in images_data if img["success_download"]]

    # zip کردن فقط عکس‌های موفق
    zipped_image_urls = dict(zip(successful_image_sources, cms_image_urls))
    sleep(1)

    # بازگشت و ویرایش خبر
    back_link = driver.find_element(By.XPATH, '//a[@class="nav-link" and contains(text(), "بازگشت")]')
    back_link.click()
    sleep(1)

    edit_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@class="nav-link" and contains(text(), "ویرایش")]')))
    edit_link.click()

    replace_image_URLs(driver, zipped_image_urls)
    sleep(1)

    # چاپ لینک‌هایی که دانلود نشده‌اند
    failed = [img["source_url"] for img in images_data if not img["success_download"]]
    if failed:
        print(f"⚠️ تصاویر زیر دانلود نشدند و جایگزین نشدند:\n{failed}")

# ============================================================================================================================

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def publish_article(
    news_id: str,
    news: NewsSchema,
    cms_base_url: str,
    auth_data: tuple,
    republish=False
):
    try:
        if not republish:
            from agentutil.agent import SJAssistant
            sj_agent = SJAssistant()
            sj_agent.save_news_content(news_id=news_id, news=news)

        with get_db() as db:

            news_obj: NewsORM = db.query(NewsORM).filter(
                NewsORM.id == news_id
            ).first()

            if not news_obj:
                return False, None
                        
            # ساخت درایور
            driver = create_driver(headless=False, remote=True)
            sleep(1)

            # ورود به سامانه
            success, message = login_to_admin_panel(
                driver=driver,
                username=auth_data[0],
                password=auth_data[1],
                cms_login_url=cms_base_url
            )
            sleep(1)

            if not success:
                driver.quit()
                return False, message

            # رفتن به صفحه انتشار خبر
            open_submit_news_page(driver)
            sleep(1)

            # ایجاد یک خبر جدید
            success, news_id = submit_new_news(driver, news)
            sleep(1)

            # فرآیند مربوط به عکس ها
            image_links = extract_image_links(news.content)

            print(f"{image_links = }")

            if len(image_links) > 0:
                add_images_to_news(driver=driver, image_links=image_links, news_id=news_id)

            if news.status == NewsStatus.PUBLISHED.value:
                change_status_to_published(driver)

            delete_downloaded_images(news_id)

            driver.quit()
            print("Enjoy :)")

            return True, int(news_id)

    except Exception as e:
        print(f"Error in news publisher: {e}")
        return False, None

# ============================================================================================================================
