"""Command-line interface for Medium Converter."""

import importlib.metadata
import random
import sys
import time

import click
from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# Create a custom theme with more vibrant colors
custom_theme = Theme(
    {
        "info": "bold cyan",
        "warning": "bold yellow",
        "error": "bold red",
        "success": "bold green",
        "title": "bold magenta",
        "url": "underline bright_blue",
        "format": "bright_green",
        "highlight": "bold bright_yellow",
        "subtle": "dim white",
        "accent": "bright_cyan",
    }
)

try:
    __version__ = importlib.metadata.version("medium-converter")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"  # Default during development

console = Console(theme=custom_theme, highlight=True)


def print_banner() -> None:
    """Print a fancy banner for the CLI."""
    banner = """
    ╭─────────────────────────────────────────────────────╮
    │                                                     │
    │   [bold bright_magenta]🔄 Medium Converter[/bold bright_magenta]                │
    │   [italic bright_cyan]✨ Convert articles ✨[/italic bright_cyan]                │
    │                                                     │
    ╰─────────────────────────────────────────────────────╯
    """
    console.print(banner)


@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="Show the version and exit.")
@click.pass_context
def main(ctx: click.Context, version: bool) -> None:
    """Convert Medium articles to various formats with LLM enhancement.

    Medium Converter allows you to download and convert Medium articles to
    different formats, with optional content enhancement using LLMs.
    """
    # Print version and exit if requested
    if version:
        console.print(
            f"[title]🔄 Medium Converter[/title] [accent]v{__version__}[/accent]"
        )
        sys.exit(0)

    # Show help if no command provided
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print(ctx.get_help())


