# Saigon Steps - AI Training

This is the AI Models Training portion of our University Graduation project. Built with Flask, YOLOv8 and Weaviate.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Required Dependencies](#required-dependencies)
- [Installation](#installation)
- [Development](#development)
- [Features](#features)
- [Suggested VS Code Extensions](#suggested-vs-code-extensions)
- [Contributors](#contributors)

## Technologies Used

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [YOLOv8](https://docs.ultralytics.com/models/yolov8/)
- [Weaviate](https://weaviate.io/)
- [Matplotlib](https://matplotlib.org/)

## Required Dependencies

- `Python` v3.11 or later: [Download Python](https://www.python.org/)
- `Pip`
- `Docker`

Make sure to have these installed before proceeding with the project setup.

## Installation

Follow these steps to set up and run the application locally.

1. Clone the repository:

   ```bash
   git clone https://github.com/YGOhappy123/Saigon-Steps-AI-Training.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Saigon-Steps-AI-Training
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

**Note:** You might consider running this project on a `python virtual environment` to prevent dependencies conflicts with local environment.

## Development

To start the development server, use:

```bash
python src/flask_server.py
```

**Note:** You have to have the `Docker containers` running first. Either using `Docker Desktop` or using the following command in a separate terminal

```bash
docker compose up -d
```

This will start the Flask server

You can view the app by visiting `http://localhost:8000` in your browser.

You can also replace `localhost` with your device's `IPv4 Address`, which can be found by entering the following command in the `terminal` and look for `Wireless LAN adapter Wi-Fi` > `IPv4 Address`:

```bash
ipconfig
```

## Connect Other Devices To This Server

**Requirement:** All devices must be connected to the same network.

Follow these steps to ensure that your firewall allows incoming connections on port 8000.

1. Open `Windows Defender Firewall`.
2. Click on `Advanced settings`.
3. Select `Inbound Rules` and then `New Rule`.
4. Choose `Port`, click `Next`.
5. Select `TCP` and enter `8000` in the specific local ports box.
6. Allow the connection and complete the wizard.

Now you can access the app using other devices by visiting `http://<IPv4 Adddess>:8000`

## Features

- **RESTful API** 🛠 Exposes endpoints following REST principles for ease of use and scalability.
- **Database Integration** 💾 Uses Weaviate vector database for data persistence.
- **Cross-Platform** 🌐 Runs on any operating system that supports Python.

## Suggested VS Code Extensions

| Extension                     | Publisher            | Required? | Supported features                                 |
| :---------------------------- | :------------------- | :-------: | :------------------------------------------------- |
| Prettier - Code formatter     | Prettier             |    Yes    | Code formatting                                    |
| Black Formatter               | Microsoft            |    Yes    | Code formatting                                    |
| Python                        | Microsoft            |    Yes    | Python runtime VS Code                             |
| Docker DX                     | Docker               |    No     | Code formatting and autocomplete                   |
| Code Spell Checker            | Street Side Software |    No     | Spelling checker for source code                   |
| Multiple cursor case preserve | Cardinal90           |    No     | Preserves case when editing with multiple cursors  |
| GitLens                       | GitKraken            |    No     | Enhanced Git integration and code history tracking |

## Contributors

Thanks to the following people for contributing to this project ✨:

<table>
    <tr>
        <td align="center">
            <a href="https://github.com/YGOhappy123">
                <img 
                    src="https://avatars.githubusercontent.com/u/90592072?v=4"
                    alt="YGOhappy123" width="100px;" height="100px;" 
                    style="border-radius: 4px; background: #fff;"
                /><br />
                <sub><b>YGOhappy123</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/hnninh21">
                <img 
                    src="https://avatars.githubusercontent.com/u/107742272?v=4"
                    alt="hnninh21" width="100px;" height="100px;"                 
                    style="border-radius: 4px; background: #fff;"
                /><br />
                <sub><b>hnninh21</b></sub>
            </a>
        </td>
    </tr>
</table>
