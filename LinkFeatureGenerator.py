import ipaddress
import whois
from datetime import datetime
import tldextract
import ssl
import socket
from urllib.parse import urlparse
import requests
from urllib.parse import quote_plus

def is_url_shortened(url):
    try:
        if len(url) < 25:
            return 1

        parsed_url = urlparse(url)
        if parsed_url.netloc in ['bit.ly', 'tinyurl.com']:
            return 1

        return 0

    except:
        return -1

def check_domain_indexed_in_google(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        url_encoded = quote_plus(f"site:{domain}")
        url_google = f"https://www.google.com/search?q={url_encoded}"
        response = requests.get(url_google)
        if response.status_code == 200:
            if 'did not match any documents' in response.text:
                return 0
            else:
                return 1
        else:
            return -1
    except:
        return -1

def check_indexed_in_google(url):
    try:
        url_encoded = quote_plus(f"site:{url}")
        url_google = f"https://www.google.com/search?q={url_encoded}"
        response = requests.get(url_google)
        if response.status_code == 200:
            if 'did not match any documents' in response.text:
                return 0
            else:
                return 1
        else:
            return -1
    except Exception as e:
        return -1

def get_redirect_count(url):
    count = 0
    try:
        response = requests.get(url, allow_redirects=True)
        while response.history:
            response = requests.get(response.url, allow_redirects=True)
            count += 1
        return count
    except Exception as e:
        # Обработка ошибок
        return -1

def check_ssl_cert(url):
    # Извлекаем хост и порт из URL
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 443

    # Создаем SSL контекст
    ssl_context = ssl.create_default_context()

    try:
        # Создаем SSL сокет
        with socket.create_connection((hostname, port)) as sock:
            with ssl_context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                # Получаем сертификат
                cert = ssl_sock.getpeercert()

        # Проверяем наличие сертификата
        if cert:
            return 1
        else:
            return 0
    except Exception as e:
        # Обработка ошибок
        return -1

def days_since_registration(url):
    domain = tldextract.extract(url).registered_domain
    try:
        w = whois.query(domain)
        registration_date = w.creation_date
        if isinstance(registration_date, list):
            registration_date = registration_date[0]
        days_since_registration = (datetime.now() - registration_date).days
        return days_since_registration
    except:
        return -1

def contains_ip_address(url):
    if url.find("http://") != -1:
        url = url.replace("http://", "")
    if url.find("https://") != -1:
        url = url.replace("https://", "")
    if url.find("/") != -1:
        url = url[:url.find("/")]

    # Проверяем, содержит ли URL-адрес порт
    if ":" in url:
        url, port = url.split(":")
        try:
            # Проверяем, является ли порт допустимым числом от 1 до 65535
            port = int(port)
            if port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            return 0
    else:
        port = 80 # Порт по умолчанию для HTTP

    try:
        ip_address = ipaddress.ip_address(url)
        return 1
    except ValueError:
        return 0