@main.command()
@click.argument("url")
@click.option(
    "--format",
    "-f",
    default="markdown",
    type=click.Choice(
        ["markdown", "pdf", "html", "latex", "epub", "docx", "text"],
        case_sensitive=False,
    ),
    help="Output format",
)
@click.option("--output", "-o", help="Output file path")
@click.option("--output-dir", "-d", help="Output directory (auto-generates filename)")
@click.option(
    "--enhance/--no-enhance", default=False, help="Use LLM to enhance content"
)
@click.option(
    "--use-cookies/--no-cookies",
    default=True,
    help="Use browser cookies for authentication",
)
@click.option(
    "--llm-provider",
    type=click.Choice(
        ["openai", "anthropic", "google", "mistral", "local"], case_sensitive=False
    ),
    help="LLM provider to use for enhancement",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def convert(
    url: str,
    format: str,
    output: str | None,
    output_dir: str | None,
    enhance: bool,
    use_cookies: bool,
    llm_provider: str | None,
    verbose: bool,
) -> None:
    """Convert a Medium article to the specified format.

    Examples:
        medium convert https://medium.com/example-article
        medium convert https://medium.com/example-article -f pdf -o article.pdf
        medium convert https://medium.com/example -enhance
    """
    # Show a fancy panel with the conversion info
    info_table = Table.grid(padding=1)
    info_table.add_column(style="bright_cyan", justify="right")
    info_table.add_column(style="bright_white")

    info_table.add_row("🔗 URL:", f"[url]{url}[/url]")

    # Get emoji for format
    format_emojis = {
        "markdown": "📝",
        "pdf": "📄",
        "html": "🌐",
        "latex": "📊",
        "epub": "📚",
        "docx": "📋",
        "text": "📃",
    }
    format_emoji = format_emojis.get(format.lower(), "📄")

    info_table.add_row(f"{format_emoji} Format:", f"[format]{format.upper()}[/format]")

    if output:
        info_table.add_row("💾 Output:", output)
    if output_dir:
        info_table.add_row("📁 Output Directory:", output_dir)
    if enhance:
        provider = llm_provider or "default"
        info_table.add_row(
            "🧠 Enhancement:",
            f"[success]Enabled[/success] ([highlight]{provider}[/highlight])",
        )
    else:
        info_table.add_row("🧠 Enhancement:", "[subtle]Disabled[/subtle]")

    cookie_status = "Enabled" if use_cookies else "Disabled"
    cookie_style = "success" if use_cookies else "subtle"
    info_table.add_row(
        "🍪 Use Cookies:",
        f"[{cookie_style}]{cookie_status}[/{cookie_style}]",
    )

    # Fancy borders and colors
    panel = Panel(
        info_table,
        title="[title]🔄 Medium Converter[/title]",
        subtitle="[info]Converting Article...[/info]",
        border_style="bright_blue",
        box=box.ROUNDED,
        highlight=True,
    )
    console.print(panel)

    # Show a progress spinner with multiple steps
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="bright_green", finished_style="bright_green"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Simulate the steps in the conversion process
        fetch_task = progress.add_task("[info]🔍 Fetching article...[/info]", total=100)

        # Simulate progress
        for i in range(101):
            progress.update(fetch_task, completed=i)
            time.sleep(0.01)

        # Additional steps for enhanced visualization
        if enhance:
            process_task = progress.add_task(
                "[info]🧮 Processing content...[/info]", total=100
            )
            for i in range(101):
                progress.update(process_task, completed=i)
                time.sleep(0.01)

            enhance_task = progress.add_task(
                "[info]🧠 Enhancing with LLM...[/info]", total=100
            )
            for i in range(101):
                progress.update(enhance_task, completed=i)
                time.sleep(0.01)

        export_task = progress.add_task(
            f"[info]📦 Exporting to {format.upper()}...[/info]", total=100
        )
        for i in range(101):
            progress.update(export_task, completed=i)
            time.sleep(0.01)

    # Print placeholder for now
    console.print(
        Panel(
            "[italic bright_cyan]Coming soon![/italic bright_cyan]",
            title="[success]✅ Status[/success]",
            border_style="bright_green",
            box=box.ROUNDED,
        )
    )


@main.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--format",
    "-f",
    default="markdown",
    type=click.Choice(
        ["markdown", "pdf", "html", "latex", "epub", "docx", "text"],
        case_sensitive=False,
    ),
    help="Output format",
)
@click.option(
    "--output-dir", "-d", required=True, help="Output directory for converted files"
)
@click.option(
    "--enhance/--no-enhance", default=False, help="Use LLM to enhance content"
)
@click.option(
    "--concurrent", "-c", default=3, help="Maximum number of concurrent downloads"
)
@click.option(
    "--use-cookies/--no-cookies",
    default=True,
    help="Use browser cookies for authentication",
)
@click.option(
    "--llm-provider",
    type=click.Choice(
        ["openai", "anthropic", "google", "mistral", "local"], case_sensitive=False
    ),
    help="LLM provider to use for enhancement",
)
def batch(
    file: str,
    format: str,
    output_dir: str,
    enhance: bool,
    concurrent: int,
    use_cookies: bool,
    llm_provider: str | None,
) -> None:
    """Convert multiple Medium articles listed in a file.

    The input file should contain one Medium URL per line.

    Examples:
        medium batch articles.txt -f pdf -d ./articles
        medium batch articles.txt -d ./articles --enhance -c 5
    """
    console.print(
        Panel(
            f"[info]📚 Batch Processing:[/info] [url]{file}[/url]",
            subtitle=f"[format]📁 Output Directory: {output_dir}[/format]",
            border_style="bright_blue",
            box=box.ROUNDED,
        )
    )

    # Placeholder code to read URLs
    with open(file) as f:
        urls = [line.strip() for line in f if line.strip()]

    console.print(f"Found [highlight]🔍 {len(urls)}[/highlight] URLs to process")

    # Create a table with the URLs for visual effect
    url_table = Table(title="📋 URLs to Process", box=box.ROUNDED)
    url_table.add_column("№", style="bright_cyan", justify="right")
    url_table.add_column("URL", style="bright_white")

    for i, url in enumerate(urls[:5], 1):
        url_table.add_row(str(i), url)

    if len(urls) > 5:
        url_table.add_row("...", "...")

    console.print(url_table)

    console.print(
        Panel(
            "[italic bright_cyan]Coming soon![/italic bright_cyan]",
            title="[info]ℹ️ Status[/info]",
            border_style="bright_blue",
            box=box.ROUNDED,
        )
    )


