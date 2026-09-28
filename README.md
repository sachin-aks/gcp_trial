# OpenWeather CLI

Fetch current weather for a city using the OpenWeather API.

1. Install the project dependencies with `poetry install`.
2. Copy `.env.example` to `.env` and set `OPENWEATHER_API_KEY` to your OpenWeather API key.
3. Run `poetry run weather London` (or `poetry run weather "New York,US"`).

Temperature units default to Celsius. Use `--units imperial` for Fahrenheit or
`--units standard` for Kelvin, for example `poetry run weather Tokyo --units imperial`.
The API key is read from `.env` and should not be committed.

## Docker

Build the image from the project root:

```sh
docker build -t gcp-weather .
```

Pass your `.env` file at runtime; it is excluded from the image:

```sh
docker run --rm --env-file .env gcp-weather London
docker run --rm --env-file .env gcp-weather Tokyo --units imperial
```
