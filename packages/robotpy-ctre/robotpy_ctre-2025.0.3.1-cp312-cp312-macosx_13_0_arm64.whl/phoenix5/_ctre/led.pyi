from __future__ import annotations
import phoenix5._ctre
import typing
__all__ = ['Animation', 'BaseStandardAnimation', 'BaseTwoSizeAnimation', 'CANdle', 'CANdleConfiguration', 'CANdleControlFrame', 'CANdleFaults', 'CANdleStatusFrame', 'CANdleStickyFaults', 'ColorFlowAnimation', 'FireAnimation', 'LEDStripType', 'LarsonAnimation', 'RainbowAnimation', 'RgbFadeAnimation', 'SingleFadeAnimation', 'StrobeAnimation', 'TwinkleAnimation', 'TwinkleOffAnimation', 'VBatOutputMode']
class Animation:
    """
    The base class for all animations that CANdle supports.
    """
    def __init__(self, idx: typing.SupportsInt, speed: typing.SupportsFloat, numLed: typing.SupportsInt, ledOffset: typing.SupportsInt) -> None:
        """
        Constructor for an Animation class
        
        :param idx:       The animation-specific ID
        :param speed:     The rate at which the animation runs at. Higher is generally faster
        :param numLed:    The number of LEDs to run the animation on
        :param ledOffset: Where to start the animation
        """
    def getAnimationIdx(self) -> int:
        ...
    def getBaseStandardAnimation(self) -> BaseStandardAnimation:
        ...
    def getBaseTwoSizeAnimation(self) -> BaseTwoSizeAnimation:
        ...
    def getLedOffset(self) -> int:
        ...
    def getNumLed(self) -> int:
        ...
    def getSpeed(self) -> float:
        ...
    def setLedOffset(self, ledOffset: typing.SupportsInt) -> None:
        """
        Sets where the animation starts along the strip
        
        :param ledOffset: Where to start the animation along the strip
        """
    def setNumLed(self, numLed: typing.SupportsInt) -> None:
        """
        Sets the number of LEDs the animation will run on
        
        :param numLed: The number of LEDs to run the animation on
        """
    def setSpeed(self, speed: typing.SupportsFloat) -> None:
        """
        Sets the speed of the animation
        
        :param speed: The rate at which the animation runs at. Higher is generally faster
        """
class BaseStandardAnimation(Animation):
    """
    The base class for one generic type of animation.
    These animations do not allow the user to specify a color.
    """
    def __init__(self, idx: typing.SupportsInt, brightness: typing.SupportsFloat, speed: typing.SupportsFloat, numLed: typing.SupportsInt, param4: typing.SupportsFloat, param5: typing.SupportsFloat, reverseDirection: bool, ledOffset: typing.SupportsInt) -> None:
        """
        Constructor for the BaseStandardAnimation object
        
        :param idx:              The animation-specific ID
        :param brightness:       The brightness to run the animation at. This is a scalar from [0, 1]
        :param speed:            The rate at which the animation runs at. Higher is generally faster
        :param numLed:           The number of LEDs to run the animation on
        :param param4:           Animation-specific parameter
        :param param5:           Animation-specific parameter
        :param reverseDirection: True to reverse the animation direction, so instead of going "away" from the CANdle, it will go "toward" the CANdle.
        :param ledOffset:        Where to start the animation
        """
    def getBaseStandardAnimation(self) -> BaseStandardAnimation:
        ...
    def getBaseTwoSizeAnimation(self) -> BaseTwoSizeAnimation:
        ...
    def getBrightness(self) -> float:
        ...
    def getParam4(self) -> float:
        ...
    def getParam5(self) -> float:
        ...
    def getReverseDirection(self) -> bool:
        ...
    def setBrightness(self, brightness: typing.SupportsFloat) -> None:
        """
        Sets the brightness of this animation
        
        :param brightness: The brightness to run the animation at. This is a scalar from [0, 1]
        """
    def setParam4(self, param4: typing.SupportsFloat) -> None:
        ...
    def setParam5(self, param5: typing.SupportsFloat) -> None:
        ...
    def setReverseDirection(self, reverseDirection: bool) -> None:
        """
        Set the Direction of the animation
        
        :param reverseDirection: True to reverse the animation direction, so instead of fire going "away" from the CANdle, it will go "toward" the CANdle.
        """
