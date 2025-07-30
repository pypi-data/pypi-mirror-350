## apollo keyboard controller

This is a simple keyboard controller for the Apollo. It allows you to send control command according to your key operation.

### Requirements

- Apollo runtime(`cyber`, `canbus` and `common_msgs`), you should run it in the `apollo` docker container.
- locale set to `C.UTF-8` (or `en_US.UTF-8`)

### Installation

```bash
pip3 install akbc
```

### Usage

```bash
akbc --dbc_file <path_of_dbc_file> --device <can0>
```
