import { AbstractToolbox, IntellisenseEntry, IToolbox } from "./AbstractToolbox";
import { Order,RGenerator,rGenerator,JoinMutatorBlock } from "./RGenerator";
import { INotebookTracker } from "@jupyterlab/notebook";
import * as Blockly from 'blockly/core';
// Import the default blocks. We just need to load them here (side effect). Ignore usage check.
import * as libraryBlocks from 'blockly/blocks';
// Import English message file (determines language of blocks)
import * as en from 'blockly/msg/en';

export class RToolbox extends AbstractToolbox implements IToolbox {

    generator = rGenerator;

    toolboxDefinition = {
        "kind": "categoryToolbox",
        "contents": [
            {
                "kind": "CATEGORY",
                // OLD: we now have a dynamic flyout similar to VARIABLE
                // "contents": [
                //     {
                //         "kind": "BLOCK",
                //         "type": "import"
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
                        "type": "doubleIndexer"
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
                        "type": "uniqueBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "reversedBlock"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "unlistBlock"
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
                        "type": "textFromFile"
                    },
                    {
                        "kind": "BLOCK",
                        "type": "readFile"
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
            {
                "kind": "CATEGORY",
                "name": "SPECIAL",
                "colour": "270",
                "custom": "SPECIAL"
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

    isFunction(query: string, info: string): boolean {
        //to handle both parent and children cases, we truncate namespace from the query
        const index: number = query.indexOf("::");
        if (index >= 0) {
            query = query.slice(index + 1)
        }

        // for %>% and other backticked functions
        if (query.startsWith("`")) {
            return true;
        }
        // indicates it takes parameters
        else if (info.includes(query + "(")) {
            return true;
        }
        // explicit marking of function in documentation
        else if (info.includes("Class attribute:\n\'function\'")) {
            return true;
        }
        else if (info.includes("Usage") && info.includes("Arguments")) {
            return true;
        }
        // look for words that otherwise indicate functionhood. These matchers might be too aggressive; hard to say since R is mostly functions
        else if (info.includes("function") || info.includes("Function")) {
            return true;
        }
        else if (info.includes("object") || info.includes("Object")) {
            return true;
        }
        else {
            return false;
        }
    }

    isProperty(query: string, info: string): boolean {
        return false;
    }

    isClass(info: string): boolean {
        return !this.isFunction("", info);
    }

    dotString(): string {
        return "::"
    }

    /**
     * R seems to not need special handling, so no-op
     * @param parent 
     * @param children 
     * @returns 
     */
    GetSafeChildCompletions(parent: IntellisenseEntry, children: string[]): string[] {
        // See python toolbox for example of safe completions
        return children;

    }

    GetChildrenInspections(parent: IntellisenseEntry, children: string[]): Promise<string>[] {
        // Set up inspections for all children; use a timeout promise so we don't wait forever; make timeout dynamic based on which child this is (assumes serial bottleneck at kernel)
        const pr: Promise<string>[] = children.map((childCompletion: string, index: number) => this.timeoutPromise<string>(100 * (index + 1), this.GetKernelInspection(childCompletion)));

        return pr;
    }

    GetCleanChildName(childCompletion: string) {
        //remove parent prefix, e.g. dplyr::select
        const index = childCompletion.lastIndexOf(":");
        let cleanName = "";
        if(index < 0) {
            cleanName = childCompletion;
        }
        else {
            cleanName = childCompletion.substring(index+1);
        }
        return cleanName;
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
                this.setTooltip(((("You can put any R code in this block. Use this block if you " + (hasInput ? "do" : "don\'t")) + " need to connect an input block and ") + (hasOutput ? "do" : "don\'t")) + " need to connect an output block.");
                this.setHelpUrl("https://cran.r-project.org/manuals.html");
            },
        };
        // RGenerator[blockName] = ((block: Blockly.Block): string | string[] => {
        rGenerator.forBlock[blockName] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            const userCode: string = block.getFieldValue("CODE").toString();
            let code: string;
            if (hasInput) {
                const input_1: string = generator.valueToCode(block, "INPUT", Order.ATOMIC);
                code = ((userCode + " ") + input_1).trim();
            }
            else {
                code = userCode.trim();
            }
            return hasOutput ? [code, Order.ATOMIC] : (code + "\n");
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
                this.setHelpUrl("https://cran.r-project.org/manuals.html");
            },
        };
        // RGenerator[blockName] = ((block: Blockly.Block): string | string[] => {
        rGenerator.forBlock[blockName] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
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
     * Create a Blockly/R templated import block
     */
    makeImportBlock(blockName: string, labelOne: string): void {
        Blockly.Blocks[blockName] = {
            init: function () {
                this.appendDummyInput().appendField(labelOne).appendField(new Blockly.FieldVariable("<select>") as Blockly.Field, "VAR");
                this.setNextStatement(true);
                this.setPreviousStatement(true);
                this.setColour(230);
                this.setTooltip("Load an R package to access functions in that package");
                this.setHelpUrl("https://stat.ethz.ch/R-manual/R-devel/library/base/html/library.html");
            },
        };
        // RGenerator[blockName] = ((block: Blockly.Block): string => {
        rGenerator.forBlock[blockName] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let libraryVar = generator.getVariableName(block.getFieldValue("libraryName"));
            let code = "library(" + libraryVar + ")\n";
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
                this.appendValueInput("x").setCheck(void 0).appendField(label);
                this.setInputsInline(true);
                this.setOutput(true, outputType);
                this.setColour(230);
                this.setTooltip(tooltip);
                this.setHelpUrl(helpurl);
            },
        };
        // RGenerator[blockName] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock[blockName] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            const valueCode = generator.valueToCode(block, "x", Order.MEMBER);
            const sanitizedValueCode = valueCode.replace(/^\[|\]$/g, "");
            return [`${functionStr}(${sanitizedValueCode})`, Order.FUNCTION_CALL];
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
        // We use @ts-ignore to override the protected class attributes we need to modify; an alternative would be to extend RGenerator and then do these overrides within that new class

