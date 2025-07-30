# CHANGE LOG

### [1.3.3] - 2025-05-26
- Fixed toml file error. Added new create_toml_file method for the Application class.
- Updated minimum required python version
- Updated toml file contents

### [1.3.2] - 2025-05-26
- Fixed base command hinheritance bug

### [1.3.1] - 2025-05-15
- Added documentation for utils.py

## [1.3.0] - 2025-05-15
- Added methods to the RCCNContainer class to directly add parameters
- Added documentation for Application, Service, RCCNCommand and RCCNContainer classes
- Added support for Float datatype Rust generation in Arguments and ParameterEntries

## [1.2.0] - 2025-05-05
- Added argument hints for RCCNCommand, Service and RCCNContainer
- New create_and_add_service() method for the Application
- New create_and_add_command() method for the Service
- Better error messages
- Subtypes of RCCNCommands and RCCNContainers are defined automatically, if not specified by the user
- General refactoring for more readable code
- Added add_integer_parameter method to RCCNContainer
- Bug fixes

### [1.1.2] - 2025-04-23
- The `export_directory` argument for the `Application` is now mandatory.  

### [1.1.1] - 2025-04-22
- Changed the user input checking to allow for multiple command with the same name and subtype, as long as they are associated to different services.

## [1.1.0] - 2025-04-14
- Added derive statements to the rust container structs in the telemetry.rs file.
- Inherit subtype of a container from the `condition` argument, if given, or from the new (optional) `subtype` argument. If only the latter is given, condition is created from that. Subtype is included in the derive statements.
- Added missing `use anyhow::Result` import and bug fixes in `main.rs` file. 
- Added new dependencies in `cargo.toml` file.
- Changed names of command structs to differentiate between trait names and struct names. 
- Include bit number statement in enum declaration.
- The `tc` parameter in the service.rs file is now mutable.
- `System` of a command is obtained from the base command, if no system argument is given.
- Added support for long and short descriptions of commands, arguments and supported telemetry parameters.
- Bug fixes.
