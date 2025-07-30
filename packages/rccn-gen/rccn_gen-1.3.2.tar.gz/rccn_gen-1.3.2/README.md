# RCCN Code Generator
This generator is used to generate Rust files to deploy on the RACCOON OS satellite based on the pymdb config files used to generate the ground station XTCE files.

To see whats new, see the [CHANGELOG](CHANGELOG.md).
## Setup
- Set up a virtual python environment with `python3` and activate:
    ```zsh
    python -m venv .venv
    source .venv/bin/activate
    ```
- Install with `pip install rccn-gen`

## Using the Generator
The generator is based on [`pymdb`](https://github.com/yamcs/pymdb) and uses the same structure. Where `pymdb` gives the user freedom in defining systems, subsystems and their respective relations, the definitions for rust code generation is more restricted. For the rust generation, the user is bound to the following classes:
- `Application`,
- `Service`,
- `RCCNCommand`, and
- `RCCNContainer`.

The Application and Service classes inherit from pymdb's Subsystem class and extend their functionality. The RCCNCommand extends the Command class and the RCCNContainer extends the Container class of pymdb. This means that an existing pymdb definition can be used to generate rust code by renaming the respective instances. No functionality for pymdb's XTCE generation will be lost. 

A root system may be defined for the satellite.
```python
root_system = System("Satellite")
```

### Application
An application can be defined with the following statement.
```python
app = Application(system=root_system, name="ExampleApp", apid=42)
```
It has the obligatory arguments **system**, **name** and **apid**. After all Applications, Services and RCCNCommands are defined, the rust code generator can be called on the application with `app.generate_rccn_code(export_directory='.')`.

### Service

A service may be defined with the following command.
```python
service = Service(name="ExampleService", system=app, service_id = 131)
```
Or like this:
```python
service = Service(name="ExampleService", service_id = 131)
app.add_service(service)
```

It has the obligatory arguments **name** and **system**. The system corresponds to the application where the service is associated to. Note that each service has one associated app. A service cannot be associated to more than one app. You may think of the Application-Service-Command structure as a mathematical tree, where merging branches are not allowed. However, you can create multiple instances of the same service and associate them to different applications, or create multiple identical command instances and associate them to different services. 

### RCCNCommand
An RCCNCommand can be defined with the following statement.
```python
RCCNCommand(
    system=service,
    assignments={"subtype": 2},
    name="StopProcess",
    arguments=[StringArgument("name", encoding=StringEncoding())],
)
```

Or like this:
```python
my_command = RCCNCommand(
    assignments={"subtype": 2},
    name="StopProcess",
    arguments=[StringArgument("name", encoding=StringEncoding())],
)
service.add_command(my_command)
```

The only obligatory argument is **name**. If the subtype assignment is not given, a value will be chosen automatically. The connection to a service can also be achieved with base commands, where every base command must be unique to a service. For example:

```python
base_cmd = RCCNCommand(
    system=service,
    assignments={"type": service.service_id},
    name="base",
    base="/PUS/pus-tc"
)
my_command = RCCNCommand(
    base=base_cmd,
    assignments={"subtype": 2},
    name="StopProcess",
    arguments=[StringArgument("name", encoding=StringEncoding())],
)
```

### RCCNContainer
A container to hold telemetry information can be created with:
```python
my_container = RCCNContainer(
    system=service,
    name='BatteryInformation',
    short_description='This container holds information on battery voltage and current'
)
my_container.add_integer_parameter_entry(
    name='BatteryNumber',
    minimum=1,
    maximum=4,
    encoding=IntegerEncoding(bits=3),
    short_description='Number of the battery'
)
my_container.add_float_parameter_entry(
    name='Current',
    units='Ampere',
    encoding=FloatEncoding(bits=32),
    short_description='Electric current of the battery.'
)
my_container.add_float_parameter_entry(
    name='Voltage',
    units='Volts',
    encoding=FloatEncoding(bits=32),
    short_description='Electric voltage of the battery.'
)
```
## Output
From the python configuration, the `main.rs`, `service.rs`, `command.rs`, `mod.rs`, `Cargo.toml` and `telemetry.rs` files are generated and are structured accordingly:
- rccn_usr_example_app/
    - Cargo.toml
    - src/
        - main.rs
        - example_service/
            - command.rs
            - service.rs
            - mod.rs
            - telemetry.rs

The `Cargo.toml` and `mod.rs` files are generated only if the files don't exist already, as their content doesn't depend on the pymdb config. No user changes will be overwritten. The command and service files are created for each service in the application. 

## How It Works
The code is generated from templates in the `text_modules` folder. Base templates define the structure for all generated files, respectively. In the templates, two types of keywords can be found and are indicated by `<<KEYWORD>>` encapsulation. 

Keywords beginning with `VAR_` point to a value in the python config created by the user, as shown above. Examples for this are the application identifier (APID) with `<<VAR_APID>>` or the service name with `<<VAR_SERVICE_NAME_UCASE>>`. 

Keywords beginning with `SERVICE_MODULE` or `COMMAND_MODULE` point to other template files in the same folder. The prefix `SERVICE` or `COMMAND` indicates, that this module should be inserted once for every service in the application or once for every command in the service. In this way, the structure of the generated code can be segmented, organized and restructured without any need to change the code generator itself. 

The keyword `<<SERVICE_MODULE_REGISTER_SERVICE>>` for example can be found in the main template and inserts the contents from the `service_module_register_service.txt` file for every service:

```rust
let service<<VAR_SERVICE_ID>> = <<VAR_SERVICE_NAME_UCASE>>::new();
app.register_service(service<<VAR_SERVICE_ID>>);
```

The variable keywords are replaced with the corresponding values in the python configuration. 

## Editing Generated Files
The code generator allows for the user to make changes to the generated .rs files directly and to keep those changes if the files are regenerated. For this purpose, snapshots of the .rs files are taken, .diff files are created and user changes are rebased to regenerated .rs files. If this behaviour is not desired, it can be turned off with the commands showed below.

```python
app.generate_rccn_code(rebase_changes=False) # Turn off rebaseing of user changes to newly generated .rs files
app.generate_rccn_code(snapshots=False, rebase_changes=False) # Turn of rebaseing and snapshot creation 
```

Please note that switching off rebasing and snapshot creation means that **existing files will be overwritten** and all changes made prior will be lost. 

### Sequence in File Generation
With the snapshot and rebase functionality enabled, the following steps are run through during the generation of every file. For this example it is assumed that the file that is about to be generated already exists in the export directory from a previous generation and user changes where made to the generated file since then. 

1. If a snapshot exists in `.rccn_snapshots/generated/`, a diff file containing the changes from the snapshot to the file as it exists in the export directory is created.
2. The current file in the export directory is copied to `.rccn_snapshots/user/`. A subfolder indicates the time of creation.
3. The new .rs file is generated based on the pymdb config and exported to the export directory, overwriting the existing file.
4. The new .rs file is copied to `.rccn_snapshots/generated/` for future use.
5. The new .rs file is patched using the diff file from step 1.

The sequence from above is changed accordingly if no previous snapshot exists. In the `/generated/` folder, there is only one snapshot per application at one time. And this snapshot always represents the .rs file as it is generated. No user changes to the .rs files are tracked in this snapshot. It is only used to determine the user changes to the .rs file in the export directory since the generation.

Snapshots of the .rs files in the export directory are stored in `/user/`. These can be used to undo code regeneration if conflicts arise during the patching. Please note that by default, only the last 10 user snapshots are stored. You can change this property with the following command.

```python
app.keep_snapshots = 15 # Whatever value you want
```

With the sequence from above, it becomes apperant that changes to the .rs file in the export directory always trump changes to the pymdb config. If for example, a main.rs file is generated for an application with and APID of 42, and this apid is changed in the main.rs file to 45, this change will persist after regenerating from the python config. Even if changes to the pymdb config where made after the changes to the main.rs file. 