        rGenerator.finish = ((code: string): string => {
            const imports: string[] = [];
            const functions: string[] = [];
            // @ts-ignore
            let enumerator: any = Object.keys(rGenerator.definitions_);
            for (let i in enumerator) {
                // @ts-ignore
                const definitions: any = rGenerator.definitions_;
                const def: string = definitions[enumerator[i]];
                if (def.indexOf("library(") >= 0) {
                    void (imports.push(def));
                }
                if ((def.indexOf("function() ") === 0) ? true : (def.indexOf("# ") === 0)) {
                    void (functions.push(def));
                }
            }
            // @ts-ignore
            delete rGenerator.definitions_;
            // @ts-ignore
            delete rGenerator.functionNames_;
            // @ts-ignore
            rGenerator.nameDB_.reset();
            return ((("\n" + imports) + ("\n" + functions)) + "\n\n") + code;
        });

        //-----------------
        //define new blocks
        //-----------------
        //we use the old API since RGenerator uses the old API
        //for current guidelines, see https://developers.google.com/blockly/guides/configure/web/custom-blocks
        //notably we define on Blockly.Blocks directly rather than using Blockly.common.defineBlocks

        Blockly.Blocks["textFromFile"] = {
            init: function () {
                console.log("textFromFile init");
                this.appendValueInput("FILENAME").setCheck("String").appendField("read text from file");
                this.setOutput(true, void 0);
                this.setColour(230);
                this.setTooltip("Use this to read a flat text file. It will output a string.");
                this.setHelpUrl("https://stackoverflow.com/a/9069670");
            },
        };
        // RGenerator["textFromFile"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["textFromFile"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            const fileName: string = generator.valueToCode(block, "FILENAME", Order.ATOMIC);
            const code = "readChar(" + fileName + ", file.info(" + fileName + ")$size)";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["readFile"] = {
            init: function () {
                console.log("readFile init");
                this.appendValueInput("FILENAME").setCheck("String").appendField("read file");
                this.setOutput(true, void 0);
                this.setColour(230);
                this.setTooltip("Use this to read a file. It will output a file, not a string.");
                this.setHelpUrl("https://stat.ethz.ch/R-manual/R-devel/library/base/html/connections.html");
            },
        };
        // RGenerator["readFile"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["readFile"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let fileName = generator.valueToCode(block, "FILENAME", Order.ATOMIC);
            let code = "file(" + fileName + ", 'rt')";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["indexer"] = {
            init: function () {
                this.appendValueInput("INDEX").appendField(new Blockly.FieldVariable("{dictVariable}") as Blockly.Field, "VAR").appendField("[");
                this.appendDummyInput().appendField("]");
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour(230);
                this.setTooltip("Gets a list from the variable at a given indices. Not supported for all variables.");
                this.setHelpUrl("https://cran.r-project.org/doc/manuals/R-lang.html#Indexing");
            },
        };
        // RGenerator["indexer"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["indexer"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let varName = block.getFieldValue("VAR").toString();
            let input = generator.valueToCode(block, "INDEX", Order.ATOMIC);
            let code = varName + "[" + input + "]" //+ "\n"
            return [code, Order.ATOMIC];
        });

        Blockly.Blocks["doubleIndexer"] = {
            init: function () {
                this.appendValueInput("INDEX").appendField(new Blockly.FieldVariable("{dictVariable}") as Blockly.Field, "VAR").appendField("[[");
                this.appendDummyInput().appendField("]]");
                this.setInputsInline(true);
                this.setOutput(true);
                this.setColour(230);
                this.setTooltip("Gets an item from the variable at a given index. Not supported for all variables.");
                this.setHelpUrl("https://cran.r-project.org/doc/manuals/R-lang.html#Indexing");
            },
        };
        // RGenerator["doubleIndexer"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["doubleIndexer"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let varName = block.getFieldValue("VAR").toString();
            let input = generator.valueToCode(block, "INDEX", Order.ATOMIC);
            let code = varName + "[[" + input + "]]" //+ "\n"
            return [code, Order.ATOMIC];
        });

        Blockly.Blocks["unlistBlock"] = {
            init: function () {
                this.appendValueInput("LIST").setCheck("Array").appendField("vector");
                this.setInputsInline(true);
                this.setOutput(true, "Array");
                this.setColour(230);
                this.setTooltip("Use this to convert a list to a vector");
                this.setHelpUrl("https://www.rdocumentation.org/packages/base/versions/3.6.2/topics/unlist");
            },
        };
        // RGenerator["unlistBlock"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["unlistBlock"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let args = generator.valueToCode(block, "LIST", Order.MEMBER);
            let code = "unlist(" + args + ", use.names = FALSE)";
            return [code, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["uniqueBlock"] = {
            init: function () {
                this.appendValueInput("LIST").setCheck("Array").appendField("unique");
                this.setInputsInline(true);
                this.setOutput(true, "Array");
                this.setColour(230);
                this.setTooltip("Use this to get the unique elements of a list");
                this.setHelpUrl("https://stackoverflow.com/questions/3879522/finding-unique-values-from-a-list");
            },
        };
        // RGenerator["uniqueBlock"] = ((block: Blockly.Block): string[] => {
        rGenerator.forBlock["uniqueBlock"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            let args = generator.valueToCode(block, "LIST", Order.MEMBER);
            let code = "unique(unlist(" + args + ", use.names = FALSE))"
            return [code, Order.FUNCTION_CALL];
        });

        //Special blocks
        Blockly.Blocks["pipe"] = Blockly.Blocks["lists_create_with"];
        this.createDynamicArgumentMutator("pipeMutator", 1, "add pipe output", "to", "then to");
        Blockly.Blocks["pipe"] = {
            init: function () {
                const input_1: Blockly.Input = this.appendValueInput("INPUT");
                input_1.appendField("pipe");
                this.appendDummyInput("EMPTY");
                this.setOutput(true);
                this.setColour(230);
                this.setTooltip("A dplyr pipe, i.e. %>%");
                this.setHelpUrl("");
                Blockly.Extensions.apply("pipeMutator", this, true);
            }
        }
        // RGenerator["pipe"] = ((block: any): string[] => {
        rGenerator.forBlock["pipe"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            const elements: string[] = [];
            let jmm = block as JoinMutatorBlock;
            const itemCount = jmm.itemCount_;
            for (let i = 0; i < itemCount; i++) {
                const addValue = generator.valueToCode(block, "ADD" + i, Order.COMMA);
                elements.push(addValue);
            }
            const elementString = elements.join(" %>%\n    ");
            const inputCode = generator.valueToCode(block, "INPUT", Order.MEMBER);
            const outputCode = `${inputCode} %>%\n    ${elementString}`;
            return [outputCode, Order.FUNCTION_CALL];
        });

        Blockly.Blocks["ggplot_plus"] = Blockly.Blocks["lists_create_with"];
        this.createDynamicArgumentMutator("plusMutator", 1, "add plot element", "with", "and with");
        Blockly.Blocks["ggplot_plus"] = {
            init: function () {
                const input_1: Blockly.Input = this.appendValueInput("INPUT");
                input_1.appendField("make plot");
                this.appendDummyInput("EMPTY");
                this.setOutput(true);
                this.setColour(230);
                this.setTooltip("A ggplot");
                this.setHelpUrl("");
                Blockly.Extensions.apply("plusMutator", this, true);
            }
        }
        // RGenerator["ggplot_plus"] = ((block: any): string[] => {
            rGenerator.forBlock["ggplot_plus"] = ((block: Blockly.Block, generator :RGenerator): [string, number] | string => {
            const elements: string[] = [];
            let jmm = block as JoinMutatorBlock;
            const itemCount = jmm.itemCount_;
            for (let i = 0; i < itemCount; i++) {
                const addValue = generator.valueToCode(block, "ADD" + i, Order.COMMA);
                elements.push(addValue);
            }
            const elementString = elements.join(" +\n    ");
            const inputCode = generator.valueToCode(block, "INPUT", Order.MEMBER);
            const outputCode = `${inputCode} +\n    ${elementString}`;
            return [outputCode, Order.FUNCTION_CALL];
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
        this.makeImportBlock("import", "library");


        //make various blocks that take a list as single argument
        this.makeFunctionBlock("reversedBlock", "reversed", "None", "Provides a reversed version of its argument.", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/rev.html", "rev");

        this.makeFunctionBlock("boolConversion", "as bool", "Boolean", "Convert something to Boolean.", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/logical.html", "as.logical");

        this.makeFunctionBlock("strConversion", "as str", "String", "Convert something to String.", "https://stat.ethz.ch/R-manual/R-patched/library/base/html/toString.html", "toString");

        this.makeFunctionBlock("floatConversion", "as float", "Number", "Convert something to Float.", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/numeric.html", "as.numeric");

        this.makeFunctionBlock("intConversion", "as int", "Number", "Convert something to Int.", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/integer.html", "as.integer");

    }

    /**
     *  Do any late stage initialization of the toolbox. 
     * Note that final initialization is called when the kernel changes, so only then is it appropriate to make intelliblocks,
     * which are kernel-dependent.
     * For R create the SPECIAL toolbox category
     * @param workspace 
     */
    DoFinalInitialization(): void {

        //make intellisense blocks
        this.makeMemberIntellisenseBlock(this, "varGetProperty", "from", "get", (ie: IntellisenseEntry): boolean => !ie.isFunction, false, true);

        this.makeMemberIntellisenseBlock(this, "varDoMethod", "with", "do", (ie: IntellisenseEntry): boolean => ie.isFunction, true, true);

        this.makeMemberIntellisenseBlock(this, "varCreateObject", "with", "create", (ie: IntellisenseEntry): boolean => ie.isClass, true, true);

        // custom flyout for special blocks, i.e. primitive blocks that only exist if a library has been loaded
        if (this.workspace) {
            this.workspace.registerToolboxCategoryCallback("SPECIAL", (workspace: Blockly.Workspace): any[] => {
                const blockList: any[] = [];
                const label: any = document.createElement("label");
                label.setAttribute("text", "Occassionally blocks appear here as you load libraries (e.g. %>%). See VARIABLES for most cases.");
                void (blockList.push(label));
                if (this.intellisenseLookup.has("dplyr")) {
                    const block: any = document.createElement("block");
                    block.setAttribute("type", "pipe");
                    void (blockList.push(block));
                }
                if (this.intellisenseLookup.has("ggplot2")) {
                    const block_1: any = document.createElement("block");
                    block_1.setAttribute("type", "ggplot_plus");
                    void (blockList.push(block_1));
                }
                return blockList;
            });
        }

        //custom flyout for importing libraries
        if (this.workspace) {
            this.workspace.registerToolboxCategoryCallback("IMPORT", (workspace: Blockly.Workspace): any[] => {
                // create button for naming libraries. 
                // The is hopefully a less confusing UI then having them rename a default import variable
                const blockList: any[] = [];
                const button = document.createElement('button');
                button.setAttribute('text', "Load library...");
                button.setAttribute('callbackKey', 'CREATE_VARIABLE');
                (workspace as Blockly.WorkspaceSvg).registerButtonCallback('CREATE_VARIABLE', function (button) {
                Blockly.Variables.createVariableButtonHandler(button.getTargetWorkspace());
                });
                void (blockList.push(button));

                //add import block
                //blocks appear if an import label has been created; by default show the most recent label
                const variableModelList: Blockly.VariableModel[] = workspace.getVariablesOfType("");
                if (variableModelList.length > 0) {
                    const lastVariableModel : Blockly.VariableModel = variableModelList[variableModelList.length - 1];
                    // add import blocks
                    const importAs: Element = Blockly.utils.xml.createElement("block");
                    importAs.setAttribute("type", "import");
                    importAs.setAttribute("gap", Blockly.Blocks.importAs ? "8" : "24");
                    importAs.appendChild(Blockly.Variables.generateVariableFieldDom(lastVariableModel));
                    blockList.push(importAs);
                }
                return blockList;
            });
        }
    }

    registerMemberIntellisenseCodeGenerator(blockName: string, hasArgs: boolean, hasDot: boolean) {
        rGenerator.forBlock[blockName] = ((block: Blockly.Block, generator: any): [string, number] | string => {
            return this.generateMemberIntellisenseCode(block, Order.FUNCTION_CALL, generator, hasArgs, hasDot)
        });
    };
}