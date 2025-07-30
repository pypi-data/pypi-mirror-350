import re
import inflect
import os
from caseconverter import *
from yamcs.pymdb import IntegerArgument, FloatArgument, BooleanArgument, EnumeratedArgument, StringArgument


def to_upper_camel_case(s):
    """
    Convert a string to UpperCamelCase (PascalCase).
    
    Converts the first letter to uppercase and capitalizes each word 
    after spaces or underscores, removing all non-alphanumeric characters.
    
    Parameters:
    -----------
    s : str
        The input string to convert.
        
    Returns:
    --------
    str
        The converted string in UpperCamelCase.
    """
    if s[0].islower():
        s = s[0].upper() + s[1:]
    if ' ' in s or '_' in s:
        words = re.split(r'[^a-zA-Z0-9]', s)
        return ''.join(word.capitalize() for word in words if word)
    return s

def to_snake_case(s):
    """
    Convert a string to snake_case.
    
    Inserts underscores before uppercase letters, converts the string to lowercase,
    replaces non-alphanumeric characters with underscores, and eliminates consecutive underscores.
    
    Parameters:
    -----------
    s : str
        The input string to convert.
        
    Returns:
    --------
    str
        The converted string in snake_case.
    """
    s = re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()
    s = re.sub(r'[^a-zA-Z0-9_]', '_', s)
    s = re.sub(r'__', '_', s)
    return s

def replace_with_indentation(text, keyword, replacement):
    """
    Replace a keyword in text while preserving the original indentation.
    
    This function finds the indentation level of the line containing the keyword
    and applies the same indentation to each line of the replacement text.
    
    Parameters:
    -----------
    text : str
        The original text containing the keyword.
    keyword : str
        The keyword to replace.
    replacement : str
        The replacement text.
        
    Returns:
    --------
    str
        The text with the keyword replaced by properly indented replacement text.
    """
    lines = text.split('\n')
    indent = 0
    for line in lines:
        if keyword in line:
            indent = len(line) - len(line.lstrip())
    
    return text.replace(keyword, replacement.replace('\n', ('\n'+(indent*' '))))

def insert_before_with_indentation(text, keyword, replacement):
    """
    Insert text before a keyword while preserving the original indentation.
    
    This function finds the indentation level of the line containing the keyword
    and applies the same indentation to each line of the text to be inserted.
    
    Parameters:
    -----------
    text : str
        The original text containing the keyword.
    keyword : str
        The keyword before which to insert text.
    replacement : str
        The text to insert before the keyword.
        
    Returns:
    --------
    str
        The text with the replacement inserted before the keyword with proper indentation.
    """
    lines = text.split('\n')
    indent = 0
    for line in lines:
        if keyword in line:
            indent = len(line) - len(line.lstrip())
    return text.replace(keyword, (replacement.replace('\n', ('\n'+(indent*' ')))+keyword))

def get_keywords(text):
    """
    Extract all keywords from a text.
    
    Keywords are identified as text enclosed between double angle brackets.
    For example: <<KEYWORD>>
    
    Parameters:
    -----------
    text : str
        The text to search for keywords.
        
    Returns:
    --------
    list
        A list of all keywords found in the text.
    """
    pattern = r'<<.*?>>'
    return re.findall(pattern, text)

def get_var_keywords(text):
    """
    Extract variable keywords from a text.
    
    Variable keywords are identified as text starting with <<VAR_ and ending with >>.
    For example: <<VAR_NAME>>
    
    Parameters:
    -----------
    text : str
        The text to search for variable keywords.
        
    Returns:
    --------
    list
        A list of all variable keywords found in the text.
    """
    pattern = r'<<VAR_.*?>>'
    return re.findall(pattern, text)

def get_service_module_keywords(text):
    """
    Extract service module keywords from a text.
    
    Service module keywords are identified as text starting with <<SERVICE_MODULE_ and ending with >>.
    For example: <<SERVICE_MODULE_NAME>>
    
    Parameters:
    -----------
    text : str
        The text to search for service module keywords.
        
    Returns:
    --------
    list
        A list of all service module keywords found in the text.
    """
    pattern = r'<<SERVICE_MODULE_.*?>>'
    return re.findall(pattern, text)

