import click

import teensytoany


@click.command(epilog=f"Version {teensytoany.__version__}")
@click.option(
    '--serial-number',
    default=None,
    help=(
        'Serial number of the Teensy device to program. '
        'If not provided and only one Teensy device found, '
        'it will be programmed.'
    )
)
# Create an option with 2 valid inputs TEENSY40 and TEENSY32
@click.option(
    '--mcu',
    type=click.Choice(['TEENSY40', 'TEENSY32']),
    default='TEENSY40',
    help='Microcontroller to program.'
)
@click.option(
    '--firmware-version',
    default=None,
    type=str,
    help='Firmware version to program. If not provided, the latest version will be programmed.'
)
@click.option(
    '--firmware-variant',
    default=None,
    type=str,
    help='Firmware variant to program. If not provided, the standard variant will be programmed.'
)
@click.option(
    '--download-only',
    is_flag=True,
    default=False,
    help='Download the firmware only, do not program the device.'
)
# Make the epligue print the version
@click.version_option(teensytoany.__version__)
def teensytoany_programmer(
    serial_number=None,
    mcu='TEENSY40',
    firmware_version=None,
    firmware_variant=None,
    download_only=False
):
    """Program a Teensy device with a given firmware version"""
    variant_str = f"variant {firmware_variant} of " if firmware_variant else ""
    if download_only:
        for mcu_to_download in ['TEENSY40', 'TEENSY32']:
            if firmware_version is None:
                firmware_version = teensytoany.TeensyToAny.get_latest_available_firmware_version(
                    mcu=mcu_to_download, online=True, local=False
                )
            print(
                f"Downloading {variant_str} firmware version {firmware_version} "
                f"for {mcu_to_download}."
            )
            teensytoany.TeensyToAny.download_firmware(
                mcu=mcu_to_download,
                version=firmware_version,
                variant=firmware_variant
            )
        return

    print('Programming Teensy with:')
    teensytoany.TeensyToAny.program_firmware(
        serial_number,
        mcu=mcu,
        version=firmware_version,
        variant=firmware_variant
    )
    teensy = teensytoany.TeensyToAny(serial_number)
    print(f"TeensyToAny version: {teensy.version}")
    print(f"TeensyToAny variant: {firmware_variant}")
    print(f"TeensyToAny serial_number: {teensy.serial_number}")
    teensy.close()


if __name__ == '__main__':
    teensytoany_programmer()
