## Intel SGX build configurations

TODO : copied from intel -> to simplify

There are typically two types of build configurations that a non-Intel SGX SW project defines:
Debug and Release. These configurations are both supported for Intel SGX enclaves.
Developers may also want to experiment with a non-production enclave built with release
compilation and linking flags, on a real hardware SGX-enabled platform. This would be an
enclave built exactly as a production enclave, except for the signing process, which would be
Single-step. To support the generation of this kind of enclave, Intel SGX supports a hardware
non-debug build configuration known as Prerelease.
In addition, Intel SGX-enabled projects must support building and testing Intel SGX-enabled
applications on non-Intel SGX platforms (or an emulator) using simulation libraries. This need is
supported by a Simulation mode. Simulation mode can be thought of as an overlay that can be
used with either Debug, Release, or Pre-Release enclaves. In actual practice, however, it is most
often used with Debug enclaves.
