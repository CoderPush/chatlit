# Chatlit

Chatlit is an open-source web application powered by Streamlit, designed to provide an extensible chat interface with individual chat histories and multiple chat models. This project is licensed under the MIT license.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10
- Google account for authentication
- pipenv

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/CoderPush/chatlit.git
    cd chatlit
    ```

2. Install dependencies:

    ```bash
    pipenv install
    ```

### Running Locally

Before running the application in the development mode, you need to set up your environment variables. We use a `.env` file, which is gitignored. In production, these are loaded from Stream secrets.

Run the app:

    streamlit run chat.py

## Contributing

We use a trunk-based development workflow, meaning new work is created on a new branch, which is then created as a pull request against the "main" branch. Merging the PR to main will auto deploy the app.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
