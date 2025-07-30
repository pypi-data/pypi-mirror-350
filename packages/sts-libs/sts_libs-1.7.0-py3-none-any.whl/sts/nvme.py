"""NVMe device management.

This module provides functionality for managing NVMe devices:
- Device discovery
- Device information
- Device operations

NVMe (Non-Volatile Memory Express) is a protocol designed for:
- High-performance SSDs
- Low latency access
- Parallel operations
- Advanced management features

Key advantages over SCSI/SATA:
- Higher queue depths
- Lower protocol overhead
- Better error handling
- More detailed device information
"""
#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from sts.base import StorageDevice
from sts.utils.cmdline import run
from sts.utils.errors import DeviceError


@dataclass
class NvmeDevice(StorageDevice):
    """NVMe device representation.

    NVMe devices are identified by:
    - Controller number (e.g. nvme0)
    - Namespace ID (e.g. n1)
    - Combined name (e.g. nvme0n1)

    Device information includes:
    - Model and serial number
    - Firmware version
    - Capacity and block size
    - Health and error logs

    Args:
        name: Device name (optional, e.g. 'nvme0n1')
        path: Device path (optional, defaults to /dev/<name>)
        size: Device size in bytes (optional, discovered from device)
        model: Device model (optional, discovered from device)
        serial: Device serial number (optional, discovered from device)
        firmware: Device firmware version (optional, discovered from device)

    Example:
        ```python
        device = NvmeDevice(name='nvme0n1')  # Discovers other values
        device = NvmeDevice(model='Samsung SSD 970 EVO')  # Discovers device by model
        ```
    """

    # Optional parameters from parent classes
    name: str | None = None
    path: Path | str | None = None
    size: int | None = None
    model: str | None = None

    # Optional parameters for this class
    serial: str | None = None  # Device serial number
    firmware: str | None = None  # Firmware version

    # Device nodes path
    NVME_PATH: ClassVar[Path] = Path('/dev/nvme')

    def __post_init__(self) -> None:
        """Initialize NVMe device.

        Discovery process:
        1. Set device path if needed
        2. Get controller information (model, serial, firmware)
        3. Get namespace information (size, block size)

        Raises:
            DeviceError: If device cannot be initialized
        """
        # Set path based on name if not provided
        if not self.path and self.name:
            self.path = f'/dev/{self.name}'

        # Initialize parent class
        super().__post_init__()

        # Discover device info if path is available
        if self.path:
            # Get controller information (nvme id-ctrl)
            result = run(f'nvme id-ctrl {self.path} -o json')
            if result.succeeded and result.stdout:
                try:
                    info = json.loads(result.stdout)
                    if not self.model:
                        self.model = info.get('mn', '').strip()
                    if not self.serial:
                        self.serial = info.get('sn', '').strip()
                    if not self.firmware:
                        self.firmware = info.get('fr', '').strip()
                except json.JSONDecodeError:
                    pass

            # Get namespace information (nvme id-ns)
            if not self.size:
                result = run(f'nvme id-ns {self.path} -o json')
                if result.succeeded and result.stdout:
                    try:
                        info = json.loads(result.stdout)
                        if 'nsze' in info:
                            # Calculate size: blocks * block size
                            self.size = int(info['nsze']) * int(info.get('lbaf', [{}])[0].get('ds', 512))
                    except (json.JSONDecodeError, IndexError, ValueError):
                        pass

    def format(self) -> bool:
        """Format device.

        Performs a low-level format:
        - Erases all data
        - Resets metadata
        - May take significant time
        - Requires admin privileges

        Returns:
            True if successful, False otherwise

        Example:
            ```python
            device.format()
            True
            ```
        """
        if not self.path:
            logging.error('Device path not available')
            return False

        result = run(f'nvme format {self.path}')
        return result.succeeded

    def sanitize(self) -> bool:
        """Sanitize device.

        Performs secure data erasure:
        - More thorough than format
        - May use crypto erase
        - Takes longer than format
        - Not all devices support this

        Returns:
            True if successful, False otherwise

        Example:
            ```python
            device.sanitize()
            True
            ```
        """
        if not self.path:
            logging.error('Device path not available')
            return False

        result = run(f'nvme sanitize {self.path}')
        return result.succeeded

    def get_smart_log(self) -> dict[str, str]:
        """Get SMART log.

        Retrieves device health information:
        - Critical warnings
        - Temperature
        - Available spare
        - Media errors
        - Read/write statistics

        Returns:
            Dictionary of SMART log entries

        Example:
            ```python
            device.get_smart_log()
            {'critical_warning': '0x0', 'temperature': '35 C', ...}
            ```
        """
        if not self.path:
            return {}

        result = run(f'nvme smart-log {self.path} -o json')
        if result.failed or not result.stdout:
            return {}

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}

    def get_error_log(self) -> dict[str, str]:
        """Get error log.

        Retrieves device error history:
        - Error count
        - Error types
        - Error locations
        - Timestamps

        Returns:
            Dictionary of error log entries

        Example:
            ```python
            device.get_error_log()
            {'error_count': '0', 'error_entries': [], ...}
            ```
        """
        if not self.path:
            return {}

        result = run(f'nvme error-log {self.path} -o json')
        if result.failed or not result.stdout:
            return {}

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {}

    @classmethod
    def get_all(cls) -> list[NvmeDevice]:
        """Get list of all NVMe devices.

        Lists all NVMe devices in the system:
        - Controllers and namespaces
        - Both active and standby
        - Including hot-plugged devices

        Returns:
            List of NvmeDevice instances

        Example:
            ```python
            NvmeDevice.get_all()
            [NvmeDevice(name='nvme0n1', ...), NvmeDevice(name='nvme1n1', ...)]
            ```
        """
        # Get device list using nvme-cli
        result = run('nvme list -o json')
        if result.failed or not result.stdout:
            return []

        # Parse JSON output
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            logging.warning('Failed to parse nvme list output')
            return []

        # Extract device paths from JSON
        device_paths = [dev_info['DevicePath'] for dev_info in data.get('Devices', []) if 'DevicePath' in dev_info]

        # Create device objects
        devices = []
        for path in device_paths:
            name = Path(path).name
            try:
                device = cls(name=name)
                devices.append(device)
            except (ValueError, TypeError, DeviceError) as e:
                logging.warning(f'Failed to create device {name}: {e}')

        return devices

    @classmethod
    def get_by_model(cls, model: str) -> list[NvmeDevice]:
        """Get devices by model.

        Finds devices matching model string:
        - Case-sensitive match
        - Returns multiple if found
        - Empty list if none found

        Args:
            model: Device model (e.g. 'Samsung SSD 970 EVO')

        Returns:
            List of NvmeDevice instances

        Example:
            ```python
            NvmeDevice.get_by_model('Samsung SSD 970 EVO')
            [NvmeDevice(name='nvme0n1', ...), NvmeDevice(name='nvme1n1', ...)]
            ```
        """
        return [device for device in cls.get_all() if device.model == model]