class BaseTwoSizeAnimation(Animation):
    """
    The base class for one generic type of animation.
    These animations do allow the user to specify a color.
    """
    def __init__(self, idx: typing.SupportsInt, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt, speed: typing.SupportsFloat, numLed: typing.SupportsInt, direction: typing.SupportsInt, size: typing.SupportsInt, ledOffset: typing.SupportsInt) -> None:
        """
        Constructor for the BaseStandardAnimation object
        
        :param idx:       The animation-specific ID
        :param r:         The amount of red to set, a value between [0, 255]
        :param g:         The amount of green to set, a value between [0, 255]
        :param b:         The amount of blue to set, a value between [0, 255]
        :param w:         The amount of white to set, a value between [0, 255]
        :param speed:     The rate at which the animation runs at. Higher is generally faster
        :param numLed:    The number of LEDs to run the animation on
        :param direction: An animation-specific parameter for its direction
        :param size:      An animation-specific parameter for its size
        :param ledOffset: Where to start the animation
        """
    def getB(self) -> int:
        ...
    def getBaseStandardAnimation(self) -> BaseStandardAnimation:
        ...
    def getBaseTwoSizeAnimation(self) -> BaseTwoSizeAnimation:
        ...
    def getDirection(self) -> int:
        ...
    def getG(self) -> int:
        ...
    def getR(self) -> int:
        ...
    def getSize(self) -> int:
        ...
    def getW(self) -> int:
        ...
    def setB(self, b: typing.SupportsInt) -> None:
        """
        Sets the B value of the LEDs
        
        :param b: The amount of blue to set, a value between [0, 255]
        """
    def setDirection(self, direction: typing.SupportsInt) -> None:
        ...
    def setG(self, g: typing.SupportsInt) -> None:
        """
        Sets the G value of the LEDs
        
        :param g: The amount of green to set, a value between [0, 255]
        """
    def setR(self, r: typing.SupportsInt) -> None:
        """
        Sets the R value of the LEDs
        
        :param r: The amount of red to set, a value between [0, 255]
        """
    def setSize(self, size: typing.SupportsInt) -> None:
        ...
    def setW(self, w: typing.SupportsInt) -> None:
        """
        Sets the W value of the LEDs
        
        :param w: The amount of white to set, a value between [0, 255]
        """
