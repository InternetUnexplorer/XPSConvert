# XPSConvert

This code is part of a tool I was working on to convert projects from Xilinx
Platform Studio (XPS) to Vivado. The tool is no longer needed, but I'm
publishing some of the finished parts in case someone finds them useful.

The project went through several iterations as I learned more about the
software. The final design was fairly simple, and mostly relied on Vivado's
ability to automatically upgrade IP (although clocking and AXI-related stuff
required some intervention).

### Using the Demo

A small demo is included which reads the MHS and XMP files in a XPS project and
prints some information about them. It should serve as a good starting point for
manipulating the data structures returned by `parse_mhs` and `parse_xps`.

As an example, to read and print information about an XPS project located in the
directory `~/Desktop/Project/`, you would run:
```sh
$ python -m xps_convert ~/Desktop/Project/
```

### Helpful Documentation

Aside from looking at a lot of `.mhs` and `.bd` files, here is some
documentation that I found helpful:

- [ISE to Vivado Design Suite Migration Guide (UG911)][1]
- [Platform Specification Format Reference Manual (UG642)][2]
- [Xilinx LogiCORE IP AXI Interconnect (v1.06.a) (DS768)][3]

[1]: https://www.xilinx.com/support/documentation/sw_manuals/xilinx2014_1/ug911-vivado-migration.pdf
[2]: https://www.xilinx.com/support/documentation/sw_manuals/xilinx14_7/psf_rm.pdf
[3]: https://www.xilinx.com/support/documentation/ip_documentation/axi_interconnect/v1_06_a/ds768_axi_interconnect.pdf