@main.command(name="config")
@click.argument("action", type=click.Choice(["show", "set", "get", "reset"]))
@click.argument("key", required=False)
@click.argument("value", required=False)
def config_cmd(action: str, key: str | None, value: str | None) -> None:
    """Manage configuration settings.

    Examples:
        medium config show
        medium config set default_format pdf
        medium config get llm.provider
        medium config reset
    """
    if action == "show":
        # Example configuration table
        config_table = Table(
            title="⚙️ Configuration", box=box.ROUNDED, border_style="bright_magenta"
        )
        config_table.add_column("🔑 Key", style="bright_cyan")
        config_table.add_column("📊 Value", style="bright_green")

        # These would be actual configuration values
        config_table.add_row("default_format", "markdown")
        config_table.add_row("output_dir", "~/Documents/medium-articles")
        config_table.add_row("use_browser_cookies", "true")
        config_table.add_row("llm.provider", "openai")
        config_table.add_row("llm.temperature", "0.7")
        config_table.add_row("export.include_metadata", "true")
        config_table.add_row("cache.enable", "true")
        config_table.add_row("cache.ttl", "86400")

        console.print(config_table)
    elif action == "set" and key and value:
        # Split into two lines to avoid line length issues
        text = Text()
        text.append("✅ Set ", style="success")
        text.append(key, style="accent")
        text.append(" to ", style="default")
        text.append(value, style="highlight")
        console.print(text)
        console.print(
            "[italic bright_cyan]Configuration coming soon.[/italic bright_cyan]"
        )
    elif action == "get" and key:
        # Split into two lines to avoid line length issues
        text = Text()
        text.append("🔍 Value ", style="info")
        text.append(key, style="accent")
        text.append(": ", style="default")
        text.append("example_value", style="highlight")
        console.print(text)
        console.print(
            "[italic bright_cyan]Configuration coming soon.[/italic bright_cyan]"
        )
    elif action == "reset":
        console.print("[warning]⚠️ Reset all settings to defaults?[/warning]")
        console.print(
            "[italic bright_cyan]Configuration coming soon.[/italic bright_cyan]"
        )
    else:
        console.print(
            Panel(
                "[italic bright_cyan]Configuration coming soon.[/italic bright_cyan]",
                title="[info]ℹ️ Status[/info]",
                border_style="bright_blue",
                box=box.ROUNDED,
            )
        )


@main.command()
def list_formats() -> None:
    """List all available export formats with details."""
    formats_table = Table(
        title="📊 Available Export Formats",
        box=box.ROUNDED,
        border_style="bright_green",
        highlight=True,
    )

    formats_table.add_column("🏷️ Format", style="bright_cyan")
    formats_table.add_column("📝 Description", style="bright_white")
    formats_table.add_column("🔍 Extension", style="bright_green")
    formats_table.add_column("🧩 Dependencies", style="bright_yellow")

    formats_table.add_row(
        "Markdown",
        "Plain text format with lightweight markup",
        ".md",
        "None (built-in)",
    )
    formats_table.add_row(
        "PDF", "Portable Document Format for high-quality prints", ".pdf", "reportlab"
    )
    formats_table.add_row("HTML", "Web page format with styling", ".html", "jinja2")
    formats_table.add_row("LaTeX", "Professional typesetting system", ".tex", "jinja2")
    formats_table.add_row(
        "EPUB", "Electronic publication for e-readers", ".epub", "ebooklib"
    )
    formats_table.add_row("DOCX", "Microsoft Word document", ".docx", "python-docx")
    formats_table.add_row(
        "Text", "Plain text without formatting", ".txt", "None (built-in)"
    )

    console.print(formats_table)


@main.command()
def list_providers() -> None:
    """List all available LLM providers with details."""
    providers_table = Table(
        title="🧠 Available LLM Providers",
        box=box.ROUNDED,
        border_style="bright_magenta",
        highlight=True,
    )

    providers_table.add_column("🤖 Provider", style="bright_cyan")
    providers_table.add_column("🔧 Models", style="bright_white")
    providers_table.add_column("✨ Features", style="bright_green")
    providers_table.add_column("📦 Dependencies", style="bright_yellow")

    providers_table.add_row(
        "OpenAI", "GPT-3.5-Turbo, GPT-4", "High quality, widely used", "openai"
    )
    providers_table.add_row(
        "Anthropic",
        "Claude 3 (Haiku, Sonnet, Opus)",
        "Long context, high quality",
        "anthropic",
    )
    providers_table.add_row(
        "Google",
        "Gemini Pro, Gemini Pro Vision",
        "Competitive pricing",
        "google-generativeai",
    )
    providers_table.add_row(
        "Mistral",
        "Mistral Small, Medium, Large",
        "Good performance, reasonable cost",
        "mistralai",
    )
    providers_table.add_row(
        "Local",
        "Various open-source models via GGUF",
        "Privacy, no API costs",
        "llama-cpp-python",
    )

    console.print(providers_table)


