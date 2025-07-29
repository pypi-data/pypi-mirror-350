# -*- coding: utf-8 -*-
"""
Sweeper Class for Conducting Voltage Sweeps with the Nanonis System.

This module provides the Sweeper class to perform 1D and 2D voltage sweeps
across a set of gates using the Nanonis system. It logs measurement data and
generates animated plots for analysis. The class enables precise control of sweep
parameters and records experimental metadata.

Classes:
    Sweeper: Conducts voltage sweeps on specified gates, logs results, and
             generates plots for analysis.

Created on Wed Nov 06 10:46:06 2024
@author:
Chen Huang <chen.huang23@imperial.ac.uk>
"""

from datetime import datetime, date
import math
import time
import os
import logging
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from nanonis_tramea import Nanonis
from .gate import GatesGroup, Gate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Sweeper:
    """
    Sweeper class to perform and log voltage sweeps on defined gates.
    """

    def __init__(
        self,
        outputs: GatesGroup = None,
        inputs: GatesGroup = None,
        nanonisInstance: Nanonis = None,
        temperature: str = None,
        device: str = None,
    ) -> None:
        """Initialize the Sweeper class.

        Args:
            outputs (GatesGroup): Group of output gates to control
            inputs (GatesGroup): Group of input gates to measure
            temperature (str): Temperature of the experiment
            device (str): Device identifier

        Raises:
            ValueError: If outputs or inputs are not GatesGroup instances
        """
        if outputs is not None and not isinstance(outputs, GatesGroup):
            raise ValueError("outputs must be a GatesGroup instance")
        if inputs is not None and not isinstance(inputs, GatesGroup):
            raise ValueError("inputs must be a GatesGroup instance")

        self.outputs = outputs
        self.inputs = inputs
        self.nanonisInstance = nanonisInstance
        self.temperature = temperature
        self.device = device

        # Create necessary directories
        try:
            os.makedirs("data", exist_ok=True)
            os.makedirs("figures", exist_ok=True)
            os.makedirs("logs", exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create directories: {str(e)}")
            raise

        # Initialize other attributes
        self._initialize_attributes()

        logger.info("Sweeper initialized successfully")

    def _initialize_attributes(self):
        """Initialize class attributes with default values."""
        # Labels and file metadata
        self.x_label = None
        self.y_label = None
        self.z_label = None
        self.comments = None
        self.filename = None
        self.base_filename = None

        # Sweep configuration
        self.X_start_volt = None
        self.X_end_volt = None
        self.X_step = None
        self.X_slew_rate = None

        self.Y_start_volt = None
        self.Y_end_volt = None
        self.Y_step = None

        self.total_time = None
        self.time_step = None

        # Measurement data
        self.X_volt = None
        self.Y_volt = None

        self.X_volt_list = []
        self.current_list = []
        self.is_2d_sweep = False

        # Units
        self.X_volt_unit = "V"
        self.Y_volt_unit = "V"
        self.current_unit = "uA"

        self.X_volt_scale = 1
        self.Y_volt_scale = 1
        self.current_scale = 1

    def _set_units(self) -> None:
        """Set voltage and current units based on their respective unit strings."""
        unit_map_voltage = {"V": 1, "mV": 1e3, "uV": 1e6, "nV": 1e9}
        self.X_volt_scale = unit_map_voltage.get(self.X_volt_unit, 1)
        self.Y_volt_scale = unit_map_voltage.get(self.Y_volt_unit, 1)

        unit_map_current = {"mA": 1e-3, "uA": 1, "nA": 1e3, "pA": 1e6}
        self.current_scale = unit_map_current.get(self.current_unit, 1)

    def _convert_units(self, voltage_pack: list[float, str]) -> float:
        """Convert a voltage value with unit to the base unit (Volts).

        Args:
            voltage_pack (list): [value, unit], e.g. [1.0, 'mV'].

        Returns:
            float: Voltage converted to Volts.
        """
        voltage, unit = voltage_pack
        unit_map_voltage = {"V": 1, "mV": 1e-3, "uV": 1e-6, "nV": 1e-9}
        return voltage * unit_map_voltage.get(unit, 1)

    def convert_value(self, value, unit="V"):
        """
        Convert a value with unit to an appropriate SI prefixed string.

        Args:
            value (float): Numerical value.
            unit (str): Unit string (e.g., 'V', 'A').

        Returns:
            str: Formatted string with SI prefix (e.g., '100.000 mV').
        """
        prefixes = {
            -24: "y",
            -21: "z",
            -18: "a",
            -15: "f",
            -12: "p",
            -9: "n",
            -6: "u",
            -3: "m",
            0: "",
            3: "k",
            6: "M",
            9: "G",
            12: "T",
            15: "P",
            18: "E",
            21: "Z",
            24: "Y",
        }
        base_units = {"V", "A"}

        # Split prefix and base unit
        if len(unit) > 1 and unit[0] in ["m", "μ", "u", "n", "p", "k", "M", "G", "T"]:
            prefix = unit[0]
            base_unit = unit[1:]
            if base_unit not in base_units:
                base_unit = unit  # Handle cases without prefix
                prefix = ""
        else:
            prefix = ""
            base_unit = unit

        # Convert to base unit
        prefix_factors = {
            "Y": 1e24,
            "Z": 1e21,
            "E": 1e18,
            "P": 1e15,
            "T": 1e12,
            "G": 1e9,
            "M": 1e6,
            "k": 1e3,
            "": 1,
            "m": 1e-3,
            "μ": 1e-6,
            "u": 1e-6,  # Handle both μ and u for micro-
            "n": 1e-9,
            "p": 1e-12,
            "f": 1e-15,
            "a": 1e-18,
            "z": 1e-21,
            "y": 1e-24,
        }
        base_value = value * prefix_factors.get(prefix, 1)

        # Determine optimal prefix
        if base_value == 0:
            return f"{0:>7.3f} [{base_unit}]"

        exponent = math.floor(math.log10(abs(base_value)))
        exponent_3 = (exponent // 3) * 3
        exponent_3 = max(min(exponent_3, 24), -24)
        new_prefix = prefixes[exponent_3]
        scaled_value = base_value / (10**exponent_3)
        return f"{scaled_value:>7.3f} [{new_prefix}{base_unit}]"

    def _set_filename(self, prefix: str) -> None:
        """Generate a unique filename based on sweep parameters."""
        date_str = date.today().strftime("%Y%m%d")
        labels = {
            "1D": f"[{self.z_label}]_vs_[{self.x_label}]",
            "2D": f"[{self.z_label}]_vs_[{self.x_label}]_[{self.y_label}]",
            "time": f"[{self.z_label}]_vs_time",
        }
        self.base_filename = f"{date_str}_{self.temperature}_{labels[prefix]}"
        if self.comments:
            self.base_filename += f"_{self.comments}"
        self.filename = self._get_unique_filename()

    def _get_unique_filename(self) -> str:
        """Ensure unique filenames by appending a counter."""
        counter = 1
        while os.path.isfile(f"data/{self.base_filename}_run{counter}.txt"):
            counter += 1
        return f"{self.base_filename}_run{counter}"

    def _setup_plot_style(self) -> None:
        """Configure common plotting parameters."""
        plt.rcParams.update(
            {
                "legend.fontsize": 22,
                "legend.framealpha": 0.9,
                "xtick.labelsize": 24,
                "ytick.labelsize": 24,
                "xtick.color": "#2C3E50",
                "ytick.color": "#2C3E50",
                "axes.labelcolor": "#2C3E50",
                "axes.titlesize": 32,
                "figure.facecolor": "white",
            }
        )

    def _log_params_start(self, sweep_type: str = "voltage") -> None:
        """Log initial parameters and setup information."""
        log_path = f"logs/log_{self.base_filename}.txt"
        with open(log_path, "a") as f:
            self.start_time = datetime.now()
            f.write(f"--------/// Run started at {self.start_time} ///--------\n")
            f.write(f"{'Filename:':<16} {self.filename}.txt \n")
            f.write(f"{'Device:':<16} {self.device} \n")
            f.write(f"{'Measured Input:':<16} {self.z_label} \n\n")

            f.write(f"{'X Swept Gates:':<16} {self.x_label} \n")
            if sweep_type == "voltage":
                f.write(f"{'Start:':<16} {self.convert_value(self.X_start_volt)} \n")
                f.write(f"{'End:':<16} {self.convert_value(self.X_end_volt)} \n")
                f.write(f"{'Step:':<16} {self.convert_value(self.X_step)} \n\n")

            if self.is_2d_sweep:
                f.write(f"{'Y Swept Gates:':<16} {self.y_label} \n")
                f.write(f"{'Start:':<16} {self.convert_value(self.Y_start_volt)} \n")
                f.write(f"{'End:':<16} {self.convert_value(self.Y_end_volt)} \n")
                f.write(f"{'Step:':<16} {self.convert_value(self.Y_step)} \n\n")

            if sweep_type == "time":
                f.write(f"{'Total Time:':<16} {self.total_time:>16.2f} [s] \n")
                f.write(f"{'Time Step:':<16} {self.time_step:>16.2f} [s] \n\n")

            f.write("Initial Voltages of all outputs before sweep: \n")
            for gate in self.outputs.gates:
                voltage = gate.get_volt()
                f.write(f"{gate.label:<55} {self.convert_value(voltage)} \n")
            f.write("\n")

    def _log_params_end(self) -> None:
        """Log completion time and total duration."""
        log_path = f"logs/log_{self.base_filename}.txt"
        with open(log_path, "a") as f:
            f.write(f"{'Total Time:':<16} {datetime.now() - self.start_time} \n")
            f.write(f"--------/// Run ended at {datetime.now()} ///--------\n\n")

    def _validate_voltage_params(self, start: list, end: list, step: list) -> None:
        """Validate voltage parameters with proper error messages."""
        if any(not isinstance(v, list) or len(v) != 2 for v in [start, end, step]):
            raise ValueError("Voltage parameters must be [value, unit] lists")
        if step[0] <= 0:
            raise ValueError("Step voltage must be positive")
        if self._convert_units(start) == self._convert_units(end):
            raise ValueError("Start and end voltages are identical")

    def _validate_units(self, unit: str, unit_type: str = "voltage") -> None:
        """Validate unit specifications.

        Args:
            unit (str): Unit to validate
            unit_type (str): Type of unit ('voltage' or 'current')

        Raises:
            ValueError: If unit is invalid
        """
        voltage_units = {"V", "mV", "uV" "μV", "nV"}
        current_units = {"mA", "uA", "μA", "nA", "pA"}

        if unit_type == "voltage" and unit not in voltage_units:
            raise ValueError(f"Invalid voltage unit. Must be one of {voltage_units}")
        elif unit_type == "current" and unit not in current_units:
            raise ValueError(f"Invalid current unit. Must be one of {current_units}")

    def _write_to_file(self, filepath, content):
        """Helper method to write content to a file."""
        try:
            with open(filepath, "a") as file:
                file.write(content)
        except IOError as e:
            logger.error(f"Failed to write to file {filepath}: {str(e)}")
            raise

    def sweep1D(
        self,
        swept_outputs: GatesGroup,
        measured_inputs: GatesGroup,
        start_voltage: list[float, str],
        end_voltage: list[float, str],
        step: list[float, str],
        slew_rate: float = 1.0,
        initial_state: list = [],
        current_unit: str = "uA",
        comments: str = None,
        is_2d_sweep: bool = False,
        is_show: bool = True,
    ) -> tuple:
        """
        Perform a 1D voltage sweep with enhanced step calculation and logging.

        Args:
            swept_outputs: Gates to sweep.
            measured_inputs: Gates to measure.
            start_voltage: [value, unit] starting voltage.
            end_voltage: [value, unit] ending voltage.
            step: [value, unit] step size.
            slew_rate: Voltage ramp rate in V/s.
            initial_state: List of (Gate, voltage, unit) for initial setup.
            current_unit: Unit for current measurements.
            comments: Additional comments for logging.
            is_2d_sweep: Internal flag for 2D integration.
            is_show: Whether to display the plot.

        Returns:
            Tuple of voltage and current arrays.
        """
        try:
            # Validate inputs
            self._validate_voltage_params(start_voltage, end_voltage, step)
            self._validate_units(current_unit, "current")

            # Set sweep labels and units
            self.x_label = swept_outputs.labels
            self.z_label = measured_inputs.labels
            self.X_volt_unit = step[1]
            self.current_unit = current_unit
            self.comments = comments
            self.is_2d_sweep = is_2d_sweep
            self.is_show = is_show

            self._set_units()

            if not self.is_2d_sweep:
                self._set_filename("1D")

            # Convert voltage parameters
            self.X_start_volt = self._convert_units(start_voltage)
            self.X_end_volt = self._convert_units(end_voltage)
            self.X_step = self._convert_units(step)
            self.X_slew_rate = slew_rate

            # Pre-allocate data arrays for better performance
            total_points = round(
                abs(self.X_end_volt - self.X_start_volt) / self.X_step + 1
            )
            self.X_volt_list = np.zeros(total_points)
            self.current_list = np.zeros(total_points)

            # Initialize plotting
            if not is_2d_sweep:
                self._setup_1d_plot()

            # Set initial state
            self._set_initial_state(initial_state, swept_outputs)

            # Log parameters and start sweep
            if not self.is_2d_sweep:
                self._log_params_start(sweep_type="voltage")

            if not self.is_2d_sweep:
                self._write_data_header()
                logger.info(
                    f"Starting 1D sweep from {self.X_start_volt * self.X_volt_scale:.3f} "
                    f"[{self.X_volt_unit}] to {self.X_end_volt * self.X_volt_scale:.3f} "
                    f"[{self.X_volt_unit}]"
                )

            # Perform sweep
            for gate in swept_outputs.gates:
                gate.set_slew_rate(self.X_slew_rate)  # Set slew rate to 1 V/s
            for i in tqdm(
                range(total_points), desc="Sweeping", ncols=80, disable=is_2d_sweep
            ):
                self.X_volt = (
                    self.X_start_volt + i * self.X_step
                    if self.X_start_volt < self.X_end_volt
                    else self.X_start_volt - i * self.X_step
                )

                # Set voltage and measure
                swept_outputs.voltage(self.X_volt)
                self.X_volt_list[i] = self.X_volt * self.X_volt_scale
                self.current_list[i] = (
                    measured_inputs.gates[0].read_current() * self.current_scale
                )

                # Update plot
                if not is_2d_sweep:
                    self._update_plot(i)
                self._write_measurement_data(i)

            # Finalize
            if not self.is_2d_sweep:
                self._log_params_end()

                # Save and show plot
                self._save_and_show_plot()
                logger.info("1D sweep complete and figure saved")
            else:
                return self.X_volt_list, self.current_list

        except Exception as e:
            logger.error(f"Error during 1D sweep: {str(e)}")
            raise

    def _set_initial_state(self, initial_state, swept_outputs=None):
        """Set up initial state for the sweep."""
        if not self.is_2d_sweep:
            logger.info("Setting up initial state")
        # Set initial states
        converted_init_state = []
        if swept_outputs is not None:
            for gate in swept_outputs.gates:
                gate.set_slew_rate(0.1)  # Set slew rate to 100 mV/s
                gate.voltage(self.X_start_volt, is_wait=False)
                
            for gate, init_volt, init_unit in initial_state:
                if gate not in swept_outputs.gates:
                    gate.set_slew_rate(0.1)  # Set slew rate to 100 mV/s
                    converted_init_volt = self._convert_units([init_volt, init_unit])
                    converted_init_state.append([gate, converted_init_volt])
                    gate.voltage(converted_init_volt, is_wait=False)
                
            # Wait for stabilization
            while not all(
                [
                    gate.is_at_target_voltage(voltage)
                    for gate, voltage in converted_init_state if gate not in swept_outputs.gates
                ]
            ):
                time.sleep(0.1)
                
            while not all(
                [
                    gate.is_at_target_voltage(self.X_start_volt)
                    for gate in swept_outputs.gates
                ]
            ):
                time.sleep(0.1)
                    
                    
        else:
            for gate, init_volt, init_unit in initial_state:
                gate.set_slew_rate(0.1)  # Set slew rate to 100 mV/s
                converted_init_volt = self._convert_units([init_volt, init_unit])
                converted_init_state.append([gate, converted_init_volt])
                gate.voltage(converted_init_volt, is_wait=False)
                
            while not all(
                [
                    gate.is_at_target_voltage(voltage)
                    for gate, voltage in converted_init_state
                ]
            ):
                time.sleep(0.1)
                

    def _setup_1d_plot(self):
        """Set up the initial 1D plot."""

        # Set up figure and axes
        plt.ion()
        plt.rc("legend", fontsize=22, framealpha=0.9)
        plt.rc("xtick", labelsize=24, color="#2C3E50")
        plt.rc("ytick", labelsize=24, color="#2C3E50")

        self.fig, self.ax = plt.subplots(figsize=(12, 7))

        # Configure plot style
        self.fig.patch.set_facecolor("white")

        # Border
        for spine in self.ax.spines.values():
            spine.set_color("#2C3E50")

        # Axes labels
        self.ax.set_xlabel(
            f"{self.x_label} [{self.X_volt_unit}]", color="#2C3E50", fontsize=32
        )
        self.ax.set_ylabel(
            f"{self.z_label} [{self.current_unit}]", color="#2C3E50", fontsize=32
        )

        # Ticks
        self.ax.tick_params(
            axis="y",
            direction="in",
            width=4,
            length=10,
            pad=10,
            right=True,
            labelsize=24,
        )
        self.ax.tick_params(
            axis="x",
            direction="in",
            width=4,
            length=10,
            pad=10,
            top=False,
            labelsize=24,
        )

        # Create image plot
        (self.data_lines,) = self.ax.plot([], [], lw=2)

    def _update_plot(self, index):
        """Update the plot with new data."""
        if index > 0:  # Only update after first point
            self.ax.set_xlim(
                min(self.X_volt_list[: index + 1]) - self.X_step * self.X_volt_scale,
                max(self.X_volt_list[: index + 1]) + self.X_step * self.X_volt_scale,
            )
            curr_min = min(self.current_list[: index + 1])
            curr_max = max(self.current_list[: index + 1])
            self.ax.set_ylim(
                curr_min - (curr_max - curr_min) / 4,
                curr_max + (curr_max - curr_min) / 4,
            )
        self.data_lines.set_data(
            self.X_volt_list[: index + 1], self.current_list[: index + 1]
        )
        plt.draw()
        plt.pause(0.001)

    def _write_data_header(self):
        """Write the data file header."""
        try:
            with open(f"data/{self.filename}.txt", "a") as file:
                header = f"{self.x_label} [{self.X_volt_unit}]".rjust(
                    16
                ) + f"{self.z_label} [{self.current_unit}]".rjust(16)
                file.write(header + "\n")
        except IOError as e:
            logger.error(f"Failed to write data header: {str(e)}")
            raise

    def _write_measurement_data(self, index):
        """Write measurement data to file."""
        try:
            content = (
                f"{self.Y_volt * self.Y_volt_scale:>16.4f} "
                f"{self.X_volt_list[index]:>16.4f} "
                f"{self.current_list[index]:>16.8f}\n"
                if self.is_2d_sweep
                else f"{self.X_volt_list[index]:>16.4f} "
                f"{self.current_list[index]:>16.8f}\n"
            )
            self._write_to_file(f"data/{self.filename}.txt", content)
        except IOError as e:
            logger.error(f"Failed to write measurement data: {str(e)}")
            raise

    def _save_and_show_plot(self):
        """Save and optionally show the final plot."""
        try:
            plt.ioff()
            plt.tight_layout()
            plt.savefig(f"figures/{self.filename}.png", dpi=300, bbox_inches="tight")
            if self.is_show:
                plt.show()
            else:
                plt.close()
        except Exception as e:
            logger.error(f"Failed to save or show plot: {str(e)}")
            raise

    def sweep2D(
        self,
        X_swept_outputs: GatesGroup,
        X_start_voltage: list[float, str],
        X_end_voltage: list[float, str],
        X_step: list[float, str],
        Y_swept_outputs: GatesGroup,
        Y_start_voltage: list[float, str],
        Y_end_voltage: list[float, str],
        Y_step: list[float, str],
        measured_inputs: GatesGroup,
        initial_state: list,
        current_unit: str = "uA",
        comments: str = None,
        is_show: bool = True,
    ):
        """
        Perform a 2D voltage sweep over two axes by sweeping one set of outputs for each voltage
        setting of another set.

        Args:
            X_swept_outputs (GatesGroup): Gates to sweep along the X axis.
            X_start_voltage (list): Starting voltage for X axis as [value, unit].
            X_end_voltage (list): Ending voltage for X axis as [value, unit].
            X_step (list): Voltage step for X axis as [value, unit].
            Y_swept_outputs (GatesGroup): Gates to sweep along the Y axis.
            Y_start_voltage (list): Starting voltage for Y axis as [value, unit].
            Y_end_voltage (list): Ending voltage for Y axis as [value, unit].
            Y_step (list): Voltage step for Y axis as [value, unit].
            measured_inputs (GatesGroup): Group of input gates for measurements.
            initial_state (list): List of tuples (gate, init_voltage) where init_voltage is [value, unit].
            current_unit (str): Current unit for display.
            comments (str): Additional comments for logging.
            is_show (bool): Whether to show the plot after completion.
        """
        try:
            # Validate inputs
            for params in [
                (X_start_voltage, X_end_voltage, X_step),
                (Y_start_voltage, Y_end_voltage, Y_step),
            ]:
                self._validate_voltage_params(*params)
            self._validate_units(current_unit, "current")

            # Set up sweep parameters
            self.X_volt_unit = X_step[1]
            self.Y_volt_unit = Y_step[1]
            self.current_unit = current_unit
            self.is_2d_sweep = True
            self._set_units()

            # Convert voltage parameters
            self.X_start_volt = self._convert_units(X_start_voltage)
            self.X_end_volt = self._convert_units(X_end_voltage)
            self.X_step = self._convert_units(X_step)
            self.Y_start_volt = self._convert_units(Y_start_voltage)
            self.Y_end_volt = self._convert_units(Y_end_voltage)
            self.Y_step = self._convert_units(Y_step)

            # Set labels and filename
            self.x_label = X_swept_outputs.labels
            self.y_label = Y_swept_outputs.labels
            self.z_label = measured_inputs.labels
            self.comments = comments
            self.is_show = is_show
            self._set_filename("2D")

            # Write header and start logging
            self._write_2d_data_header()
            self._set_initial_state(initial_state, X_swept_outputs)
            self._log_params_start(sweep_type="voltage")

            # Set up plotting
            # Calculate array dimensions
            X_num = (
                int(round(abs(self.X_end_volt - self.X_start_volt) / self.X_step)) + 1
            )
            Y_num = (
                int(round(abs(self.Y_end_volt - self.Y_start_volt) / self.Y_step)) + 1
            )

            # Pre-allocate data array
            self.data = np.full((Y_num, X_num), np.nan)

            self._setup_2d_plot()

            # Prepare 1D sweep parameters
            params = {
                "swept_outputs": X_swept_outputs,
                "start_voltage": X_start_voltage,
                "end_voltage": X_end_voltage,
                "step": X_step,
                "measured_inputs": measured_inputs,
                "initial_state": initial_state.copy(),
                "current_unit": self.current_unit,
                "comments": comments,
                "is_2d_sweep": True,
            }

            # Perform 2D sweep
            logger.info(
                f"Starting 2D sweep with {Y_num} Y steps and {X_num} X steps per Y value"
            )
            self.Y_volt = self.Y_start_volt

            # Initialize a single progress bar for the entire 2D sweep
            for i in tqdm(range(Y_num), desc="Sweeping", ncols=80):
                tmp_init_state = initial_state.copy()
                for Y_gate in Y_swept_outputs.gates:
                    tmp_init_state.append([Y_gate, self.Y_volt, "V"])
                params["initial_state"] = tmp_init_state

                # if i % 2 == 0:  # Use modulo instead of floor division for clarity
                # params["start_voltage"] = X_start_voltage
                # params["end_voltage"] = X_end_voltage
                # else:
                # params["start_voltage"] = X_end_voltage
                # params["end_voltage"] = X_start_voltage

                params["start_voltage"] = X_start_voltage
                params["end_voltage"] = X_end_voltage

                # Perform 1D sweep
                _, Z_values = self.sweep1D(**params)
                # self.data[i] = Z_values[::-1] if i % 2 == 1 else Z_values
                self.data[i] = Z_values

                # Update plot
                self._update_2d_plot()

                # Calculate next Y voltage
                if i < Y_num - 1:
                    self.Y_volt += (
                        self.Y_step
                        if self.Y_start_volt < self.Y_end_volt
                        else -self.Y_step
                    )

            # Save and show plot
            self._log_params_end()
            self._save_and_show_plot()
            logger.info("2D sweep completed successfully")

        except Exception as e:
            logger.error(f"Error during 2D sweep: {str(e)}")
            raise

    def _write_2d_data_header(self):
        """Write header for 2D sweep data file."""
        try:
            content = (
                f"{self.y_label} [{self.Y_volt_unit}]".rjust(16)
                + f"{self.x_label} [{self.X_volt_unit}]".rjust(16)
                + f"{self.z_label} [{self.current_unit}]".rjust(16)
                + "\n"
            )
            self._write_to_file(f"data/{self.filename}.txt", content)
        except IOError as e:
            logger.error(f"Failed to write data header: {str(e)}")
            raise

    def _setup_2d_plot(self):
        """Set up the initial 2D plot."""

        # Set up figure and axes
        plt.ion()
        plt.rc("legend", fontsize=22, framealpha=0.9)
        plt.rc("xtick", labelsize=24, color="#2C3E50")
        plt.rc("ytick", labelsize=24, color="#2C3E50")
        self.fig, self.ax = plt.subplots(figsize=(12, 7))

        # Configure plot style
        self.fig.patch.set_facecolor("white")

        # Border
        for spine in self.ax.spines.values():
            spine.set_color("#2C3E50")

        # Axes labels
        self.ax.set_xlabel(
            f"{self.x_label} [{self.X_volt_unit}]", color="#2C3E50", fontsize=32
        )
        self.ax.set_ylabel(
            f"{self.y_label} [{self.Y_volt_unit}]", color="#2C3E50", fontsize=32
        )

        # Ticks
        self.ax.tick_params(
            axis="y",
            direction="in",
            width=4,
            length=10,
            pad=10,
            right=True,
            labelsize=24,
        )
        self.ax.tick_params(
            axis="x",
            direction="in",
            width=4,
            length=10,
            pad=10,
            top=False,
            labelsize=24,
        )

        # Set up colormap
        colorsbar = ["#02507d", "#ede8e5", "#b5283b"]
        cm = LinearSegmentedColormap.from_list("", colorsbar, N=500)

        # Create image plot
        self.img = self.ax.imshow(
            self.data,
            cmap=cm,
            aspect="auto",
            origin="lower",
            extent=[
                self.X_start_volt * self.X_volt_scale,
                self.X_end_volt * self.X_volt_scale,
                self.Y_start_volt * self.Y_volt_scale,
                self.Y_end_volt * self.Y_volt_scale,
            ],
            interpolation="none",
        )

        # Add colorbar
        self.cbar = self.fig.colorbar(self.img, pad=0.005, extend="both")
        self.cbar.ax.set_title(
            rf"         {self.z_label} [{self.current_unit}]", fontsize=28, pad=10
        )
        self.cbar.ax.tick_params(direction="in", width=2, length=5, labelsize=12)

    def _update_2d_plot(
        self,
    ):
        """Update the 2D plot with new data."""
        self.img.set_data(self.data)

        # Update colorbar limits
        valid_data = self.data[np.isfinite(self.data)]
        if len(valid_data) > 0:
            clim_min = np.nanmin(valid_data)
            clim_max = np.nanmax(valid_data)
            self.img.set_clim(clim_min, clim_max)

            # Update colorbar ticks
            barticks = np.linspace(clim_min, clim_max, 5)
            self.cbar.set_ticks(barticks)
            self.cbar.ax.set_yticklabels([f"{t:.2f}" for t in barticks])
            self.cbar.update_normal(self.img)
        plt.draw()
        plt.pause(0.001)

    def sweepTime(
        self,
        measured_inputs: GatesGroup,
        total_time: float,
        time_step: float,
        initial_state: list,
        current_unit: str = "uA",
        comments: str = None,
        oversampling: int = 1,
        is_plot: bool = True,
        is_show: bool = True,
    ) -> None:
        """
        Perform a time-based sweep by recording current measurements over a specified duration.

        Args:
            measured_inputs (GatesGroup): Group of input gates for measurement.
            total_time (float): Total duration of the sweep in seconds.
            time_step (float): Time interval between measurements in seconds.
            initial_state (list): List of tuples (gate, init_voltage) for initial state.
            current_unit (str): Unit for current measurements.
            comments (str): Additional comments for logging.

        Raises:
            ValueError: If input parameters are invalid.
        """
        try:
            # Validate inputs
            if total_time <= 0:
                raise ValueError("Total time must be positive")
            if time_step <= 0:
                raise ValueError("Time step must be positive")
            if time_step >= total_time:
                raise ValueError("Time step must be smaller than total time")
            self._validate_units(current_unit, "current")

            # Set up parameters
            self.x_label = "time"
            self.z_label = measured_inputs.labels
            self.current_unit = current_unit
            self.comments = comments
            self.total_time = total_time
            self.time_step = time_step
            self.is_plot = is_plot
            self.is_show = is_show

            self.nanonisInstance.ThreeDSwp_AcqChsSet([gate.source.read_index for gate in measured_inputs.gates])

            self._set_units()
            self._set_filename("time")

            # Set up initial state
            logger.info("Setting up initial state")
            self._set_initial_state(initial_state)

            # Write header and start logging
            self._log_params_start(sweep_type="time")

            # Perform time sweep
            logger.info(
                f"Starting time sweep for {total_time:.1f}s with {time_step:.3f}s steps"
            )

            self.nanonisInstance.Util_RTOversamplSet(oversampling)  # oversampling
            
            self.nanonisInstance.ThreeDSwp_SaveOptionsSet(
                Series_Name=self.filename,
                Create_Date_Time_Folder=2,
                Comment=self.comments,
                Modules_Names=""
                )
            
            self.nanonisInstance.ThreeDSwp_SwpChPropsSet(int(self.total_time // self.time_step)+1, 1, 0, 0, 0.0, 0)

            self.nanonisInstance.ThreeDSwp_SwpChTimingSet(
                InitSettlingTime=1e-3, 
                SettlingTime=1e-3, 
                IntegrationTime=time_step, 
                EndSettlingTime=1e-3, 
                MaxSlewRate=0
                )

            self.nanonisInstance.ThreeDSwp_Start(1)

            self._log_params_end()
            
            #plt.plot(currents)
            #plt.show()

            #logger.info("Time sweep completed successfully")

        except Exception as e:
            logger.error(f"Error during time sweep: {str(e)}")
            raise

    def _write_time_sweep_header(self):
        """Write header for time sweep data file."""
        try:
            content = (
                f"{self.x_label} [s]".rjust(16)
                + f"{self.z_label} [{self.current_unit}]".rjust(16)
                + "\n"
            )
            self._write_to_file(f"data/{self.filename}.txt", content)
        except IOError as e:
            logger.error(f"Failed to write time sweep header: {str(e)}")
            raise

    def _update_time_sweep_plot(self, time_points, currents, current_idx):
        """Update the plot during time sweep."""
        if current_idx > 0:
            # Update axis limits
            self.ax.set_xlim(0, time_points[current_idx] + self.time_step)
            curr_min = min(currents[: current_idx + 1])
            curr_max = max(currents[: current_idx + 1])
            if curr_min == curr_max:
                curr_min -= 0.001
                curr_max += 0.001
            self.ax.set_ylim(
                curr_min - (curr_max - curr_min) / 4,
                curr_max + (curr_max - curr_min) / 4,
            )

        # Update plot data
        self.data_lines.set_data(
            time_points[: current_idx + 1], currents[: current_idx + 1]
        )
        plt.draw()
        plt.pause(0.001)

    def _write_time_sweep_data(self, current_time, current):
        """Write measurement data during time sweep."""
        try:
            content = f"{current_time:>16.4f} {current:>16.8f}\n"
            self._write_to_file(f"data/{self.filename}.txt", content)
        except IOError as e:
            logger.error(f"Failed to write time sweep data: {str(e)}")
            raise

    def cleanup(self):
        """Clean up resources and reset gates."""
        try:
            # Close all matplotlib figures
            plt.close("all")

            # Reset all outputs to 0V if they exist
            if self.outputs:
                self.outputs.turn_off()

            # Reset attributes
            self._initialize_attributes()
            logger.info("System cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
