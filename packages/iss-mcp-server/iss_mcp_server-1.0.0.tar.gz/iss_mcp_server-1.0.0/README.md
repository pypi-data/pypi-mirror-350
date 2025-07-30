# ISS Telemetry MCP Server

A Model Context Protocol (MCP) server that provides access to International Space Station (ISS) telemetry data. This server is built using the FastMCP SDK and offers real-time data on environmental conditions, orbital parameters, solar array positions, and waste/water management systems.

## 🚀 Features

- **Environmental Data**: Cabin pressure, temperature, humidity, CO2 and oxygen levels
- **Orbital Parameters**: Altitude, velocity, position, and orbital period
- **Solar Array Position**: Gimbal angles and power output data
- **Waste & Water Management**: Tank levels and system status
- **Communication Status**: Signal acquisition and ground station contact
- **Data Persistence**: Save telemetry data to files for analysis

## 📋 Available Tools

1. `get_iss_environmental_data()` - Current environmental conditions inside the ISS
2. `get_iss_orbital_data()` - Current orbital parameters and position
3. `get_iss_solar_array_position()` - Solar array angles and power output
4. `get_iss_waste_water_management()` - Waste and water system status
5. `get_iss_signal_status()` - Communication signal status with ground
6. `get_all_iss_telemetry()` - Comprehensive data from all systems
7. `save_telemetry_to_file(data_type, filename)` - Save data to JSON files

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Option 1: Install via uvx (Recommended)

The easiest way to install and run the ISS MCP server is using `uvx`:

```bash
# Install uvx if you don't have it
pip install uvx

# Install and run the ISS MCP server
uvx iss-mcp-server

# Or install from GitHub (once published)
uvx --from git+https://github.com/yourusername/iss-mcp-server iss-mcp-server

# Run the client example
uvx --from git+https://github.com/yourusername/iss-mcp-server iss-mcp-client-example
```

### Option 2: Install via pipx

```bash
# Install pipx if you don't have it
pip install pipx

# Install from GitHub
pipx install git+https://github.com/yourusername/iss-mcp-server

# Run the server
iss-mcp-server

# Run the client example
iss-mcp-client-example
```

### Option 3: Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd iss_mcp
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install in development mode:**
   ```bash
   pip install -e .
   ```

## 🚀 Usage

### After uvx/pipx Installation

Once installed via uvx or pipx, you can use the console commands:

```bash
# Run the MCP server
iss-mcp-server

# Run in test mode to see sample data
iss-mcp-server --test

# Run the client example
iss-mcp-client-example
```

### Local Development Usage

### Running the MCP Server

**Option 1: As an MCP Server (for use with MCP clients)**
```bash
python iss_mcp_server.py
```

**Option 2: Test Mode (to see sample data)**
```bash
python iss_mcp_server.py --test
```

### Using the Client Example

Run the example client to see all available data:
```bash
python client_example.py
```

### Quick Test

Test a single tool with the simple test script:
```bash
python test_single_tool.py
```

### Integration with Other MCP Clients

You can use this server with any MCP-compatible client. The server follows the standard MCP protocol and can be integrated into various AI applications.

**Example with FastMCP Client:**
```python
from fastmcp import Client
import asyncio

async def get_iss_data():
    client = Client("iss_mcp_server.py")
    async with client:
        # Get environmental data
        env_data = await client.call_tool("get_iss_environmental_data")
        print(env_data)
        
        # Get orbital data
        orbital_data = await client.call_tool("get_iss_orbital_data")
        print(orbital_data)

asyncio.run(get_iss_data())
```

**Using with Claude Desktop or other MCP clients:**

Add this server to your MCP client configuration:
```json
{
  "mcpServers": {
    "iss-telemetry": {
      "command": "python",
      "args": ["/path/to/iss_mcp/iss_mcp_server.py"]
    }
  }
}
```

## 📊 Data Structure

### Environmental Data
```json
{
  "cabin_pressure": {"timestamp": "...", "value": 760.2, "unit": "mmHg"},
  "cabin_temperature": {"timestamp": "...", "value": 22.1, "unit": "°C"},
  "humidity": {"timestamp": "...", "value": 45.3, "unit": "%"},
  "co2_level": {"timestamp": "...", "value": 2.8, "unit": "ppm"},
  "oxygen_level": {"timestamp": "...", "value": 20.9, "unit": "%"}
}
```

### Orbital Data
```json
{
  "altitude": {"timestamp": "...", "value": 408.2, "unit": "km"},
  "velocity": {"timestamp": "...", "value": 7.66, "unit": "km/s"},
  "latitude": {"timestamp": "...", "value": 23.4, "unit": "degrees"},
  "longitude": {"timestamp": "...", "value": -45.7, "unit": "degrees"},
  "orbital_period": {"timestamp": "...", "value": 92.8, "unit": "minutes"}
}
```

### Solar Array Data
```json
{
  "beta_gimbal_angle": {"timestamp": "...", "value": 45.2, "unit": "degrees"},
  "alpha_gimbal_angle": {"timestamp": "...", "value": 12.8, "unit": "degrees"},
  "power_output": {"timestamp": "...", "value": 84500, "unit": "watts"},
  "sun_tracking_status": "TRACKING"
}
```

## 🔧 Configuration

The server currently provides simulated data that represents realistic ISS telemetry values. To connect to actual ISS data feeds, you would need to:

1. Obtain access to NASA's ISS Live API or similar data sources
2. Implement authentication and connection logic
3. Replace the simulated data functions with real data fetching

## 🌟 Inspiration

This MCP server was inspired by the JavaScript implementation that connects to the Lightstreamer ISS Live data feed. While this version currently provides simulated data, it demonstrates the structure and capabilities needed for real ISS telemetry integration.

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new telemetry data types
- Implement real ISS data feed connections
- Improve data validation and error handling
- Add more comprehensive testing

## 🔗 Related Resources

- [NASA ISS Live](https://www.nasa.gov/live/)
- [ISS Tracker](https://spotthestation.nasa.gov/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Note**: This server currently provides simulated ISS telemetry data for demonstration purposes. For production use with real ISS data, additional authentication and data source integration would be required. 