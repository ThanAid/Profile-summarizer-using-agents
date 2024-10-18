"""This module contains the code to scrape LinkedIn profiles
using the Proxycurl API. The Proxycurl API is a paid service

To create and store a mock LinkedIn profile, run this file"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()


def scrape_linkedin_profile(linkedin_url: str, mock: bool = False) -> dict:
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        with open("mock_data/linkedin_profile.json") as f:
            data = json.load(f)

    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint, params={"url": linkedin_url}, headers=header_dic, timeout=10
        )

        data = response.json()

        # Clean unwanted fields
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    data = scrape_linkedin_profile(
        linkedin_url="https://www.linkedin.com/in/thanos-aidinis-589950175/", mock=True
    )
    print(data)
    with open("mock_data/linkedin_profile.json", "w") as f:
        json.dump(data, f)
    print("saved to mock_data/linkedin_profile.json")
