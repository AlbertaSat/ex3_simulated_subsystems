# EX3 Simulate Subsystem KSP Interface

This repository contains an interfafce server to KSP using kRPC for the ex3 simulated susbsystem to use for simple visual demonstration of LEOP sequence and as a source for simple data such as GPS positional data, temperature, etc.

## Requirements

- KSP 12.5.3190 (KSP base game with the Making History and Breaking Ground expansions)
- CKAN (for installing mods)
- Python 3.

## Installation

### KSP

Install KSP then install CKAN. Their install guides can be found on their respective websites.

Using CKAN, install the modpack included in this repository.

Copy the included craft file to your KSP install directory under `Ships/VAB/` in your KSP install directory.

### Python Server

Create and activate a python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required python packages

```bash
pip install -r requirements.txt
```

## Usage

### KSP

1. Launch KSP and start a new sandbox game.
2. Load the `ExAlta3` craft in the VAB then launch the craft.
3. Add a kRPC server by clicking the `Add Server` button in the kRPC window (which can be accessed by clicking the `kRPC` button in the toolbar on the right).
4. Start the server by clicking the `Start Server` button in the kRPC window.
5. Open the KSP debug menu then click on the cheats tab.
6. Go to the orbit cheats section and click the `Set Orbit` button.

To start the interface server, run the following command:

```bash
python server.py
```

For simple test client access, you can use netcat (nc) to connect to the server and send commands.

```bash
nc 127.0.0.1 <port>
```

where `<port>` is the port the server is running on (default is 3000).

Once the above command is ran, you can type in commands to the server then press enter to send the command, the server will respond with the result of the command in JSON format or null.