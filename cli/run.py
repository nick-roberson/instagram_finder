import time

import instaloader
import requests
import pandas as pd

from tqdm import tqdm
from rich import print
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def scrape_user_followers(driver, username: str):
    """Scrape user followers"""
    # Find element in the page that has ` followers` in it
    followers_element = driver.find_elements(
        By.XPATH, "//a[contains(text(), ' followers')]"
    )
    followers_text = [element.text for element in followers_element]
    print(f"Found {followers_text} on the page")
    return followers_text


def scrape_related_users(driver, username: str):
    user_elements, user_text, related_user_list = [], [], []

    # Get all cards that have a Follow button
    elements = driver.find_elements(By.XPATH, "//div[contains(text(), 'Follow')]")
    for element in tqdm(elements, desc="Fetching User Cards"):
        # Go up 4 spaces to get the card element
        for i in range(4):
            element = element.find_element(By.XPATH, "./parent::*")
        user_elements.append(element)

    print(f"Found {len(user_elements)} users to follow")
    # Try to get the elements of those cards (username, name, etc)
    for user in tqdm(user_elements, desc="Fetching User Info"):
        child_elements = user.find_elements(By.CSS_SELECTOR, '[dir="auto"]')
        child_text = [
            child.text.strip()
            for child in child_elements
            if child.text.lower() != "follow"
        ]
        user_text.append(child_text)

    # Close the browser
    driver.quit()

    # Make into a dictionary and print
    for user in tqdm(user_text, desc="Processing User Info"):
        # Skip if there are no users or if min length is not met
        if len(user) < 2:
            continue

        # confirm that profile can be loaded before adding to list
        profile_link = f"https://www.instagram.com/{user[0]}"
        try:
            requests.get(profile_link)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            continue

        # add to list
        related_user_list.append(
            {
                "Username": user[0],
                "Profile Name": user[1],
                "Profile Link": profile_link,
            }
        )
    return related_user_list


def scrape_user_data(username: str):
    # Setup ChromeDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    )
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"http://www.instagram.com/{username}")

    # Add in waits for dynamic content to load
    driver.implicitly_wait(10)
    time.sleep(10)

    results = {}

    # Scrape related users and save
    related_users = scrape_related_users(driver, username)
    df = pd.DataFrame(related_users)
    df.to_csv(f"{username}_related_users.csv", index=False)
    print(f"Saved {len(related_users)} related users to {username}_related_users.csv")

    # Scrape followers and save
    followers = scrape_user_followers(driver, username)
    print(f"Potential follower count: {followers}")


def similar_account(
    username: str = None,
    target_user: str = None,
    min_followers: int = 100000,
    max_followers: int = 1000000,
):
    # Optionally get username from input of CLI, and then load the
    username = username or input("Username to search similar accounts for:")
    ig = instaloader.Instaloader()
    ig.load_session_from_file(username)

    # Get profile info
    prof = instaloader.Profile.from_username(ig.context, target_user)
    print(prof)
    # Get follower range
    if min_followers is None:
        min_followers = int(input("Follower Range Minimum: "))
    if max_followers is None:
        max_followers = int(input("Follower Range Max: "))

    approval_lst = []

    # Open window, not sure with what.
    driver = webdriver.Chrome()
    x = input("Have you logged in in the AUTO-WINDOW? (PRESS ANY KEY)")

    # Begin to fetch similar accounts
    seen_profiles = []
    target_similar_accounts = list(prof.get_similar_accounts())
    print(
        f"Found {len(target_similar_accounts)} similar accounts between {username} and {target_user}"
    )

    # Get similar accounts filtered
    print(f"Fetching similar accounts to {target_user}, this may take a minute ...")
    similar_accounts = [
        act
        for act in target_similar_accounts
        if act.username not in seen_profiles
        and min_followers <= act.followers <= max_followers
    ]
    print(
        f"Filtered down to {len(similar_accounts)} similar accounts "
        f"(max followers: {max_followers}, min followers: {min_followers})"
    )

    for index, act in enumerate(list(similar_accounts)):
        approval_lst.append(
            {
                "username": act.username,
                "followers": act.followers,
                "url": f"https://www.instagram.com/{act.username}",
            }
        )

    print(f"Approved accounts that meet follower requirements:")
    for index, user in enumerate(approval_lst):
        print(f"{index}: {user}")
