# Yannick Leeuwin
# 15208761
# Assignment 2 - MVC (controller)

import pyvisa


def list_resources():
    """Creates list of available resources.

    Returns:
        list: list of VISA resources
    """
    rm = pyvisa.ResourceManager("@py")
    resources = rm.list_resources()
    return resources


class ArduinoVisaDevice:
    """This class is responsible for the communication with the Arduino.

    Contents of this class: getting identification, input/output of values.
    """

    def __init__(self, port):
        """Creates possibility to communicate with connected port.

        Args:
            port (string): this defines the port that is going to be communicated with (in this case the Arduino)
        """
        rm = pyvisa.ResourceManager("@py")

        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )
        self.port = port

    def get_identification(self):
        """Shows identification of connected port.

        Returns:
            string: identification string of Arduino
        """
        identification = self.device.query("*IDN?")
        return identification

    def set_output_value(self, value):
        """Raw value of current is chosen and sent to Arduino on channel 0.

        Args:
            value (int): chosen raw value of current
        """
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self):
        """Retrieves output value of current on channel 0.

        Returns:
            int: raw value of current
        """
        value = self.device.query("OUT:CH0?")
        return value

    def get_input_value(self, channel):
        """Raw value of voltage through channel is asked.

        Args:
            channel (int): number of channel

        Returns:
            int: raw input value through specified channel is shown
        """
        value = self.device.query(f"MEAS:CH{channel}?")
        return value

    def get_input_voltage(self, channel):
        """Voltage of channel is asked. The raw value is converted to voltage using scaling factor (3.3 V / 1024 bits).

        Args:
            channel (int): number of channel on motherboard

        Returns:
            float: voltage is calculated and returned for specific channel
        """
        value = float(self.device.query(f"MEAS:CH{channel}?"))
        step = 3.3 / 1023
        volt = value * step
        return volt

    def close(self):
        self.device.close()
    