Python¶
Templates can also be written in Python code. The template will automatically be interpreted as Python if lines are prefixed with !. Note: You can't mix Python and Jinja2.

An example of a complex Python macro:

[gcode_macro clean_nozzle]
gcode:
  !wipe_count = 8
  !emit("G90")
  !emit("G0 Z15 F300")
  !for wipe in range(wipe_count):
  !  for coordinate in [(275, 4), (235, 4)]:
  !    emit(f"G0 X{coordinate[0]} Y{coordinate[1] + 0.25 * wipe} Z9.7 F12000")
For ease of writing python macros, they may be read from a .py file. Python type stubs for macros are also available under klippy.macro.

## printer.cfg

[gcode_macro clean_nozzle]
gcode: !!include my_macros/clean_nozzle.py

## my_macros/clean_nozzle.py

wipe_count = 8
emit("G90")
emit("G0 Z15 F300")
...
Python: Rawparams¶
[gcode_macro G4]
rename_existing: G4.1
gcode:
  !if rawparams and "S" in rawparams:
  !  s = int(rawparams.split("S")[1])
  !  respond_info(f"Sleeping for {s} seconds")
  !  emit(f"G4.1 P{s * 1000}")
  !else:
  !  p = int(rawparams.split("P")[1])
  !  respond_info(f"Sleeping for {p/1000} seconds")
  !  emit(f"G4.1 {rawparams}")
Python: Variables¶
[gcode_macro POKELOOP]
variable_count: 10
variable_speed: 3
gcode:
  !for i in range(own_vars.count):
  !  emit(f"BEACON_POKE SPEED={own_vars.speed} TOP=5 BOTTOM=-0.3")
Python: Printer objects¶
[gcode_macro EXTRUDER_TEMP]
gcode:
    !ACTUAL_TEMP = printer["extruder"]["temperature"]
    !TARGET_TEMP = printer["extruder"]["target"]
    !
    !respond_info("Extruder Target: %.1fC, Actual: %.1fC" % (TARGET_TEMP, ACTUAL_TEMP))
Python: Helpers¶
emit
wait_while
wait_until
wait_moves
blocking
sleep
set_gcode_variable
emergency_stop / action_emergency_stop
respond_info / action_respond_info
raise_error / action_raise_error
call_remote_method / action_call_remote_method
math