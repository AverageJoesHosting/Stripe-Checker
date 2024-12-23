# Stripe Checker

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/AverageJoesHosting/Stripe-Checker.svg)
![GitHub Stars](https://img.shields.io/github/stars/AverageJoesHosting/Stripe-Checker.svg)

## Overview

**Stripe Checker** is a Python-based tool developed by **Average Joe's Hosting LLC** designed to audit and validate Stripe API keys. It ensures the security and proper configuration of both secret and publishable keys through various testing modes. Whether you're a developer or a security professional, Stripe Checker provides a comprehensive solution to safeguard your Stripe integrations against potential vulnerabilities and misconfigurations.

## Features

- **Multiple Testing Modes:**
  - **Default:** Validate the secret key by listing charges.
  - **Brute-Force:** Discover customers by brute-forcing customer IDs within a specified range.
  - **Publishable Key Validation:** Verify publishable keys by creating test tokens.
  - **Full Validation:** Assess both secret and publishable keys simultaneously.
  - **Restricted Key Testing:** Validate restricted secret keys with limited permissions.
  - **Custom Endpoint Testing:** Test specific endpoints using a secret key.

- **Configurable Parameters:**
  - **Delay:** Set the delay (in milliseconds) between requests during brute-force operations.
  - **Customer ID Range:** Define the start and stop range for brute-forcing customer IDs.
  - **Output Directory:** Specify a custom folder to save test results.

- **Comprehensive Reporting:**
  - Generates detailed CSV reports with test results, statuses, and relevant data.
  - Displays results in a structured table format within the console for quick analysis.

- **User-Friendly Interface:**
  - Intuitive menu with clear usage instructions and examples.
  - Integrated help content for easy reference and guidance.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AverageJoesHosting/Stripe-Checker.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd Stripe-Checker
   ```
3. **Install Dependencies:**
   Ensure you have Python 3.8 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the `stripeChecker.py` script with the desired mode and options:

```bash
python stripeChecker.py -m <mode> [OPTIONS]
```

### Available Modes and Usage

1. **Default Mode**
   - **Description:** Validate the secret key by listing charges.
   - **Usage:**
     ```bash
     python stripeChecker.py -m default --secretkey <SECRET_KEY>
     ```

2. **Brute-Force Mode**
   - **Description:** Discover customers by brute-forcing customer IDs within a specified range.
   - **Usage:**
     ```bash
     python stripeChecker.py -m brute-force --secretkey <SECRET_KEY> --start <START_ID> --stop <STOP_ID> [--delay <DELAY_MS>]
     ```

3. **Publishable Key Validation**
   - **Description:** Validate the publishable key by creating tokens.
   - **Usage:**
     ```bash
     python stripeChecker.py -m pubkey --pubkey <PUBLISHABLE_KEY>
     ```

4. **Full Validation Mode**
   - **Description:** Validate both secret and publishable keys simultaneously.
   - **Usage:**
     ```bash
     python stripeChecker.py -m full --secretkey <SECRET_KEY> --pubkey <PUBLISHABLE_KEY>
     ```

5. **Restricted Key Testing**
   - **Description:** Validate restricted secret keys by listing charges.
   - **Usage:**
     ```bash
     python stripeChecker.py -m restricted --secretkey <RESTRICTED_KEY>
     ```

6. **Custom Endpoint Testing**
   - **Description:** Test a custom endpoint using a secret key.
   - **Usage:**
     ```bash
     python stripeChecker.py -m custom --secretkey <SECRET_KEY> --custom-endpoint <ENDPOINT>
     ```

### Additional Options

- `--delay`: Set the delay (in ms) between requests during brute-force (default: 500ms).
- `--start/--stop`: Define the range for brute-forcing customer IDs (required for brute-force mode).
- `--output-folder`: Specify the folder to save results (default: `./output`).

### Example Commands

- **Validate a Secret Key:**
  ```bash
  python stripeChecker.py -m default --secretkey sk_test_xxx
  ```

- **Discover Customers with Brute-Force:**
  ```bash
  python stripeChecker.py -m brute-force --secretkey sk_test_xxx --start 1 --stop 100 --delay 200
  ```

- **Validate a Publishable Key:**
  ```bash
  python stripeChecker.py -m pubkey --pubkey pk_test_xxx
  ```

- **Full Validation of Both Keys:**
  ```bash
  python stripeChecker.py -m full --secretkey sk_test_xxx --pubkey pk_test_xxx
  ```

- **Test a Custom Endpoint:**
  ```bash
  python stripeChecker.py -m custom --secretkey sk_test_xxx --custom-endpoint https://yourapi.com/test
  ```

## Usage Tips

- **API Keys:**
  - Ensure you have the correct API keys (secret and/or publishable) before running tests.
  - Use Stripe's test keys (`sk_test_...` and `pk_test_...`) to avoid unintended charges.

- **Rate Limits:**
  - When using brute-force mode, be mindful of Stripe's rate limits to prevent temporary blocking.

- **Security:**
  - Store your API keys securely and avoid hardcoding them in scripts or sharing them publicly.

- **Review Outputs:**
  - Review the output CSV files for detailed results and potential issues.

## Best Practices

- **Key Rotation:**
  - Regularly rotate your API keys to maintain security.

- **Permission Management:**
  - Limit the permissions of restricted keys to only what is necessary for your application.

- **Monitoring:**
  - Monitor Stripe's dashboard for any unusual activity or access patterns.

- **Secure Storage:**
  - Use environment variables or secure storage solutions to manage your API keys in production environments.

- **Output Security:**
  - Keep the `output` folder secure, especially if it contains sensitive information from your tests.

## Common Scenarios

- **Validating Keys:**
  - Use `default` or `full` mode to ensure your secret and publishable keys are active and correctly configured.

- **Security Audits:**
  - Utilize `restricted` mode to test keys with limited permissions, ensuring they adhere to the principle of least privilege.

- **Custom Integrations:**
  - Leverage `custom` mode to test specific endpoints tailored to your application's needs.

- **Data Discovery:**
  - Apply `brute-force` mode responsibly to identify and manage customer IDs within a specified range.

## 🤝 Contributing

We welcome contributions to improve the project:

1. **Fork the Repository:**
   Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork:**
   ```bash
   git clone https://github.com/AverageJoesHosting/Stripe-Checker.git
   cd Stripe-Checker
   ```

3. **Create a New Branch:**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes:**
   Implement your feature or bug fix.

5. **Commit Your Changes:**
   ```bash
   git commit -m "Add your commit message"
   ```

6. **Push to Your Fork:**
   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request:**
   Go to the original repository and click "Compare & pull request" to submit your changes.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 📞 Support

For questions or assistance, reach out to Average Joe's Hosting:

- 🌐 **Website:** [AverageJoesHosting.com](https://AverageJoesHosting.com)
- 📧 **Email:** [helpme@averagejoeshosting.com](mailto:helpme@averagejoeshosting.com)
- ☎️ **Phone:** (888) 563-1216

## 👋 About Average Joe's Hosting

Average Joe's Hosting specializes in delivering affordable, high-quality technology solutions to small businesses and organizations. Our mission is to make security and technology accessible to everyone.

Let’s work together to secure the web, one test at a time! 🌟

## Follow Us on Social Media

- 🐦 **Twitter:** [@AverageJoesHost](https://twitter.com/AverageJoesHost)
- 🎥 **YouTube:** [Average Joe's Hosting on YouTube](https://www.youtube.com/@AverageJoesHosting)
- 👥 **Facebook:** [Average Joe's Hosting on Facebook](https://www.facebook.com/AverageJoesHosting)
- 💼 **LinkedIn:** [Average Joe's Hosting on LinkedIn](https://www.linkedin.com/company/averagejoeshosting/)

🎉 Get started with Automation Booster and let your Discord server do the work for you!

---
