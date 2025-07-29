
import sys
import platform
import threading
import fibre
import abidrive
import abidrive.enums
from abidrive.utils import *

def print_banner():
    print("Website: https://abirobotics.com/")
    print("Docs: https://abirobotics.com/ABIDrive/")

    print()
    print('Please connect your ABIDrive.')
    print('You can also type help() or quit().')

def print_help(args, have_devices):
    print('')
    if have_devices:
        print('Connect your ABIDrive to {} and power it up.'.format(args.path))
        print('After that, the following message should appear:')
        print('  "Connected to ABIDrive [serial number] as dev0"')
        print('')
        print('Once the ABIDrive is connected, type "dev0." and press <tab>')
    else:
        print('Type "dev0." and press <tab>')
    print('This will present you with all the properties that you can reference')
    print('')
    print('For example: "dev0.axis0.encoder.pos_estimate"')
    print('will print the current encoder position on axis 0')
    print('and "dev0.axis0.controller.input_pos = 0.5"')
    print('will send axis 0 to 0.5 turns')
    print('')


interactive_variables = {}

discovered_devices = []

def benchmark(abidrv):
    import asyncio
    import time

    async def measure_async():
        start = time.monotonic()
        futures = [abidrv.vbus_voltage for i in range(1000)]
#        data = [await f for f in futures]
#        print("took " + str(time.monotonic() - start) + " seconds. Average is " + str(sum(data) / len(data)))

    fibre.libfibre.libfibre.loop.call_soon_threadsafe(lambda: asyncio.ensure_future(measure_async()))

def launch_shell(args, logger):
    """
    Launches an interactive python or IPython command line
    interface.
    As ABIDrives are connected they are made available as
    "dev0", "dev1", ...
    """

    interactive_variables = {
        'start_liveplotter': start_liveplotter,
        'dump_errors': dump_errors,
        'benchmark': benchmark,
        'oscilloscope_dump': oscilloscope_dump,
        'dump_interrupts': dump_interrupts,
        'dump_threads': dump_threads,
        'dump_dma': dump_dma,
        'dump_timing': dump_timing,
        'BulkCapture': BulkCapture,
        'step_and_plot': step_and_plot,
        'calculate_thermistor_coeffs': calculate_thermistor_coeffs,
        'set_motor_thermistor_coeffs': set_motor_thermistor_coeffs
    }

    # Expose all enums from abidrive.enums
    interactive_variables.update({k: v for (k, v) in abidrive.enums.__dict__.items() if not k.startswith("_")})

    async def mount(obj):
        serial_number_str = await abidrive.utils.get_serial_number_str(obj)
        if ((not args.serial_number is None) and (serial_number_str != args.serial_number)):
            return None # reject this object
        if hasattr(obj, '_otp_valid_property') and not await obj._otp_valid_property.read():
            #logger.warn("Device {}: Not a genuine ABIDrive! Some features may not work as expected.".format(serial_number_str))
            return ("device " + serial_number_str, "dev")
        return ("ABIDrive " + serial_number_str, "dev")

    fibre.launch_shell(args, mount,
                       interactive_variables,
                       print_banner, print_help,
                       logger)
