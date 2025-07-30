import type { Block, BlockSvg } from 'blockly/core';
import { CodeGenerator, Variables, Names, Workspace } from 'blockly/core';
// Some stuff doesn't export well except at top level
import * as Blockly from 'blockly';


//---------BEGIN HACK---------------
// We can't access these types; they are not exported.
// to prevent compile time errors, we recreate minimal types and functions 
// from the Blockly library

type CreateWithBlock = Block & ListCreateWithMixin;
interface ListCreateWithMixin extends Block { //ListCreateWithMixinType {
    itemCount_: number;
}

//AO this composition is slightly wrong but hopefully doesn't matter
export type JoinMutatorBlock = BlockSvg & JoinMutatorMixin;
type JoinMutatorMixin = typeof JOIN_MUTATOR_MIXIN;
const JOIN_MUTATOR_MIXIN = {
    itemCount_: 0,
}
//-------END HACK---------------------

/**
 * Order of operation ENUMs.
 * https://developer.mozilla.org/en/R/Reference/Operators/Operator_Precedence
 */
export enum Order {
    ATOMIC = 0,           // 0 "" ...
    NEW = 1.1,            // new
    MEMBER = 1.2,         // . []
    FUNCTION_CALL = 2,    // ()
    INCREMENT = 3,        // ++
    DECREMENT = 3,        // --
    BITWISE_NOT = 4.1,    // ~
    UNARY_PLUS = 4.2,     // +
    UNARY_NEGATION = 4.3, // -
    LOGICAL_NOT = 4.4,    // !
    TYPEOF = 4.5,         // typeof
    VOID = 4.6,           // void
    DELETE = 4.7,         // delete
    AWAIT = 4.8,          // await
    EXPONENTIATION = 5.0, // **
    // AO: switched
    DIVISION = 5.1,       // /
    MULTIPLICATION = 5.2, // *
    // AO: switched
    MODULUS = 5.3,        // %
    // AO: switched
    ADDITION = 6.1,       // +
    SUBTRACTION = 6.2,    // -
    // AO: switched
    BITWISE_SHIFT = 7,    // << >> >>>
    RELATIONAL = 8,       // < <= > >=
    IN = 8,               // in
    INSTANCEOF = 8,       // instanceof
    EQUALITY = 9,         // == != === !==
    BITWISE_AND = 10,     // &
    BITWISE_XOR = 11,     // ^
    BITWISE_OR = 12,      // |
    LOGICAL_AND = 13,     // &&
    LOGICAL_OR = 14,      // ||
    CONDITIONAL = 15,     // ?:
    ASSIGNMENT = 16,      // = += -= **= *= /= %= <<= >>= ...
    YIELD = 17,           // yield
    COMMA = 18,           // ,
    NONE = 99,            // (...)
}

export class RGenerator extends CodeGenerator {
    /**
     * List of outer-inner pairings that do NOT require parentheses.
     */
    ORDER_OVERRIDES: [Order, Order][] = [
        // (foo()).bar -> foo().bar
        // (foo())[0] -> foo()[0]
        [Order.FUNCTION_CALL, Order.MEMBER],
        // (foo())() -> foo()()
        [Order.FUNCTION_CALL, Order.FUNCTION_CALL],
        // (foo.bar).baz -> foo.bar.baz
        // (foo.bar)[0] -> foo.bar[0]
        // (foo[0]).bar -> foo[0].bar
        // (foo[0])[1] -> foo[0][1]
        [Order.MEMBER, Order.MEMBER],
        // (foo.bar)() -> foo.bar()
        // (foo[0])() -> foo[0]()
        [Order.MEMBER, Order.FUNCTION_CALL],

        // !(!foo) -> !!foo
        [Order.LOGICAL_NOT, Order.LOGICAL_NOT],
        // a * (b * c) -> a * b * c
        [Order.MULTIPLICATION, Order.MULTIPLICATION],
        // a + (b + c) -> a + b + c
        [Order.ADDITION, Order.ADDITION],
        // a && (b && c) -> a && b && c
        [Order.LOGICAL_AND, Order.LOGICAL_AND],
        // a || (b || c) -> a || b || c
        [Order.LOGICAL_OR, Order.LOGICAL_OR]
    ];

    // AO: don't think we need this
    /**
   * Empty loops or conditionals are not allowed in Python.
   */
    // PASS: string = ''; // Initialised by init().

    /** @param name Name of the language the generator is for. */
    constructor(name = 'R') {
        super(name);
        this.isInitialized = false;

        // Copy Order values onto instance for backwards compatibility
        // while ensuring they are not part of the publically-advertised
        // API.
        //
        // TODO(#7085): deprecate these in due course.  (Could initially
        // replace data properties with get accessors that call
        // deprecate.warn().)
        for (const key in Order) {
            // Must assign Order[key] to a temporary to get the type guard to work;
            // see https://github.com/microsoft/TypeScript/issues/10530.
            const value = Order[key];
            // Skip reverse-lookup entries in the enum.  Due to
            // https://github.com/microsoft/TypeScript/issues/55713 this (as
            // of TypeScript 5.5.2) actually narrows the type of value to
            // never - but that still allows the following assignment to
            // succeed.
            if (typeof value === 'string') continue;
            (this as unknown as Record<string, Order>)['ORDER_' + key] = value;
        }

        // List of illegal variable names.  This is not intended to be a
        // security feature.  Blockly is 100% client-side, so bypassing
        // this list is trivial.  This is intended to prevent users from
        // accidentally clobbering a built-in object or function.
        this.addReservedWords(
            'Blockly,' +  // In case JS is evaled in the current window.
            //https://stat.ethz.ch/R-manual/R-devel/library/base/html/Reserved.html
            //AO: not sure if .. can be handled correctly this way
            "if,else,repeat,while,function,for,in,next,break,TRUE,FALSE,NULL,Inf,NaN,NA,NA_integer_,NA_real_,NA_complex_,NA_character_,...,..1,..2,..3,..4,..5,..6,..7,..8,..9");
    }

    /**
   * Initialise the database of variable names.
   *
   * @param workspace Workspace to generate code from.
   */
    init(workspace: Workspace) {
        super.init(workspace);

        // this.PASS = this.INDENT + 'pass\n';

        if (!this.nameDB_) {
            this.nameDB_ = new Names(this.RESERVED_WORDS_);
        } else {
            this.nameDB_.reset();
        }

        this.nameDB_.setVariableMap(workspace.getVariableMap());
        this.nameDB_.populateVariables(workspace);
        this.nameDB_.populateProcedures(workspace);

        const defvars = [];
        // Add developer variables (not created or named by the user).
        const devVarList = Variables.allDeveloperVariables(workspace);
        for (let i = 0; i < devVarList.length; i++) {
            defvars.push(
                this.nameDB_.getName(devVarList[i], Names.DEVELOPER_VARIABLE_TYPE) +
                ' = None',
            );
        }

        // Add user variables, but only ones that are being used.
        const variables = Variables.allUsedVarModels(workspace);
        for (let i = 0; i < variables.length; i++) {
            defvars.push(this.getVariableName(variables[i].getId()) + ' = None');
        }

        // TODO: this was commented out in the original version - do we need it?
        // this.definitions_['variables'] = defvars.join('\n');
        this.isInitialized = true;
    }

    /**
   * Prepend the generated code with variable definitions.
   * NOTE: NO IMPORTS
   *
   * @param code Generated code.
   * @returns Completed code.
   */
    finish(code: string): string {
        // Convert the definitions dictionary into a list.
        const definitions = [];
        for (let name in this.definitions_) {
            definitions.push(this.definitions_[name]);
        }
        // Call Blockly.CodeGenerator's finish.
        code = super.finish(code);
        this.isInitialized = false;

        this.nameDB_!.reset();
        return definitions.join('\n\n') + '\n\n\n' + code;
    }

