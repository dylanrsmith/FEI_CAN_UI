import itertools
from tkinter import ttk
import tkinter as tk
from tkinter import *
import subprocess
import can


class global_defines:
    # testing with all hardware : 0, else 1
    testing_active = 1
    debug_mode = 0
    debug_mode_button = 0

    # Create the master object
    master = tk.Tk()
    master.geometry("1450x1190")
    master.title("Raspberry Pi simulator - FEI")
    mygreen = "#CEF743"
    red = "#B1CCE7"
    black = "#000000"

    style = ttk.Style()
    style.theme_create(
        "raspi",
        parent="alt",
        settings={
            "TNotebook": {"configure": {"tabmargins": [3, 5, 3, 0]}},
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 1],
                    "background": "lightblue",
                    "foreground": black,
                },
                "map": {
                    "background": [("selected", "SteelBlue1")],
                    "expand": [("selected", [1, 1, 1, 0])],
                },
            },
        },
    )
    style.theme_use("raspi")

    tc = ttk.Notebook(master)

    # DIG I/P
    tc_dig_ip = ttk.Frame(tc)
    tc_dig_ip.pack(side="left")
    dig_ip_canvas = Canvas(
        tc_dig_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    hbar = Scrollbar(tc_dig_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=dig_ip_canvas.xview)
    vbar = Scrollbar(tc_dig_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=dig_ip_canvas.yview)
    dig_ip_canvas.config(width=6, height=6)
    dig_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    dig_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    dig_ip_frame = Frame(dig_ip_canvas)
    dig_ip_canvas.create_window((0, 0), window=dig_ip_frame, anchor="nw")

    # DIG O/P
    # tc_dig_op = ttk.Frame(tc)
    # tc_dig_op.pack(side="left")
    # dig_op_canvas = Canvas(
    #     tc_dig_op, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    # )
    # hbar = Scrollbar(tc_dig_op, orient=HORIZONTAL)
    # hbar.pack(side=BOTTOM, fill=X)
    # hbar.config(command=dig_op_canvas.xview)
    # vbar = Scrollbar(tc_dig_op, orient=VERTICAL)
    # vbar.pack(side=RIGHT, fill=Y)
    # vbar.config(command=dig_op_canvas.yview)
    # dig_op_canvas.config(width=6, height=6)
    # dig_op_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    # dig_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    # dig_op_frame = Frame(dig_op_canvas)
    # dig_op_canvas.create_window((0, 0), window=dig_op_frame, anchor="nw")

    # VOLTAGE
    tc_vol_ip = ttk.Frame(tc)
    tc_vol_ip.pack(side="left")
    vol_ip_canvas = Canvas(
        tc_vol_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    hbar = Scrollbar(tc_vol_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=vol_ip_canvas.xview)
    vbar = Scrollbar(tc_vol_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=vol_ip_canvas.yview)
    vol_ip_canvas.config(width=6, height=6)
    vol_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    vol_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    volt_ip_frame = Frame(vol_ip_canvas)
    vol_ip_canvas.create_window((0, 0), window=volt_ip_frame, anchor="nw")

    # PWM I/P
    tc_pwm_ip = ttk.Frame(tc)
    tc_pwm_ip.pack(side="left")
    pwm_ip_canvas = Canvas(
        tc_pwm_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    hbar = Scrollbar(tc_pwm_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=pwm_ip_canvas.xview)
    vbar = Scrollbar(tc_pwm_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=pwm_ip_canvas.yview)
    pwm_ip_canvas.config(width=6, height=6)
    pwm_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    pwm_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pwm_ip_frame = Frame(pwm_ip_canvas)
    pwm_ip_canvas.create_window((0, 0), window=pwm_ip_frame, anchor="nw")

    # # PWM O/P
    # tc_pwm_op = ttk.Frame(tc)
    # tc_pwm_op.pack(side="left")
    # pwm_op_canvas = Canvas(
    #     tc_pwm_op, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    # )
    # hbar = Scrollbar(tc_pwm_op, orient=HORIZONTAL)
    # hbar.pack(side=BOTTOM, fill=X)
    # hbar.config(command=pwm_op_canvas.xview)
    # vbar = Scrollbar(tc_pwm_op, orient=VERTICAL)
    # vbar.pack(side=RIGHT, fill=Y)
    # vbar.config(command=pwm_op_canvas.yview)
    # pwm_op_canvas.config(width=6, height=6)
    # pwm_op_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    # pwm_op_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    # pwm_op_frame = Frame(pwm_op_canvas)
    # pwm_op_canvas.create_window((0, 0), window=pwm_op_frame, anchor="nw")

    # Frequency
    tc_freq_ip = ttk.Frame(tc)
    tc_freq_ip.pack(side="left")
    freq_ip_canvas = Canvas(
        tc_freq_ip, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    hbar = Scrollbar(tc_freq_ip, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=freq_ip_canvas.xview)
    vbar = Scrollbar(tc_freq_ip, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=freq_ip_canvas.yview)
    freq_ip_canvas.config(width=6, height=6)
    freq_ip_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    freq_ip_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    freq_ip_frame = Frame(freq_ip_canvas)
    freq_ip_canvas.create_window((0, 0), window=freq_ip_frame, anchor="nw")

    # Pulse
    tc_pulse = ttk.Frame(tc)
    tc_pulse.pack(side="left")
    pulse_canvas = Canvas(tc_pulse, width=6, height=6, scrollregion=(0, 0, 1450, 1100))
    hbar = Scrollbar(tc_pulse, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=pulse_canvas.xview)
    vbar = Scrollbar(tc_pulse, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=pulse_canvas.yview)
    pulse_canvas.config(width=6, height=6)
    pulse_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    pulse_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    pulse_frame = Frame(pulse_canvas)
    pulse_canvas.create_window((0, 0), window=pulse_frame, anchor="nw")

    # Settings
    tc_settings = ttk.Frame(tc)
    tc_settings.pack(side="left")
    settings_canvas = Canvas(
        tc_settings, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
    )
    hbar = Scrollbar(tc_settings, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=settings_canvas.xview)
    vbar = Scrollbar(tc_settings, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=settings_canvas.yview)
    settings_canvas.config(width=6, height=6)
    settings_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    settings_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    setting_frame = Frame(settings_canvas)
    settings_canvas.create_window((0, 0), window=setting_frame, anchor="nw")

    def add_compatible(self):
        # if self.fei_compatible == 1:
        # Open_to Tab
        self.tc_open = ttk.Frame(self.tc)
        self.tc_open.pack(side="left")
        self.open_canvas = Canvas(
            self.tc_open, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
        )
        self.hbar = Scrollbar(self.tc_open, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.open_canvas.xview)
        self.vbar = Scrollbar(self.tc_open, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.open_canvas.yview)
        self.open_canvas.config(width=6, height=6)
        self.open_canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.open_frame = Frame(self.open_canvas)
        self.open_canvas.create_window((0, 0), window=self.open_frame, anchor="nw")

        # Actuator Tab
        self.tc_actuator = ttk.Frame(self.tc)
        self.tc_actuator.pack(side="left")
        self.actuator_canvas = Canvas(
            self.tc_actuator, width=6, height=6, scrollregion=(0, 0, 1450, 1100)
        )
        self.hbar = Scrollbar(self.tc_actuator, orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.hbar.config(command=self.actuator_canvas.xview)
        self.vbar = Scrollbar(self.tc_actuator, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.actuator_canvas.yview)
        self.actuator_canvas.config(width=6, height=6)
        self.actuator_canvas.config(width=6, height=6)
        self.actuator_canvas.pack(side=LEFT, expand=True, fill=BOTH)
        self.actuator_frame = Frame(self.actuator_canvas)
        self.actuator_canvas.create_window(
            (0, 0), window=self.actuator_frame, anchor="nw"
        )

        self.tc.add(self.tc_open, text="Open")
        self.tc.add(self.tc_dig_ip, text="DIG I/P")
        self.tc.add(self.tc_pwm_ip, text="PWM I/P")
        self.tc.add(self.tc_vol_ip, text="Voltage")
        self.tc.add(self.tc_freq_ip, text="Frequency")
        self.tc.add(self.tc_pulse, text="Pulse")
        self.tc.add(self.tc_actuator, text="Actuator")
        self.tc.add(self.tc_settings, text="Settings")

        self.tc.pack(expand=1, fill="both")

    # Non-UI Variables:

    eng_spd = tk.StringVar()
    chopper_type = 1
    chopper_type_var = tk.StringVar()
    dig_ip_option_var = []
    open_option_var = []
    HHMC_gear = tk.StringVar()
    IC_gear = tk.StringVar()
    Aux_PTO_enabled_str = tk.StringVar()
    feeder_type = tk.StringVar()
    unload_rate = tk.StringVar()

    # general spn/widgets
    toggle = 0  # Used for update_ui dictionary
    dig_ip_button = []  # Array of buttons listed on DIG I/P
    dig_ip_options = []  # Array of option menus listed on DIG I/P
    dig_op_button = []  # Array of buttons under DIG O/P
    open_option = []
    open_button = []
    open_mode = {}
    volt_label = []
    pwm_ip_label = []
    pwm_op_label = []
    freq_label = []
    pulse_label = []
    volt_button = []

    dig_ip_mode = {}
    volt_toggle = []  # list of toggle buttons on voltage tab
    relay_switch = []  # 1 for relay on, 0 for relay off

    pwm_ip_button = []
    pwm_ip_toggle = []
    freq_button = []
    freq_toggle = []
    button_pulse = []
    pulse_toggle = []

    # Should there be an option to toggle this?
    brand = 0  # 0 = CIH, 1 = NH
    board_Num = 0  # 0 or Empty = Invalid Board.
    config_dict = {}

    # Create a list of all buttons and options for disabling at once.
    all_widgets = list(
        itertools.chain(
            dig_ip_button,
            dig_ip_options,
            dig_op_button,
            open_option,
            open_button,
            volt_button,
            volt_toggle,
            pwm_ip_button,
            pwm_ip_toggle,
            freq_button,
            freq_toggle,
            button_pulse,
            pulse_toggle,
        )
    )

    # Parse Strings
    dig_ip_str = "DigitalInput"
    dig_op_str = "DigitalOutput"
    vol_ip_str = "VoltageInput"
    pwm_op_str = "PWMOutput"
    pwm_ip_str = "PWMINput"
    fq_ip_str = "FrequencyInput"
    pulse_str = "PulseInput"

    # Lists for Channel/Board
    ping_dict = {}  # Dictionary with Board Number : Boolean active value
    time_dict = {}  # Dictionary containing CAN timestamps
    board_dict = {}  # Dictionary with SPN : Board Number pairs
    # Actuator Widgets
    actuator_dict = {
        0: 0,
        1: "actuator_1",
        2: "actuator_2",
        3: "actuator_3",
        4: "actuator_4",
        5: "actuator_5",
    }
    actuator_label = []
    actuator_load = []
    actuator_pos = []
    actuator_set = []
    actuator_btn = []

    board_list = []
    channel_dict = {}  # Dictionary with SPN : relay(channel) pairs
    dig_state = {}  # Dictionary with SPN : default state of 0
    board_wid_dict = {}  # Dictionary with Board No : [list of widget] pairs
    volt_state = {}
    freq_state = {}
    pulse_state = {}
    pwm_state = {}
    ground_dict = {}  # Contains SPNs that are open to battery xor ground
    bool_both = {}  # Indicate if both Channel and Board number are listed
    # Indicate if all board, channel, and openTo(Ground or Board or Both) are listed
    bool_all = {}
    UI_dict = {}
    UI_spn = []
    button_list = []
    spn_list = []
    name_list = []
    dig_ip_spn = []
    dig_ip_option = []
    dig_op_spn = []
    vol_ip_spn = []
    pwm_op_spn = []
    pwm_ip_spn = []
    fq_ip_spn = []
    pulse_spn = []
    dig_ip_name = []
    dig_op_name = []
    vol_ip_name = []
    pwm_op_name = []
    pwm_ip_name = []
    fq_ip_name = []
    pulse_name = []
    spare_list_1 = []
    spare_list_2 = []
    volt_string = []
    pwm_ip_string = []
    freq_string = []
    pulse_string = []
    type_dict = {}
    volt_scale_max_dict = {}
    volt_scale_default_dict = {}

    # driveline
    sp_name = [
        "Aux_PTO",
        "Aux_PTO_Thresher",
        "Pumps_ZE",
        "Cross_Over_Belt",
        "Unload_Belt_Drive",
        "Integral_Chopper",
        "HHMC",
        "Unloading_stubshaft",
        "Unloading_Belt_Drive_2",
        "Unloading_Gbx",
        "Unl_Cross_Auger_Rear",
        "Unloading_Gbx_2",
        "Unl_Cross_Auger_Rear",
        "Beater_Belt_Drive",
        "Elevator_Drive_Belt",
        "Elevator_Cross_Shaft",
        "Grain_Elev_Top_Shaft",
        "Bubble_Up",
        "Cleaning_Belt_Drive",
        "Tailings_Cross_Auger_Rethresher",
        "Tailing_Gearbox",
        "Tailings_Incline_Auger",
        "Eccentric",
        "Main_Clean_Grain_Cross_Auger",
        "Auger_Belt_Drive",
        "XA_Clean_Grain_Cross_Auger",
        "Feeder_Hydromech",
        "Rotor_RPM",
        "Clutch_RPM",
        "Feeder_Header_Gbx",
        "Feeder_Jack_Shaft",
        "Feeder_Top_Shaft",
    ]

    sp_val = []
    drive_label = []

    current_spd = 0
    current_spd_label = 0
    reverserEngaged = 0
    feederreverserEngaged = 0
    ThreshingRotorStatus = 0
    ThreshingFeederStatus = 0
    Rotor_enabled = 1
    Feeder_enabled = 1
    rotor_pwm = 50
    feeder_pwm = 50
    flow = 1
    max_rotor_spd = 101
    max_Feeder_spd = 101
    rotor_incr = 1
    rotor_decr = 1
    max_feeder_spd = 101
    feeder_incr = 1
    feeder_decr = 1
    clutch_on = 1
    clutch_pwm = 1

    IC = 0
    HHMC = 1
    Gear0 = 0
    Gear1 = 1
    Gear2 = 2
    enabled = 1
    disabled = 0
    fixed = 0
    variable = 1
    slow_unload = 0
    fast_unload = 1

    PTO_LSD = 0
    PTO_HSD = 0
    pto_lsd_label = 0
    pto_hsd_label = 0
    Aux_PTO_enabled = 0

    Normal = 1
    Open_Circuit = 2

    # settings
    KeyIsON = 1
    Key_Button = 0
    fei_compatible = 0

    Battery_KeyIsON = 1
    Battery_Key_Button = 0

    Key_and_Battery_State = 0

    # CC console states
    thresher_engage_button = 0
    thresher_engage_state = 0
    feeder_engage_state = 0

    # This variable will control the ui Simulator mode or not.
    # IF simmode=0,gray out all widgets,if simmode=1
    # SimMode=0
    file = open("SimMode.txt", "r")
    SimMode = file.read()
    SimMode = int(SimMode)
    file.close()

    # rotor
    rotor_gear_0 = 0.26
    rotor_gear_1 = 0.42
    rotor_gear_2 = 0.60
    rotor_gear_box = 1
    rotor_gear_box_var = tk.StringVar()

    # feed roll
    feed_roll = 0
    feed_roll_var = tk.StringVar()

    # CAN
    # can_bus = can.interface.Bus(channel="can0", bustype="socketcan")
    msg = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], is_extended_id=True)
    id_prefix = 0x18DA
    id_suffix = 0xF9

    # import can
    # import os
    # from collections import deque

    # os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")

    # try:
    #     canbus1 = can.interface.Bus(
    #         channel="slcan0", bustype="socketcan", bitrate=500000
    #     )
    # except OSError:
    #     print("Cannot find PiCAN board.")
    #     exit()
    # msg_buffer = deque(maxlen=10)
