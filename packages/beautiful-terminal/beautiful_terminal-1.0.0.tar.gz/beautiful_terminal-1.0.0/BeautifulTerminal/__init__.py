if __name__ == "__main__":
    from terminal import BeautifulTerminal
else:
    from BeautifulTerminal.terminal import BeautifulTerminal

BeautifulTerminal()

try:
    import requests
    import pkg_resources

    installed_version = pkg_resources.get_distribution('beautiful-terminal').version

    response = requests.get(f'https://pypi.org/pypi/beautiful-terminal/json').raise_for_status()
    data = response.json()
    latest_version = data['info']['version']

    if latest_version:
        if installed_version == latest_version:
            print(f"beautiful-terminal {latest_version} is up to date!", color="green")
        else:
            print(f"beautiful-terminal {installed_version} is not up to date. There is a newer version {latest_version}. To update, run 'pip install --upgrade beautiful-terminal'.", color="yellow")
except:
    pass