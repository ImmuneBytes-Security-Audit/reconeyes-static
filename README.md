# Reconeyes - a static analyzer for Solidity smart contracts



<div align="center"> <br><br>
  <img src="https://github.com/ImmuneBytes-Security-Audit/reconeyes-static/blob/main/logo_black.jpg" alt="Logo"><br><br>
</div>



Reconeyes is a static analysis tool designed to detect vulnerabilities in Solidity smart contracts. With a focus on security, Reconeyes aims to provide developers and auditors with a reliable means of identifying potential risks in their smart contracts.

## **Features**

- Support for 80+ vulnerabilities
- Up to date with Solidity versions >0.7.0
- Integration with CI/CD Pipelines
- Cross-Platform Compatibility
- Support for Smart Contract Libraries

## Installing Reconeyes

### Prerequisites

First, clone the repository into your local machine:

```jsx
git clone https://github.com/ImmuneBytes-Security-Audit/reconeyes-static
```

You will need to have Python 3.7+ installed on your machine. Reconeyes also uses solidity_parser, termcolor, shutil, os, pprint and solcx python packages. You can install the packages using pip.

```jsx
pip install <package name>

```
After that, you should be good to go.

## Using Reconeyes

To start using Reconeyes, go to the reconeyes-static directory, then use the following command:

```jsx
python3 main.py /path/to/your/contract.sol

```
After the scan is completed, you will get the results and corresponding recommendations.

## Detectors

Reconeyes gives you the ability to scan your smart contract code to find the underlying vulnerabilities listed in the sheet [here](https://docs.google.com/spreadsheets/d/1qiN27zqaVhNk-uTlLTbEhOBoMNPPXfmd90QpmVMe4SQ/edit#gid=143538190) 🔗.

## Contributing

At the core of our philosophy lies the belief that everyone can contribute and enact meaningful change. Whether you're passionate about coding, adept at bug-fixing, or simply eager to share feedback, your contributions are invaluable and warmly welcomed.

We invite active security researchers and auditors in the Web3 security domain to contribute to Reconeyes. Your expertise can help us enhance the tool's capabilities and ensure its effectiveness in identifying vulnerabilities in Solidity smart contracts. 

Here's how you can contribute:

- **Add and Improve Detectors**: Enhance Reconeyes by adding new detectors or improving existing ones to detect a wider range of vulnerabilities.
- **User Experience**: Help us refine the user experience to make it more intuitive and user-friendly.
- **Compatibility**: Ensure Reconeyes is compatible with different operating systems to maximize its accessibility and usability.

We are also building an ML aspect to Reconeyes, wherein we have employed new-gen deep learning algorithms to further eradicate the occurrence of false positives and increase accuracy. If you're interested in contributing to the machine learning aspect of Reconeyes, please fill out the following Google Form to join our closed group of devs: [Google Form](https://forms.gle/qomeGfSVTpiP66d68) 📄

## Community

To achieve our ambitious goal of securing Web3, we require a diverse community of contributors. Whether you're an experienced developer or just embarking on your journey of security audits, there's a place for you here! Join the Reconeyes community on our Telegram server, where you can ask questions, exchange ideas, and receive assistance from both fellow developers and the Reconeyes team directly!

Additionally, feel free to follow us on Twitter for updates, sneak peeks, and all the latest news. It's a fantastic way to stay informed and engaged with our progress 😄.

We're excited to welcome you aboard!
