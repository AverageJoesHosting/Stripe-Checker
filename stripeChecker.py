import requests
import time
import json
import typer
import sys
import csv  # Added import
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# Initialize Rich Console
console = Console()

# Simplified Header
def display_header():
    console.print("Stripe Checker: A Tool for Auditing and Validating Stripe API Keys", style="bold cyan")
    console.print("=" * 70, style="cyan")

# Menu Options with Integrated Help Content
def display_menu():
    menu = """
[bold green]Available Modes and Features:[/bold green]

[bold cyan]1.[/bold cyan] [bold yellow]default[/bold yellow]     - Validate the secret key by listing charges.
                          Usage: -m default --secretkey <SECRET_KEY>

[bold cyan]2.[/bold cyan] [bold yellow]brute-force[/bold yellow] - Discover customers by brute-forcing customer IDs.
                          Usage: -m brute-force --secretkey <SECRET_KEY> --start <START_ID> --stop <STOP_ID> [--delay <DELAY_MS>]

[bold cyan]3.[/bold cyan] [bold yellow]pubkey[/bold yellow]      - Validate the publishable key by creating tokens.
                          Usage: -m pubkey --pubkey <PUBLISHABLE_KEY>

[bold cyan]4.[/bold cyan] [bold yellow]full[/bold yellow]        - Validate both secret and publishable keys.
                          Usage: -m full --secretkey <SECRET_KEY> --pubkey <PUBLISHABLE_KEY>

[bold cyan]5.[/bold cyan] [bold yellow]restricted[/bold yellow]  - Validate restricted secret keys by listing charges.
                          Usage: -m restricted --secretkey <RESTRICTED_KEY>

[bold cyan]6.[/bold cyan] [bold yellow]custom[/bold yellow]      - Test a custom endpoint using a secret key.
                          Usage: -m custom --secretkey <SECRET_KEY> --custom-endpoint <ENDPOINT>

[bold green]Help Content:[/bold green]
Usage: stripeChecker.py [OPTIONS]

  Stripe Checker: A Tool for Auditing and Validating Stripe API Keys

Options:
  -m, --mode TEXT            Testing mode (default, brute-force, pubkey, full, restricted, custom)
  --secretkey TEXT           Stripe secret key (sk_test_xxx or rk_test_xxx)
  --pubkey TEXT              Stripe publishable key (pk_test_xxx)
  --start INTEGER            Start of customer ID range (used with brute-force mode)
  --stop INTEGER             End of customer ID range (used with brute-force mode)
  --delay INTEGER            Time delay between requests in milliseconds (default: 500ms)
  --custom-endpoint TEXT     Custom endpoint to test (used with custom mode)
  --output-folder TEXT       Folder to save results (default: output)
  --help                     Show this message and exit.

[bold green]Additional Features:[/bold green]
--delay         - Set the delay (in ms) between requests during brute-force (default: 500ms).
--start/--stop  - Define the range for brute-forcing customer IDs (required for brute-force mode).
--output-folder - Specify the folder to save results (default: ./output).

[bold green]Usage Tips:[/bold green]
• Ensure you have the correct API keys (secret and/or publishable) before running tests.
• Use Stripe's test keys (`sk_test_...` and `pk_test_...`) to avoid unintended charges.
• When using brute-force mode, be mindful of Stripe's rate limits to prevent temporary blocking.
• Store your API keys securely and avoid hardcoding them in scripts or sharing them publicly.
• Review the output CSV files for detailed results and potential issues.

[bold green]Best Practices:[/bold green]
• Regularly rotate your API keys to maintain security.
• Limit the permissions of restricted keys to only what is necessary for your application.
• Monitor Stripe's dashboard for any unusual activity or access patterns.
• Use environment variables or secure storage solutions to manage your API keys in production environments.
• Keep the `output` folder secure, especially if it contains sensitive information from your tests.

[bold green]Common Scenarios:[/bold green]
• **Validating Keys:** Use `default` or `full` mode to ensure your secret and publishable keys are active and correctly configured.
• **Security Audits:** Utilize `restricted` mode to test keys with limited permissions, ensuring they adhere to the principle of least privilege.
• **Custom Integrations:** Leverage `custom` mode to test specific endpoints tailored to your application's needs.
• **Data Discovery:** Apply `brute-force` mode responsibly to identify and manage customer IDs within a specified range.

[bold green]Example Usage:[/bold green]
• Validate a secret key:
  `python stripeChecker.py -m default --secretkey sk_test_xxx`

• Discover customers with brute-force:
  `python stripeChecker.py -m brute-force --secretkey sk_test_xxx --start 1 --stop 100 --delay 200`

• Validate a publishable key:
  `python stripeChecker.py -m pubkey --pubkey pk_test_xxx`

• Full validation of both keys:
  `python stripeChecker.py -m full --secretkey sk_test_xxx --pubkey pk_test_xxx`

• Test a custom endpoint:
  `python stripeChecker.py -m custom --secretkey sk_test_xxx --custom-endpoint https://yourapi.com/test`

[bold green]Help Content Continued:[/bold green]
For detailed information on each option and mode, refer to the official [Stripe API Documentation](https://stripe.com/docs/api) or use the `--help` flag with any command.
"""
    console.print(menu)