    /**
     * Naked values are top-level blocks with outputs that aren't plugged into
     * anything.  
     * @param {string} line Line of generated code.
     * @return {string} Legal line of code.
     */
    scrubNakedValue(line: string): string {
        // return line + ';\n';
        return line + '\n';
    };

    /**
     * Encode a string as a properly escaped R string, complete with
     * quotes. AO: changed to double quotes
     * @param {string} string Text to encode.
     * @return {string} R string.
     * @private
    */
    quote_(string: string): string {
        // Can't use goog.string.quote since Google's style guide recommends
        // JS string literals use single quotes.
        string = string.replace(/\\/g, '\\\\')
            .replace(/\n/g, '\\\n')
            .replace(/"/g, '\\\"');
        return '\"' + string + '\"';
    };

    /**
     * Encode a string as a properly escaped multiline R string, complete
     * with quotes. AO: changed to double quote
     * @param {string} string Text to encode.
     * @return {string} R string.
     * @private
     */
    multiline_quote_(string: string): string {
        // Can't use goog.string.quote since Google's style guide recommends
        // JS string literals use single quotes.
        var lines = string.split(/\n/g).map(this.quote_);
        return lines.join(' + \"\\n\" +\n');
    };

    /**
     * Common tasks for generating R from blocks.
     * Handles comments for the specified block and any connected value blocks.
     * Calls any statements following this block.
     * @param {!Blockly.Block} block The current block.
     * @param {string} code The R code created for this block.
     * @param {boolean=} opt_thisOnly True to generate code for only this statement.
     * @return {string} R code with comments and subsequent blocks added.
     * @private
     */
    scrub_(block: Block, code: string, opt_thisOnly?: boolean): string {
        let commentCode = '';
        // Only collect comments for blocks that aren't inline.
        if (!block.outputConnection || !block.outputConnection.targetConnection) {
            // Collect comment for this block.
            let comment = block.getCommentText();
            if (comment) {
                comment = Blockly.utils.string.wrap(comment, this.COMMENT_WRAP - 3);
                commentCode += this.prefixLines(comment + '\n', '# ');
            }
            // Collect comments for all value arguments.
            // Don't collect comments for nested statements.
            for (let i = 0; i < block.inputList.length; i++) {
                // if (block.inputList[i].connection) { //AO this was the original; copying new api
                if (block.inputList[i].type === Blockly.inputs.inputTypes.VALUE) {
                    let childBlock = block.inputList[i].connection?.targetBlock();
                    if (childBlock) {
                        let comment = this.allNestedComments(childBlock);
                        if (comment) {
                            commentCode += this.prefixLines(comment, '# ');
                        }
                    }
                }
            }
        }
        const nextBlock = block.nextConnection && block.nextConnection.targetBlock();
        const nextCode = opt_thisOnly ? '' : this.blockToCode(nextBlock);
        return commentCode + code + nextCode;
    }
}

// !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!  
/**
 * R code generator instance
 */
export const rGenerator: any = new RGenerator('R');

// !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   !!!   

// We now forBlock an a big batch

//***********************************************************************
//lists.js
// generator.lists = {}

rGenerator.forBlock['lists_create_empty'] = function(block: Block, generator: RGenerator) {
    // Create an empty list.
    return ['list()', Order.ATOMIC];
};

rGenerator.forBlock['lists_create_with'] = function(block: Block, generator: RGenerator) {
    // Create a list with any number of elements of any type.
    const createWithBlock = block as CreateWithBlock;
    var elements = new Array(createWithBlock.itemCount_);
    for (var i = 0; i < createWithBlock.itemCount_; i++) {
        elements[i] = generator.valueToCode(block, 'ADD' + i,
            Order.COMMA) || 'NULL'; //AO: think NULL better than NA here
    }
    var code = 'list(' + elements.join(', ') + ')';
    return [code, Order.ATOMIC];
};

rGenerator.forBlock['lists_repeat'] = function(block: Block, generator: RGenerator) {
    // Create a list with one element repeated.
    var element = generator.valueToCode(block, 'ITEM',
        Order.COMMA) || 'NULL'; //AO: think NULL better than NA here
    var repeatCount = generator.valueToCode(block, 'NUM',
        Order.COMMA) || '0';
    var code = "as.list(rep(" + element + ', ' + repeatCount + '))';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_length'] = function(block: Block, generator: RGenerator) {
    // String or array length.
    var list = generator.valueToCode(block, 'VALUE',
        Order.MEMBER) || 'list()';
    return ['length(' + list + ')', Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_isEmpty'] = function(block: Block, generator: RGenerator) {
    // Is the string null or array empty?
    var list = generator.valueToCode(block, 'VALUE',
        Order.MEMBER) || 'list()';
    return ['!' + 'length(' + list + ')', Order.LOGICAL_NOT];
};

rGenerator.forBlock['lists_indexOf'] = function(block: Block, generator: RGenerator) {
    // Find an item in the list.
    // var operator = block.getFieldValue('END') == 'FIRST' ?
    //     'indexOf' : 'lastIndexOf';
    var item = generator.valueToCode(block, 'FIND',
        Order.NONE) || '\"\"';
    var list = generator.valueToCode(block, 'VALUE',
        Order.MEMBER) || 'list()';
    var code = ""
    if (block.getFieldValue('END') == 'FIRST') {
        code = 'match(' + item + ',' + list + ')'
    }
    else {
        code = 'length(' + list + ') + 1L - match(' + item + ', rev(' + list + '))'
        //length(l) + 1L - match("j",rev(l))
    }
    //list + '.' + operator + '(' + item + ')';
    // if (block.workspace.options.oneBasedIndex) {
    //   return [code + ' + 1', Order.ADDITION];
    // }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_getIndex'] = function(block: Block, generator: RGenerator) {
    // Get element at index.
    // Note: Until January 2013 this block did not have MODE or WHERE inputs.
    var mode = block.getFieldValue('MODE') || 'GET';
    var where = block.getFieldValue('WHERE') || 'FROM_START';
    var listOrder = (where == 'RANDOM') ? Order.COMMA :
        Order.MEMBER;
    var list = generator.valueToCode(block, 'VALUE', listOrder) || 'list()';

    switch (where) {
        case ('FIRST'):
            if (mode == 'GET') {
                var code = list + '[1]';
                return [code, Order.MEMBER];
            } else if (mode == 'GET_REMOVE') {
                // var listVar = generator.variableDB_.getDistinctName('tmp_list', 'VARIABLE');
                var listVar = generator.nameDB_?.getDistinctName('tmp_list', 'VARIABLE');
                var code = listVar + '<-' + list + '\n' + list + '<-' + list + '[-1]\n' + listVar + '[1]';
                return [code, Order.MEMBER];
            } else if (mode == 'REMOVE') {
                return list + '[1] <- NULL\n';
            }
            break;
        case ('LAST'):
            if (mode == 'GET') {
                var code = list + '[length(' + list + ')]';
                return [code, Order.MEMBER];
            } else if (mode == 'GET_REMOVE') {
                // var listVar = generator.variableDB_.getDistinctName('tmp_list', 'VARIABLE');
                var listVar = generator.nameDB_?.getDistinctName('tmp_list', 'VARIABLE');
                var code = listVar + '<-' + list + '\n' + list + '<-' + list + '[-length(' + list + ')]\n' + listVar + '[length(' + list + ')]';
                return [code, Order.MEMBER];
            } else if (mode == 'REMOVE') {
                return list + '[length(' + list + ')] <- NULL\n';
            }
            break;
        case ('FROM_START'):
            var at = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            if (mode == 'GET') {
                var code = list + '[' + at + ']';
                return [code, Order.MEMBER];
            } else if (mode == 'GET_REMOVE') {
                // var listVar = generator.variableDB_.getDistinctName('tmp_list', 'VARIABLE');
                var listVar = generator.nameDB_?.getDistinctName('tmp_list', 'VARIABLE');
                var code = listVar + '<-' + list + '\n' + list + '<-' + list + '[-' + at + ']\n' + listVar + '[' + at + ']';
                return [code, Order.MEMBER];
            } else if (mode == 'REMOVE') {
                return list + '[' + at + '] <- NULL\n';
            }
            break;
        case ('FROM_END'):
            var at = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            if (mode == 'GET') {
                var code = list + '[length(' + list + ') -' + at + ']';
                return [code, Order.FUNCTION_CALL];
            } else if (mode == 'GET_REMOVE') {
                // var listVar = generator.variableDB_.getDistinctName('tmp_list', 'VARIABLE');
                var listVar = generator.nameDB_?.getDistinctName('tmp_list', 'VARIABLE');
                var code = listVar + '<-' + list + '\n' + list + '<-' + list + '[-(length(' + list + ') -' + at + ')]\n' + listVar + '[length(' + list + ') -' + at + ']';
                return [code, Order.FUNCTION_CALL];
            } else if (mode == 'REMOVE') {
                return list + '[length(' + list + ') -' + at + '] <- NULL\n';
            }
            break;
        case ('RANDOM'):
            var at: string = 'sample(1:length(' + list + '),1)'
            if (mode == 'GET') {
                var code = list + '[' + at + ']';
                return [code, Order.MEMBER];
            } else if (mode == 'GET_REMOVE') {
                // var listVar = generator.variableDB_.getDistinctName('tmp_list', "VARIABLE");
                var listVar = generator.nameDB_?.getDistinctName('tmp_list', 'VARIABLE');
                // var atVar = generator.variableDB_.getDistinctName('at_var', "VARIABLE");
                var atVar = generator.nameDB_?.getDistinctName('at_var', 'VARIABLE');
                var code = atVar + '<-' + at + '\n' + listVar + '<-' + list + '\n' + list + '<-' + list + '[-' + atVar + ']\n' + listVar + '[' + atVar + ']';
                return [code, Order.MEMBER];
            } else if (mode == 'REMOVE') {
                return list + '[' + at + '] <- NULL\n';
            }
            break;
    }
    throw Error('Unhandled combination (lists_getIndex).');
};

rGenerator.forBlock['lists_setIndex'] = function(block: Block, generator: RGenerator) {
    // Set element at index.
    // Note: Until February 2013 this block did not have MODE or WHERE inputs.
    var list = generator.valueToCode(block, 'LIST',
        Order.MEMBER) || 'list()';
    var mode = block.getFieldValue('MODE') || 'GET';
    var where = block.getFieldValue('WHERE') || 'FROM_START';
    var value = generator.valueToCode(block, 'TO',
        Order.ASSIGNMENT) || 'NULL'; //AO: think NULL better than NA here

    switch (where) {
        case ('FIRST'):
            if (mode == 'SET') {
                return list + '[1] <- ' + value + '\n';
            } else if (mode == 'INSERT') {
                return 'append(' + list + ',' + value + '1)\n';
            }
            break;
        case ('LAST'):
            if (mode == 'SET') {
                return list + '[length(' + list + ')] <- ' + value + '\n';
            } else if (mode == 'INSERT') {
                return 'append(' + list + ',' + value + ', length(' + list + '))\n';
            }
            break;
        case ('FROM_START'):
            var at = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            if (mode == 'SET') {
                return list + '[' + at + '] <- ' + value + ';\n';
            } else if (mode == 'INSERT') {
                return 'append(' + list + ',' + value + ', ' + at + ')\n';
            }
            break;
        case ('FROM_END'):
            var at = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            if (mode == 'SET') {
                return list + '[length(' + list + ') -' + at + '] <- ' + value + ';\n';
            } else if (mode == 'INSERT') {
                return 'append(' + list + ',' + value + ', length(' + list + ') -' + at + ')\n';
            }
            break;
        case ('RANDOM'):
            var at: string = 'sample(1:length(' + list + '),1)'
            if (mode == 'SET') {
                var code = list + '[' + at + '] <- ' + value + ';\n';
                return [code, Order.MEMBER];
            } else if (mode == 'INSERT') {
                return 'append(' + list + ',' + value + ', ' + at + ')\n';
            }
            break;
    }
    throw Error('Unhandled combination (lists_setIndex).');
};

/**
 * AO: this appears to be internal only....
 * Returns an expression calculating the index into a list.
 * @param {string} listName Name of the list, used to calculate length.
 * @param {string} where The method of indexing, selected by dropdown in Blockly
 * @param {string=} opt_at The optional offset when indexing from start/end.
 * @return {string} Index expression.
 * @private
 */
// const lists_getIndex_ = function (listName: any, where: any, opt_at: any) {
//     if (where == 'FIRST') {
//         return '0';
//     } else if (where == 'FROM_END') {
//         return 'length(' + listName + ') - ' + opt_at;
//     } else if (where == 'LAST') {
//         return 'length(' + listName + ')';
//     } else {
//         return opt_at;
//     }
// };

rGenerator.forBlock['lists_getSublist'] = function(block: Block, generator: RGenerator) {
    // Get sublist.
    var list = generator.valueToCode(block, 'LIST',
        Order.MEMBER) || 'list()';
    var where1 = block.getFieldValue('WHERE1');
    var where2 = block.getFieldValue('WHERE2');
    if (where1 == 'FIRST' && where2 == 'LAST') {
        var code = list;
    } else {
        // If the list is a variable or doesn't require a call for length, don't
        // generate a helper function.
        switch (where1) {
            case 'FROM_START':
                var at1: string = generator.valueToCode(block, 'AT1', Order.NONE) || '1';
                break;
            case 'FROM_END':
                var at1: string = generator.valueToCode(block, 'AT1', Order.NONE) || '1';
                at1 = 'length(' + list + ') - ' + at1;
                break;
            case 'FIRST':
                var at1: string = '1';
                break;
            default:
                throw Error('Unhandled option (lists_getSublist).');
        }
        switch (where2) {
            case 'FROM_START':
                var at2: string = generator.valueToCode(block, 'AT2', Order.NONE) || '1';
                break;
            case 'FROM_END':
                var at2: string = generator.valueToCode(block, 'AT2', Order.NONE) || '1';
                at2 = 'length(' + list + ') - ' + at2;
                break;
            case 'LAST':
                var at2: string = 'length(' + list + ')';
                break;
            default:
                throw Error('Unhandled option (lists_getSublist).');
        }
        code = list + '[' + at1 + ':' + at2 + ']';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_sort'] = function(block: Block, generator: RGenerator) {
    // Block for sorting a list.
    var list = generator.valueToCode(block, 'LIST',
        Order.FUNCTION_CALL) || 'list()';
    var direction = block.getFieldValue('DIRECTION') === '1' ? 'FALSE' : 'TRUE';
    //AO: doesn't seem like R allows us to mess with type (numeric/alphabetical)
    // var type = block.getFieldValue('TYPE');
    var code = 'as.list(sort(unlist(' + list + '), decreasing=' + direction + '))';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_split'] = function(block: Block, generator: RGenerator) {
    // Block for splitting text into a list, or joining a list into text.
    var input = generator.valueToCode(block, 'INPUT',
        Order.MEMBER);
    var delimiter = generator.valueToCode(block, 'DELIM',
        Order.NONE) || '\"\"';
    var mode = block.getFieldValue('MODE');
    if (mode == 'SPLIT') {
        if (!input) {
            input = '\"\"';
        }
        var code = 'as.list(unlist(strsplit(' + input + ', ' + delimiter + ')))'; //AO note delimiter is regex
    } else if (mode == 'JOIN') {
        if (!input) {
            input = 'list()';
        }
        var code = 'paste0(' + input + ',collapse=' + delimiter + ')';
    } else {
        throw Error('Unknown mode: ' + mode);
    }
    // var code = input + '.' + functionName + '(' + delimiter + ')';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['lists_reverse'] = function(block: Block, generator: RGenerator) {
    // Block for reversing a list.
    var list = generator.valueToCode(block, 'LIST',
        Order.FUNCTION_CALL) || 'list';
    var code = 'rev(' + list + ')';
    return [code, Order.FUNCTION_CALL];
};

//***********************************************************************
//text.js

rGenerator.forBlock['text'] = function(block: Block, generator: RGenerator) {
    // Text value.
    var code = generator.quote_(block.getFieldValue('TEXT'));
    return [code, Order.ATOMIC];
};

rGenerator.forBlock['text_multiline'] = function(block: Block, generator: RGenerator): [string, number] {
    // Text value.
    const code = generator.multiline_quote_(block.getFieldValue('TEXT'));
    return [code, Order.ATOMIC];
};

/**
 * Regular expression to detect a single-quoted string literal.
 */
const strRegExp = /^\s*'([^']|\\')*'\s*$/;

/**
 * Enclose the provided value in 'String(...)' function.
 * Leave string literals alone.
 * @param {string} value Code evaluating to a value.
 * @return {string} Code evaluating to a string.
 * @private
*/
const forceString_ = function (value: string): string {
    if (strRegExp.test(value)) {
        return value;
        // AO trying to hold existing return types for now
        // return [value, Order.ATOMIC];
    }
    return 'toString(' + value + ')';
    // return ['str(' + value + ')', Order.FUNCTION_CALL];
};

/**
 * Regular expression to detect a single-quoted string literal.
 */

rGenerator.forBlock['text_join'] = function(block: Block, generator: RGenerator): [string, number] {
    const joinBlock = block as JoinMutatorBlock;
    // Create a string made up of any number of elements of any type.
    let code: string;
    switch (joinBlock.itemCount_) {
        case 0:
            code = '\"\"';
            return [code, Order.ATOMIC];
        case 1: {
            const element = generator.valueToCode(block, 'ADD0', Order.NONE) || '\"\"';
            code = forceString_(element);
            return [code, Order.FUNCTION_CALL];
        }
        case 2: {
            const element0 = generator.valueToCode(block, 'ADD0', Order.NONE) || '\"\"';
            const element1 = generator.valueToCode(block, 'ADD1', Order.NONE) || '\"\"';
            code = 'paste0(' + forceString_(element0) + ', ' +
                forceString_(element1) + ')';
            return [code, Order.ADDITION];
        }
        default: {
            const elements: string[] = new Array(joinBlock.itemCount_);
            for (let i = 0; i < joinBlock.itemCount_; i++) {
                elements[i] = generator.valueToCode(block, 'ADD' + i, Order.COMMA) || '\"\"';
            }
            code = 'paste0(' + elements.join(', ') + ')';
            return [code, Order.FUNCTION_CALL];
        }
    }
};


rGenerator.forBlock['text_append'] = function(block: Block, generator: RGenerator): string {
    // Append to a variable in place.
    const varName: string = generator.getVariableName(block.getFieldValue("VAR"));

    const value = generator.valueToCode(block, 'TEXT', Order.NONE) || '\"\"';
    return varName + ' <- paste0(' + varName + ', ' + forceString_(value) + ')\n';
};

rGenerator.forBlock['text_length'] = function(block: Block, generator: RGenerator): [string, number] {
    // String or array length.
    const text = generator.valueToCode(block, 'VALUE', Order.FUNCTION_CALL) || '\"\"';
    const code = 'nchar(' + text + ')';
    return [code, Order.MEMBER];
};

rGenerator.forBlock['text_isEmpty'] = function(block: Block, generator: RGenerator): [string, number] {
    // Is the string null or array empty?
    const text = generator.valueToCode(block, 'VALUE', Order.MEMBER) || '\"\"';
    const code = '(is.na(' + text + ') || ' + text + ' == "")';
    return [code, Order.LOGICAL_NOT];
};

rGenerator.forBlock['text_indexOf'] = function(block: Block, generator: RGenerator): [string, number] {
    // Search the text for a substring.
    const operator = block.getFieldValue('END') == 'FIRST' ?
        'indexOf' : 'lastIndexOf';
    const substring = generator.valueToCode(block, 'FIND', Order.NONE) || '\"\"';
    const text = generator.valueToCode(block, 'VALUE', Order.MEMBER) || '\"\"';
    let code = '';
    if (operator === 'indexOf') {
        code = 'regexpr(' + substring + ',' + text + ')';
    } else {
        const reverseText = 'paste(rev(strsplit(' + text + ', "")[[1]]),collapse="")';
        const reverseSubstring = 'paste(rev(strsplit(' + substring + ', "")[[1]]),collapse="")';
        code = 'nchar(' + text + ') + 1L - nchar(' + substring + ') + 1 - regexpr(' + reverseSubstring + ', ' + reverseText + ')';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['text_charAt'] = function(block: Block, generator: RGenerator): [string, number] {
    // Get letter at index.
    // Note: Until January 2013 this block did not have the WHERE input.
    const where = block.getFieldValue('WHERE') || 'FROM_START';
    const textOrder = (where == 'RANDOM') ? Order.NONE :
        Order.MEMBER;
    const text = generator.valueToCode(block, 'VALUE', textOrder) || '\"\"';
    let code = '';
    switch (where) {
        case 'FIRST':
            code = 'substr(' + text + ', 1, 1)';
            return [code, Order.FUNCTION_CALL];
        case 'LAST':
            code = 'substr(' + text + ', nchar(' + text + '), nchar(' + text + '))';
            return [code, Order.FUNCTION_CALL];
        case 'FROM_START':
            const at = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            code = 'substr(' + text + ', ' + at + ',' + at + ')';
            return [code, Order.FUNCTION_CALL];
        case 'FROM_END':
            const atEnd = generator.valueToCode(block, 'AT', Order.NONE) || '1';
            code = 'substr(' + text + ', nchar(' + text + ') - ' + atEnd + ', nchar(' + text + ') - ' + atEnd + ')';
            return [code, Order.FUNCTION_CALL];
        case 'RANDOM':
            const atRandom = 'sample(1:nchar(' + text + '),1)';
            code = 'substr(' + text + ', ' + atRandom + ',' + atRandom + ')';
            return [code, Order.FUNCTION_CALL];
    }
    throw Error('Unhandled option (text_charAt).');
};

/**
 * AO: internal only?
 * Returns an expression calculating the index into a string.
 * @param {string} stringName Name of the string, used to calculate length.
 * @param {string} where The method of indexing, selected by dropdown in Blockly
 * @param {string=} opt_at The optional offset when indexing from start/end.
 * @return {string} Index expression.
 * @private
 */
// const text_getIndex_ = function (stringName: string, where: string, opt_at?: string): string {
//     if (where == 'FIRST') {
//         return '0';
//     } else if (where == 'FROM_END') {
//         return stringName + '.length - 1 - ' + opt_at;
//     } else if (where == 'LAST') {
//         return stringName + '.length - 1';
//     } else {
//         return opt_at || '';
//     }
// };

rGenerator.forBlock['text_getSubstring'] = function(block: Block, generator: RGenerator): [string, number] {
    // Get substring.
    const text = generator.valueToCode(block, 'STRING', Order.FUNCTION_CALL) || '\"\"';
    const where1 = block.getFieldValue('WHERE1');
    const where2 = block.getFieldValue('WHERE2');
    let code = '';
    if (where1 == 'FIRST' && where2 == 'LAST') {
        code = text;
    } else {
        // If the text is a variable or literal or doesn't require a call for
        // length, don't generate a helper function.
        let at1 = '';
        let at2 = '';
        switch (where1) {
            case 'FROM_START':
                at1 = generator.valueToCode(block, 'AT1', Order.NONE) || '1';
                break;
            case 'FROM_END':
                at1 = generator.valueToCode(block, 'AT1', Order.NONE) || '1';
                at1 = 'nchar(' + text + ') - ' + at1;
                break;
            case 'FIRST':
                at1 = '0';
                break;
            default:
                throw Error('Unhandled option (text_getSubstring).');
        }
        switch (where2) {
            case 'FROM_START':
                at2 = generator.valueToCode(block, 'AT2', Order.NONE) || '1';
                break;
            case 'FROM_END':
                at2 = generator.valueToCode(block, 'AT2', Order.NONE) || '1';
                at2 = 'nchar(' + text + ') - ' + at2;
                break;
            case 'LAST':
                at2 = 'nchar(' + text + ')';
                break;
            default:
                throw Error('Unhandled option (text_getSubstring).');
        }
        code = 'substr(' + text + ', ' + at1 + ', ' + at2 + ')';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['text_changeCase'] = function(block: Block, generator: RGenerator): [string, number] {
    // Change capitalization.
    const operator = block.getFieldValue('CASE');
    const textOrder = operator ? Order.MEMBER : Order.NONE;
    const text = generator.valueToCode(block, 'TEXT', textOrder) || '\"\"';
    let code = '';
    if (operator === 'UPPERCASE') {
        code = 'toupper(' + text + ')';
    } else if (operator === 'LOWERCASE') {
        code = 'tolower(' + text + ')';
    } else {
        code = 'tools::toTitleCase(' + text + ')';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['text_trim'] = function(block: Block, generator: RGenerator): [string, number] {
    // Trim spaces.
    const operator = block.getFieldValue('MODE');
    const text = generator.valueToCode(block, 'TEXT', Order.MEMBER) || '\"\"';
    let code = '';
    if (operator === 'LEFT') {
        code = 'trimws(' + text + ', "left")';
    } else if (operator === 'RIGHT') {
        code = 'trimws(' + text + ', "right")';
    } else {
        code = 'trimws(' + text + ', "both")';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['text_print'] = function(block: Block, generator: RGenerator): string {
    // Print statement.
    const msg = generator.valueToCode(block, 'TEXT', Order.NONE) || '\"\"';
    return 'print(' + msg + ');\n';
};

rGenerator.forBlock['text_prompt_ext'] = function(block: Block, generator: RGenerator): [string, number] {
    // Prompt function.
    let msg = '';
    if (block.getField('TEXT')) {
        // Internal message.
        msg = generator.quote_(block.getFieldValue('TEXT'));
    } else {
        // External message.
        msg = generator.valueToCode(block, 'TEXT', Order.NONE) || '\"\"';
    }
    let code = 'readline(' + msg + ')';
    const toNumber = block.getFieldValue('TYPE') == 'NUMBER';
    if (toNumber) {
        code = 'as.numeric(' + code + ')';
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['text_prompt'] = rGenerator.forBlock['text_prompt_ext'];

rGenerator.forBlock['text_count'] = function(block: Block, generator: RGenerator): [string, number] {
    const text = generator.valueToCode(block, 'TEXT', Order.MEMBER) || '\"\"';
    const sub = generator.valueToCode(block, 'SUB', Order.NONE) || '\"\"';
    const code = 'lengths(regmatches(' + text + ', gregexpr(' + sub + ', ' + text + ')))';
    return [code, Order.SUBTRACTION];
};

rGenerator.forBlock['text_replace'] = function(block: Block, generator: RGenerator): [string, number] {
    const text = generator.valueToCode(block, 'TEXT', Order.MEMBER) || '\"\"';
    const from = generator.valueToCode(block, 'FROM', Order.NONE) || '\"\"';
    const to = generator.valueToCode(block, 'TO', Order.NONE) || '\"\"';
    const code = 'gsub(' + to + ',' + from + ',' + text + ',fixed=TRUE)';
    return [code, Order.MEMBER];
};

rGenerator.forBlock['text_reverse'] = function(block: Block, generator: RGenerator): [string, number] {
    const text = generator.valueToCode(block, 'TEXT', Order.MEMBER) || '\"\"';
    const code = 'paste(rev(strsplit(' + text + ', "")[[1]]),collapse="")';
    return [code, Order.MEMBER];
};

//***********************************************************************
//math.js

rGenerator.forBlock['math_number'] = function(block: Block, generator: RGenerator): [string | number, number] {
    // Numeric value.
    const code = Number(block.getFieldValue('NUM'));
    if (code == Infinity) {
        return ['Inf', Order.ATOMIC];
    } else if (code == -Infinity) {
        return ['-Inf', Order.ATOMIC];
    }
    const order = code >= 0 ? Order.ATOMIC : Order.UNARY_NEGATION;
    return [code, order];
};

rGenerator.forBlock['math_arithmetic'] = function(block: Block, generator: RGenerator): [string, number] {
    // Basic arithmetic operators, and power.
    const OPERATORS: { [key: string]: [string, number] } = {
        'ADD': [' + ', Order.ADDITION],
        'MINUS': [' - ', Order.SUBTRACTION],
        'MULTIPLY': [' * ', Order.MULTIPLICATION],
        'DIVIDE': [' / ', Order.DIVISION],
        'POWER': [' ^ ', Order.EXPONENTIATION]
    };
    const tuple = OPERATORS[block.getFieldValue('OP')];
    const operator = tuple[0];
    const order = tuple[1];
    const argument0 = generator.valueToCode(block, 'A', order) || '0';
    const argument1 = generator.valueToCode(block, 'B', order) || '0';
    const code = argument0 + operator + argument1;
    return [code, order];
};

rGenerator.forBlock['math_single'] = function(block: Block, generator: RGenerator): [string, number] {
    // Math operators with single operand.
    const operator = block.getFieldValue('OP');
    let code = '';
    let arg = '';
    if (operator == 'NEG') {
        // Negation is a special case given its different operator precedence.
        arg = generator.valueToCode(block, 'NUM', Order.UNARY_NEGATION) || '0';
        code = '-' + arg;
        return [code, Order.UNARY_NEGATION];
    }
    if (operator == 'SIN' || operator == 'COS' || operator == 'TAN') {
        arg = generator.valueToCode(block, 'NUM', Order.DIVISION) || '0';
    } else {
        arg = generator.valueToCode(block, 'NUM', Order.NONE) || '0';
    }
    // First, handle cases which generate values that don't need parentheses
    // wrapping the code.
    switch (operator) {
        case 'ABS':
            code = 'abs(' + arg + ')';
            break;
        case 'ROOT':
            code = 'sqrt(' + arg + ')';
            break;
        case 'LN':
            code = 'log(' + arg + ')';
            break;
        case 'EXP':
            code = 'exp(' + arg + ')';
            break;
        case 'POW10':
            code = '10 ** ' + arg;
            break;
        case 'ROUND':
            code = 'round(' + arg + ')';
            break;
        case 'ROUNDUP':
            code = 'ceiling(' + arg + ')';
            break;
        case 'ROUNDDOWN':
            code = 'floor(' + arg + ')';
            break;
        case 'SIN':
            code = 'sin(' + arg + ' *pi/180)';
            break;
        case 'COS':
            code = 'cos(' + arg + ' *pi/180)';
            break;
        case 'TAN':
            code = 'tan(' + arg + ' *pi/180)';
            break;
    }
    if (code) {
        return [code, Order.FUNCTION_CALL];
    }
    // Second, handle cases which generate values that may need parentheses
    // wrapping the code.
    switch (operator) {
        case 'LOG10':
            code = 'log10(' + arg + ')';
            break;
        case 'ASIN':
            code = 'asin(' + arg + ' *pi/180)';
            break;
        case 'ACOS':
            code = 'acos(' + arg + ' *pi/180)';
            break;
        case 'ATAN':
            code = 'atan(' + arg + ' *pi/180)';
            break;
        default:
            throw Error('Unknown math operator: ' + operator);
    }
    return [code, Order.DIVISION];
};

rGenerator.forBlock['math_constant'] = function(block: Block, generator: RGenerator): [string, number] {
    // Constants: PI, E, the Golden Ratio, sqrt(2), 1/sqrt(2), INFINITY.
    const CONSTANTS: { [key: string]: [string, number] } = {
        'PI': ['pi', Order.MEMBER],
        'E': ['exp(1)', Order.MEMBER],
        'GOLDEN_RATIO': ['(1 + sqrt(5)) / 2', Order.DIVISION],
        'SQRT2': ['sqrt(2)', Order.MEMBER],
        'SQRT1_2': ['sqrt(.5)', Order.MEMBER],
        'INFINITY': ['Inf', Order.ATOMIC]
    };
    return CONSTANTS[block.getFieldValue('CONSTANT')];
};

rGenerator.forBlock['math_number_property'] = function(block: Block, generator: RGenerator): [string, number] {
    // Check if a number is even, odd, prime, whole, positive, or negative
    // or if it is divisible by certain number. Returns true or false.
    const number_to_check = generator.valueToCode(block, 'NUMBER_TO_CHECK', Order.MODULUS) || '0';
    const dropdown_property = block.getFieldValue('PROPERTY');
    let code = '';
    if (dropdown_property == 'PRIME') {
        code = number_to_check + ' == 2L || all(' + number_to_check + ' %% 2L:max(2,floor(sqrt(' + number_to_check + '))) != 0)';
        return [code, Order.FUNCTION_CALL];
    }
    switch (dropdown_property) {
        case 'EVEN':
            code = number_to_check + ' %% 2 == 0';
            break;
        case 'ODD':
            code = number_to_check + ' %% 2 == 1';
            break;
        case 'WHOLE':
            code = number_to_check + ' %% 1 == 0';
            break;
        case 'POSITIVE':
            code = number_to_check + ' > 0';
            break;
        case 'NEGATIVE':
            code = number_to_check + ' < 0';
            break;
        case 'DIVISIBLE_BY':
            const divisor = generator.valueToCode(block, 'DIVISOR', Order.MODULUS) || '0';
            code = number_to_check + ' %% ' + divisor + ' == 0';
            break;
    }
    return [code, Order.EQUALITY];
};

rGenerator.forBlock['math_change'] = function(block: Block, generator: RGenerator): string {
    // Add to a variable in place.
    const argument0 = generator.valueToCode(block, 'DELTA', Order.ADDITION) || '0';
    const varName: string = generator.getVariableName(block.getFieldValue("VAR"));
    return varName + ' = ifelse(length(' + varName + ')>0 & is.numeric(' + varName + '),' + varName + ' + ' + argument0 + ',' + argument0 + ')';
};


// Rounding functions have a single operand.
rGenerator.forBlock['math_round'] = rGenerator.forBlock['math_single'];
// Trigonometry functions have a single operand.
rGenerator.forBlock['math_trig'] = rGenerator.forBlock['math_single'];

rGenerator.forBlock['math_on_list'] = function(block: Block, generator: RGenerator): [string, number] {
    // Math functions for lists.
    const func = block.getFieldValue('OP');
    let list, code;
    switch (func) {
        case 'SUM':
            list = generator.valueToCode(block, 'LIST', Order.MEMBER) || 'list()';
            code = 'sum(unlist(' + list + '))';
            break;
        case 'MIN':
            list = generator.valueToCode(block, 'LIST', Order.COMMA) || 'list()';
            code = 'min(unlist(' + list + '))';
            break;
        case 'MAX':
            list = generator.valueToCode(block, 'LIST', Order.COMMA) || 'list()';
            code = 'max(unlist(' + list + '))';
            break;
        case 'AVERAGE':
            list = generator.valueToCode(block, 'LIST', Order.NONE) || 'list()';
            code = 'mean(unlist(' + list + '))';
            break;
        case 'MEDIAN':
            list = generator.valueToCode(block, 'LIST', Order.NONE) || 'list()';
            code = 'median(unlist(' + list + '))';
            break;
        case 'MODE':
            list = generator.valueToCode(block, 'LIST', Order.NONE) || 'list()';
            code = 'unique(unlist(' + list + '))[which.max(tabulate(match(' + list + ', unique(unlist(' + list + ')))))]';
            break;
        case 'STD_DEV':
            list = generator.valueToCode(block, 'LIST', Order.NONE) || 'list()';
            code = 'sd(unlist(' + list + '))';
            break;
        case 'RANDOM':
            list = generator.valueToCode(block, 'LIST', Order.NONE) || 'list()';
            code = 'list[sample(1:length(' + list + '),1)]';
            break;
        default:
            throw Error('Unknown operator: ' + func);
    }
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['math_modulo'] = function(block: Block, generator: RGenerator): [string, number] {
    // Remainder computation.
    const argument0 = generator.valueToCode(block, 'DIVIDEND', Order.MODULUS) || '0';
    const argument1 = generator.valueToCode(block, 'DIVISOR', Order.MODULUS) || '0';
    const code = argument0 + ' %% ' + argument1;
    return [code, Order.MODULUS];
};

rGenerator.forBlock['math_constrain'] = function(block: Block, generator: RGenerator): [string, number] {
    // Constrain a number between two limits.
    const argument0 = generator.valueToCode(block, 'VALUE', Order.COMMA) || '0';
    const argument1 = generator.valueToCode(block, 'LOW', Order.COMMA) || '0';
    const argument2 = generator.valueToCode(block, 'HIGH', Order.COMMA) || 'Inf';
    const code = 'min(max(' + argument0 + ', ' + argument1 + '), ' + argument2 + ')';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['math_random_int'] = function(block: Block, generator: RGenerator): [string, number] {
    // Random integer between [X] and [Y].
    const argument0 = generator.valueToCode(block, 'FROM', Order.COMMA) || '0';
    const argument1 = generator.valueToCode(block, 'TO', Order.COMMA) || '0';
    const code = 'sample(' + argument0 + ':' + argument1 + ',1)';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['math_random_float'] = function(block: Block, generator: RGenerator): [string, number] {
    // Random fraction between 0 and 1.
    return ['runif(1,0,1)', Order.FUNCTION_CALL];
};

rGenerator.forBlock['math_atan2'] = function(block: Block, generator: RGenerator): [string, number] {
    // Arctangent of point (X, Y) in degrees from -180 to 180.
    const argument0 = generator.valueToCode(block, 'X', Order.COMMA) || '0';
    const argument1 = generator.valueToCode(block, 'Y', Order.COMMA) || '0';
    return ['atan2(' + argument1 + ', ' + argument0 + ') / pi * 180', Order.DIVISION];
};

//***********************************************************************
//variables.js

rGenerator.forBlock['variables_get'] = function(block: Block, generator: RGenerator): [string, number] {
    // Variable getter.
    const code: string = generator.getVariableName(block.getFieldValue("VAR"));
    return [code, Order.ATOMIC];
};

rGenerator.forBlock['variables_set'] = function(block: Block, generator: RGenerator): string {
    // Variable setter.
    const argument0 = generator.valueToCode(block, 'VALUE', Order.NONE) || '0';
    const varName: string = generator.getVariableName(block.getFieldValue("VAR"));
    return varName + ' = ' + argument0 + '\n';
};

//***********************************************************************
//variables_dynamic.js

// AO: not sure what this does...
// R is dynamically typed.
rGenerator.forBlock['variables_get_dynamic'] = rGenerator.forBlock['variables_get'];
rGenerator.forBlock['variables_set_dynamic'] = rGenerator.forBlock['variables_set'];

//***********************************************************************
//logic.js

rGenerator.forBlock['controls_if'] = function(block: Block, generator: RGenerator): string {
    // If/elseif/else condition.
    let n = 0;
    let code = '', branchCode, conditionCode;
    if (generator.STATEMENT_PREFIX) {
        // Automatic prefix insertion is switched off for this block.  Add manually.
        code += generator.injectId(generator.STATEMENT_PREFIX, block);
    }
    do {
        conditionCode = generator.valueToCode(block, 'IF' + n, Order.NONE) || 'FALSE';
        branchCode = generator.statementToCode(block, 'DO' + n);
        if (generator.STATEMENT_SUFFIX) {
            branchCode = generator.prefixLines(generator.injectId(generator.STATEMENT_SUFFIX, block), generator.INDENT) + branchCode;
        }
        code += (n > 0 ? ' else ' : '') + 'if (' + conditionCode + ') {\n' + branchCode + '}';
        ++n;
    } while (block.getInput('IF' + n));

    if (block.getInput('ELSE') || generator.STATEMENT_SUFFIX) {
        branchCode = generator.statementToCode(block, 'ELSE');
        if (generator.STATEMENT_SUFFIX) {
            branchCode = generator.prefixLines(generator.injectId(generator.STATEMENT_SUFFIX, block), generator.INDENT) + branchCode;
        }
        code += ' else {\n' + branchCode + '}';
    }
    return code + '\n';
};

rGenerator.forBlock['controls_ifelse'] = rGenerator.forBlock['controls_if'];

rGenerator.forBlock['logic_compare'] = function(block: Block, generator: RGenerator): [string, number] {
    // Comparison operator.
    const OPERATORS: Record<string, string> = {
        'EQ': '==',
        'NEQ': '!=',
        'LT': '<',
        'LTE': '<=',
        'GT': '>',
        'GTE': '>='
    };
    const operator = OPERATORS[block.getFieldValue('OP')];
    const order = (operator == '==' || operator == '!=') ? Order.EQUALITY : Order.RELATIONAL;
    const argument0 = generator.valueToCode(block, 'A', order) || '0';
    const argument1 = generator.valueToCode(block, 'B', order) || '0';
    const code = argument0 + ' ' + operator + ' ' + argument1;
    return [code, order];
};

rGenerator.forBlock['logic_operation'] = function(block: Block, generator: RGenerator): [string, number] {
    // Operations 'and', 'or'.
    const operator = (block.getFieldValue('OP') == 'AND') ? '&&' : '||'; //AO: R has both & and &&; && seems appropriate here
    const order = (operator == '&&') ? Order.LOGICAL_AND : Order.LOGICAL_OR;
    let argument0 = generator.valueToCode(block, 'A', order);
    let argument1 = generator.valueToCode(block, 'B', order);
    if (!argument0 && !argument1) {
        // If there are no arguments, then the return value is false.
        argument0 = 'FALSE';
        argument1 = 'FALSE';
    } else {
        // Single missing arguments have no effect on the return value.
        const defaultArgument = (operator == '&&') ? 'TRUE' : 'FALSE';
        if (!argument0) {
            argument0 = defaultArgument;
        }
        if (!argument1) {
            argument1 = defaultArgument;
        }
    }
    const code = argument0 + ' ' + operator + ' ' + argument1;
    return [code, order];
};

rGenerator.forBlock['logic_negate'] = function(block: Block, generator: RGenerator): [string, number] {
    // Negation.
    const order = Order.LOGICAL_NOT;
    const argument0 = generator.valueToCode(block, 'BOOL', order) || 'TRUE';
    const code = '!' + argument0;
    return [code, order];
};


rGenerator.forBlock['logic_boolean'] = function(block: Block, generator: RGenerator): [string, number] {
    // Boolean values true and false.
    const code = (block.getFieldValue('BOOL') == 'TRUE') ? 'TRUE' : 'FALSE';
    return [code, Order.ATOMIC];
};

rGenerator.forBlock['logic_null'] = function(block: Block, generator: RGenerator): [string, number] {
    // Null data type.
    return ['NULL', Order.ATOMIC];
};

rGenerator.forBlock['logic_ternary'] = function(block: Block, generator: RGenerator): [string, number] {
    // Ternary operator.
    const value_if = generator.valueToCode(block, 'IF', Order.CONDITIONAL) || 'FALSE';
    const value_then = generator.valueToCode(block, 'THEN', Order.CONDITIONAL) || 'NULL';
    const value_else = generator.valueToCode(block, 'ELSE', Order.CONDITIONAL) || 'NULL';
    const code = 'ifelse(' + value_if + ', ' + value_then + ', ' + value_else + ')';
    return [code, Order.CONDITIONAL];
};

//***********************************************************************
//loops.js

rGenerator.forBlock['controls_repeat_ext'] = function(block: Block, generator: RGenerator): string {
    // Repeat n times.
    let repeats;
    if (block.getField('TIMES')) {
        // Internal number.
        repeats = String(parseInt(block.getFieldValue('TIMES'), 10));
    } else {
        // External number.
        repeats = generator.valueToCode(block, 'TIMES', Order.NONE) || '0';
    }
    if (Blockly.utils.string.isNumber(repeats)) {
        repeats = parseInt(repeats, 10);
    } else {
        repeats = 'strtoi(' + repeats + ')';
    }
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block);
    // const loopVar: string = generator.getVariableName(block.getFieldValue("count"));
    const loopVar: string | undefined = generator.nameDB_?.getDistinctName('count', Blockly.Names.NameType.VARIABLE);
    const code = 'for (' + loopVar + ' in 1:' + repeats + ') {\n' + branch + '}\n';
    return code;
};

rGenerator.forBlock['controls_repeat'] = rGenerator.forBlock['controls_repeat_ext'];

rGenerator.forBlock['controls_whileUntil'] = function(block: Block, generator: RGenerator): string {
    // Do while/until loop.
    const until = block.getFieldValue('MODE') == 'UNTIL';
    let argument0 = generator.valueToCode(block, 'BOOL', until ? Order.LOGICAL_NOT : Order.NONE) || 'FALSE';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block);
    if (until) {
        argument0 = '!' + argument0;
    }
    return 'while (' + argument0 + ') {\n' + branch + '}\n';
};

rGenerator.forBlock['controls_for'] = function(block: Block, generator: RGenerator): string {
    // For loop.
    const variable0: string = generator.getVariableName(block.getFieldValue("VAR"));
    const argument0 = generator.valueToCode(block, 'FROM', Order.ASSIGNMENT) || '0';
    const argument1 = generator.valueToCode(block, 'TO', Order.ASSIGNMENT) || '0';
    const increment = generator.valueToCode(block, 'BY', Order.ASSIGNMENT) || '1';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block);
    const code = 'for (' + variable0 + ' in seq(from=' + argument0 + ', to=' + argument1 + ', by=' + increment + ')) {\n' + branch + '}\n';
    return code;
};

rGenerator.forBlock['controls_forEach'] = function(block: Block, generator: RGenerator): string {
    // For each loop.
    const variable0: string = generator.getVariableName(block.getFieldValue("VAR"));
    const argument0 = generator.valueToCode(block, 'LIST', Order.ASSIGNMENT) || 'list()';
    let branch = generator.statementToCode(block, 'DO');
    branch = generator.addLoopTrap(branch, block);
    const code = 'for (' + variable0 + ' in ' + argument0 + ') {\n' + branch + '}\n';
    return code;
};

rGenerator.forBlock['controls_flow_statements'] = function(block: Block, generator: RGenerator): string {
    // Flow statements: continue, break.
    let xfix = '';
    if (generator.STATEMENT_PREFIX) {
        xfix += generator.injectId(generator.STATEMENT_PREFIX, block);
    }
    if (generator.STATEMENT_SUFFIX) {
        xfix += generator.injectId(generator.STATEMENT_SUFFIX, block);
    }
    if (generator.STATEMENT_PREFIX) {
        // AO: easier to disable this check that recreate type
        // @ts-ignore
        const loop = block.getSurroundLoop();
        // const loop = (block as ControlFlowInLoopBlock).getSurroundLoop();
        if (loop && !loop.suppressPrefixSuffix) {
            xfix += generator.injectId(generator.STATEMENT_PREFIX, loop);
        }
    }
    switch (block.getFieldValue('FLOW')) {
        case 'BREAK':
            return xfix + 'break\n';
        case 'CONTINUE':
            return xfix + 'next\n';
    }
    throw Error('Unknown flow statement.');
};

//***********************************************************************
//procedures.js

rGenerator.forBlock['procedures_defreturn'] = function(block: Block, generator: RGenerator): string {
    // Define a procedure with a return value.
    const funcName: string = generator.getVariableName(block.getFieldValue("VAR"));
    let xfix1 = '';
    if (generator.STATEMENT_PREFIX) {
        xfix1 += generator.injectId(generator.STATEMENT_PREFIX, block);
    }
    if (generator.STATEMENT_SUFFIX) {
        xfix1 += generator.injectId(generator.STATEMENT_SUFFIX, block);
    }
    if (xfix1) {
        xfix1 = generator.prefixLines(xfix1, generator.INDENT);
    }
    let loopTrap = '';
    if (generator.INFINITE_LOOP_TRAP) {
        loopTrap = generator.prefixLines(generator.injectId(generator.INFINITE_LOOP_TRAP, block), generator.INDENT);
    }
    let branch = generator.statementToCode(block, 'STACK');
    let returnValue = generator.valueToCode(block, 'RETURN', Order.NONE) || '';
    let xfix2 = '';
    if (branch && returnValue) {
        xfix2 = xfix1;
    }
    if (returnValue) {
        returnValue = generator.INDENT + 'return(' + returnValue + ')';
    }
    const args = [];
    const variables = block.getVars();
    for (let i = 0; i < variables.length; i++) {
        args[i] = generator.getVariableName(variables[i]);
    }
    let code = funcName + ' <- function(' + args.join(', ') + ') {\n' + xfix1 + loopTrap + branch + xfix2 + returnValue + '}\n';
    code = generator.scrub_(block, code);
    // Add % so as not to collide with helper functions in definitions list.
    // AO current API seems to hack this "(generator as AnyDuringMigration).definitions_['%' + funcName] = code;"
    // @ts-ignore
    generator.definitions_['%' + funcName] = code;
    return '';
};

// Defining a procedure without a return value uses the same generator as
// a procedure with a return value.
rGenerator.forBlock['procedures_defnoreturn'] = rGenerator.forBlock['procedures_defreturn'];

rGenerator.forBlock['procedures_callreturn'] = function(block: Block, generator: RGenerator): [string, number] {
    // Call a procedure with a return value.
    const funcName: string = generator.getVariableName(block.getFieldValue("NAME"));
    const args = [];
    const variables = block.getVars();
    for (let i = 0; i < variables.length; i++) {
        args[i] = generator.valueToCode(block, 'ARG' + i, Order.COMMA) || 'NULL';
    }
    const code = funcName + '(' + args.join(', ') + ')';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['procedures_callnoreturn'] = function(block: Block, generator: RGenerator): string {
    // Call a procedure with no return value.
    // Generated code is for a function call as a statement is the same as a
    // function call as a value, with the addition of line ending.
    const tuple = rGenerator['procedures_callreturn'](block, generator);
    return tuple[0] + '\n';
};

rGenerator.forBlock['procedures_ifreturn'] = function(block: Block, generator: RGenerator): string {
    // Conditionally return value from a procedure.
    const condition = generator.valueToCode(block, 'CONDITION', Order.NONE) || 'FALSE';
    let code = 'if (' + condition + ') {\n';
    if (generator.STATEMENT_SUFFIX) {
        // Inject any statement suffix here since the regular one at the end
        // will not get executed if the return is triggered.
        code += generator.prefixLines(generator.injectId(generator.STATEMENT_SUFFIX, block), generator.INDENT);
    }
    // AO: another case where the type is not exported and it is less
    // messy to disable checks than recreate the type
    // @ts-ignore
    if (block.hasReturnValue_) {
        const value = generator.valueToCode(block, 'VALUE', Order.NONE) || 'NULL';
        code += generator.INDENT + 'return(' + value + ')\n';
    } else {
        code += generator.INDENT + 'return(NULL)\n'; //AO: R returns last expression event without a return statement. If we return NULL, we *might* achieve the desired behavior
    }
    code += '}\n';
    return code;
};
//***********************************************************************
//colour.js

rGenerator.forBlock['colour_picker'] = function(block: Block, generator: RGenerator): [string, number] {
    // Colour picker.
    const code = generator.quote_(block.getFieldValue('COLOUR'));
    return [code, Order.ATOMIC];
};

rGenerator.forBlock['colour_random'] = function(block: Block, generator: RGenerator): [string, number] {
    // Generate a random colour.
    const code = 'rgb(sample(1:255,1),sample(1:255,1),sample(1:255,1),maxColorValue=255)';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['colour_rgb'] = function(block: Block, generator: RGenerator): [string, number] {
    // Compose a colour from RGB components expressed as percentages.
    const red = generator.valueToCode(block, 'RED', Order.COMMA) || '0';
    const green = generator.valueToCode(block, 'GREEN', Order.COMMA) || '0';
    const blue = generator.valueToCode(block, 'BLUE', Order.COMMA) || '0';
    const code = 'rgb(' + red + ', ' + green + ', ' + blue + ',maxColorValue=255)';
    return [code, Order.FUNCTION_CALL];
};

rGenerator.forBlock['colour_blend'] = function(block: Block, generator: RGenerator): [string, number] {
    // Blend two colours together.
    const c1 = generator.valueToCode(block, 'COLOUR1', Order.COMMA) || '\'#000000\'';
    const c2 = generator.valueToCode(block, 'COLOUR2', Order.COMMA) || '\'#000000\'';
    const ratio = generator.valueToCode(block, 'RATIO', Order.COMMA) || 0.5;
    //AO: this could reasonably be a function, but avoiding that because of current function handling issues
    const code = 'c1 <- col2rgb(' + c1 + ')\n' +
        'c2 <- col2rgb(' + c2 + ')\n' +
        'r <- sqrt((1 - ' + ratio + ') * c1[1]^2 + ' + ratio + '* c2[1]^2)\n' +
        'g <- sqrt((1 - ' + ratio + ') * c1[2]^2 + ' + ratio + '* c2[2]^2)\n' +
        'b <- sqrt((1 - ' + ratio + ') * c1[3]^2 + ' + ratio + '* c2[3]^2)\n' +
        'rgb(r,g,b,maxColorValue=255)';
    return [code, Order.FUNCTION_CALL];
};

