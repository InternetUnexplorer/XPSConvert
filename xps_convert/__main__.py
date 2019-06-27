from argparse import ArgumentParser
from collections import defaultdict
from os.path import join
from typing import Dict, List

from xps_convert.read.mhs_parser import parse_mhs
from xps_convert.read.xmp_parser import parse_xmp

"""
This is a brief demo that reads the XMP and MHS files associated with a project
and prints some information about them.

Usage: python -m xps_convert [-h] [-a] [-d] [-c] [-C] PROJECT_DIR
"""

if __name__ == "__main__":
    # Get command-line arguments
    parser = ArgumentParser(description="Show information about an XPS project.")
    parser.add_argument(
        "project_dir", metavar="PROJECT_DIR", help="XPS project directory"
    )
    parser.add_argument(
        "--all", "-a", help="show everything (default)", action="store_true"
    )
    parser.add_argument(
        "--device", "-d", help="show the device part name", action="store_true"
    )
    parser.add_argument(
        "--components", "-c", help="show the list of components", action="store_true"
    )
    parser.add_argument(
        "--connections", "-C", help="show the list of connections", action="store_true"
    )
    args = parser.parse_args()

    project_dir = args.project_dir
    show_all = args.all or not any((args.device, args.components, args.connections))
    show_device = args.device or show_all
    show_components = args.components or show_all
    show_connections = args.connections or show_all

    # Load the XMP file (system.xmp)
    with open(join(project_dir, "system.xmp"), "r") as file:
        xmp = parse_xmp("system.xmp", file)

    # Load the MHS file (specified in system.xmp)
    mhs_file = xmp.values.get("MHS File")
    with open(join(project_dir, mhs_file), "r") as file:
        mhs = parse_mhs("system.mhs", file)

    # Print device part name
    if show_device:
        # Part name is a combination of the Device, Package, and SpeedGrade fields
        device = "".join(map(xmp.values.get, ("Device", "Package", "SpeedGrade")))
        print(f"Device: {device}\n")

    # Print list of components
    if show_components:
        print(f"Components: ({len(mhs.components)})")
        for component in mhs.components.values():
            print(f"- {component.instance_name} ({component.peripheral_name})")
        print()

    # Print list of connections
    if show_connections:
        # Create map of component port connections
        port_map: Dict[str, List[str]] = defaultdict(list)
        # Add component ports
        for component in mhs.components.values():
            for port, dests in component.assignments.ports.items():
                for dest in dests.split("&"):
                    port_map[dest.strip()].append(f"{component.instance_name}/{port}")
        # Add board ports
        for port, dests in mhs.assignments.ports.items():
            for dest in dests.split(",", 1)[0].split("&"):
                port_map[dest.strip()].append(port)
        # Print port connections
        print(f"Port connections: ({len(port_map)})")
        for name, ports in port_map.items():
            print(f"- {name}: ({len(ports)})")
            for connection in ports:
                print(f"  - {connection}")
        print()

        # Create map of component interface connections
        interface_map: Dict[str, List[str]] = defaultdict(list)
        # Add component interface connections
        for component in mhs.components.values():
            for interface, dest in component.assignments.bus_interfaces.items():
                interface_map[dest].append(f"{component.instance_name}/{interface}")
        # Print interface connections
        print(f"Interface connections: ({len(interface_map)})")
        for name, interfaces in interface_map.items():
            print(f"- {name}: ({len(interfaces)})")
            for interface in interfaces:
                print(f"  - {interface}")
        print()
