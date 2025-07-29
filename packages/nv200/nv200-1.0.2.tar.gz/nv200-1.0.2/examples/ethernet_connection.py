import asyncio
from nv200.device_interface import DeviceClient
from nv200.transport_protocols import TelnetProtocol


async def ethernet_auto_detect():
    """
    Automatically detects and establishes an Ethernet connection to a device using Telnet.

    This asynchronous function creates a Telnet transport, initializes a device client,
    connects to the device, prints the connected device's IP address, and then closes the connection.
    """
    transport = TelnetProtocol()
    client = DeviceClient(transport)
    await client.connect()
    print(f"Connected to device with IP: {transport.host}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(ethernet_auto_detect())
