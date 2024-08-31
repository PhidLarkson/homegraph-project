# HomeLink

**HomeLink** is a decentralized smart home dashboard that integrates Ethereum smart contracts, GhanaNLP language support, real-time data monitoring, and IoT control via an ESP32 microcontroller. This platform allows users to manage bills, monitor transactions, control their smart home devices, and communicate in local languages—all from a powerful and professional interface.

## 🚀 Features

- **Smart Home Control**: Use an ESP32 microcontroller to manage your home devices via Wi-Fi.
- **Decentralized Billing**: Generate, track, and pay bills using Ethereum smart contracts.
- **Real-time Data Visualization**: Monitor transactions, utility usage, and other relevant data.
- **GhanaNLP Integration**: Translate and generate audio in local Ghanaian languages for enhanced accessibility.
- **MetaMask Integration**: Connect your wallet to interact with smart contracts directly from the dashboard.
- **The Graph Protocol**: Query data from the Ethereum blockchain for accurate and up-to-date information.

## 🛠 How It’s Built

### Technologies Used

- **ESP32 Microcontroller**: Represents the smart home, enabling real-time IoT control.
- **Django Backend**: Manages a JSON-based local API to trigger actions and update the system.
- **JavaScript & HTMX**: Power the dynamic front-end, enabling real-time interaction with smart contracts and data visualization.
- **Ethereum Smart Contracts**: Written in Solidity, these handle bill generation, payments, and tracking.
- **The Graph Protocol**: Used to query blockchain data, ensuring accurate and up-to-date information.
- **MetaMask Integration**: Facilitates wallet connection for blockchain interaction.
- **GhanaNLP**: Provides language support for translation and audio generation in Ghanaian dialects, making the smart home accessible to non-English speakers.

### Notable Hacks

One particularly notable hack is how HomeLink’s smart home setup was streamlined using only an ESP32 and a JSON file acting as the local API. The monitoring script leverages this setup to trigger actions without requiring a heavy backend. Additionally, the integration of GhanaNLP for localized language support involved fine-tuning models to handle both translation and TTS functionalities efficiently within the existing system architecture.

## 📂 Project Structure

```plaintext
HomeLink/
├── backend/
│   ├── django_app/
│   └── contracts/
├── frontend/
│   ├── static/
│   ├── templates/
│   ├── js/
│   └── css/
├── esp32/
│   ├── firmware/
│   └── config/
├── data/
│   └── json/
└── README.md
```

## 📦 Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/YourUsername/HomeLink.git
    cd HomeLink
    ```

2. **Install Dependencies**

    - **Backend** (Django & Python packages)

      ```bash
      cd backend/django_app
      pip install -r requirements.txt
      ```

    - **Frontend** (JavaScript & CSS)

      *(No specific installation required for JS/CSS dependencies in this template)*

    - **ESP32** (Arduino IDE or PlatformIO)

      ```bash
      cd esp32/firmware
      # Load and compile the firmware using Arduino IDE or PlatformIO
      ```

3. **Setup Environment Variables**

    Create a `.env` file in the backend directory with the necessary environment variables:

    ```plaintext
    SECRET_KEY=your_secret_key
    ETHEREUM_NODE_URL=https://your.ethereum.node.url
    ```

4. **Run the Django Server**

    ```bash
    cd backend/django_app
    python manage.py migrate
    python manage.py runserver
    ```

5. **Deploy Smart Contracts**

    Deploy the Solidity contracts and update the deployed contract addresses in the Django settings.

6. **Connect ESP32**

    Flash the ESP32 with the firmware and ensure it’s connected to the Wi-Fi network.

## 🔗 Demo & Links

- **Video Demo**: [Watch Here](#)
- **Deployed Application**: [Visit Here](#)
- **GitHub Repository**: [HomeLink Repository](#)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributions

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.