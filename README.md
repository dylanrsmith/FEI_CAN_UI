Raspberry Pi Next Generation Combine Bench Code - Fargo Engineering Inc.
=========================================================================

The code largely consists of a tkinter-generated user interface, where a user can toggle various relay states and I/O values.

HwConnect
-----------
These Modules handle communication over i2c, SPI, and CAN.

PlantModels
------------
4 Possible UCM's to test.

UserInterface
--------------
Tkinter based notebook-style interface.



v10.2:
    Adding ping functionality and disabling of widgets that are offline.

    Added Backwards Compatibility: 
        Open and Actuator Tabs will only show if ConfigSheet is properly configured.

    Added Simulator Mode: 
        Turn Off to disable Relay controls and Enable Bypass Relay Boards. 
        Turn on to control relays manually. Button located under settings.
        Value is written to SimMode.txt file for storage between power cycles.


Config_sheet vs Config_sheet_old:
    the new config sheet has 3 new columns between I/O name and UI type,
    under the SPN Sheet.
    'board_no' is used to define the SPN's configured Relay Board number on the bench. [1-99]
    'channel_no' is used to define the SPN's configured relay number, within the specified board. [1-16]
    'open_to' sets the ground configuration/relay behavior tied to the ui callback

load time = 27.35 s

Remove DIG/OP tab
remove blue buttons and flashing buttons for dropdowns.
this was done by commenting the .grid() functions for the buttons in generate_ui