@main.command()
def info() -> None:
    """Display system information and environment details."""
    import os
    import platform

    info_table = Table(
        title="🖥️ System Information",
        box=box.ROUNDED,
        border_style="bright_blue",
        highlight=True,
    )

    info_table.add_column("📋 Item", style="bright_cyan")
    info_table.add_column("📊 Value", style="bright_green")

    info_table.add_row("Medium Converter Version", f"🔄 {__version__}")
    info_table.add_row("Python Version", f"🐍 {platform.python_version()}")
    info_table.add_row(
        "Operating System", f"💻 {platform.system()} {platform.release()}"
    )
    info_table.add_row("Platform", f"🔧 {platform.platform()}")

    # Environment variables
    env_vars = {
        "OPENAI_API_KEY": "✅" if os.environ.get("OPENAI_API_KEY") else "❌",
        "ANTHROPIC_API_KEY": "✅" if os.environ.get("ANTHROPIC_API_KEY") else "❌",
        "GOOGLE_API_KEY": "✅" if os.environ.get("GOOGLE_API_KEY") else "❌",
        "MISTRAL_API_KEY": "✅" if os.environ.get("MISTRAL_API_KEY") else "❌",
    }

    for key, value in env_vars.items():
        info_table.add_row(f"ENV: {key}", value)

    console.print(info_table)

    # Show Python packages
    try:
        import pkg_resources  # Already installed type stubs for this

        packages = [
            (dist.key, dist.version)
            for dist in pkg_resources.working_set
            if dist.key
            in [
                "click",
                "rich",
                "httpx",
                "beautifulsoup4",
                "pydantic",
                "openai",
                "anthropic",
                "google-generativeai",
                "mistralai",
            ]
        ]

        if packages:
            pkg_table = Table(
                title="📦 Installed Packages",
                box=box.ROUNDED,
                border_style="bright_cyan",
            )
            pkg_table.add_column("📋 Package", style="bright_white")
            pkg_table.add_column("🔢 Version", style="bright_yellow")

            for pkg, ver in sorted(packages):
                pkg_table.add_row(pkg, ver)

            console.print(pkg_table)
    except Exception:
        pass


@main.command()
def examples() -> None:
    """Show example usage of Medium Converter."""
    examples_md = """
    # 📚 Examples

    ## 🔄 Basic conversion
    ```bash
    medium convert https://medium.com/example-article
    ```

    ## 📄 Convert to PDF
    ```bash
    medium convert https://medium.com/example-article -f pdf -o article.pdf
    ```

    ## 🧠 Convert with LLM enhancement
    ```bash
    medium convert https://medium.com/example-article --enhance --llm-provider openai
    ```

    ## 📚 Batch conversion
    ```bash
    medium batch articles.txt -f markdown -d ./articles
    ```

    ## ⚙️ Configuration
    ```bash
    medium config set default_format pdf
    ```
    """

    console.print(
        Panel(
            Markdown(examples_md),
            title="[bright_magenta]✨ Example Usage[/bright_magenta]",
            border_style="bright_cyan",
            box=box.ROUNDED,
        )
    )


@main.command()
def random_tip() -> None:
    """Display a random tip about Medium Converter."""
    tips = [
        "💡 Use the --enhance flag to improve article quality with AI.",
        "💡 Export to PDF for the best print quality.",
        "💡 Using --use-cookies allows access to member-only articles.",
        "💡 Batch convert multiple articles with the 'batch' command.",
        "💡 Try different LLM providers to see which gives the best enhancements.",
        "💡 The HTML format preserves most of the original article styling.",
        "💡 Local LLMs provide privacy but require more system resources.",
        "💡 Use 'medium list-formats' to see all available export formats.",
        "💡 You can customize output with configuration settings.",
        "💡 Save your favorite settings with 'medium config set'.",
    ]

    tip = random.choice(tips)

    console.print(
        Panel(
            f"[bright_yellow]{tip}[/bright_yellow]",
            title="[bright_cyan]💡 Random Tip[/bright_cyan]",
            border_style="bright_yellow",
            box=box.ROUNDED,
        )
    )


if __name__ == "__main__":
    main()
