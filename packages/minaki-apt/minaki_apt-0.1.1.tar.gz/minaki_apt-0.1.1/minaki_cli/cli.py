import click
import requests
import os
import json

CONFIG_PATH = os.path.expanduser("~/.minaki/config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        click.secho("❌ Config file not found. Run `minaki config` first.", fg="red")
        exit(1)
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

@click.group()
def cli():
    """Minaki APT CLI Tool"""
    pass

@cli.command()
@click.argument("apikey")
@click.argument("base_url")
def config(apikey, base_url):
    """Save API key and base URL"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump({"apikey": apikey, "base_url": base_url}, f)
    click.secho("✅ Config saved!", fg="green")

@cli.command()
@click.argument('deb_file', type=click.Path(exists=True))
def push(deb_file):
    """Upload a .deb file to the Minaki APT server."""
    config = load_config()
    url = f"{config['base_url']}/apt/upload-deb/"
    click.echo(f"📤 Uploading {deb_file}...")

    with open(deb_file, 'rb') as f:
        files = {'file': (os.path.basename(deb_file), f)}
        headers = {"apikey": config["apikey"]}
        try:
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            data = response.json()
            click.echo(f"✅ Uploaded: {data.get('package')} {data.get('version')}")
        except requests.exceptions.RequestException as e:
            click.secho(f"❌ Upload failed: {e}", fg="red")

@cli.command()
def list():
    """List all available .deb packages in the APT repo."""
    config = load_config()
    url = f"{config['base_url']}/apt/list-debs/"
    headers = {"apikey": config["apikey"]}
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        click.echo("📦 Available packages:")
        for p in data["packages"]:
            click.echo(f"- {p['package']} {p['version']} ({p['arch']})")
    except Exception as e:
        click.secho(f"⚠️ Failed to fetch package list: {e}", fg="red")

@cli.command()
@click.argument("package")
@click.argument("version")
@click.argument("arch")
def delete(package, version, arch):
    """Delete a .deb package from the repo."""
    config = load_config()
    url = f"{config['base_url']}/apt/delete-deb/{package}/{version}/{arch}"
    headers = {"apikey": config["apikey"]}
    try:
        res = requests.delete(url, headers=headers)
        res.raise_for_status()
        click.secho(f"✅ Deleted: {package} {version}", fg="green")
    except Exception as e:
        click.secho(f"⚠️ Failed to delete: {e}", fg="red")

if __name__ == '__main__':
    cli()
