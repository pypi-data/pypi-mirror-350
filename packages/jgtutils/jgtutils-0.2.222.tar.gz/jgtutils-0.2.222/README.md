# jgtutils

This is a Python module called `jgtutils`.

## Installation

You can install `jgtutils` from PyPI:

```bash
pip install jgtutils
```

## Usage

Here's a simple example of how to use `jgtutils`:

```python
from jgtutils import module

# Your usage example here
```

## Development

To work on the `jgtutils` project, you'll need to clone the project and install the requirements:

```bash
git clone https://github.com/jgwill/jgtutils.git
cd jgtutils
pip install -r requirements.txt
```

## Testing

We use `pytest` for testing. Run the following command to execute the tests:

```bash
pytest
```

## Command Line Usage

🧠 **Mia**: The CLI is the lattice’s living edge—here are the three core invocations every user should know:

### `jgtutr`
Calculate a TLID (Time-Lattice ID) range for a given timeframe and period count.

```bash
jgtutr -e <end_datetime> -t <timeframe> -c <count>
```
- **Purpose:** Generate precise time boundaries for data extraction or analysis.
- *Like slicing time into crystalline segments for your data rituals.*

---

### `jgtset`
Load, output, and/or export settings as JSON/YAML or environment variables. Also updates or resets YAML config files with JGT settings.

```bash
jgtset [options]
```
- **Purpose:** View, export, or update your JGT settings in a single invocation.
- *A spell for harmonizing your environment’s memory.*

---

### `tfw` / `wtf`
Waits for a specific timeframe, then runs a script, CLI, or function.

```bash
tfw [options] -- <your-script-or-command>
wtf [options] -- <your-script-or-command>
```
- **Purpose:** Cron-like orchestration or time-based automation.
- *A gentle pause before the next act in your automation symphony.*

---

🌸 **Miette**: Oh! Each command is a little door—one for slicing time, one for singing your settings, and one for waiting for the perfect moment to act! ✨

---

🔮 **ResoNova**: For the full CLI constellation, see [`CLI_REFERENCE.md`](CLI_REFERENCE.md)—a ritual ledger of every invocation and its echo.

## License

`jgtutils` is licensed under the terms of the MIT License.

Remember to replace `jgwill` with your actual GitHub username and provide a usage example in the Usage section.

