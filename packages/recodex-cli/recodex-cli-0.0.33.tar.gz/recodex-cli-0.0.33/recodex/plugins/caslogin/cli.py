import click
import requests
from pathlib import Path
from string import Template
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup

from recodex.api import ApiClient
from recodex.config import UserContext
from recodex.decorators import pass_data_dir


CAS_URL = Template("https://idp.cuni.cz/cas/login?service=$service_url&renew=true")


@click.command()
@click.argument("api_url")
@pass_data_dir
def caslogin(data_dir: Path, api_url):
    """
    Log in using CAS UK
    """

    cas_url = CAS_URL.substitute(service_url=quote_plus(api_url))

    username = click.prompt("User name")
    password = click.prompt("Password", hide_input=True)

    session = requests.session()
    login_page = session.get(cas_url)

    soup = BeautifulSoup(login_page.text, "lxml")
    form = soup.select("form#fm1")[0]

    form_data = {}
    for input in form.select("input"):
        form_data[input["name"]] = input["value"] if input.has_attr("value") else ""

    form_data.update({
        "username": username,
        "password": password
    })

    response = session.post(cas_url, data=form_data, allow_redirects=False)
    ticket = parse_qs(urlparse(response.raw.get_redirect_location()).query)["ticket"][0]

    api = ApiClient(api_url)
    api_login_response = api.login_external("cas-uk", "cas", {
        "ticket": ticket,
        "clientUrl": api_url
    })

    api_token = api_login_response["accessToken"]
    UserContext(api_url, api_token).store(data_dir / "context.yaml")
