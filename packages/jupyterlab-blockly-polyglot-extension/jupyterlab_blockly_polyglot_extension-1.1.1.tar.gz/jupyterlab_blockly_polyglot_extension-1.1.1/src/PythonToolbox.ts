import { AbstractToolbox, IntellisenseEntry, IToolbox } from "./AbstractToolbox";
import { INotebookTracker } from "@jupyterlab/notebook";
import * as Blockly from 'blockly/core';
import { Order, pythonGenerator } from 'blockly/python';
// Import the default blocks. We just need to load them here (side effect). Ignore usage check.
import * as libraryBlocks from 'blockly/blocks';
// Import English message file (determines language of blocks)
import * as en from 'blockly/msg/en';

export class PythonToolbox extends AbstractToolbox implements IToolbox {
    /**
     * Terrible hack for importing libraries
     */
    temp = "";

    generator = pythonGenerator;

    toolboxDefinition = {
        "kind": "categoryToolbox",
        "contents": [
            {
                "kind": "CATEGORY",
                // OLD: we now have a dynamic flyout similar to VARIABLE
                // "contents": [
                //     {
                //         "kind": "BLOCK",
                //         "type": "importAs"
                //     },
                //     {
                //         "kind": "BLOCK",
                //         "type": "importFrom"
                //     }
                // ],
                "name": "IMPORT",
                "colour": "255",
                "custom": "IMPORT"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "dummyOutputCodeBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "dummyNoOutputCodeBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "valueOutputCodeBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "valueNoOutputCodeBlock"
                    }
                ],
                "name": "FREESTYLE",
                "colour": "290"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "dummyOutputCommentBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "dummyNoOutputCommentBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "valueOutputCommentBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "valueNoOutputCommentBlock"
                    }
                ],
                "name": "COMMENT",
                "colour": "20"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "controls_if"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_compare"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_operation"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_negate"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_boolean"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_null"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "logic_ternary"
                    }
                ],
                "name": "LOGIC",
                "colour": "260"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "controls_repeat_ext"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "controls_whileUntil"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "controls_for"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "comprehensionForEach"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "controls_forEach"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "controls_flow_statements"
                    }
                ],
                "name": "LOOPS",
                "colour": "120"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "math_number"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_arithmetic"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_single"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_trig"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_constant"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_number_property"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_round"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_on_list"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_modulo"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_constrain"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_random_int"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_random_float"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "math_atan2"
                    }
                ],
                "name": "MATH",
                "colour": "230"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "text"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_join"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_append"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_length"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_isEmpty"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_indexOf"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_charAt"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_getSubstring"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_changeCase"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_trim"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_print"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "text_prompt_ext"
                    }
                ],
                "name": "TEXT",
                "colour": "160"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "lists_create_with"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_repeat"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_length"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_isEmpty"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_indexOf"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_getIndex"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_setIndex"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_getSublist"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "indexer"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_split"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "lists_sort"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "setBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "sortedBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "zipBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "dictBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "listBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "tupleBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "tupleConstructorBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "reversedBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "selector_train_test_split"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "train_test_split"
                    }
                ],
                "name": "LISTS",
                "colour": "260"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "boolConversion"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "intConversion"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "floatConversion"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "strConversion"
                    }
                ],
                "name": "CONVERSION",
                "colour": "120"
            },
            {
                "kind": "CATEGORY",
                "contents": [
                    {
                        "kind": "BLOCK",
                        "type": "withAs"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "textFromFile"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "openReadFile"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "openWriteFile"
                    }
                ],
                "name": "I/O",
                "colour": "190"
            },
            {
                "kind": "SEP"
            },
            {
                "kind": "CATEGORY",
                "name": "VARIABLES",
                "colour": "330",
                "custom": "VARIABLE"
            },
            {
                "kind": "CATEGORY",
                "name": "FUNCTIONS",
                "colour": "290",
                "custom": "PROCEDURE"
            },
            // search box: https://google.github.io/blockly-samples/plugins/toolbox-search/README
            {
                'kind': 'search',
                'name': 'Search',
                'contents': [],
            }
        ],
    };

    constructor(notebooks: INotebookTracker, workspace: Blockly.WorkspaceSvg) {
        super(notebooks, workspace);
    }

    // We match against docstrings to determine type, cf. https://github.com/rr-/docstring_parser/blob/master/docstring_parser/epydoc.pyhttps://github.com/rr-/docstring_parser/blob/master/docstring_parser/epydoc.py
    // This is a moving target absent standardization, so if intelliblocks are not 
    // correctly sorting types, this is the first place to check
    // May 2025:
    // Pandas:
    // Use IndexSlice as canonical property: 'Type:'
    // array and concat as canonical functions: 'Signature:' and 'Type:     function'
    // ArrowDType as canonical class: 'signature:' and 'Type:     type'
    // Numpy:
    // Use int16 as canoncial class: 'signature:' and 'Type:     type'
    // Use abs as canonical function: 'signature:' and 'Type:     ufunc'
    // asarray and array both have 'Type:     ufunc' but no signature, so remove signature requirement


    function_regex = /\btype:[^\n]*(func|method)/i;
    isFunction(query: string, info: string): boolean {
        // let debug = this.function_regex.test(info);
        // debug.valueOf();
        // functions have function type; we ignore signature/method/parameter matches because numpy seems to skip these in some cases
        return this.function_regex.test(info); 
        // old metho
        // return (info.includes("Signature:") && info.includes("function")) || (info.includes("Signature:") && info.includes("method"));
    }

    isProperty(query: string, info: string): boolean {
        // properties won't have examples of use with parameters
        return !info.includes("." + query + "(");
        // properties don't have parameters or a signature -- fails for loaded dataframe cols, whose infos are Series (class) plus annotation
        // !info.includes("Parameters") && !info.includes("ignature:");
    }

    class_regex = /\btype:[^\n]*type/i;
    isClass(info: string): boolean {
        // let debug = this.class_regex.test(info);
        // debug.valueOf();
        // constructors have signatures but are not functions
        return info.includes("ignature:") && !this.function_regex.test(info);  
        // old method
        // return info.includes("signature:") && info.includes("class");
    }

    dotString(): string {
        return "."
    }

    GetSafeChildCompletions(parent: IntellisenseEntry, children: string[]): string[] {
        let safeCompletions: string[] = children.filter((s: string) => {
            if (parent.Info.startsWith("Signature: DataFrame")) {
                return !(s.startsWith("_")) && !(s.startsWith("style"));
            }
            return true;
        });
        return safeCompletions;

    }

    GetChildrenInspections(parent: IntellisenseEntry, children: string[]): Promise<string>[] {
        // See R toolbox for example of dynamic waiting for completion
        // For Python we don't currently seem to have a problem with promises not returning
        const pr: Promise<string>[] = children.map((childCompletion: string, index: number) => this.GetKernelInspection(parent.Name + "." + childCompletion));
        return pr;
    }

    GetCleanChildName(childCompletion: string) {
        return childCompletion;
    }

    /**
     * A template to create arbitrary code blocks (FREESTYLE) in these dimensions: dummy/input; output/nooutput
     * @param blockName 
     * @param hasInput 
     * @param hasOutput 
     * @param generator 
     */
    makeCodeBlock(blockName: string, hasInput: boolean, hasOutput: boolean): void {
        Blockly.Blocks[blockName] = {
            init: function () {
                const input: Blockly.Input = hasInput ? this.appendValueInput("INPUT").setCheck(null) : this.appendDummyInput();
                console.log(blockName + " init");
                input.appendField(new Blockly.FieldTextInput("type code here...") as Blockly.Field, "CODE");
                if (hasOutput) {
                    this.setOutput(true, null);
                }
                else {
                    this.setNextStatement(true);
                    this.setPreviousStatement(true);
                }
                this.setColour(230);
                this.setTooltip(((("You can put any Python code in this block. Use this block if you " + (hasInput ? "do" : "don\'t")) + " need to connect an input block and ") + (hasOutput ? "do" : "don\'t")) + " need to connect an output block.");
                this.setHelpUrl("https://docs.python.org/3/");
            },
        };
        pythonGenerator.forBlock[blockName] = ((block: Blockly.Block, generator): [string, number] | string => {
            const userCode: string = block.getFieldValue("CODE").toString();
            let code: string;
            if (hasInput) {
                const input_1: string = generator.valueToCode(block, "INPUT", Order.ATOMIC);
                code = ((userCode + " ") + input_1).trim();
            }
            else {
                code = userCode.trim();
            }
            return hasOutput ? [code, Order.ATOMIC] : code + "\n";
        });
    }

    /**
     * A template to create arbitrary COMMENT blocks in these dimensions: dummy/input; output/nooutput
     * @param blockName 
     * @param hasInput 
     * @param hasOutput 
     * @param generator 
     */
    makeCommentBlock(blockName: string, hasInput: boolean, hasOutput: boolean): void {
        Blockly.Blocks[blockName] = {
            init: function () {
                const input: Blockly.Input = hasInput ? this.appendValueInput("INPUT").setCheck(null) : this.appendDummyInput();
                console.log(blockName + " init");
                input.appendField("# ").appendField(new Blockly.FieldTextInput("type comment here...") as Blockly.Field, "COMMENT");
                if (hasOutput) {
                    this.setOutput(true, null);
                }
                else {
                    this.setNextStatement(true);
                    this.setPreviousStatement(true);
                }
                this.setColour(230);
                this.setTooltip(((("You can put any text comment in this block. Use this block if you " + (hasInput ? "do" : "don\'t")) + " need to connect an input block and ") + (hasOutput ? "do" : "don\'t")) + " need to connect an output block.");
                this.setHelpUrl("https://docs.python.org/3/");
            },
        };
        pythonGenerator.forBlock[blockName] = ((block: Blockly.Block, generator): [string, number] | string => {
            const userCode: string = block.getFieldValue("COMMENT").toString();
            let code: string;
            if (hasInput) {
                const input_1: string = generator.valueToCode(block, "INPUT", Order.ATOMIC);
                code = (("# " + userCode + " ") + input_1).trim();
            }
            else {
                code = "# " + userCode.trim();
            }
            return hasOutput ? [code, Order.ATOMIC] : (code + "\n");
        });
    }

    /**
     * Create a Blockly/Python templated import block
     */
    makeImportBlock(blockName: string, labelOne: string, labelTwo: string): void {
        Blockly.Blocks[blockName] = {
            init: function () {
                this.appendDummyInput().appendField(labelOne).appendField(new Blockly.FieldTextInput("some library") as Blockly.Field, "libraryName").appendField(labelTwo).appendField(new Blockly.FieldVariable("<select>") as Blockly.Field, "VAR");
                this.setNextStatement(true);
                this.setPreviousStatement(true);
                this.setColour(230);
                this.setTooltip("Import a python package to access functions in that package");
                this.setHelpUrl("https://docs.python.org/3/reference/import.html");
            },
        };
        pythonGenerator.forBlock[blockName] = ((block: Blockly.Block, generator): string => {
            let libraryName = block.getFieldValue("libraryName");
            let libraryAlias = generator.getVariableName(block.getFieldValue("VAR"));
            let code = labelOne + " " + libraryName + " " + labelTwo + " " + libraryAlias + "\n";
            return code;
        });
    }


    /**
     * A template for variable argument function block creation (where arguments are in a list), including the code generator.
     * @param blockName 
     * @param label 
     * @param outputType 
     * @param tooltip 
     * @param helpurl 
     * @param functionStr 
     */
    makeFunctionBlock(blockName: string, label: string, outputType: string, tooltip: string, helpurl: string, functionStr: string): void {
        Blockly.Blocks[blockName] = {
            init: function () {
                console.log(blockName + " init");
                this.appendValueInput("x").setCheck(null).appendField(label);
                this.setInputsInline(true);
                this.setOutput(true, outputType);
                this.setColour(230);
                this.setTooltip(tooltip);
                this.setHelpUrl(helpurl);
            },
        };
        pythonGenerator.forBlock[blockName] = ((block: Blockly.Block, generator): [string, number] | string => {
            let args: string = generator.valueToCode(block, "x", Order.MEMBER);
            let cleanArgs = args.replace(/^\\[|\\]$/g, "");
            let code = functionStr + "(" + cleanArgs + ")";
            return [code, Order.FUNCTION_CALL];
        });
    }

    InitializeGenerator(): void {

        // Blockly.Blocks is empty at this point
        // We have to do a no-op with libraryBlocks for them to attach to Blockly.Blocks (side effect)
        if (libraryBlocks) { } //you're not supposed to understand this :)

        // Set blocks language to English; override the type error
        // @ts-ignore
        Blockly.setLocale(en);

        //-------------------------------------
        //override default blockly functionality
        //-------------------------------------
        // We use @ts-ignore to override the protected class attributes we need to modify; an alternative would be to extend pythonGenerator and then do these overrides within that new class

        pythonGenerator.finish = ((code: string): string => {
            const imports: string[] = [];
            const functions: string[] = [];
            // @ts-ignore
            let enumerator: any = Object.keys(pythonGenerator.definitions_);
            for (let i in enumerator) {
                // @ts-ignore
                const definitions: any = pythonGenerator.definitions_;
                const def: string = definitions[enumerator[i]];
                if (def.indexOf("import") >= 0) {
                    void (imports.push(def));
                }
                if ((def.indexOf("def ") === 0) ? true : (def.indexOf("# ") === 0)) {
                    void (functions.push(def));
                }
            }
            // @ts-ignore
            delete pythonGenerator.definitions_;
            // @ts-ignore
            delete pythonGenerator.functionNames_;
            // @ts-ignore
            pythonGenerator.nameDB_.reset();
            return ((("\n" + imports) + ("\n" + functions)) + "\n\n") + code;
        });

        //-----------------
        //define new blocks
        //-----------------
        //we combine elements of the old API with current guidelines, see https://developers.google.com/blockly/guides/configure/web/custom-blocks
        //notably we define on Blockly.Blocks directly rather than using Blockly.common.defineBlocks

        Blockly.Blocks["comprehensionForEach"] = {
            init: function () {
                console.log("comprehensionForEach init");
                this.appendValueInput("LIST").setCheck(null).appendField("for each item").appendField(new Blockly.FieldVariable("i") as Blockly.Field, "VAR").appendField("in list");
                this.appendValueInput("YIELD").setCheck(null).setAlign(Blockly.inputs.Align.RIGHT).appendField("yield");
                this.setOutput(true, null);
                this.setColour(230);
                this.setTooltip("Use this to generate a sequence of elements, also known as a comprehension. Often used for list comprehensions.");
                this.setHelpUrl("https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions");
            },
        };
        pythonGenerator.forBlock['comprehensionForEach'] = ((block: Blockly.Block, generator): [string, number] => {
            const var$: string = generator.getVariableName(block.getFieldValue("VAR"))
            const list: string = generator.valueToCode(block, "LIST", Order.ATOMIC);
            const yieldValue: string = generator.valueToCode(block, "YIELD", Order.ATOMIC);
            const code = yieldValue + " for " + var$ + " in " + list;
            return [code, Order.ATOMIC];
        })


        Blockly.Blocks["withAs"] = {
            init: function () {
                console.log("withAs init");
                this.appendValueInput("EXPRESSION").setCheck(null).appendField("with");
                this.appendDummyInput().appendField("as").appendField(new Blockly.FieldVariable("item") as Blockly.Field, "TARGET");
                this.appendStatementInput("SUITE").setCheck(null);
                this.setNextStatement(true);
                this.setPreviousStatement(true);
                // const value_3: any = this.setInputsInline(true);
                this.setColour(230);
                this.setTooltip("Use this to open resources (usually file-type) in a way that automatically handles errors and disposes of them when done. May not be supported by all libraries.");
                this.setHelpUrl("https://docs.python.org/3/reference/compound_stmts.html#with");
            },
        };
        pythonGenerator.forBlock["withAs"] = ((block: Blockly.Block, generator): string => {
            let copyOfStruct: any = (generator.statementToCode(block, "SUITE"));
            let expression: string = generator.valueToCode(block, "EXPRESSION", Order.ATOMIC);
            let target: string = generator.getVariableName(block.getFieldValue("TARGET"));
            let code = ("with " + expression + " as " + target + ":\n" + copyOfStruct.toString());
            return code
        });


        Blockly.Blocks["textFromFile"] = {
            init: function () {
                console.log("textFromFile init");
                this.appendValueInput("FILENAME").setCheck("String").appendField("read text from file");
                this.setOutput(true, null);
                this.setColour(230);
                this.setTooltip("Use this to read a text file. It will output a string.");
                this.setHelpUrl("https://docs.python.org/3/tutorial/inputoutput.html");
            },
        };
        pythonGenerator.forBlock["textFromFile"] = ((block: Blockly.Block, generator): [string, number] => {
            let fileName = generator.valueToCode(block, "FILENAME", Order.ATOMIC);
            let code = "open(" + fileName + ",encoding=\'utf-8\').read()";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["openReadFile"] = {
            init: function () {
                console.log("openReadFile init");
                this.appendValueInput("FILENAME").setCheck("String").appendField("open file for reading");
                this.setOutput(true, null);
                this.setColour(230);
                this.setTooltip("Use this to read a file. It will output a file, not a string.");
                this.setHelpUrl("https://docs.python.org/3/tutorial/inputoutput.html");
            },
        };
        pythonGenerator.forBlock["openReadFile"] = ((block: Blockly.Block, generator): [string, number] => {
            let filename = generator.valueToCode(block, "FILENAME", Order.ATOMIC);
            let code = "open(" + filename + ",encoding=\'utf-8\')";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["openWriteFile"] = {
            init: function () {
                console.log("openWriteFile init");
                this.appendValueInput("FILENAME").setCheck("String").appendField("open file for writing");
                this.setOutput(true, null);
                this.setColour(230);
                this.setTooltip("Use this to write to a file. It will output a file, not a string.");
                this.setHelpUrl("https://docs.python.org/3/tutorial/inputoutput.html");
            },
        };
        pythonGenerator.forBlock["openWriteFile"] = ((block: Blockly.Block, generator): [string, number] => {
            let filename = generator.valueToCode(block, "FILENAME", Order.ATOMIC);
            let code = "open(" + filename + ",\'w\',encoding=\'utf-8\')";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["indexer"] = {
            init: function () {
                this.appendValueInput("INDEX").appendField(new Blockly.FieldVariable("{dictVariable}") as Blockly.Field, "VAR").appendField("[");
                this.appendDummyInput().appendField("]");
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour(230);
                this.setTooltip("Gets an item from the variable at a given index. Not supported for all variables.");
                this.setHelpUrl("https://docs.python.org/3/reference/datamodel.html#object.__getitem__");
            },
        };
        pythonGenerator.forBlock["indexer"] = ((block: Blockly.Block, generator): [string, number] => {
            let varName = generator.getVariableName(block.getFieldValue("VAR"));
            let input = generator.valueToCode(block, "INDEX", Order.ATOMIC);
            let code = varName + "[" + input + "]";
            return [code, Order.ATOMIC];
        });

        Blockly.Blocks["tupleBlock"] = {
            init: function () {
                this.appendValueInput("FIRST").setCheck(null).appendField("(");
                this.appendValueInput("SECOND").setCheck(null).appendField(",");
                this.appendDummyInput().appendField(")");
                this.setInputsInline(true);
                this.setOutput(true, null);
                this.setColour(230);
                this.setTooltip("Use this to create a two-element tuple");
                this.setHelpUrl("https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences");
            },
        };
        pythonGenerator.forBlock["tupleBlock"] = ((block: Blockly.Block, generator): [string, number] => {
            let firstArg = generator.valueToCode(block, "FIRST", Order.ATOMIC);
            let secondArg = generator.valueToCode(block, "SECOND", Order.ATOMIC);
            let code = "(" + firstArg + "," + secondArg + ")";
            return [code, Order.NONE];
        });

        // TODO: copy the SPECIAL category from the R extension so package-specific blocks like those below only appear when the package is loaded
        /**
         * Block for splitting a DataFrame into training and testing datasets.
         * The user can specify the test size, the DataFrame to be split,
         * the label column for prediction, and the feature columns to use.
         */
        Blockly.Blocks['train_test_split'] = {
            init: function () {
                this.appendValueInput('teste_size').setAlign(Blockly.inputs.Align.RIGHT).appendField('Test Size').setCheck('Number');
                this.appendValueInput('dataframe').appendField('(train test split)').appendField('DataFrame');
                this.appendValueInput('label').setAlign(Blockly.inputs.Align.RIGHT).appendField('Label');
                this.appendValueInput('features').setAlign(Blockly.inputs.Align.RIGHT).appendField('Features');
                this.setColour(230);
                this.setTooltip("Split a DataFrame into training and testing datasets.");
                this.setHelpUrl("");
                this.setOutput(true);
            }
        };
        pythonGenerator.forBlock["train_test_split"] = ((block: Blockly.Block, generator): [string, number] => {
            const testSize: string = generator.valueToCode(block, 'teste_size', Order.MEMBER) || '0.2';
            const dataframe: string = generator.valueToCode(block, 'dataframe', Order.MEMBER) || '[]';
            const label: string = generator.valueToCode(block, 'label', Order.MEMBER) || '[]';
            const features: string = generator.valueToCode(block, 'features', Order.MEMBER) || '[]';
            //NOTE: overriding access of protected member definitions_
            //@ts-ignore
            generator.definitions_['import_sklearn.model_selection'] = 'from sklearn.model_selection import train_test_split';
            if (!dataframe || !label || !features) {
                console.warn('Invalid inputs for train_test_split block. Generated code may be invalid.');
            };
            const code: string = `train_test_split(${dataframe}[${features}], ${dataframe}[${label}], test_size=${testSize})`;
            return [code, Order.FUNCTION_CALL];
        });

        /**
         * Block for selecting train/test split outputs.
        */
        Blockly.Blocks['selector_train_test_split'] = {
            init: function () {
                this.appendValueInput('train_test')
                    .appendField('Train Test Split:')
                    .appendField(new Blockly.FieldDropdown([
                        ['X Train', 'x_train'],
                        ['X Test', 'x_test'],
                        ['Y Train', 'y_train'],
                        ['Y Test', 'y_test'],
                    ]), 'SPLITSELECTOR');
                this.setColour(230);
                this.setTooltip("Selects the output of the train/test split (X Train, X Test, Y Train, Y Test).");
                this.setHelpUrl("");
                this.setOutput(true);
            }
        };
        pythonGenerator.forBlock["selector_train_test_split"] = ((block: Blockly.Block, generator): [string, number] => {
            const dataframe: string = generator.valueToCode(block, 'train_test', Order.MEMBER) || '[]';
            const field: string = block.getFieldValue('SPLITSELECTOR') || '';
            if (!dataframe) {
                console.warn('No DataFrame input provided in "selector_train_test_split" block. Generated code may be invalid.');
                return ['', Order.NONE];
            };
            const fieldMap: { [key: string]: number } = {
                "x_train": 0,
                "x_test": 1,
                "y_train": 2,
                "y_test": 3
            };
            const index: number = fieldMap[field];
            const code: string = `${dataframe}[${index}]`;
            return [code, Order.FUNCTION_CALL];
        });


        //make all varieties of code block
        this.makeCodeBlock("dummyOutputCodeBlock", false, true);
        this.makeCodeBlock("dummyNoOutputCodeBlock", false, false);
        this.makeCodeBlock("valueOutputCodeBlock", true, true);
        this.makeCodeBlock("valueNoOutputCodeBlock", true, false);

        //make all varieties of comment block
        this.makeCommentBlock("dummyOutputCommentBlock", false, true);
        this.makeCommentBlock("dummyNoOutputCommentBlock", false, false);
        this.makeCommentBlock("valueOutputCommentBlock", true, true);
        this.makeCommentBlock("valueNoOutputCommentBlock", true, false);

        //make all varieties of import block
        this.makeImportBlock("importAs", "import", "as");
        this.makeImportBlock("importFrom", "from", "import");

        //make various blocks that take a list as single argument
        this.makeFunctionBlock(
            "reversedBlock",
            "reversed",
            "None",
            "Create a reversed iterator to reverse a list or a tuple; wrap it in a new list or tuple.",
            "https://docs.python.org/3/library/functions.html#reversed",
            "reversed");
        this.makeFunctionBlock(
            "tupleConstructorBlock",
            "tuple",
            "None",
            "Create a tuple from a list, e.g. [\'a\',\'b\'] becomes (\'a\',\'b\')", "https://docs.python.org/3/library/stdtypes.html#tuple", "tuple");
        this.makeFunctionBlock(
            "dictBlock",
            "dict",
            "None",
            "Create a dictionary from a list of tuples, e.g. [(\'a\',1),(\'b\',2)...]",
            "https://docs.python.org/3/tutorial/datastructures.html#dictionaries",
            "dict");
        this.makeFunctionBlock(
            "listBlock",
            "list",
            "None",
            "Create a list from an iterable, e.g.list(zip(...))",
            "https://docs.python.org/3/library/stdtypes.html#typesseq-list",
            "list");
        this.makeFunctionBlock(
            "zipBlock",
            "zip",
            "Array",
            "Zip together two or more lists",
            "https://docs.python.org/3.3/library/functions.html#zip",
            "zip");
        this.makeFunctionBlock(
            "sortedBlock",
            "as sorted",
            "Array",
            "Sort lists of stuff",
            "https://docs.python.org/3.3/library/functions.html#sorted",
            "sorted");
        this.makeFunctionBlock(
            "setBlock",
            "set",
            "Array",
            "Make a set with unique members of a list.",
            "https://docs.python.org/2/library/sets.html",
            "set");
        this.makeFunctionBlock(
            "boolConversion",
            "as bool",
            "Boolean",
            "Convert something to Boolean.",
            "https://docs.python.org/3/library/stdtypes.html#boolean-values",
            "bool");
        this.makeFunctionBlock(
            "strConversion",
            "as str",
            "String",
            "Convert something to String.",
            "https://docs.python.org/3/library/stdtypes.html#str",
            "str");
        this.makeFunctionBlock(
            "floatConversion",
            "as float",
            "Number",
            "Convert something to Float.",
            "https://docs.python.org/3/library/functions.html#float",
            "float");
        this.makeFunctionBlock(
            "intConversion",
            "as int",
            "Number",
            "Convert something to Int.",
            "https://docs.python.org/3/library/functions.html#int",
            "int");
        this.makeFunctionBlock(
            "getInput",
            "input",
            "String",
            "Present the given prompt to the user and wait for their typed input response.",
            "https://docs.python.org/3/library/functions.html#input",
            "input");

    }

    /**
     * Do any late stage initialization of the toolbox. 
     * Note that final initialization is called when the kernel changes, so only then is it appropriate to make intelliblocks,
     * which are kernel-dependent.
     */
    DoFinalInitialization(): void {

        //make intellisense blocks
        this.makeMemberIntellisenseBlock(this, "varGetProperty", "from", "get", (ie: IntellisenseEntry): boolean => ie.isProperty, false, true);

        this.makeMemberIntellisenseBlock(this, "varDoMethod", "with", "do", (ie: IntellisenseEntry): boolean => ie.isFunction, true, true);

        this.makeMemberIntellisenseBlock(this, "varCreateObject", "with", "create", (ie: IntellisenseEntry): boolean => ie.isClass, true, true);

        //custom flyout for importing libraries
        if (this.workspace) {
            this.workspace.registerToolboxCategoryCallback("IMPORT", (workspace: Blockly.Workspace): any[] => {
                // create button for naming libraries; hopefully a less confusing UI then having them rename a default import variable
                const blockList: any[] = [];
                const button = document.createElement('button');
                button.setAttribute('text', "Import...");
                button.setAttribute('callbackKey', 'CREATE_VARIABLE');
                
                //chain two modal windows: one for library name and one for alias/element name
                (workspace as Blockly.WorkspaceSvg).registerButtonCallback('CREATE_VARIABLE', (button: any): void => { //function (button) {
                    //get library name first
                    let promptResult = prompt("Library name");
                    this.temp = promptResult != null ? promptResult : "";
                    //then get variable name
                    Blockly.Variables.createVariableButtonHandler(button.getTargetWorkspace());
                });
                void (blockList.push(button));
                //blocks appear if an import label has been created; by default show the most recent label
                const variableModelList: Blockly.VariableModel[] = workspace.getVariablesOfType("");
                if (variableModelList.length > 0) {
                    const lastVariableModel : Blockly.VariableModel = variableModelList[variableModelList.length - 1];
                    // add import blocks
                    const importAs: Element = Blockly.utils.xml.createElement("block");
                    importAs.setAttribute("type", "importAs");
                    importAs.setAttribute("gap", Blockly.Blocks.importAs ? "8" : "24");
                    // append field label first
                    let asField = Blockly.utils.xml.createElement('field');
                    asField.setAttribute('name','libraryName');
                    let asName = Blockly.utils.xml.createTextNode(this.temp);
                    asField.appendChild(asName);
                    importAs.appendChild(asField);
                    importAs.appendChild(Blockly.Variables.generateVariableFieldDom(lastVariableModel));
                    blockList.push(importAs);

                    const importFrom: Element = Blockly.utils.xml.createElement("block");
                    importFrom.setAttribute("type", "importFrom");
                    importFrom.setAttribute("gap", Blockly.Blocks.importFrom ? "8" : "24");
                    let fromField = Blockly.utils.xml.createElement('field');
                    fromField.setAttribute('name','libraryName');
                    let fromName = Blockly.utils.xml.createTextNode(this.temp);
                    fromField.appendChild(fromName);
                    importFrom.appendChild(fromField);
                    importFrom.appendChild(Blockly.Variables.generateVariableFieldDom(lastVariableModel));
                    blockList.push(importFrom);
                }
                return blockList;
            });
        }
    }

    registerMemberIntellisenseCodeGenerator(blockName: string, hasArgs: boolean, hasDot: boolean) {
        pythonGenerator.forBlock[blockName] = ((block: Blockly.Block, generator): [string, number] | string => {
            return this.generateMemberIntellisenseCode(block, Order.FUNCTION_CALL, generator, hasArgs, hasDot)
        });
    };
}