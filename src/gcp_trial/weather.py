"""Fetch and display current weather from OpenWeather."""

import os
from enum import Enum

import requests
import typer
from dotenv import load_dotenv

API_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch current conditions for a city from OpenWeather."""
    response = requests.get(
        API_URL,
        params={"q": city, "appid": api_key, "units": units},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


class Units(str, Enum):
    standard = "standard"
    metric = "metric"
    imperial = "imperial"


app = typer.Typer()


@app.command()
def weather(
    city: str = typer.Argument(..., help="City name, for example 'London' or 'London,UK'"),
    units: Units = typer.Option(Units.metric, help="Temperature units (default: metric)"),
) -> None:
    load_dotenv()

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        typer.echo("OPENWEATHER_API_KEY is not set. Add it to your .env file.", err=True)
        raise typer.Exit(code=1)

    try:
        current = fetch_weather(city, api_key, units.value)
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        if status == 401:
            message = "OpenWeather rejected the API key. Check OPENWEATHER_API_KEY."
        elif status == 404:
            message = f"City not found: {city}"
        else:
            message = f"OpenWeather request failed (HTTP {status})."
        typer.echo(message, err=True)
        raise typer.Exit(code=1)
    except requests.RequestException as error:
        typer.echo(f"Could not reach OpenWeather: {error}", err=True)
        raise typer.Exit(code=1)

    details = current["main"]
    description = current["weather"][0]["description"].capitalize()
    temperature_unit = {Units.standard: "K", Units.metric: "C", Units.imperial: "F"}[units]
    wind_unit = "m/s" if units != Units.imperial else "mph"
    typer.echo(f"{current['name']}: {description}")
    typer.echo(f"Temperature: {details['temp']:.1f} {temperature_unit}")
    typer.echo(f"Feels like: {details['feels_like']:.1f} {temperature_unit}")
    typer.echo(f"Humidity: {details['humidity']}%")
    typer.echo(f"Wind speed: {current['wind']['speed']} {wind_unit}")


def main() -> None:
    app()


if __name__ == "__main__":
    raise SystemExit(main())