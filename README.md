# massmesh ./build usage

### Build a meshnode profile for espressobin
`./build massmesh meshnode globalscale_espressobin`

### Build a for a wireless meshradio for nanostation 
`./build massmesh meshradio ns5ac-loco`

### Examples
```
% ./build massmesh
Please specify a build profile:
- meshnode
- meshradio

% ./build massmesh meshradio
[./build] Please specify a device:
- ubnt_nanostation-ac-loco
- ubnt_unifiac-mesh

% ./build massmesh meshradio ubnt_unifiac-mesh
....building!

% ./build massmesh meshnode
[./build] Please specify a device:
- apu2
- globalscale_espressobin
- rpi-4

% ./build massmesh meshnode rpi-4
....building!

```

# meta ImageBuilder (Called by ./build)

Instead of downloading (and updating) ImageBuilders manually, this script does
all the work. Automatically download ImageBuilder and create desired image.
Extra variables like `$PACKAGES` are forwarded to the ImageBuilder make call.

## Usage

Build `ar71xx/generic/tl-wr710n-v2.1` with latest (17.01.4) release:

    PROFILE="tl-wr710n-v2.1" TARGET="ar71xx" SUBTARGET="generic" ./meta

Build latest snapshot of the same target/profile combo (both work):

    PROFILE="tl-wr710n-v2.1" RELEASE=snapshots TARGET="ar71xx" SUBTARGET="generic" ./meta

### Custom repositories

To support other distributions like LibreMesh which is based on OpenWrt but
which use additional repositories, it is possible to replace the
`repositories.conf` with a custom version.

The massmesh packages repository (http://downloads.massmesh.net) is already
included automatically.

You may setup extra repositories exporting the `REPOS` variable. Example:

    export REPOS="""src/gz libremesh http://repo.libremesh.org/releases/{{ version }}/packages/{{ pkg_arch }}/libremesh
    src/gz libremap http://repo.libremesh.org/releases/{{ version }}/packages/{{ pkg_arch }}/libremap
    src/gz limeui http://repo.libremesh.org/releases/{{ version }}/packages/{{ pkg_arch }}/limeui
    src/gz lm_routing http://repo.libremesh.org/releases/{{ version }}/packages/{{ pkg_arch }}/routing
    src/gz lm_profiles http://repo.libremesh.org/network-profiles/"""

The following variables are automatically replaced:

* `{{ version }}` Custom version
* `{{ ib_version }}` OpenWrt ImageBuilder version
* `{{ pkg_arch }}` Automatically determined package architecture
* `{{ target }}`
* `{{ subtarget }}`
