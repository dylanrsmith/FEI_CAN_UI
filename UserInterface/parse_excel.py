from global_defines import *
import pandas as pd
import os


class parse_excel:
    """
    This module is used to parse necessary data that has been configured in the Excel file: `Config_sheet.xlsx`

    Utilizes `pandas` python module to parse and read data from the CSV file, and converts said data into a pandas dataframe for manipulation.
    """

    global df, _pe

    def __init__(self, ob):
        """
        Module Initializing function.

        NOTE: may need to alter slash in path variable to match with OS file system...
        For windows, use backslash, for Unix, use forward slash.
        """
        path = os.path.dirname(__file__)
        # path += "/Config_sheet.xlsx"
        path += "/output_file.xlsx"
        self.df = pd.read_excel(path, "SPN", header=0)
        self._pe = ob

    def parse_excel(self):
        """
        Opens the file specified by `path` variable, and parses data listed in SPN table.

        Tkinter will generate necessary components, based on the excel configuration.
        """
        # for i in range(1452):
        for i in range(len(self.df.index)):
            # if True:
            spn = i
            self._pe.spn_list.append(spn)
            spn_data = self.df.loc[i, "UI_type"]
            spn_type = str(spn_data)

            # Check if 3 columns are configured:
            if (
                ("Board_Num" in self.df.columns)
                and ("Channel" in self.df.columns)
                and ("open_to" in self.df.columns)
            ):
                self._pe.fei_compatible = 1
            else:
                self._pe.fei_compatible = 0

            # Only if type column has valid entries
            if (
                (self._pe.dig_ip_str in spn_type)
                or (self._pe.dig_op_str in spn_type)
                or (self._pe.vol_ip_str in spn_type)
                or (self._pe.pwm_op_str in spn_type)
                or (self._pe.pwm_ip_str in spn_type)
                or (self._pe.fq_ip_str in spn_type)
                or (self._pe.pulse_str in spn_type)
            ):
                # required data
                # name = self.df.loc[spn, "Name"]
                name = self.df.loc[spn, "Description"]
                self._pe.name_list.append(name)
                self._pe.UI_spn.append(spn)
                self._pe.UI_dict.update({spn: 0})
                xl_spn = self.df.loc[spn, "SPN"]
                name_spn = "SPN" + " " + str(xl_spn)
                self._pe.config_dict.update({spn: name})  # all data in dictionary

                # Populate Relay State Dictionaries:
                self._pe.dig_state.update({spn: 0})
                self._pe.volt_state.update({spn: 0})
                self._pe.freq_state.update({spn: 0})
                self._pe.pulse_state.update({spn: 0})
                self._pe.pwm_state.update({spn: 0})

                # Read Relay Columns if they exist
                if self._pe.fei_compatible == 1:
                    # Parses excel for Board Number Entries
                    board_no = self.df.loc[spn, "Board_Num"]
                    self._pe.board_no_str = str(board_no)

                    # Parses for Channel(Relay)
                    channel = self.df.loc[spn, "Channel"]
                    self._pe.channel_no_str = str(channel)

                    # Parses for O2B/G
                    openTo = self.df.loc[spn, "open_to"]
                    self._pe.openTo_str = str(openTo)

                    # Parse open_to, channel, and board number columns
                    # Also creating list of boards from excel
                    if board_no != "nan":
                        self._pe.board_dict.update({spn: board_no})
                    if (pd.notna(board_no)) and (
                        board_no not in self._pe.board_list
                    ):
                        self._pe.board_list.append(int(board_no))
                    if channel != "nan":
                        self._pe.channel_dict.update({spn: channel})
                    if self._pe.openTo_str != "nan":
                        self._pe.ground_dict.update({spn: self._pe.openTo_str})

                    # Populate boolean dictionaries
                    # Check if Board Number and Channel are both configured
                    if self._pe.board_no_str and self._pe.channel_no_str != "nan":
                        self._pe.bool_both.update({spn: 1})
                    else:
                        self._pe.bool_both.update({spn: 0})

                    # Check if Board Number and Channel and OpenToB/G are all configured
                    if self._pe.board_no_str and self._pe.channel_no_str != "nan":
                        if self._pe.openTo_str != "nan":
                            self._pe.bool_all.update({spn: 1})
                    else:
                        self._pe.bool_all.update({spn: 0})

                new_name = str(name_spn) + " : " + str(name) + " | Board: " + str(board_no) + " | Channel: " + str(channel)
                if self._pe.dig_ip_str in spn_type:
                    self._pe.dig_ip_spn.append(spn)
                    self._pe.dig_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "digout"})

                # elif self._pe.dig_op_str in spn_type:
                #     self._pe.dig_op_spn.append(spn)
                #     self._pe.dig_op_name.append(new_name)
                #     self._pe.type_dict.update({spn: "digout"})

                elif self._pe.vol_ip_str in spn_type:
                    self._pe.vol_ip_spn.append(spn)
                    self._pe.vol_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "volt"})
                    # max_val = self.df.loc[i, "max"]
                    # def_val = self.df.loc[i, "default"]
                    # self._pe.volt_scale_max_dict.update({spn: int(max_val)})
                    # self._pe.volt_scale_default_dict.update({spn: int(def_val)})

                elif self._pe.pwm_ip_str in spn_type:
                    self._pe.pwm_ip_spn.append(spn)
                    self._pe.pwm_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "pwmout"})

                # elif self._pe.pwm_op_str in spn_type:
                #     self._pe.pwm_op_spn.append(spn)
                #     self._pe.pwm_op_name.append(new_name)
                #     self._pe.type_dict.update({spn: "pwmout"})

                elif self._pe.fq_ip_str in spn_type:
                    self._pe.fq_ip_spn.append(spn)
                    self._pe.fq_ip_name.append(new_name)
                    self._pe.type_dict.update({spn: "freqin"})

                elif self._pe.pulse_str in spn_type:
                    self._pe.pulse_spn.append(spn)
                    self._pe.pulse_name.append(new_name)
                #     self._pe.type_dict.update({spn: "pulse"})
                else:
                    pass
            else:
                self._pe.spare_list_1.append(spn)
            # else:
            #     self._pe.spare_list_2.append(i)
