# System Details — Voron 2.4 (Monolith 4WD, Beacon, XOL)

## Platform
- Firmware: Klipper running the Kalico fork. See https://docs.kalico.gg and https://github.com/KalicoCrew/kalico/
- UI/Services: Moonraker, Fluidd, KlipperScreen, Crowsnest (camera), Spoolman (inventory), Sonar (Wi‑Fi keepalive).
- Repo intent: Keep `printer.cfg` lean; hardware, features, and macros live under `hardware/`, `features/`, and `macros/` and are included via globbing.

## Motion & Gantry
- Kinematics: CoreXY with “4WD” Monolith gantry (dual X and dual Y drives):
  - XY: `stepper_x`, `stepper_x1`, `stepper_y`, `stepper_y1` on Octopus.
  - Drivers: TMC2240 (SPI soft). `microsteps: 128`, `rotation_distance: 40`, `run_current: ${constants.run_current_xy}` (1.2A default), `rref: 12000`, `driver_SLOPE_CONTROL: 2`.
  - Endstops: X endstop on `nhk:gpio13`, Y endstop on `PG6`. Homing to max (`position_endstop: 285`, `homing_positive_dir: true`).
- Motor sync: `features/motors_sync.cfg` uses the Beacon accelerometer for XY microstep synchronization. Invoked via `SYNC_MOTORS` (called in `PRINT_START`).
- Input shaping: `features/input_shaper.cfg` (mzv; X 91.4 Hz, Y 66.4 Hz). Resonance tester uses Beacon as the accelerometer.

## Z, Leveling, and Mesh
- Z: Four independent Z steppers (`stepper_z`, `z1`, `z2`, `z3`), TMC2209, `microsteps: 64`, `gear_ratio: 80:16`.
- Homing: Beacon virtual endstop (`endstop_pin: probe:z_virtual_endstop`).
- Gantry tramming: `features/quad_gantry_level.cfg` with defined bed corners and 4 probe points. Helper macro `QUAD_GANTRY_SCAN` runs QGL and parks.
- Probing: Beacon RevH configured in `hardware/probe_beacon.cfg` (`x_offset: 0`, `y_offset: 19`, homing at `home_xy_position: 145,135`). Includes contact/proximity modes and nozzle thermal expansion macros (`macros/Beacon/`).
- Mesh: `features/bed_mesh.cfg` dense 50×50 bicubic mesh, `horizontal_move_z: 0`, `zero_reference_position: 145,135`.
- KAMP: Adaptive meshing/purging enabled (Moonraker `enable_object_processing: True`). Settings macro in `features/KAMP_Settings.cfg`. Start flow calls `BED_MESH_CALIBRATE ADAPTIVE=1 RUNS=2`.

## Extrusion & Hotend
- Toolhead MCU: Nitehawk36 (`[mcu nhk]`).
- Extruder: Sherpa Mini (`gear_ratio: 50:8`, `rotation_distance: 22.67895`, 200‑step motor). TMC2209 (`run_current: 0.30`).
- Hotend: XOL. Extruder heater uses MPC (`heater_power: 100`), PT1000 sensor on `nhk:gpio29` with `pullup_resistor: 2200`. `ambient_temp_sensor: temperature_sensor beacon_coil` is referenced.
- Fans: `heater_fan hotend_fan` on `nhk:gpio5` with tach (`nhk:gpio16`); print fan on `nhk:gpio6`.

## Bed, Chamber, and Cooling
- Bed: SSR on `PA3`, 3950 thermistor on `PF3`. MPC enabled (`heater_power: 400`).
- Chamber: PTC heater as `heater_generic chamber_heater` using two combined 3950 sensors (`temperature_combined` over `Chamber1`/`Chamber2`). Watermark control with verification guard.
- Controller fans: Stepper cooling on `PD14`/`PD15` (hardware PWM), chamber/bed controller fans on `PD12` and `PD13`.

## Lighting & Peripherals
- Case light: `hardware/leds_caselight.cfg` (PB10).
- Hotend LEDs: `hardware/leds_hotend.cfg` (`neopixel HE_LEDS`, chain 2). Optional `output_pin act_led` on `nhk:gpio8`.
- Camera: `modules/crowsnest.conf` set for Logitech C525 (1080p@15fps, port 8080).
- Spoolman: `macros/spoolman.cfg` exposes `SET_ACTIVE_SPOOL` and `CLEAR_ACTIVE_SPOOL`.

## MCUs
- Mainboard: Octopus F446 (`hardware/mcu_octopus.cfg`).
- Toolhead: Nitehawk36 RP2040 (`hardware/mcu_nitehawk36.cfg`).
- Optional: Hotkey RP2040 (`hardware/mcu_hotkey.cfg`, non‑critical).

## Start/End Flow (Key Calls)
- Start (`macros/Print/print_start.cfg`): lights on → `SYNC_MOTORS` → conditional home → heat bed/chamber → `G28 Z METHOD=CONTACT CALIBRATE=1` → `QUAD_GANTRY_SCAN` → `BED_MESH_CALIBRATE ADAPTIVE=1 RUNS=2` → `M109` → apply Beacon thermal offset → `LINE_PURGE`.
- End (`macros/Print/print_end.cfg`): retract, safe moves, heaters off, LEDs dim, `MOTION_MINDER`, clear mesh.

## Notes
- Do not hand‑edit auto `SAVE_CONFIG` blocks; rerun tuning and let Klipper write them.
- KAMP settings are stored in `features/KAMP_Settings.cfg`. Ensure the printer include path matches this repository layout.