# Function to Save Results to a File
def save_results_to_file(results, output_folder):
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_folder) / f"stripe_test_results_{timestamp}.csv"  # Changed to CSV

    # Prepare data for CSV
    csv_data = []
    for test, data in results.items():
        if isinstance(data, dict):
            status = "PASS" if data.get("status") else f"FAIL ({data.get('error', data.get('raw_response', 'Unknown Error'))})"
            if "raw_response" in data:
                # Pretty-print JSON for better readability
                if isinstance(data["raw_response"], (dict, list)):
                    result_str = json.dumps(data["raw_response"], indent=2)
                else:
                    result_str = str(data["raw_response"])
                csv_data.append({"Test": test, "Result": result_str, "Status": status})
            elif "found_customers" in data:
                for customer in data["found_customers"]:
                    customer_info = f"{customer['id']} ({customer.get('email', 'No Email')})"
                    customer_status = "PASS" if customer.get("id") else "FAIL"
                    csv_data.append({"Test": "Found Customer", "Result": customer_info, "Status": customer_status})
            else:
                csv_data.append({"Test": test, "Result": "-", "Status": status})
        else:
            # For simple boolean or string results
            status = "PASS" if data is True else f"FAIL ({data})"
            csv_data.append({"Test": test, "Result": "-", "Status": status})

    # Save results to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Test", "Result", "Status"])
        writer.writeheader()
        writer.writerows(csv_data)

    console.print(f"\n[bold green]Results saved to {output_file}[/bold green]")

# Function to Display Results
def display_results(results):
    """Display test results in a table with three columns: Test, Result, Status."""
    table = Table(title="Test Results")
    table.add_column("Test", justify="left", style="cyan", no_wrap=True)
    table.add_column("Result", justify="left", style="green")
    table.add_column("Status", justify="center", style="magenta")  # Added Status column

    for test, data in results.items():
        if isinstance(data, dict):
            if "raw_response" in data:
                status = "PASS" if data.get("status") else "FAIL"
                # Convert raw_response to a JSON string for better readability
                raw_response = data.get("raw_response", "-")
                raw_response_str = json.dumps(raw_response, indent=2) if isinstance(raw_response, (dict, list)) else str(raw_response)
                table.add_row(test, raw_response_str, status)
            elif "found_customers" in data:
                for customer in data["found_customers"]:
                    customer_info = f"{customer['id']} ({customer.get('email', 'No Email')})"
                    customer_status = "PASS" if customer.get("id") else "FAIL"
                    table.add_row("Found Customer", customer_info, customer_status)
            else:
                status = "PASS" if data.get("status") else f"FAIL ({data.get('error', 'Unknown Error')})"
                table.add_row(test, "-", status)
        else:
            # For simple boolean or string results
            status = "PASS" if data is True else f"FAIL ({data})"
            table.add_row(test, "-", status)

    console.print(table)

# Example Function Definitions (Replace these with actual implementations)
def brute_force_customers(secret_key, delay, start, stop):
    # Placeholder implementation
    time.sleep(delay / 1000)  # Convert ms to seconds
    # Simulate found customers
    return {
        "found_customers": [
            {"id": f"cus_{start:010}", "email": "customer1@example.com"},
            {"id": f"cus_{stop:010}", "email": None}  # Example with no email
        ]
    }