def get_command_module_keywords(text):
    """
    Extract command module keywords from a text.
    
    Command module keywords are identified as text starting with <<COMMAND_MODULE_ and ending with >>.
    For example: <<COMMAND_MODULE_NAME>>
    
    Parameters:
    -----------
    text : str
        The text to search for command module keywords.
        
    Returns:
    --------
    list
        A list of all command module keywords found in the text.
    """
    pattern = r'<<COMMAND_MODULE_.*?>>'
    return re.findall(pattern, text)

def delete_all_keywords(text):
    """
    Remove all keywords from a text.
    
    Finds all text enclosed in double angle brackets and removes them.
    
    Parameters:
    -----------
    text : str
        The text containing keywords to be removed.
        
    Returns:
    --------
    str
        The text with all keywords removed.
    """
    keywords = get_keywords(text)
    for keyword in keywords:
        text = text.replace(keyword, '')
    return text

def delete_all_command_module_keywords(text):
    """
    Remove all command module keywords from a text.
    
    Finds all text starting with <<COMMAND_MODULE_ and enclosed in double angle brackets, 
    then removes them.
    
    Parameters:
    -----------
    text : str
        The text containing command module keywords to be removed.
        
    Returns:
    --------
    str
        The text with all command module keywords removed.
    """
    keywords = get_command_module_keywords(text)
    for keyword in keywords:
        text = text.replace(keyword, '')
    return text

def arg_type_to_rust(arg, bit_number_str='32'):
    """
    Convert a pymdb argument type to its corresponding Rust type.
    
    Maps different argument types from pymdb to their equivalent Rust data types.
    
    Parameters:
    -----------
    arg : object
        A pymdb argument object (IntegerArgument, FloatArgument, etc.)
    bit_number_str : str, optional
        Bit width for numeric types. Default is '32'.
        
    Returns:
    --------
    str
        The corresponding Rust type name, or None if the type is not supported.
    """
    if isinstance(arg, IntegerArgument):
        if arg.signed:
            return 'i'+bit_number_str
        else:
            return 'u'+bit_number_str
    elif isinstance(arg, FloatArgument):
        return 'f'+bit_number_str
    elif isinstance(arg, BooleanArgument):
        return 'bool'
    elif isinstance(arg, EnumeratedArgument):
        return arg.name
    elif isinstance(arg, StringArgument):
        return 'String'
    else:
        print('Argument type is not supported: '+str(type(arg)))
        return None
    
def arg_enum_rust_definition(arg):
    """
    Generate Rust enum definition from an EnumeratedArgument.
    
    Creates a Rust enum definition with all choices from the enumerated argument.
    
    Parameters:
    -----------
    arg : EnumeratedArgument
        The enumerated argument to convert to a Rust enum definition.
        
    Returns:
    --------
    str
        A string containing the complete Rust enum definition.
        
    Raises:
    -------
    ValueError
        If the provided argument is not an EnumeratedArgument.
    """
    if not isinstance(arg, EnumeratedArgument):
        raise ValueError('Provided Argument is not of type EnumeratedArgument.')
    definition_text = 'pub enum '+arg.name+' {\n'
    for choice in arg.choices:
        definition_text += ('\t'+str(choice[1])+' = '+str(choice[0])+',\n')
    definition_text += '}\n'
    return definition_text

def engineering_bit_number(raw_bit_number):
    """
    Calculate an appropriate engineering bit width based on a raw bit width.
    
    Rounds up the raw bit width to the next power of 2, with a minimum of 8 bits.
    
    Parameters:
    -----------
    raw_bit_number : int
        The raw bit width (1-128).
        
    Returns:
    --------
    int
        The calculated engineering bit width (a power of 2, minimum 8).
        
    Raises:
    -------
    ValueError
        If raw_bit_number is not between 1 and 128.
    """
    if raw_bit_number < 1 or raw_bit_number > 128:
        raise ValueError("raw_bit_number must be between 1 and 128")
    power = 1
    while 2**power < raw_bit_number:
        power += 1
    bit_number = 2**power
    if bit_number < 8:
        bit_number = 8
    return (bit_number)

