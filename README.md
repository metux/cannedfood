# CannedFood - CAN message modeling and code generator

CannedFood is a tool for modeling CAN messages, payloads and nodes via simple
yaml files and autogenerating the encoding, decoding and multiplexing logic.

The C generator creates several header and source files for:

* global enum with all message CAN-Ids
* per-node enums with only the CAN-Ids of messages supported by the node
  (using different per-node symbol prefixes), eg. to prevent accential
  usage of IDs that aren't supposed to be used according to the model
  per-node receive demultiplexer - calls per-message handlers with the
  unpacked payload values as parameters (these have to be implemented
  by the developer)
* message encoder inline functions that pack the payload from parameters

### Prerequisites

Python2 (Python3 should also work) and python-yaml

## Getting Started

See examples/ directory.

The Makefile calls the generator and compiles a trivial example.

## 2DO

* messsage scopes to better differenciate overlapping can-id's on disjunct busses.
- automatic unit conversion (eg. conversion and scaling from/to native types)
- autogen: bridge for selectively connecting busses (eg. in C or BPF)
- autogen: acyclic status variable xmit (eg. via timers or threads)
- autogen: instrumentation tools (eg. check for cyclic messages)
- autogen: local variable update on received messages
- bus load / timing calculation
- priority vs. canid checks (eg. check whether higher prio messages have
  lower canid)
- can to 9p bridging

## Authors

* **Enrico Weigelt, metux IT consult** - info@metux.net - +49-151-27565287 - [metux](https://github.com/metux)

See also the list of [contributors](https://github.com/metux/cannedfood/contributors) who participated in this project.

## License

This project is licensed under the AGPLv3 - see: https://www.gnu.org/licenses/agpl-3.0.txt
