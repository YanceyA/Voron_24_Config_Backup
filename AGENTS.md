# Repository Guidelines

This repository targets a Klipper printer running the Kalico fork. For the full hardware/architecture overview and configuration map, see `SYSTEM_DETAILS.md`.

## Project Structure & Module Organization
`printer.cfg` is the root include file and should remain minimal; use `[include]` directives to pull in per-feature configs. Organize updates in the existing folders:
- `hardware/` holds board, sensor, and motion subsystem wiring.
- `macros/` contains grouped automation flows (`macros/Print`, `macros/Beacon`, etc.) and shared `variables.txt`.
- `features/` tracks optional Klipper modules (bed mesh, KAMP, ShakeTune) so they can be toggled by include order.
- `modules/` captures companion service configs (`KlipperScreen.conf`, `crowsnest.conf`).
- `config_backups/` and results folders (`adxl_results/`, `ShakeTune_results/`) store captured data; keep raw exports here, not in feature directories.
Respect the include globbing already declared in `printer.cfg` when adding new files.

## Build, Test, and Development Commands
- `~/klipper/scripts/check_klippy.py printer.cfg` validates syntax and inclusion paths before you reload the printer.
- `~/klipper/scripts/calc_estimate.py -c printer.cfg` helps verify motion limits if you alter speeds/accelerations.
- `./autocommit.sh` backs up `~/printer_data/config`, captures Klipper/Moonraker versions, and pushes to the `main` branch.

## Coding Style & Naming Conventions
Follow the existing two-space indentation and align parameters on the same column where practical. Use lowercase snake case for sections and filenames (`heater_bed`, `park_bed.cfg`). Mirror Klipper option names exactly; add clarifying block comments in all-caps dividers (`#####################################################################`) if you introduce new subsystems. Store reusable constants under `[gcode_macro ...]` variables instead of duplicating values.

## Testing Guidelines
After validation, deploy with `RESTART` from the console and confirm `STATUS` reports clean load. For macros, run a dry-fire in `PRINT_START` or targeted macros with `FIRMWARE_RESTART` ready if something fails. Attach ADXL or ShakeTune captures to the matching results directory and mention the dataset name in your PR. Avoid editing the auto-generated `SAVE_CONFIG` blocks; instead rerun tuning commands and let Klipper rewrite them.

## Commit & Pull Request Guidelines
Automated backups use the `Autocommit from <timestamp>` format; for manual work prefer `area: short imperative` (e.g., `macros: adjust purge sequence`). Provide a brief summary of changed files, a verification log (commands, macros exercised), and reference any issue or tune ID. Screenshots of UI changes or sensor plots help reviewers. Ensure PRs stay focused—split hardware, macro, and feature adjustments into separate branches when possible.