class CANdle:
    """
    CTRE CANdle
    
    Device for controlling LEDs from the CAN bus.
    
    ::
    
      {@code
      // Example usage of a CANdle
      CANdle candle{0}; // creates a new CANdle with ID 0
      
      CANdleConfiguration config;
      config.stripType = LEDStripType::RGB; // set the strip type to RGB
      config.brightnessScalar = 0.5; // dim the LEDs to half brightness
      candle.ConfigAllSettings(config);
      
      candle.SetLEDs(255, 255, 255); // set the CANdle LEDs to white
      
      // create a rainbow animation:
      // - max brightness
      // - half speed
      // - 64 LEDs
      RainbowAnimation rainbowAnim{1, 0.5, 64};
      candle.Animate(rainbowAnim);
      
      ErrorCode error = candle.GetLastError(); // gets the last error generated by the CANdle
      CANdleFaults faults;
      ErrorCode faultsError = candle.GetFaults(faults); // fills faults with the current CANdle faults; returns the last error generated
      }
    """
    def __init__(self, deviceId: typing.SupportsInt, canbus: str = '') -> None:
        """
        Constructor for a CANdle Device
        
        :param deviceId: The Device ID of the CANdle
        :param canbus:   Name of the CANbus; can be a SocketCAN interface (on Linux),
                         or a CANivore device name or serial number
        """
    def animate(self, animation: Animation, animSlot: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Animates the CANdle with the passed-in animation
        If the animation changes after calling this function,
        it must be passed into animate again for the changes to take effect
        
        :param animation: The animation that CANdle will run. If this is null, it will clear the animation at the specified slot
        :param animSlot:  The animation slot to use for the animation, range is [0, getMaxSimultaneousAnimationCount()) exclusive
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def clearStickyFaults(self, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Clears the sticky faults.
        
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configAllSettings(self, allConfigs: CANdleConfiguration, timeoutMs: typing.SupportsInt = 50) -> phoenix5._ctre.ErrorCode:
        """
        Configures all persistent settings.
        
        :param allConfigs: Object with all of the persistant settings
        :param timeoutMs:  Timeout value in ms. If nonzero, function will wait for
                           config success and report an error if it times out.
                           If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configBrightnessScalar(self, brightness: typing.SupportsFloat, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures the brightness scalar to be applied to every LED output.
        This value is bounded to [0, 1].
        
        Setting this to 1 will allow the LEDs to function at max brightness.
        Setting this to 0.5 will scale all values to half their applied value.
        Setting this to 0 will turn off the LEDs.
        
        Forcing the LEDs off this way may be useful in certain testing circumstances
        but is generally not necessary. Self-test (Tuner) may be used to verify what
        the effective scalar is in case user forgot to restore the scalar to a
        non-zero value.
        
        :param brightness: Value from [0, 1] that will scale the LED output.
        :param timeoutMs:  Timeout value in ms. If nonzero, function will wait for
                           config success and report an error if it times out.
                           If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configFactoryDefault(self, timeoutMs: typing.SupportsInt = 50) -> phoenix5._ctre.ErrorCode:
        """
        Configures all persistent settings to defaults.
        
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configGetCustomParam(self, paramIndex: typing.SupportsInt, timeoutMs: typing.SupportsInt = 0) -> int:
        """
        Gets the value of a custom parameter. This is for arbitrary use.
        
        Sometimes it is necessary to save calibration/duty cycle/output
        information in the device. Particularly if the
        device is part of a subsystem that can be replaced.
        
        :param paramIndex: Index of custom parameter. [0-1]
        :param timeoutMs:  Timeout value in ms. If nonzero, function will wait for
                           config success and report an error if it times out.
                           If zero, no blocking or checking is performed.
        
        :returns: Value of the custom param.
        """
    def configGetParameter(self, param: phoenix5._ctre.ParamEnum, ordinal: typing.SupportsInt, timeoutMs: typing.SupportsInt = 0) -> float:
        """
        Gets a parameter. Generally this is not used.
        This can be utilized in
        - Using new features without updating API installation.
        - Errata workarounds to circumvent API implementation.
        - Allows for rapid testing / unit testing of firmware.
        
        :param param:     Parameter enumeration.
        :param ordinal:   Ordinal of parameter.
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Value of parameter.
        """
    def configLEDType(self, type: LEDStripType, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures the type of LED the CANdle controls
        
        :param type:      The type of the LEDs the CANdle controls
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def configLOSBehavior(self, disableWhenLOS: bool, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures what the CANdle should do if it loses communications to the Controller
        
        :param disableWhenLOS: Set to true to disable the LEDs on Loss of Signal.
        :param timeoutMs:      Timeout value in ms. If nonzero, function will wait for
                               config success and report an error if it times out.
                               If zero, no blocking or checking is performed.
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def configSetCustomParam(self, paramIndex: typing.SupportsInt, value: typing.SupportsInt, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Sets the value of a custom parameter. This is for arbitrary use.
        
        Sometimes it is necessary to save calibration/duty cycle/output
        information in the device. Particularly if the
        device is part of a subsystem that can be replaced.
        
        :param newValue:   Value for custom parameter.
        :param paramIndex: Index of custom parameter. [0-1]
        :param timeoutMs:  Timeout value in ms. If nonzero, function will wait for
                           config success and report an error if it times out.
                           If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configSetParameter(self, param: phoenix5._ctre.ParamEnum, value: typing.SupportsFloat, subValue: typing.SupportsInt = 0, ordinal: typing.SupportsInt = 0, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Sets a parameter. Generally this is not used.
        This can be utilized in
        - Using new features without updating API installation.
        - Errata workarounds to circumvent API implementation.
        - Allows for rapid testing / unit testing of firmware.
        
        :param param:     Parameter enumeration.
        :param value:     Value of parameter.
        :param subValue:  Subvalue for parameter. Maximum value of 255.
        :param ordinal:   Ordinal of parameter.
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configStatusLedState(self, disableWhenRunning: bool, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures how the status led will behave when the CANdle is actively controlling LEDs
        If the CANdle is LOS or not actively commanded a value, it will always turn on its status LED.
        
        :param disableWhenRunning: Disables the status LED when the CANdle is running
        :param timeoutMs:          Timeout value in ms. If nonzero, function will wait for
                                   config success and report an error if it times out.
                                   If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def configV5Enabled(self, v5Enabled: bool, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures the enable state for the 5V rail. This also affects the on-board LEDs.
        
        :param v5Enabled: True to enable the 5V rail.
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def configVBatOutput(self, mode: VBatOutputMode, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Configures how the VBat Output will behave
        
        :param mode:      VBat Output Behavior
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def get5VRailVoltage(self) -> float:
        """
        Gets the Voltage of the 5V line as measured by CANdle
        
        :returns: Voltage of the 5V line
        """
    def getAllConfigs(self, allConfigs: CANdleConfiguration, timeoutMs: typing.SupportsInt = 50) -> None:
        """
        Gets all persistant settings.
        
        :param allConfigs: Object with all of the persistant settings
        :param timeoutMs:  Timeout value in ms. If nonzero, function will wait for
                           config success and report an error if it times out.
                           If zero, no blocking or checking is performed.
        """
    def getBusVoltage(self) -> float:
        """
        Gets the Voltage of VBat as measured by CANdle
        
        :returns: Voltage of VBat
        """
    def getCurrent(self) -> float:
        """
        Gets the low-side current as measured by CANdle
        
        :returns: Current in Amps
        """
    def getFaults(self, toFill: CANdleFaults) -> phoenix5._ctre.ErrorCode:
        """
        Gets the CANdle fault status
        
        :param toFill: Container for fault statuses.
        
        :returns: Error Code generated by function. OK indicates no error.
        """
    def getLastError(self) -> phoenix5._ctre.ErrorCode:
        """
        Call GetLastError() generated by this object.
        Not all functions return an error code but can
        potentially report errors.
        
        This function can be used to retrieve those error codes.
        
        :returns: The last ErrorCode generated.
        """
    def getMaxSimultaneousAnimationCount(self) -> int:
        """
        Gets the maximum number of simultaneous animations this version of CANdle firmware supports.
        If you specify an animation slot >= to this return, Phoenix will error out.
        You can also get the maximum count from a self-test snapshot.
        
        :returns: Maximum number of simultaneous animations this version of firmware supports.
        """
    def getStatusFramePeriod(self, frame: CANdleStatusFrame, timeoutMs: typing.SupportsInt = 0) -> int:
        """
        Gets the period of the given status frame.
        
        :param frame:     Frame to get the period of.
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Period of the given status frame.
        """
    def getStickyFaults(self, toFill: CANdleStickyFaults) -> phoenix5._ctre.ErrorCode:
        """
        Gets the CANdle sticky fault status
        
        :param toFill: Container for sticky fault statuses.
        
        :returns: Error Code generated by function. OK indicates no error.
        """
    def getTemperature(self) -> float:
        """
        Gets the temperature of the CANdle in Celcius
        
        :returns: Temperature in Celcius
        """
    def getVBatModulation(self) -> float:
        """
        Gets the applied vbat modulation in percent.
        If the CANdle is configured to always enable VBat, this returns 1
        If the CANdle is confgigured to always disable VBat, this returns 0
        Otherwise it returns the last set Modulation as a value [0, 1]
        
        :returns: VBat Output Modulation
        """
    def hasResetOccurred(self) -> bool:
        """
        Returns true if the device has reset since last call.
        
        :returns: Has a Device Reset Occurred?
        """
    def modulateVBatOutput(self, dutyCyclePrcnt: typing.SupportsFloat) -> phoenix5._ctre.ErrorCode:
        """
        Modulates the VBat output to the specified duty cycle percentage
        This function will only do something if the CANdle's VBatOutput is configured to Modulated
        
        :param dutyCyclePrcnt: The duty cycle of the output modulation [0, 1]
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def setControlFramePeriod(self, frame: CANdleControlFrame, periodMs: typing.SupportsInt) -> phoenix5._ctre.ErrorCode:
        """
        Sets the period of the given control frame.
        
        :param frame:    Frame whose period is to be changed.
        :param periodMs: Period in ms for the given frame.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
    def setLEDs(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, startIdx: typing.SupportsInt = 0, count: typing.SupportsInt = 512) -> phoenix5._ctre.ErrorCode:
        """
        Sets a block of LEDs to the specified color
        
        :param r:        The amount of Red to set, range is [0, 255]
        :param g:        The amount of Green to set, range is [0, 255]
        :param b:        The amount of Blue to set, range is [0, 255]
        :param w:        The amount of White to set, range is [0, 255]. This only applies for LED strips with white in them.
        :param startIdx: Where to start setting the LEDs
        :param count:    The number of LEDs to apply this to
        
        :returns: ErrorCode generated by function. OK indicates no error.
        """
    def setStatusFramePeriod(self, frame: CANdleStatusFrame, periodMs: typing.SupportsInt, timeoutMs: typing.SupportsInt = 0) -> phoenix5._ctre.ErrorCode:
        """
        Sets the period of the given status frame.
        
        :param frame:     Frame whose period is to be changed.
        :param periodMs:  Period in ms for the given frame.
        :param timeoutMs: Timeout value in ms. If nonzero, function will wait for
                          config success and report an error if it times out.
                          If zero, no blocking or checking is performed.
        
        :returns: Error Code generated by function. 0 indicates no error.
        """
class CANdleConfiguration(phoenix5._ctre.CustomParamConfiguration):
    """
    Configurables available to CANdle
    """
    def __init__(self) -> None:
        ...
    def __str__(self, prependString: str = '') -> str:
        """
        :param prependString: String to prepend to configs
        
        :returns: String representation of configs
        """
    @property
    def brightnessScalar(self) -> float:
        """
        Brightness scalar for all LEDs controlled
        """
    @brightnessScalar.setter
    def brightnessScalar(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def disableWhenLOS(self) -> bool:
        """
        True to turn off LEDs when Loss of Signal occurrs
        """
    @disableWhenLOS.setter
    def disableWhenLOS(self, arg0: bool) -> None:
        ...
    @property
    def statusLedOffWhenActive(self) -> bool:
        """
        True to turn off Status LED when CANdle is actively being controlled
        """
    @statusLedOffWhenActive.setter
    def statusLedOffWhenActive(self, arg0: bool) -> None:
        ...
    @property
    def stripType(self) -> LEDStripType:
        """
        What type of LEDs the CANdle controls
        """
    @stripType.setter
    def stripType(self, arg0: LEDStripType) -> None:
        ...
    @property
    def v5Enabled(self) -> bool:
        """
        True to turn off the 5V rail. This turns off the on-board LEDs as well.
        """
    @v5Enabled.setter
    def v5Enabled(self, arg0: bool) -> None:
        ...
    @property
    def vBatOutputMode(self) -> VBatOutputMode:
        """
        The behavior of VBat output
        """
    @vBatOutputMode.setter
    def vBatOutputMode(self, arg0: VBatOutputMode) -> None:
        ...
class CANdleControlFrame:
    """
    Enumerated type for status frame types.
    
    Members:
    
      CANdle_Control_1_General
    
      CANdle_Control_2_ModulatedVBatOutput
    """
    CANdle_Control_1_General: typing.ClassVar[CANdleControlFrame]  # value = <CANdleControlFrame.CANdle_Control_1_General: 262144>
    CANdle_Control_2_ModulatedVBatOutput: typing.ClassVar[CANdleControlFrame]  # value = <CANdleControlFrame.CANdle_Control_2_ModulatedVBatOutput: 262208>
    __members__: typing.ClassVar[dict[str, CANdleControlFrame]]  # value = {'CANdle_Control_1_General': <CANdleControlFrame.CANdle_Control_1_General: 262144>, 'CANdle_Control_2_ModulatedVBatOutput': <CANdleControlFrame.CANdle_Control_2_ModulatedVBatOutput: 262208>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CANdleFaults:
    """
    Faults available to CANdle (Currently has none)
    """
    @typing.overload
    def __init__(self, bits: typing.SupportsInt) -> None:
        """
        Updates current fault list with specified bit field of faults
        
        :param bits: bit field of faults to update with
        """
    @typing.overload
    def __init__(self) -> None:
        ...
    def hasAnyFault(self) -> bool:
        """
        :returns: true if any faults are tripped
        """
    def toBitfield(self) -> int:
        """
        :returns: Current fault list as a bit field
        """
    def update(self, bits: typing.SupportsInt) -> None:
        ...
    @property
    def APIError(self) -> bool:
        """
        API error detected.  Make sure API and firmware versions are compatible.
        """
    @APIError.setter
    def APIError(self, arg0: bool) -> None:
        ...
    @property
    def BootDuringEnable(self) -> bool:
        """
        Boot while receiving an enable frame
        """
    @BootDuringEnable.setter
    def BootDuringEnable(self, arg0: bool) -> None:
        ...
    @property
    def HardwareFault(self) -> bool:
        """
        Device detects hardware failure
        """
    @HardwareFault.setter
    def HardwareFault(self, arg0: bool) -> None:
        ...
    @property
    def ShortCircuit(self) -> bool:
        """
        Output pin is shorted to something
        """
    @ShortCircuit.setter
    def ShortCircuit(self, arg0: bool) -> None:
        ...
    @property
    def SoftwareFuse(self) -> bool:
        """
        Exceeded output current of 6 amps
        """
    @SoftwareFuse.setter
    def SoftwareFuse(self, arg0: bool) -> None:
        ...
    @property
    def ThermalFault(self) -> bool:
        """
        Device is over temperature
        """
    @ThermalFault.setter
    def ThermalFault(self, arg0: bool) -> None:
        ...
    @property
    def V5TooHigh(self) -> bool:
        """
        5V Line is over 6V
        """
    @V5TooHigh.setter
    def V5TooHigh(self, arg0: bool) -> None:
        ...
    @property
    def V5TooLow(self) -> bool:
        """
        5V Line is under 4 V
        """
    @V5TooLow.setter
    def V5TooLow(self, arg0: bool) -> None:
        ...
    @property
    def VBatTooHigh(self) -> bool:
        """
        VBat is over 30V
        """
    @VBatTooHigh.setter
    def VBatTooHigh(self, arg0: bool) -> None:
        ...
    @property
    def VBatTooLow(self) -> bool:
        """
        VBat is under 5V
        """
    @VBatTooLow.setter
    def VBatTooLow(self, arg0: bool) -> None:
        ...
class CANdleStatusFrame:
    """
    Enumerated type for status frame types.
    
    Members:
    
      Status_1_General
    
      Status_2_Startup
    
      Status_3_FirmwareApiStatus
    
      Status_4_ControlTelem
    
      Status_5_PixelPulseTrain
    
      Status_6_BottomPixels
    
      Status_7_TopPixels
    """
    Status_1_General: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_1_General: 267264>
    Status_2_Startup: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_2_Startup: 267328>
    Status_3_FirmwareApiStatus: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_3_FirmwareApiStatus: 267392>
    Status_4_ControlTelem: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_4_ControlTelem: 267456>
    Status_5_PixelPulseTrain: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_5_PixelPulseTrain: 267520>
    Status_6_BottomPixels: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_6_BottomPixels: 267584>
    Status_7_TopPixels: typing.ClassVar[CANdleStatusFrame]  # value = <CANdleStatusFrame.Status_7_TopPixels: 267648>
    __members__: typing.ClassVar[dict[str, CANdleStatusFrame]]  # value = {'Status_1_General': <CANdleStatusFrame.Status_1_General: 267264>, 'Status_2_Startup': <CANdleStatusFrame.Status_2_Startup: 267328>, 'Status_3_FirmwareApiStatus': <CANdleStatusFrame.Status_3_FirmwareApiStatus: 267392>, 'Status_4_ControlTelem': <CANdleStatusFrame.Status_4_ControlTelem: 267456>, 'Status_5_PixelPulseTrain': <CANdleStatusFrame.Status_5_PixelPulseTrain: 267520>, 'Status_6_BottomPixels': <CANdleStatusFrame.Status_6_BottomPixels: 267584>, 'Status_7_TopPixels': <CANdleStatusFrame.Status_7_TopPixels: 267648>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CANdleStickyFaults:
    """
    Faults available to CANdle (Currently has none)
    """
    @typing.overload
    def __init__(self, bits: typing.SupportsInt) -> None:
        """
        Updates current fault list with specified bit field of faults
        
        :param bits: bit field of faults to update with
        """
    @typing.overload
    def __init__(self) -> None:
        ...
    def hasAnyFault(self) -> bool:
        """
        :returns: true if any faults are tripped
        """
    def toBitfield(self) -> int:
        """
        :returns: Current fault list as a bit field
        """
    def update(self, bits: typing.SupportsInt) -> None:
        ...
    @property
    def APIError(self) -> bool:
        """
        API error detected.  Make sure API and firmware versions are compatible.
        """
    @APIError.setter
    def APIError(self, arg0: bool) -> None:
        ...
    @property
    def BootDuringEnable(self) -> bool:
        """
        Boot while receiving an enable frame
        """
    @BootDuringEnable.setter
    def BootDuringEnable(self, arg0: bool) -> None:
        ...
    @property
    def HardwareFault(self) -> bool:
        """
        Device detects hardware failure
        """
    @HardwareFault.setter
    def HardwareFault(self, arg0: bool) -> None:
        ...
    @property
    def ShortCircuit(self) -> bool:
        """
        Output pin is shorted to something
        """
    @ShortCircuit.setter
    def ShortCircuit(self, arg0: bool) -> None:
        ...
    @property
    def SoftwareFuse(self) -> bool:
        """
        Exceeded output current of 6 amps
        """
    @SoftwareFuse.setter
    def SoftwareFuse(self, arg0: bool) -> None:
        ...
    @property
    def ThermalFault(self) -> bool:
        """
        Device is over temperature
        """
    @ThermalFault.setter
    def ThermalFault(self, arg0: bool) -> None:
        ...
    @property
    def V5TooHigh(self) -> bool:
        """
        5V Line is over 6V
        """
    @V5TooHigh.setter
    def V5TooHigh(self, arg0: bool) -> None:
        ...
    @property
    def V5TooLow(self) -> bool:
        """
        5V Line is under 4 V
        """
    @V5TooLow.setter
    def V5TooLow(self, arg0: bool) -> None:
        ...
    @property
    def VBatTooHigh(self) -> bool:
        """
        VBat is over 30V
        """
    @VBatTooHigh.setter
    def VBatTooHigh(self, arg0: bool) -> None:
        ...
    @property
    def VBatTooLow(self) -> bool:
        """
        VBat is under 5V
        """
    @VBatTooLow.setter
    def VBatTooLow(self, arg0: bool) -> None:
        ...
class ColorFlowAnimation(BaseTwoSizeAnimation):
    """
    Animation that gradually lights the entire LED strip one LED at a time.
    """
    class Direction:
        """
        What direction does the color go
        
        Members:
        
          Forward : Color goes forward, away from CANdle
        
          Backward : Color goes backward, toward CANdle
        """
        Backward: typing.ClassVar[ColorFlowAnimation.Direction]  # value = <Direction.Backward: 1>
        Forward: typing.ClassVar[ColorFlowAnimation.Direction]  # value = <Direction.Forward: 0>
        __members__: typing.ClassVar[dict[str, ColorFlowAnimation.Direction]]  # value = {'Forward': <Direction.Forward: 0>, 'Backward': <Direction.Backward: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, direction: ColorFlowAnimation.Direction = ..., ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a ColorFlowAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    How many LEDs is the CANdle controlling
        :param direction: What direction should the color move in
        :param ledOffset: Where to start the animation
        """
    def setDirection(self, direction: ColorFlowAnimation.Direction) -> None:
        """
        Sets the direction the color flow moves in
        
        :param direction: What direction should the color move in
        """
class FireAnimation(BaseStandardAnimation):
    """
    Animation that looks similarly to a flame flickering
    """
    def __init__(self, brightness: typing.SupportsFloat = 1, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, sparking: typing.SupportsFloat = 1, cooling: typing.SupportsFloat = 1, reverseDirection: bool = False, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a FireAnimation
        
        :param brightness:       How bright should the animation be [0, 1]
        :param speed:            How fast will the flame be processed at [0, 1]
        :param numLed:           How many LEDs is the CANdle controlling
        :param sparking:         The rate at which the Fire "Sparks" [0, 1]
        :param cooling:          The rate at which the Fire "Cools" along the travel [0, 1]
        :param reverseDirection: True to reverse the animation direction, so instead of fire going "away" from the CANdle, it will go "toward" the CANdle.
        :param ledOffset:        Where to start the animation
        """
    def setCooling(self, cooling: typing.SupportsFloat) -> None:
        """
        Sets the cooling value of the FireAnimation
        
        :param cooling: The rate at which the Fire "Cools" [0, 1]
        """
    def setSparking(self, sparking: typing.SupportsFloat) -> None:
        """
        Sets the sparking value of the FireAnimation
        
        :param sparking: The rate at which the Fire "Sparks" [0, 1]
        """
class LEDStripType:
    """
    The various LED types that the CANdle can support
    
    Members:
    
      GRB : LEDs that are controlled by Green-Red-Blue values
    
      RGB : LEDs that are controlled by Red-Green-Blue values
    
      BRG : LEDs that are controlled by Blue-Red-Green values
    
      GRBW : LEDs that are controlled by Green-Red-Blue-White values
    
      RGBW : LEDs that are controlled by Red-Green-Blue-White values
    
      BRGW : LEDs that are controlled by Blue-Red-Green-White values
    """
    BRG: typing.ClassVar[LEDStripType]  # value = <LEDStripType.BRG: 2>
    BRGW: typing.ClassVar[LEDStripType]  # value = <LEDStripType.BRGW: 8>
    GRB: typing.ClassVar[LEDStripType]  # value = <LEDStripType.GRB: 0>
    GRBW: typing.ClassVar[LEDStripType]  # value = <LEDStripType.GRBW: 6>
    RGB: typing.ClassVar[LEDStripType]  # value = <LEDStripType.RGB: 1>
    RGBW: typing.ClassVar[LEDStripType]  # value = <LEDStripType.RGBW: 7>
    __members__: typing.ClassVar[dict[str, LEDStripType]]  # value = {'GRB': <LEDStripType.GRB: 0>, 'RGB': <LEDStripType.RGB: 1>, 'BRG': <LEDStripType.BRG: 2>, 'GRBW': <LEDStripType.GRBW: 6>, 'RGBW': <LEDStripType.RGBW: 7>, 'BRGW': <LEDStripType.BRGW: 8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LarsonAnimation(BaseTwoSizeAnimation):
    """
    Animation that sends a pocket of light across the LED strip.
    """
    class BounceMode:
        """
        How the pocket of light behaves when it reaches the end of the strip
        
        Members:
        
          Front : Bounce the pocket as soon as the first LED reaches the end of the strip
        
          Center : Bounce the pocket once it is midway through the end of the strip
        
          Back : Bounce the pocket once all the LEDs are off the strip
        """
        Back: typing.ClassVar[LarsonAnimation.BounceMode]  # value = <BounceMode.Back: 2>
        Center: typing.ClassVar[LarsonAnimation.BounceMode]  # value = <BounceMode.Center: 1>
        Front: typing.ClassVar[LarsonAnimation.BounceMode]  # value = <BounceMode.Front: 0>
        __members__: typing.ClassVar[dict[str, LarsonAnimation.BounceMode]]  # value = {'Front': <BounceMode.Front: 0>, 'Center': <BounceMode.Center: 1>, 'Back': <BounceMode.Back: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, mode: LarsonAnimation.BounceMode = ..., size: typing.SupportsInt = 2, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a LarsonAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    The number of LEDs the CANdle will control
        :param mode:      How the pocket of LEDs will behave once it reaches the end of the strip
        :param size:      How large the pocket of LEDs are [0, 7]
        :param ledOffset: Where to start the animation
        """
    def setBounceMode(self, mode: LarsonAnimation.BounceMode) -> None:
        """
        Sets the bounce mode of the animation.
        
        :param mode: How the pocket of LEDs will behave once it reaches the end of the strip
        """
    def setSize(self, size: typing.SupportsInt) -> None:
        """
        Sets the size of the pocket of LEDs
        
        :param size: The size of the pocket [0, 7]
        """
class RainbowAnimation(BaseStandardAnimation):
    """
    Animation that creates a rainbow throughout all the LEDs
    """
    def __init__(self, brightness: typing.SupportsFloat = 1, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, reverseDirection: bool = False, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a RainbowAnimation
        
        :param brightness:       The brightness of the LEDs [0, 1]
        :param speed:            How fast the rainbow travels through the leds [0, 1]
        :param numLed:           How many LEDs are controlled by the CANdle
        :param reverseDirection: True to reverse the animation direction, so instead of going "toward" the CANdle, it will go "away" from the CANdle.
        :param ledOffset:        Where to start the animation
        """
class RgbFadeAnimation(BaseStandardAnimation):
    """
    Animation that fades all the LEDs of a strip simultaneously between Red, Green, and Blue
    """
    def __init__(self, brightness: typing.SupportsFloat = 1, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for an RgbFadeAnimation
        
        :param brightness: How bright the LEDs are [0, 1]
        :param speed:      How fast the LEDs fade between Red, Green, and Blue [0, 1]
        :param numLed:     How many LEDs are controlled by the CANdle
        :param ledOffset:  Where to start the animation
        """
class SingleFadeAnimation(BaseTwoSizeAnimation):
    """
    Animation that fades into and out of a specified color
    """
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a SingleFadeAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    How many LEDs the CANdle controls
        :param ledOffset: Where to start the animation
        """
class StrobeAnimation(BaseTwoSizeAnimation):
    """
    Animation that strobes the LEDs a specified color
    """
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a StrobeAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    How many LEDs the CANdle controls
        :param ledOffset: Where to start the animation
        """
class TwinkleAnimation(BaseTwoSizeAnimation):
    """
    Animation that randomly turns LEDs on and off to a certain color
    """
    class TwinklePercent:
        """
        The percentage of LEDs that are allowed to be on at any one point
        
        Members:
        
          Percent100 : All the LEDs are allowed to turn on
        
          Percent88 : 88% of LEDs are allowed to turn on
        
          Percent76 : 76% of LEDs are allowed to turn on
        
          Percent64 : 64% of LEDs are allowed to turn on
        
          Percent42 : 42% of LEDs are allowed to turn on
        
          Percent30 : 30% of LEDs are allowed to turn on
        
          Percent18 : 18% of LEDs are allowed to turn on
        
          Percent6 : 6% of LEDs are allowed to turn on
        """
        Percent100: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent100: 0>
        Percent18: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent18: 6>
        Percent30: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent30: 5>
        Percent42: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent42: 4>
        Percent6: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent6: 7>
        Percent64: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent64: 3>
        Percent76: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent76: 2>
        Percent88: typing.ClassVar[TwinkleAnimation.TwinklePercent]  # value = <TwinklePercent.Percent88: 1>
        __members__: typing.ClassVar[dict[str, TwinkleAnimation.TwinklePercent]]  # value = {'Percent100': <TwinklePercent.Percent100: 0>, 'Percent88': <TwinklePercent.Percent88: 1>, 'Percent76': <TwinklePercent.Percent76: 2>, 'Percent64': <TwinklePercent.Percent64: 3>, 'Percent42': <TwinklePercent.Percent42: 4>, 'Percent30': <TwinklePercent.Percent30: 5>, 'Percent18': <TwinklePercent.Percent18: 6>, 'Percent6': <TwinklePercent.Percent6: 7>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, divider: TwinkleAnimation.TwinklePercent = ..., ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a TwinkleAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    How many LEDs the CANdle controls
        :param divider:   What percentage of LEDs can be on at any point
        :param ledOffset: Where to start the animation
        """
    def setDivider(self, divider: TwinkleAnimation.TwinklePercent) -> None:
        """
        Sets the percentage of LEDs that are allowed on
        
        :param divider: The percentage of LEDs that are allowed on at any point
        """
class TwinkleOffAnimation(BaseTwoSizeAnimation):
    """
    Animation that randomly turns on LEDs, until it reaches the maximum count and turns them all off
    """
    class TwinkleOffPercent:
        """
        The maximum percentage of LEDs that are allowed to turn on
        
        Members:
        
          Percent100 : All the LEDs are allowed to turn on
        
          Percent88 : 88% of LEDs are allowed to turn on
        
          Percent76 : 76% of LEDs are allowed to turn on
        
          Percent64 : 64% of LEDs are allowed to turn on
        
          Percent42 : 42% of LEDs are allowed to turn on
        
          Percent30 : 30% of LEDs are allowed to turn on
        
          Percent18 : 18% of LEDs are allowed to turn on
        
          Percent6 : 6% of LEDs are allowed to turn on
        """
        Percent100: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent100: 0>
        Percent18: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent18: 6>
        Percent30: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent30: 5>
        Percent42: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent42: 4>
        Percent6: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent6: 7>
        Percent64: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent64: 3>
        Percent76: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent76: 2>
        Percent88: typing.ClassVar[TwinkleOffAnimation.TwinkleOffPercent]  # value = <TwinkleOffPercent.Percent88: 1>
        __members__: typing.ClassVar[dict[str, TwinkleOffAnimation.TwinkleOffPercent]]  # value = {'Percent100': <TwinkleOffPercent.Percent100: 0>, 'Percent88': <TwinkleOffPercent.Percent88: 1>, 'Percent76': <TwinkleOffPercent.Percent76: 2>, 'Percent64': <TwinkleOffPercent.Percent64: 3>, 'Percent42': <TwinkleOffPercent.Percent42: 4>, 'Percent30': <TwinkleOffPercent.Percent30: 5>, 'Percent18': <TwinkleOffPercent.Percent18: 6>, 'Percent6': <TwinkleOffPercent.Percent6: 7>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def __init__(self, r: typing.SupportsInt, g: typing.SupportsInt, b: typing.SupportsInt, w: typing.SupportsInt = 0, speed: typing.SupportsFloat = 1, numLed: typing.SupportsInt = -1, divider: TwinkleOffAnimation.TwinkleOffPercent = ..., ledOffset: typing.SupportsInt = 0) -> None:
        """
        Constructor for a TwinkleAnimation
        
        :param r:         How much red should the color have [0, 255]
        :param g:         How much green should the color have [0, 255]
        :param b:         How much blue should the color have [0, 255]
        :param w:         How much white should the color have [0, 255]
        :param speed:     How fast should the color travel the strip [0, 1]
        :param numLed:    How many LEDs the CANdle controls
        :param divider:   What percentage of LEDs can be on at any point
        :param ledOffset: Where to start the animation
        """
    def setDivider(self, divider: TwinkleOffAnimation.TwinkleOffPercent) -> None:
        """
        Sets the percentage of LEDs that are allowed on
        
        :param divider: The percentage of LEDs that are allowed on at any point
        """
class VBatOutputMode:
    """
    The various methods of managing the VBat output behavior
    
    Members:
    
      On : VBat output is on at full power, no modulation
    
      Off : VBat output is off, no modulation
    
      Modulated : VBat output is on at the specified modulation
    """
    Modulated: typing.ClassVar[VBatOutputMode]  # value = <VBatOutputMode.Modulated: 2>
    Off: typing.ClassVar[VBatOutputMode]  # value = <VBatOutputMode.Off: 1>
    On: typing.ClassVar[VBatOutputMode]  # value = <VBatOutputMode.On: 0>
    __members__: typing.ClassVar[dict[str, VBatOutputMode]]  # value = {'On': <VBatOutputMode.On: 0>, 'Off': <VBatOutputMode.Off: 1>, 'Modulated': <VBatOutputMode.Modulated: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
