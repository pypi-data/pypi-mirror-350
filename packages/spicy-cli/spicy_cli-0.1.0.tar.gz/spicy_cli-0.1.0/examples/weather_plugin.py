"""Example Spicy CLI plugin: Weather"""

from typing import TypedDict

import typer
from rich.console import Console
from rich.panel import Panel

from spicy_cli.commands.base import format_info, format_success
from spicy_cli.plugins import PluginBase


class ForecastDict(TypedDict):
    """Type definition for forecast dictionary."""

    day: str
    temp: int
    condition: str


class WeatherPlugin(PluginBase):
    """Plugin for checking weather."""

    name = "weather"
    help = "Check the weather for a location"

    @classmethod
    def get_typer_app(cls) -> typer.Typer:
        """Get the Typer app for this plugin."""
        app = typer.Typer(help=cls.help)
        console = Console()

        @app.command("forecast")
        def forecast_command(
            location: str = typer.Argument(..., help="The location to check"),
            days: int = typer.Option(3, "--days", "-d", help="Number of days in forecast"),
            celsius: bool = typer.Option(True, "--celsius/--fahrenheit", help="Temperature unit"),
        ) -> None:
            """Get a weather forecast for a location."""
            format_info(f"Checking weather for {location} for {days} days...")

            # In a real plugin, this would make an API call to a weather service
            # For this example, we'll just show some mock data

            unit = "°C" if celsius else "°F"

            forecasts: list[ForecastDict] = [
                {"day": "Today", "temp": 22, "condition": "Sunny"},
                {"day": "Tomorrow", "temp": 18, "condition": "Partly Cloudy"},
                {"day": "Day 3", "temp": 20, "condition": "Rain"},
                {"day": "Day 4", "temp": 19, "condition": "Cloudy"},
                {"day": "Day 5", "temp": 21, "condition": "Sunny"},
            ]

            # Convert to Fahrenheit if needed
            if not celsius:
                for forecast in forecasts:
                    forecast["temp"] = round(forecast["temp"] * 9 / 5 + 32)

            # Display the forecast
            for _, forecast in enumerate(forecasts[:days]):
                weather_icon = "☀️" if "Sunny" in forecast["condition"] else "☁️"
                weather_icon = "🌧️" if "Rain" in forecast["condition"] else weather_icon

                panel = Panel(
                    f"[bold]{forecast['condition']}[/bold] {weather_icon}\n"
                    f"Temperature: [bold]{forecast['temp']}{unit}[/bold]",
                    title=str(forecast["day"]),
                    border_style="cyan",
                )
                console.print(panel)

            format_success(f"Weather forecast for {location} complete")

        @app.command("current")
        def current_command(
            location: str = typer.Argument(..., help="The location to check"),
            celsius: bool = typer.Option(True, "--celsius/--fahrenheit", help="Temperature unit"),
        ) -> None:
            """Get current weather for a location."""
            format_info(f"Checking current weather for {location}...")

            # Mock data for example
            temp = 22  # Celsius
            if not celsius:
                temp = round(temp * 9 / 5 + 32)

            unit = "°C" if celsius else "°F"
            condition = "Sunny"
            weather_icon = "☀️"

            panel = Panel(
                f"[bold]{condition}[/bold] {weather_icon}\n"
                f"Temperature: [bold]{temp}{unit}[/bold]\n"
                f"Humidity: 65%\n"
                f"Wind: 5 km/h",
                title=f"Current Weather for {location}",
                border_style="green",
            )
            console.print(panel)

            format_success(f"Current weather for {location} displayed")

        return app


# This is required for the plugin to be loaded correctly
plugin_class = WeatherPlugin
