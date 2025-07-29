# -*- coding: utf-8 -*-
# FlashGBX
# Author: Lesserkuma (github.com/lesserkuma)

# pylint: disable=wildcard-import, unused-wildcard-import
from .LK_Device import *

class GbxDevice(LK_Device):
	DEVICE_NAME = "GBFlash"
	DEVICE_MIN_FW = 1
	DEVICE_MAX_FW = 12
	DEVICE_LATEST_FW_TS = { 5:1747991884, 10:1747991884, 11:1747991884, 12:1747991884, 13:1747991884 }
	PCB_VERSIONS = { 5:'', 12:'v1.2', 13:'v1.3' }
	
	def __init__(self):
		pass
	
	def Initialize(self, flashcarts, port=None, max_baud=2000000):
		if self.IsConnected(): self.DEVICE.close()
		conn_msg = []
		ports = []
		if port is not None:
			ports = [ port ]
		else:
			comports = serial.tools.list_ports.comports()
			for i in range(0, len(comports)):
				if comports[i].vid == 0x1A86 and comports[i].pid == 0x7523:
					ports.append(comports[i].device)
			if len(ports) == 0: return False
		
		for i in range(0, len(ports)):
			if self.TryConnect(ports[i], max_baud):
				self.BAUDRATE = max_baud
				dev = serial.Serial(ports[i], self.BAUDRATE, timeout=0.1)
				self.DEVICE = dev
			else:
				continue
			
			if self.FW is None or self.FW == {}: continue
			
			dprint(f"Found a {self.DEVICE_NAME}")
			dprint("Firmware information:", self.FW)
			# dprint("Baud rate:", self.BAUDRATE)
			
			if self.DEVICE is None or not self.IsConnected():
				self.DEVICE = None
				if self.FW is not None:
					conn_msg.append([0, "Couldn’t communicate with the " + self.DEVICE_NAME + " device on port " + ports[i] + ". Please disconnect and reconnect the device, then try again."])
				continue
			elif self.FW is None or self.FW["pcb_ver"] not in self.PCB_VERSIONS.keys() or "cfw_id" not in self.FW or self.FW["cfw_id"] != 'L' or self.FW["fw_ver"] < self.DEVICE_MIN_FW: # Not a CFW by Lesserkuma
				dprint("Incompatible firmware:", self.FW)
				dev.close()
				self.DEVICE = None
				continue
			elif self.FW["fw_ts"] > self.DEVICE_LATEST_FW_TS[self.FW["pcb_ver"]]:
				conn_msg.append([0, "Note: The " + self.DEVICE_NAME + " device on port " + ports[i] + " is running a firmware version that is newer than what this version of FlashGBX was developed to work with, so errors may occur."])
			
			self.MAX_BUFFER_READ = 0x1000
			self.MAX_BUFFER_WRITE = 0x800
			
			self.PORT = ports[i]
			self.DEVICE.timeout = self.DEVICE_TIMEOUT

			conn_msg.append([0, "For help with your GBFlash device, please visit the GitHub page: https://github.com/simonkwng/GBFlash"])

			# Load Flash Cartridge Handlers
			self.UpdateFlashCarts(flashcarts)

			# Stop after first found device
			break

		return conn_msg

	def LoadFirmwareVersion(self):
		dprint("Querying firmware version")
		try:
			self.DEVICE.timeout = 0.075
			self.DEVICE.reset_input_buffer()
			self.DEVICE.reset_output_buffer()
			self._write(self.DEVICE_CMD["QUERY_FW_INFO"])
			size = self.DEVICE.read(1)
			self.DEVICE.timeout = self.DEVICE_TIMEOUT
			if len(size) == 0:
				dprint("No response")
				self.FW = None
				return False
			size = struct.unpack("B", size)[0]
			if size != 8: return False
			data = self._read(size)
			info = data[:8]
			keys = ["cfw_id", "fw_ver", "pcb_ver", "fw_ts"]
			values = struct.unpack(">cHBI", bytearray(info))
			self.FW = dict(zip(keys, values))
			self.FW["cfw_id"] = self.FW["cfw_id"].decode('ascii')
			self.FW["fw_dt"] = datetime.datetime.fromtimestamp(self.FW["fw_ts"]).astimezone().replace(microsecond=0).isoformat()
			self.FW["ofw_ver"] = None
			self.FW["pcb_name"] = None
			self.FW["cart_power_ctrl"] = False
			self.FW["bootloader_reset"] = False
			if self.FW["cfw_id"] == "L" and self.FW["fw_ver"] >= 12:
				size = self._read(1)
				name = self._read(size)
				if len(name) > 0:
					try:
						self.FW["pcb_name"] = name.decode("UTF-8").replace("\x00", "").strip()
					except:
						self.FW["pcb_name"] = "Unnamed Device"
					self.DEVICE_NAME = self.FW["pcb_name"]

				# Cartridge Power Control support
				self.FW["cart_power_ctrl"] = True if self._read(1) == 1 else False

				# Reset to bootloader support
				temp = self._read(1)
				self.FW["bootloader_reset"] = True if temp & 1 == 1 else False
				self.FW["unregistered"] = True if temp >> 7 == 1 else False
			
			return True
		
		except Exception as e:
			dprint("Disconnecting due to an error", e, sep="\n")
			try:
				if self.DEVICE.isOpen():
					self.DEVICE.reset_input_buffer()
					self.DEVICE.reset_output_buffer()
					self.DEVICE.close()
				self.DEVICE = None
			except:
				pass
			return False

	def ChangeBaudRate(self, _):
		dprint("Baudrate change is not supported.")

	def CheckActive(self):
		if time.time() < self.LAST_CHECK_ACTIVE + 1: return True
		dprint("Checking if device is active")
		if self.DEVICE is None: return False
		if self.FW["pcb_name"] is None:
			if self.LoadFirmwareVersion():
				self.LAST_CHECK_ACTIVE = time.time()
				return True
			else:
				return False
		try:
			self._get_fw_variable("CART_MODE")
			self.LAST_CHECK_ACTIVE = time.time()
			return True
		except Exception as e:
			dprint("Disconnecting...", e)
			try:
				if self.DEVICE.isOpen():
					self.DEVICE.reset_input_buffer()
					self.DEVICE.reset_output_buffer()
					self.DEVICE.close()
				self.DEVICE = None
			except:
				pass
			return False

	def GetFirmwareVersion(self, more=False):
		s = "{:s}{:d}".format(self.FW["cfw_id"], self.FW["fw_ver"])
		if self.FW["pcb_name"] == None:
			s += " <unverified>"
		if more:
			s += " ({:s})".format(self.FW["fw_dt"])
		return s

	def GetFullNameExtended(self, more=False):
		if more:
			return "{:s} – Firmware {:s} ({:s}) on {:s}".format(self.GetFullName(), self.GetFirmwareVersion(), self.FW["fw_dt"], self.GetPort())
		else:
			return "{:s} – Firmware {:s} ({:s})".format(self.GetFullName(), self.GetFirmwareVersion(), self.GetPort())

	def CanSetVoltageManually(self):
		return False
	
	def CanSetVoltageAutomatically(self):
		return True
	
	def CanPowerCycleCart(self):
		return self.FW["cart_power_ctrl"]
	
	def GetSupprtedModes(self):
		return ["DMG", "AGB"]
	
	def IsSupported3dMemory(self):
		return True
	
	def IsClkConnected(self):
		return True

	def SupportsFirmwareUpdates(self):
		return True
	
	def FirmwareUpdateAvailable(self):
		if self.FW["pcb_ver"] == 5 or self.FW["fw_ts"] < 1730592000: # unofficial firmware
			self.FW_UPDATE_REQ = True
			return True
		if self.FW["fw_ts"] != self.DEVICE_LATEST_FW_TS[self.FW["pcb_ver"]]:
			return True
		self.FW_UPDATE_REQ = False
		return False
	
	def GetFirmwareUpdaterClass(self):
		try:
			from . import fw_GBFlash
			return (None, fw_GBFlash.FirmwareUpdaterWindow)
		except:
			return None

	def ResetLEDs(self):
		pass
	
	def SupportsBootloaderReset(self):
		return self.FW["bootloader_reset"]

	def BootloaderReset(self):
		if not self.SupportsBootloaderReset(): return False
		dprint("Resetting to bootloader...")
		try:
			self._write(self.DEVICE_CMD["BOOTLOADER_RESET"], wait=True)
			self._write(1)
			self.Close()
			return True
		except Exception as e:
			print("Disconnecting...", e)
			return False

	def SupportsAudioAsWe(self):
		return not (self.FW["pcb_ver"] < 13 and self.CanPowerCycleCart())

	def GetMode(self):
		if self.FW["fw_ts"] == 1681900614: return self.MODE
		return super().GetMode()

	def SetAutoPowerOff(self, value):
		value &= 0xFFFFFFFF
		#if value == 0 or value > 5000: value = 1500
		return super().SetAutoPowerOff(value)

	def GetFullName(self):
		if self.FW["pcb_ver"] < 13 and self.CanPowerCycleCart():
			s = "{:s} {:s} + PLUGIN 01".format(self.GetName(), self.GetPCBVersion())
		else:
			s = "{:s} {:s}".format(self.GetName(), self.GetPCBVersion())
		if self.IsUnregistered():
			s += " (unregistered)"
		return s

	def GetRegisterInformation(self):
		text = f"Your GBFlash device reported a registration error, which means it may be an illegitimate clone.\n\nThe device’s integrated piracy detection may limit the device in performance and functionality until proper registration. The {Util.APPNAME:s} software has no control over this.\n\nPlease visit <a href=\"https://gbflash.geeksimon.com/\">https://gbflash.geeksimon.com/</a> for more information.".replace("\n", "<br>")
		return text