def get_data_type(parent_classes):
    """
    Extract the data type from a list of parent class names.
    
    Searches through a list of class names to find one ending with 'DataType'.
    
    Parameters:
    -----------
    parent_classes : list
        A list of class names to search through.
        
    Returns:
    --------
    str or None
        The name of the class ending with 'DataType', or None if none is found.
    """
    for class_name in parent_classes:
        if class_name.endswith('DataType'):
            return class_name
    return None

def get_base_type(parent_classes):
    """
    Determine the base type from a list of parent class names.
    
    Checks if the parent classes include common base types like Argument, Member,
    Parameter, or DataType.
    
    Parameters:
    -----------
    parent_classes : list
        A list of class names to search through.
        
    Returns:
    --------
    str or None
        The base type name if found, or None if none of the target base types are found.
    """
    for base_type in ["Argument", "Member", "Parameter"]:
        if base_type in parent_classes:
            return base_type
    if "DataType" in parent_classes:
        return "DataType"
    return None

def rust_type_definition(pymdb_data_instance, parent_name="MyStruct"):
    """
    Generate Rust type definition code from a pymdb data instance.
    
    This is the main function for converting pymdb data types to Rust code.
    It analyzes the pymdb instance, determines its data type, and generates
    appropriate Rust code including struct fields and necessary type definitions.
    
    Parameters:
    -----------
    pymdb_data_instance : object
        A pymdb data instance (Parameter, Argument, Member, etc.).
    parent_name : str, optional
        The name of the parent struct, used for inferring unnamed elements. Default is "MyStruct".
        
    Returns:
    --------
    list
        A list with two elements:
        - [0]: The struct field definition including attributes
        - [1]: Any supporting type definitions needed (like enums)
        
    Raises:
    -------
    ValueError
        If the data type cannot be determined or is not supported.
    """
    parent_classes = list(map(lambda type: type.__name__, type(pymdb_data_instance).mro()))
    data_type = get_data_type(parent_classes)
    base_type = get_base_type(parent_classes)
    if base_type is None:
        base_type = pymdb_data_instance.__class__.__name__
    if data_type is None:
        raise ValueError("RCCN-Gen: Data type not found in parent classes.")
    if not hasattr(pymdb_data_instance, 'name') or pymdb_data_instance.name is None:
        p = inflect.engine()
        singular_name = p.singular_noun(parent_name)
        if singular_name is False:
            pymdb_data_instance.name = parent_name
        else:
            pymdb_data_instance.name = singular_name
        print("RCCN-Gen: Information: An unnamed "+base_type+" has been named \""+pascalcase(pymdb_data_instance.name)+"\" in the generated RCCN code.")
    sc_instance_name = snakecase(pymdb_data_instance.name)
    definition_text = ["",""]
    if pymdb_data_instance.short_description is not None:
        definition_text[0] += ("\n\t/// "+str(pymdb_data_instance.short_description)+"\n")
    
    # Handle IntegerDataType
    if data_type == 'IntegerDataType':
        if pymdb_data_instance.encoding is None or pymdb_data_instance.encoding.bits is None:
            raw_bit_number = 8
            print("RCCN-Gen: Warning: No encoding for "+base_type+" "+pymdb_data_instance.name+" found. Using 8 as default for raw bit number.")
        else:
            raw_bit_number = pymdb_data_instance.encoding.bits
        raw_bit_number_str = str(raw_bit_number)
        eng_bit_number = engineering_bit_number(raw_bit_number)
        eng_bit_number_str = str(eng_bit_number)
        definition_text[0] += "\t#[bits("+raw_bit_number_str+")]\n"
        if pymdb_data_instance.signed:
            definition_text[0] += ("\tpub "+sc_instance_name+": i"+eng_bit_number_str+",\n")
        else:
            definition_text[0] += ("\tpub "+sc_instance_name+": u"+eng_bit_number_str+",\n")
    
    # Handle BooleanDataType
    elif data_type == 'BooleanDataType':
        definition_text[0] += ("\t#[bits(1)]\n\tpub "+sc_instance_name+": bool,\n")
    
    # Handle StringDataType
    elif data_type == 'StringDataType':
        definition_text[0] += "\t#[null_terminated]\n\tpub "+sc_instance_name+": String,\n"
    
    # Handle ArrayDataType
    elif data_type == 'ArrayDataType':
        definition_text = rust_type_definition(pymdb_data_instance.data_type, parent_name=pymdb_data_instance.name)
        definition_text[0] = definition_text[0].replace(': ', ': Vec<').replace(',\n', '>,\n')
        if pymdb_data_instance.short_description is not None:
            definition_text[0] = "\n\t/// "+pymdb_data_instance.short_description+"\n"+definition_text[0]
        if pymdb_data_instance.long_description is not None:
            definition_text[1] = "/// "+pymdb_data_instance.long_description+"\n" + definition_text[1]
    
    # Handle EnumeratedDataType
    elif data_type == 'EnumeratedDataType':
        definition_text[0] += "\t#[bits("+str(pymdb_data_instance.encoding.bits)+")]\n"
        definition_text[0] += "\tpub "+pymdb_data_instance.name+": "+pascalcase(pymdb_data_instance.name)+",\n"
        definition_text[1] += ("#[derive(FromPrimative, ToPrimative, Debug)]\npub enum "+pascalcase(pymdb_data_instance.name)+" {\n")
        for choice in pymdb_data_instance.choices:
            definition_text[1] += "\t"+str(choice[1])+" = "+str(choice[0])+",\n"
        definition_text[1] += "}\n\n"
        if pymdb_data_instance.long_description is not None:
            definition_text[1] = "/// "+pymdb_data_instance.long_description+"\n" + definition_text[1]
    
    # Handle AggregateDataType
    elif data_type == 'AggregateDataType':
        struct_name = pascalcase(pymdb_data_instance.name)
        definition_text[0] += "\tpub "+sc_instance_name+": "+struct_name+",\n"
        if pymdb_data_instance.long_description is not None:
            definition_text[1] += "\t/// "+pymdb_data_instance.long_description+"\n"
        definition_text[1] += ("#[derive(FromPrimative, ToPrimative, Debug)]\n")
        definition_text[1] += ("pub struct "+struct_name+" {\n")
        insert, append = ["",""]
        for member in pymdb_data_instance.members:
            mem_def = rust_type_definition(member, parent_name=pymdb_data_instance.name)
            insert += mem_def[0]
            append += mem_def[1]
        definition_text[1] += insert
        definition_text[1] += "}\n\n"
        definition_text[1] += append
    
    # Handle FloatDataType
    elif data_type == 'FloatDataType':
        if pymdb_data_instance.encoding is None or pymdb_data_instance.encoding.bits is None:
            raw_bit_number = 32
            print("RCCN-Warning: No encoding for "+base_type+" "+pymdb_data_instance.name+" found. Using 32 as default for raw bit number.")
        else:
            raw_bit_number = pymdb_data_instance.encoding.bits
        raw_bit_number_str = str(raw_bit_number)
        if raw_bit_number == 32:
            eng_bit_number = 32
        elif raw_bit_number == 64:
            eng_bit_number = 64
        else:
            print("RCCN-Warning: Given raw bit number for "+base_type+" \'"+pymdb_data_instance.name+"\' is not equal to 32 or 64. A engineering bit number of 64 will be used.")
            eng_bit_number = 64
        eng_bit_number_str = str(eng_bit_number)
        definition_text[0] += "\t#[bits("+raw_bit_number_str+")]\n"
        definition_text[0] += ("\tpub "+sc_instance_name+": f"+eng_bit_number_str+",\n")
    
    # Handle unsupported data types
    else:
        definition_text = ["\t// Please implement datatype "+data_type+" here.\n", ""]
    
    return definition_text