def test_publishable_key(pubkey):
    # Updated implementation to validate the publishable key by creating a test token
    try:
        url = "https://api.stripe.com/v1/tokens"
        headers = {
            "Authorization": f"Bearer {pubkey}",
        }
        # Use Stripe's test card details
        data = {
            "card[number]": "4242424242424242",
            "card[exp_month]": "12",
            "card[exp_year]": "2025",
            "card[cvc]": "123",
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return {"status": True, "raw_response": response.json()}
        else:
            # Attempt to parse JSON error message
            try:
                error_message = response.json().get('error', response.text)
            except json.JSONDecodeError:
                error_message = response.text
            return {"status": False, "error": error_message}
    except Exception as e:
        return {"status": False, "error": str(e)}

def test_custom_endpoint(secret_key, endpoint):
    # Placeholder implementation
    try:
        headers = {"Authorization": f"Bearer {secret_key}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return {"status": True, "raw_response": response.json()}
        else:
            return {"status": False, "raw_response": response.text}
    except Exception as e:
        return {"status": False, "error": str(e)}

# Function to Test List Charges
def test_list_charges(secret_key):
    headers = {"Authorization": f"Bearer {secret_key}"}
    try:
        response = requests.get("https://api.stripe.com/v1/charges", headers=headers)
        if response.status_code == 200:
            return {"status": True, "raw_response": response.json()}
        else:
            # Attempt to parse JSON error message
            try:
                return {"status": False, "raw_response": response.json()}
            except json.JSONDecodeError:
                return {"status": False, "raw_response": response.text}
    except Exception as e:
        return {"status": False, "error": str(e)}

# Main Function
def main(
    mode: str = typer.Option(None, help="Testing mode (default, brute-force, pubkey, full, restricted, custom)", rich_help_panel="Modes"),
    secretkey: str = typer.Option(None, help="Stripe secret key (sk_test_xxx or rk_test_xxx)", rich_help_panel="Credentials"),
    pubkey: str = typer.Option(None, help="Stripe publishable key (pk_test_xxx)", rich_help_panel="Credentials"),
    start: int = typer.Option(None, help="Start of customer ID range (used with brute-force mode)", rich_help_panel="Brute-force Options"),
    stop: int = typer.Option(None, help="End of customer ID range (used with brute-force mode)", rich_help_panel="Brute-force Options"),
    delay: int = typer.Option(500, help="Time delay between requests in milliseconds (default: 500ms)", rich_help_panel="Brute-force Options"),
    custom_endpoint: str = typer.Option(None, help="Custom endpoint to test (used with custom mode)", rich_help_panel="Custom Options"),
    output_folder: str = typer.Option("output", help="Folder to save results (default: output)", rich_help_panel="Output")
):
    # Display header and menu if no arguments are provided
    if len(sys.argv) == 1:
        display_header()
        display_menu()
        raise typer.Exit()

    results = {}

    if mode == "default":
        if not secretkey:
            console.print("[bold red]Error: --secretkey is required for default mode.[/bold red]")
            raise typer.Exit()
        console.print("Testing if the secret key can list charges...")
        test_result = test_list_charges(secretkey)
        results["list_charges"] = test_result

    elif mode == "brute-force":
        if not secretkey or start is None or stop is None:
            console.print("[bold red]Error: --secretkey, --start, and --stop are required for brute-force mode.[/bold red]")
            raise typer.Exit()
        if start > stop:
            console.print("[bold red]Error: --start must be less than or equal to --stop.[/bold red]")
            raise typer.Exit()
        console.print(f"Brute-forcing customer IDs from cus_{start:010} to cus_{stop:010} with a delay of {delay}ms...")
        brute_force_data = brute_force_customers(secretkey, delay, start, stop)
        results["brute_force_results"] = brute_force_data

    elif mode == "pubkey":
        if not pubkey:
            console.print("[bold red]Error: --pubkey is required for pubkey mode.[/bold red]")
            raise typer.Exit()
        console.print("Testing Publishable Key by creating a test token...")
        pubkey_result = test_publishable_key(pubkey)
        results["test_publishable_key"] = pubkey_result

    elif mode == "full":
        if not secretkey or not pubkey:
            console.print("[bold red]Error: --secretkey and --pubkey are required for full mode.[/bold red]")
            raise typer.Exit()
        console.print("Testing full validation (secret key and publishable key)...")
        list_charges_result = test_list_charges(secretkey)
        results["list_charges"] = list_charges_result
        pubkey_result = test_publishable_key(pubkey)
        results["test_publishable_key"] = pubkey_result

    elif mode == "restricted":
        if not secretkey:
            console.print("[bold red]Error: --secretkey is required for restricted mode.[/bold red]")
            raise typer.Exit()
        console.print("Testing restricted key...")
        restricted_result = test_list_charges(secretkey)
        results["list_charges"] = restricted_result

    elif mode == "custom":
        if not secretkey or not custom_endpoint:
            console.print("[bold red]Error: --secretkey and --custom-endpoint are required for custom mode.[/bold red]")
            raise typer.Exit()
        console.print(f"Testing custom endpoint {custom_endpoint}...")
        custom_result = test_custom_endpoint(secretkey, custom_endpoint)
        results["test_custom_endpoint"] = custom_result

    else:
        console.print(f"[bold red]Error: Unknown mode '{mode}'. Please choose a valid mode.[/bold red]")
        raise typer.Exit()

    # Validate and save results
    if results:
        save_results_to_file(results, output_folder)
    else:
        console.print("[bold yellow]No results to save. Ensure the mode executed properly.[/bold yellow]")

    # Display results if available
    if results:
        display_results(results)
    else:
        console.print("[bold yellow]No results to display.[/bold yellow]")

if __name__ == "__main__":
    typer.run(main)
