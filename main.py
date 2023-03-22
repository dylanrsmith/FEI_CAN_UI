import time
from global_defines import *
from socket1 import *
from UserInterface.parse_excel import *
from UserInterface.generate_ui import *
from UserInterface.update_ui import *

start = time.time()
gd_obj = global_defines()

"""
remember to uncomment flip-all-off in generate)ui and uicallbacks
and declare canbus in global defines
uncomment updateui offline function in update_ui..with boards connected
"""

# testing_active is set to 1...

# if gd_obj.testing_active == 0:
#     # start IO control
#     io = IOCtrl(gd_obj)
#     from startup_init import *

#     st = start_init(gd_obj, io)
#     st.init_key()
#     st.init_freq()
#     st.init_spn()
# else:
#     io = IOCtrl(gd_obj)
#     st = 0

pe = parse_excel(gd_obj)
gu = generate_ui(gd_obj)
ui = update_ui(gd_obj)

pe.parse_excel()
gd_obj.add_compatible()

# if gd_obj.fei_compatible == 1:
gu.generate_actuator_ui()
gu.generate_open_ui()
gu.generate_spn_ui()
gu.generate_setting_ui()
gu.generate_cc_console_ui()
gu.get_sim_mode()


# update_ui.py
def ui_update_thread():
    if gd_obj.testing_active == 0:
        ui.update_ui_spn()
        ui.update_ui_dict()
        # ui.update_ui_driveline()
        # ui.update_ui_clrm()
        # ui.update_ui_ghcv()
        # ui.update_ui_rsch()
        # ui.update_ui_ghts()
        # # ui.update_ui_rsck()
        # ui.update_ui_ghps()
        # ui.update_ui_thcc()
        # ui.update_ui_gdpb()
        # ui.update_ui_gdhd()
        # ui.update_ui_clfn()
        # ui.update_ui_rssp()
        # ui.update_ui_hdhr()
        # ui.update_ui_hdfn()
        # ui.update_ui_agge()
        # ui.update_ui_rrts()
        # ui.update_ui_hdhc()
        # ui.update_ui_fffa()
        # ui.update_ui_gdst()
        ui.update_settings()
        ui.update_cc_console()
        ui.update_cpu()
        ui.update_ui_offline()

        th1 = threading.Timer(0.01, ui_update_thread)
        th1.setDaemon(True)
        th1.start()  # 1 Second Read Thread
    else:
        ui.update_ui_spn()
        ui.update_ui_dict()
        # ui.update_ui_driveline()
        # ui.update_ui_clrm()
        # ui.update_ui_ghcv()
        # ui.update_ui_rsch()
        # ui.update_ui_ghts()
        # # ui.update_ui_rsck()
        # ui.update_ui_ghps()
        # ui.update_ui_thcc()
        # ui.update_ui_gdpb()
        # ui.update_ui_gdhd()
        # ui.update_ui_clfn()
        # ui.update_ui_rssp()
        # ui.update_ui_hdhr()
        # ui.update_ui_hdfn()
        # ui.update_ui_agge()
        # ui.update_ui_rrts()
        # ui.update_ui_hdhc()
        # ui.update_ui_fffa()
        # ui.update_ui_gdst()
        ui.update_settings()
        ui.update_cc_console()
        ui.update_cpu()
        ui.update_ui_offline()

        th1 = threading.Timer(1, ui_update_thread)
        th1.setDaemon(True)
        th1.start()


# def plant_model_update_thread():
#     if gd_obj.testing_active == 0:
#         dv.calculate_speeds(gd_obj.current_spd)
#         cl.calculate_speed()
#         gh.calculate_state()
#         rs.rsch_temp()
#         gt.calculate()
#         rsck.calculate()
#         ghps.calculate()
#         thcc.calculate()
#         gdpb.calculate()
#         gdhd.calculate()
#         clfn.calculate_RPM()
#         rssp.calculate_rpm()
#         hdhr.calculate_hdr_volt()
#         hdfn.calculate_hdr_pos()
#         agge.calculate()
#         rrts.calculate()
#         hdhc.calculate()
#         fffa.calculate()
#         gdst.calculate()
#         rotor_obj.calculate_rotor()
#         feeder_obj.calculate_Feeder()
#         # 1 second read thread
#         th2 = threading.Timer(0.01, plant_model_update_thread)
#         th2.setDaemon(True)
#         th2.start()
#     else:
#         dv.calculate_speeds(gd_obj.current_spd)
#         cl.calculate_speed()
#         gh.calculate_state()
#         rs.calculate()
#         gt.calculate()
#         rsck.calculate()
#         ghps.calculate()
#         thcc.calculate()
#         gdpb.calculate()
#         gdhd.calculate()
#         clfn.calculate_RPM()
#         rssp.calculate_rpm()
#         hdhr.calculate_hdr_volt()
#         hdfn.calculate_hdr_pos()
#         agge.calculate()
#         rrts.calculate()
#         hdhc.calculate()
#         fffa.calculate()
#         gdst.calculate()
#         # 2 second read thread
#         th2 = threading.Timer(0.01, plant_model_update_thread)
#         th2.setDaemon(True)
#         th2.start()


end = time.time()
boot_time = end - start
print("Boot Time = %s seconds" % boot_time)


ui_update_thread()
ui.mainloop()
