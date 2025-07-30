import { ILayoutRestorer, JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { Widget } from '@lumino/widgets';
import { INotebookTracker, NotebookPanel } from "@jupyterlab/notebook";
import { Cell } from "@jupyterlab/cells";
import { showDialog } from '@jupyterlab/apputils';
// import { markdownIcon, runIcon } from '@jupyterlab/ui-components';
import * as Blockly from 'blockly/core';
import { ICommandPalette, MainAreaWidget, IWidgetTracker, ISessionContext, WidgetTracker } from '@jupyterlab/apputils';
import * as cells from "@jupyterlab/cells";
import { ICellModel } from "@jupyterlab/cells";
import { Kernel, Session, KernelMessage } from "@jupyterlab/services";
import { DocumentRegistry } from "@jupyterlab/docregistry";
import { CommandRegistry } from "@lumino/commands";
import { IToolbox } from "./AbstractToolbox";
import { PythonToolbox } from "./PythonToolbox";
import { RToolbox } from "./RToolbox";
import {getLLMReactComponent} from "./LLMReactComponent";
import { LogToServer, createJupyterLogEntry, createBlocklyLogEntry, set_id, set_log_url } from './Logging';
import { llm_explain_code, llm_explain_error, llm_next_step_hint } from './LLMClient';
import { explainCodeIcon, explainErrorIcon as explainErrorIcon, nextStepHintIcon } from './LLMClient';
import { BlockChange } from 'blockly/core/events/events_block_change';
// We have to load this extension well after blockly to avoid "Extension "text_join_mutator" is already registered"
// I believe this is because core blockly has text_join_mutator, which this overwrites. If this registers it first,
// then core blockly throws an unrecoverable error when it tries to register text_join_mutator
import '@blockly/block-plus-minus';
import '@blockly/toolbox-search';
import {
  ScrollOptions,
  ScrollBlockDragger,
  ScrollMetricsManager,
} from '@blockly/plugin-scroll-options';
import { ChangeObject, diffLines } from 'diff';
import markdownit from 'markdown-it';
// import { error } from 'console';

// TODO: seems like logging is not wired up throughout

//for converting LLM markdown to HTML
const markdown_it = markdownit()

/**
 * BlocklyWidget is a wrapper for Blockly. It does all the integration between Blockly and Jupyter. Language specific issues are handled by respective geneators and toolboxes
 */
export class BlocklyWidget extends Widget {
  /**
   * Notebooks we have open
   */
  notebooks: INotebookTracker;
  /**
   * Blockly workspace (basically Blockly session state)
   */
  workspace: Blockly.WorkspaceSvg | null;
  /**
   * Toolbox defining most blockly behavior, including language specific behavior
   */
  toolbox: IToolbox | null;
  /**
   * Flag for  whether the widget is attached to Jupyter
   */
  notHooked: boolean
  /**
   * Language generator in use
   */
  generator: any;
  /** 
   * last cell for blocks to code state managment
   */
  lastCell: Cell | null;
  /** 
   * blocks rendered flag for state managment. Set to false every time a block is created. Set to true when blocks have been deserialized OR have been serialized
   */
  blocksInSyncWithXML: boolean;
  /**
   * State for user setting of auto code execution, i.e. automatically executing code when blocks change
   */
  doAutoCodeExecution: boolean;
  /**
   * Track whether we are currently deserializing blocks as this affects how we handle some events
   */
  deserializingFlag: boolean;
  /**
   * Parser for Blockly XML
   */
  domParser: DOMParser;
  /**
   * Only do auto code gen for these block events
   */
  codeGenBlockEvents: Set<string>;
  /**
   * API key for commercial LLM, stored in user settings
   */
  llm_api_key: string;


  constructor(notebooks: INotebookTracker) {
    super();

    //--------------------
    // Initialize state
    //--------------------
    //track notebooks
    this.notebooks = notebooks;

    //listen for notebook cell changes
    this.notebooks.activeCellChanged.connect(this.onActiveCellChanged(), this);

    //set initial state
    this.lastCell = null;
    this.blocksInSyncWithXML = false;
    this.doAutoCodeExecution = true;
    this.deserializingFlag = false;
    this.domParser = new DOMParser();
    this.workspace = null;
    this.toolbox = null;
    this.notHooked = true;
    this.llm_api_key = "";

    //define block events that trigger code gen
    this.codeGenBlockEvents = new Set([
      Blockly.Events.BLOCK_CHANGE,
      Blockly.Events.BLOCK_CREATE,
      Blockly.Events.BLOCK_DELETE,
      Blockly.Events.BLOCK_MOVE,
      Blockly.Events.VAR_RENAME,
      Blockly.Events.FINISHED_LOADING,
    ]);

    //---------------------
    // Widget UI in Jupyter
    //---------------------
    //div to hold blockly
    const div: HTMLDivElement = document.createElement("div");

    //initial size will be immediately resized
    div.setAttribute("style", "height: 480px; width: 600px;");

    //id for debug and to refer to during injection
    div.id = "blocklyDivPoly";
    this.node.appendChild(div);

    //div for buttons    
    const buttonDiv: HTMLDivElement = document.createElement("div");
    buttonDiv.id = "buttonDivPoly";

    //button to trigger code generation
    const blocksToCodeButton: HTMLButtonElement = document.createElement("button");
    blocksToCodeButton.innerText = "Blocks to Code";
    blocksToCodeButton.addEventListener("click", (_arg: any): void => {
      this.BlocksToCode(this.notebooks.activeCell, true);
    });
    buttonDiv.appendChild(blocksToCodeButton);

    //button to reverse xml to blocks
    const codeToBlocksButton: HTMLButtonElement = document.createElement("button");
    codeToBlocksButton.innerText = "Code to Blocks";
    codeToBlocksButton.addEventListener("click", (_arg_1: any): void => {
      this.DeserializeBlocksFromXMLSelector();
    });
    buttonDiv.appendChild(codeToBlocksButton);

    //button for bug reports
    const bugReportButton: HTMLButtonElement = document.createElement("button");
    bugReportButton.innerText = "Report Bug";
    bugReportButton.addEventListener("click", (_arg_2: any): void => {
      const win: any = window.open("https://jupyterlab-blockly-polyglot-extension/issues", "_blank");
      win.focus();
    });
    buttonDiv.appendChild(bugReportButton);

    //checkbox for JLab sync (if cell is selected and has serialized blocks, decode them to workspace; if cell is empty, empty workspace)
    const syncCheckbox: HTMLInputElement = document.createElement("input");
    syncCheckbox.setAttribute("type", "checkbox");
    syncCheckbox.checked = true;
    syncCheckbox.id = "syncCheckboxPoly";
    const syncCheckboxLabel: HTMLLabelElement = document.createElement("label");
    syncCheckboxLabel.innerText = "Notebook Sync";
    syncCheckboxLabel.setAttribute("for", "syncCheckboxPoly");
    buttonDiv.appendChild(syncCheckbox);
    buttonDiv.appendChild(syncCheckboxLabel);

    //checkbox for automatically generating code when blocks changed (auto blocks to code)
    const autoCodeExecutionCheckbox: HTMLInputElement = document.createElement("input");
    autoCodeExecutionCheckbox.setAttribute("type", "checkbox");
    autoCodeExecutionCheckbox.checked = true;
    autoCodeExecutionCheckbox.id = "autoCodeGenCheckboxPoly";
    const autoCodeExecutionCheckboxLabel: HTMLLabelElement = document.createElement("label");
    autoCodeExecutionCheckboxLabel.innerText = "Auto Execution";
    autoCodeExecutionCheckboxLabel.setAttribute("for", "autoCodeGenCheckboxPoly");
    const autoCodeExecutionCheckboxListener = (event: Event): void => {
      const target = event.target as HTMLInputElement;
      if (target != null) this.doAutoCodeExecution = target.checked;
      this.LogToConsole("auto code execution state is now " + this.doAutoCodeExecution);
    }
    autoCodeExecutionCheckbox.addEventListener('change', autoCodeExecutionCheckboxListener);
    buttonDiv.appendChild(autoCodeExecutionCheckbox);
    buttonDiv.appendChild(autoCodeExecutionCheckboxLabel);

    this.node.appendChild(buttonDiv);
  }

  /**
   * Convenience wrapper for logging to console with name of extension
   * @param message 
   */
  LogToConsole(message: string): void {
    console.log("jupyterlab_blockly_polyglot_extension: " + message);
  }

  /**
   * A kind of registry/factory that returns the correct toolbox given the name of the kernel
   * @param kernelName 
   */
  GetToolBox(kernelName: string) {
    if (this.workspace) {
      switch (true) {
        //R kernel
        case kernelName == "ir":
          this.toolbox = new RToolbox(this.notebooks, this.workspace) as IToolbox;
          break;
        // Python kernel
        case kernelName.toLocaleLowerCase().includes("python"):
          this.toolbox = new PythonToolbox(this.notebooks, this.workspace) as IToolbox;
          break;
        default:
          window.alert(`You are attempting to use Blockly Polyglot with unknown kernel ${kernelName}. No blocks are defined for this kernel.`);

      }
      //load the toolbox with blocks
      if (this.toolbox) {
        this.toolbox.UpdateToolbox();

        this.toolbox?.DoFinalInitialization();
      }
    }

    this.LogToConsole("Attaching toolbox for " + `${kernelName}`);
  }

  /**
   * Remove blocks from workspace without affecting variable map like blockly.getMainWorkspace().clear() would
   */
  clearBlocks(): void {
    const workspace: Blockly.Workspace = Blockly.getMainWorkspace();
    const blocks = workspace.getAllBlocks(false);
    for (let i = 0; i < blocks.length; i++) {
      const block = blocks[i];
      //looks like disposing chains to child blocks, so check block exists b/f disposing
      if (workspace.getBlockById(block.id)) {
        block.dispose(false);
      }
    }
  }

  /**
   * !!!UNUSED Experimental function!!! that could replace 'blocksRendered' flag. Checks if blocks are saved/serialized. Blocks are considered saved if serialization of the current blocks matches xml in the cell. 
   */
  AreBlocksSaved(): boolean {
    const cellSerializedBlocks: string | null = this.GetActiveCellSerializedBlockXML();
    const workspaceSerializedBlocks = this.toolbox?.EncodeWorkspace();
    if (cellSerializedBlocks && cellSerializedBlocks == workspaceSerializedBlocks) {
      return true;
    } else {
      return false;
    }
  }

  /**
   * The kernel has executed. Refresh intellisense and log execution and error if it exists
   * @returns 
   */
  onKernelExecuted(): ((arg0: Kernel.IKernelConnection, arg1: KernelMessage.IIOPubMessage<any>) => boolean) {
    return (sender: Kernel.IKernelConnection, args: KernelMessage.IIOPubMessage<any>): boolean => {
      const messageType: string = args.header.msg_type.toString();
      switch (messageType) {
        case "execute_input": {
          this.LogToConsole(`kernel '${sender.name}' executed code, updating intellisense`);
          LogToServer(createJupyterLogEntry("execute-code", args.content));
          this.toolbox?.UpdateAllIntellisense();
          break;
        }
        case "error": {
          this.LogToConsole("kernel reports error executing code")
          LogToServer(createJupyterLogEntry("execute-code-error", args.content));
          break;
        }
        default: 0;
      }

      return true;
    };
  };

  /**
   * The active cell in the notebook has changed. Update state, particularly involving the clearing/serialization/deserialization of blocks.
   * @returns 
   */
  onActiveCellChanged(): (arg0: INotebookTracker, arg1: Cell<ICellModel> | null) => boolean {
    return (sender: INotebookTracker, args: Cell<ICellModel> | null): boolean => {
      if (args) {
        LogToServer(createJupyterLogEntry("active-cell-change", args.node.outerText));
        const syncCheckbox: HTMLInputElement | null = document.getElementById("syncCheckboxPoly") as HTMLInputElement;
        const autosaveCheckbox: HTMLInputElement | null = document.getElementById("autosaveCheckbox") as HTMLInputElement;

        // if autosave enabled, attempt to save our current blocks to the previous cell we just navigated off (to prevent losing work)
        if (autosaveCheckbox?.checked && this.lastCell) {
          // this.RenderCodeToLastCell(); //refactoring to BlocksToCode
          this.BlocksToCode(this.lastCell, false)
          // set lastCell to current cell
          this.lastCell = args;
        }

        // if sync enabled, the blocks workspace should:
        // clear itself when encountering a new empty cell
        // replace itself with serialized blocks if they exist
        // however, if we have blocks are not in sync with XML, we don't want to lose them by clearing the workspace
        if (syncCheckbox?.checked && this.notebooks.activeCell) {
          //if blocks are in sync and the active cell has no xml to load, just clear the workspace;
          if (this.blocksInSyncWithXML && this.GetActiveCellSerializedBlockXML() == null) {
            this.clearBlocks();
            //weird things will happen if metadata is not cleared when cell is cleared
            this.notebooks.activeCell.model.deleteMetadata("user_code_from_blocks");
            this.notebooks.activeCell.model.deleteMetadata("user_blocks_xml");
            this.notebooks.activeCell.model.deleteMetadata("user_blocks");
          }
          //otherwise try to to create blocks from xml string (fails gracefully)
          else {
            this.DeserializeBlocksFromXMLSelector();
          }
          //Update intellisense on blocks we just created
          this.toolbox?.UpdateAllIntellisense();
        }


      }
      return true;
    };
  };

  /**
   * Widget has attached to DOM and is ready for interaction. Inject blockly into div and set up event listeners for blockly events
   */
  onAfterAttach(): void {

    //toolbox can't be null or blockly throws errors
    // let starterToolbox =  { "kind": "categoryToolbox",  "contents": [] };
    // Sneak in a message to users who don't understand interface
    let starterToolbox = {
      "kind": "categoryToolbox",
      "contents": [
        { "kind": "CATEGORY", "contents": [], "colour": 20, "name": "OPEN" },
        { "kind": "CATEGORY", "contents": [], "colour": 70, "name": "A" },
        { "kind": "CATEGORY", "contents": [], "colour": 120, "name": "NOTEBOOK" },
        { "kind": "CATEGORY", "contents": [], "colour": 170, "name": "TO" },
        { "kind": "CATEGORY", "contents": [], "colour": 220, "name": "USE" },
        { "kind": "CATEGORY", "contents": [], "colour": 270, "name": "BLOCKLY" },
      ]
    };
    this.workspace = Blockly.inject(
      "blocklyDivPoly",
      {
        toolbox: starterToolbox,
        plugins: {
          // These are both required.
          // Note that the ScrollBlockDragger drags things besides blocks.
          // Block is included in the name for backwards compatibility.
          blockDragger: ScrollBlockDragger,
          metricsManager: ScrollMetricsManager,
        },
        move: {
          wheel: true, // Required for wheel scroll to work.
        },
      });

    // Initialize plugin.
    const plugin = new ScrollOptions(this.workspace);
    plugin.init();

    //2025-05-06 continuous code generation and execution, NOTE: experimental
    const codeGenListener = (e: Blockly.Events.Abstract): void => {
      if (this.workspace?.isDragging()) return; // Don't update while changes are happening.
      if (!this.codeGenBlockEvents.has(e.type)) return; //Don't update for all events, only specific events 
      if (e.type === Blockly.Events.FINISHED_LOADING) this.deserializingFlag = false; //Update deserialization flag
      if (this.deserializingFlag) return; //Don't update while we are deserializing

      // write code to active cell
      this.BlocksToCode(this.notebooks.activeCell, false);

      // experimental: execute code as well - only if this is not an intelliblock to avoid infinite loop
      if (this.doAutoCodeExecution && e.group != "INTELLISENSE") {
        // && e.group != "INTELLISENSE" && e.type == "change" && (<Blockly.Events.BlockChange>e).name != "MEMBER"){
        let changeEvent = e as BlockChange;
        if (changeEvent.oldValue != "") {
          let code_to_execute = this.toolbox?.BlocksToCode() ?? "";
          if (code_to_execute != "") {
            this.notebooks.currentWidget?.sessionContext.session?.kernel?.requestExecute({ code: code_to_execute });
            this.LogToConsole("auto executing the following code:\n" + code_to_execute + "\n");
          }
        }
      }
    }
    this.workspace.addChangeListener(codeGenListener);

    const logListener = (e: Blockly.Events.Abstract): void => {
      //this fires when user creates blocks AND when blocks are deserialized
      if (e.type === "create") {
        this.blocksInSyncWithXML = false
      }
      // "finished loading" event seems to only fire when deserializing
      if (e.type === "finished_loading") {
        this.blocksInSyncWithXML = true
      }
      LogToServer(createBlocklyLogEntry(e.type, e));
    };
    this.workspace.removeChangeListener(logListener);
    this.workspace.addChangeListener(logListener);
  }

  /**
   * Widget has been resized; update UI 
   */
  onResize(msg: Widget.ResizeMessage): void {
    const blocklyDiv: any = document.getElementById("blocklyDivPoly");
    const buttonDiv: any = document.getElementById("buttonDivPoly");
    const adjustedHeight: number = msg.height - 30;
    blocklyDiv.setAttribute("style", "position: absolute; top: 0px; left: 0px; width: " + msg.width.toString() + "px; height: " + adjustedHeight.toString() + "px");
    buttonDiv.setAttribute("style", "position: absolute; top: " + adjustedHeight.toString() + "px; left: " + "0" + "px; width: " + msg.width.toString() + "px; height: " + "30" + "px");
    Blockly.svgResize(this.workspace as Blockly.WorkspaceSvg);
  }

  /**
   * Get the XML comment string of the active cell if the string exists
   * @returns 
   */
  GetActiveCellSerializedBlockXML(): string | null {
    if (this.notebooks.activeCell) {
      const cellText: string = this.notebooks.activeCell.model.sharedModel.getSource();
      if (cellText.indexOf("xmlns") >= 0) {
        const regex = /(<xml[\s\S]+<\/xml>)/;
        let match = cellText.match(regex);
        //if we match overall and the capture group, return the capture group
        if (match && match[0]) {
          return match[0]
        }
      }
      //No xml to match against
      else {
        return null;
      }
    }
    //No active cell
    return null;
  }

  /**
   * Render blocks to code and serialize blocks at the same time. Do error checking to prevent user error IF this action was user-initiated (not autosave).
   */
  BlocksToCode(cell: Cell | null, userInitated: boolean = false): void {
    const code: string = this.toolbox?.BlocksToCode() ?? "";
    //this.generator.workspaceToCode(this.workspace);
    if (cell != null) {
      // if user called blocks to code on a markdown cell, complain
      if (userInitated && cells.isMarkdownCellModel(cell.model)) {
        window.alert("You are calling \'Blocks to Code\' on a MARKDOWN cell. Select an empty CODE cell and try again.");
        // if this is a code cell, do blocks to code
      } else if (cells.isCodeCellModel(cell.model)) {
        let blocks_xml = this.toolbox?.EncodeWorkspace();
        let cell_contents = code + "\n#" + blocks_xml;
        this.notebooks.activeCell?.model.sharedModel.setSource(cell_contents);
        this.LogToConsole(`${userInitated ? 'user' : 'auto'} wrote to cell\n` + code + "\n");
        LogToServer(createJupyterLogEntry("blocks-to-code", this.notebooks?.activeCell?.model.sharedModel.source));
        this.blocksInSyncWithXML = true;

        // EXPERIMENTAL: logging to metadata where user can't see/delete it
        // put code in metadata
        cell.model.setMetadata("user_code_from_blocks", code);
        // serialize blocks to metadata
        cell.model.setMetadata("user_blocks_xml", blocks_xml);
        // put list of blocks in metadata
        // we extract block type from XML b/c JSON seems to ignore intelliblocks
        if (blocks_xml) {
          // note this approach does not extract intelliblock parameters, just the unparameterized block
          let blocks = Array.from(blocks_xml.matchAll(/block type="([^"]+)"/gm), m => m[1]);
          cell.model.setMetadata("user_blocks", blocks);
        }
      }
    }
    else {
      this.LogToConsole("cell is null, could not execute blocks to code for\n" + code + "\n");
    }
  };

  /**
   * Select how blocks will be deserialized from code
   */
  DeserializeBlocksFromXMLSelector(): void {
    // NOTE: diffs feature is buggy/experimental
    // this.DeserializeBlocksFromXMLWithDiffs();
    this.DeserializeBlocksFromXML();
  }

  /**
   * Generates a random string of characters A-Z, a-z, and 0-9.
   * Used to approximate Blockly ids
   * @param length
   * @returns 
   */
  generateRandomString(length: number): string {
    const possibleChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';

    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * possibleChars.length);
      result += possibleChars.charAt(randomIndex);
    }
    return result;
  }

  /**
   * Create a dummy node in blockly XML format.
   * NOTE: creating nodes from scratch and cloning nodes tended to be problematic; it seems simpler to parse xml to create the node
   * @param top_block_node 
   * @param diff 
   * @returns 
   */
  createDummyNode(x: Number, y: number, offset: number, diff: ChangeObject<string>) {

    //id
    let id = this.generateRandomString(10);

    //code is actual for add and comment for remove, with multiline comments through replacement
    let code = diff.added ? diff.value : "#" + diff.value.replaceAll('\n', '\n#');

    //parse xml templated with above info
    let new_xml = this.domParser.parseFromString(`<block type="dummyNoOutputCodeBlock" id="${id}" x="${x}" y="${y + offset}"><field name="CODE">${code.trim()}</field></block>`, "text/xml");

    //first child of doc is the <block>
    return new_xml.childNodes.item(0);
  }

  /**
   * EXPERIMENTAL - SLIGHTLY BROKEN: MAY DESTROY BLOCKS IN SOME CASES
   * This function compares the code generated by 'blocks to code' with the code in the cell.
   * Extra code (diffs) are represented as freestyle blocks.
   * Rationale: True code to blocks requires AST to AST translation. 
   * Previously we called deserialization of blocks XML 'code to blocks' because from a user standpoint, it is.
   * However, if a user modifies the code by hand, which they may want to do as they transition from blocks
   * programming to coding, such modifications are lost because they are not persisted in XML.
   */
  DeserializeBlocksFromXMLWithDiffs(): void {
    if (this.notebooks.activeCell) {
      // the code generated by 'blocks to code' is stored in metadata; get it
      let user_code_from_blocks: string = this.notebooks.activeCell.model.getMetadata("user_code_from_blocks");

      // the code currently in the cell, with xml comment stripped
      let user_blocks_xml: string = this.notebooks.activeCell.model.getMetadata("user_blocks_xml");

      // cell contents
      const cellText: string = this.notebooks.activeCell.model.sharedModel.getSource();

      // first check if we should be making blocks at all, based on presence of XML in cell
      const xmlString = this.GetActiveCellSerializedBlockXML();
      if (xmlString != null) {
        try {
          //clear existing blocks so we don't junk up the workspace
          this.clearBlocks();

          //prevent auto code execution until we are done deserializing
          this.deserializingFlag = true;

          //check if there are diffs
          let code_without_xml = cellText.replace("#" + user_blocks_xml, "").trim();

          // no metadata or no diffs, decode as normal
          if (!user_code_from_blocks || code_without_xml == user_code_from_blocks.trim()) {
            // no diffs, decode as normal
            this.toolbox?.DecodeWorkspace(xmlString);
          }
          //we have diffs and need an alternative decoding procedure
          else {
            // close <next> with </block> and delete </next></block> to normalize traversal
            let clean_xml = user_blocks_xml.replaceAll("<next>", "</block>").replaceAll("</next></block>", "");

            // parse the dom to get blocks
            let doc = this.domParser.parseFromString(clean_xml, "text/xml");

            // calculate the diff
            let diffs = diffLines(user_code_from_blocks.trim() + "\n", code_without_xml + "\n");

            // iterate the dom and check the diff; each xml child "block" should be a line (descendents can be nested blocks)
            let blockCount = 0; //count of blocks into diff
            let diffIndex = 0; //count of diffs
            let xml_root = doc.childNodes.item(0);
            let new_node_list = [];
            let remove_node_list = [];
            let n = xml_root;
            let top_block_node = null;
            let top_x = 0;
            let top_y = 0;
            let block_offset_index = 1; //y offset from top block coordinate
            let do_reposition = true;
            // complex traversal: we can have more code adds than blocks
            // allow going beyond # blocks if we still have diffs
            for (let i = 0; i < xml_root.childNodes.length || diffIndex < diffs.length; i++) {
              // dom boundary checking: hold on to most recent block node but stop repositioning after all blocks have been visited
              if (i < xml_root.childNodes.length) {
                n = xml_root.childNodes.item(i);
              } else {
                do_reposition = false;
              }

              // only do something on blocks
              if (n.nodeName == "block") {

                // for debugging
                let info = (n as Element).getAttribute("type");
                console.log(info);

                //save the first block encountered, our topmost block, as a reference for all other block positions
                if (top_block_node == null) {
                  top_block_node = n;
                  top_x = parseInt((top_block_node as Element).getAttribute("x")?.valueOf() ?? "0");
                  top_y = parseInt((top_block_node as Element).getAttribute("y")?.valueOf() ?? "0");
                }

                //register that we encountered a block
                blockCount++;

                //accumulate/wait until our block count matches the size of the diff
                if (diffIndex < diffs.length && blockCount >= diffs[diffIndex].count) {
                  //if diff represents existing code, then only update traversal indices for the next diff
                  if (!diffs[diffIndex].added && !diffs[diffIndex].removed) {
                    diffIndex++;
                    blockCount = 0;
                    //diff represents added/removed code, so we need to create a block
                  } else {
                    let offset = 70 * block_offset_index;
                    //special case: if the diff is above the top block, make a negative offset
                    if (n == top_block_node) {
                      offset = -70;
                    }
                    //make node
                    let new_node = this.createDummyNode(top_x, top_y, offset, diffs[diffIndex]);
                    //insert if diff code nonempty
                    if (diffs[diffIndex].value.trim() != "") {
                      //insertion position seems to not matter relative to x/y position; this inserts at the end by default
                      //defer insertion so we don't modify the structure we are traversing
                      new_node_list.push(new_node);
                    }
                    //if this is a removal situation, mark block to remove (this will not remove multiple lines)
                    if (diffs[diffIndex].removed) {
                      remove_node_list.push(n);
                    }
                    //update indices for the next diff
                    diffIndex++;
                    blockCount = 0;
                    //special case continued: diff above top block should not count towards offset for following blocks
                    if (n != top_block_node) {
                      block_offset_index++;
                    }
                  }
                }

                // reposition existing non-top block based on the top block position
                if (top_block_node != n) {
                  if (do_reposition) {
                    //update block position referenced to top block's position
                    let element = (n as Element);
                    element.setAttribute("x", `${top_x}`);
                    element.setAttribute("y", `${top_y + 70 * block_offset_index}`);
                    // blockCount++;
                    block_offset_index++;
                    //we've run out of blocks; increment blockCount anyways so blockCount >= diffs[diffIndex].count
                  } else {
                    blockCount++;
                  }
                }
              }
              // console.log(n);
              // console.log(diffs[i]);
            } //end for childnodes.length

            //batch insertion all new nodes
            new_node_list.forEach((node) => {
              xml_root.insertBefore(node, null);
            });
            remove_node_list.forEach((node) => {
              xml_root.removeChild(node);
            });

            let serializer = new XMLSerializer();
            let diffXmlString = serializer.serializeToString(doc);
            console.log(diffXmlString);
            this.toolbox?.DecodeWorkspace(diffXmlString);
          }


          LogToServer(createJupyterLogEntry("xml-to-blocks", xmlString));
        } catch (e: any) {
          this.deserializingFlag = false;
          window.alert("Unable to perform \'Code to Blocks\'. Specific error message is: " + e.message);
          this.LogToConsole("unable to decode blocks. Specific error message is: " + e.message);
        }
      }
      else {
        this.LogToConsole("unable to decode blocks, active cell is null");
        //clear metadata for this cell if it exists; weird things can happen otherwise
        this.notebooks.activeCell.model.deleteMetadata("user_code_from_blocks");
        this.notebooks.activeCell.model.deleteMetadata("user_blocks_xml");
        this.notebooks.activeCell.model.deleteMetadata("user_blocks");
      }
    }
  };

  /**
   * Render blocks in workspace using xml. Defaults to xml present in active cell
   */
  DeserializeBlocksFromXML(): void {
    if (this.notebooks.activeCell) {
      const xmlString = this.GetActiveCellSerializedBlockXML();
      if (xmlString != null) {
        try {
          //clear existing blocks so we don't junk up the workspace
          this.clearBlocks();

          //prevent auto code execution until we are done deserializing
          this.deserializingFlag = true;

          this.toolbox?.DecodeWorkspace(xmlString)

          LogToServer(createJupyterLogEntry("xml-to-blocks", xmlString));
        } catch (e: any) {
          this.deserializingFlag = false;
          window.alert("Unable to perform \'Code to Blocks\': XML is either invald or renames existing variables. Specific error message is: " + e.message);
          this.LogToConsole("unable to decode blocks, last line is invald xml");
        }
      }
      else {
        this.LogToConsole("unable to decode blocks, active cell is null");
        //clear metadata for this cell if it exists; weird things can happen otherwise;
        // e.g. a code cell converted to markdown would have lingering code data
        this.notebooks.activeCell.model.deleteMetadata("user_code_from_blocks");
        this.notebooks.activeCell.model.deleteMetadata("user_blocks_xml");
        this.notebooks.activeCell.model.deleteMetadata("user_blocks");
      }
    }
  };

  /**
   * Removes Blockly xml comments from code
   * @param code
   * @returns 
   */
  cleanCode(code:string) : string {
    let clean = code.replace(/#<xml[\s\S]+<\/xml>/g,"");
    return clean;
  }

  /**
   * Display the LLM reply to the user
   * @param reply 
   * @param title 
   */
  showLLMReply(reply:string|undefined, title: string) : void {
    // window.alert(reply);
    // default error message
    let html = "The LLM did not provide a response. Please try again or check the browser console for error messages";
    // try to format markdown from LLM to something pretty
    if(reply) html = markdown_it.render(reply);
    showDialog(
    {
        title: title,
        body:  getLLMReactComponent(html),
        hasClose: true
    });
  }

  getPreviousMarkdownInstructions() : string {
    //get markdown instructions of the nearest preceding markdown cell
    let markdown_instructions = "";
    //traverse cells from the beginning
    let cells = this.notebooks.currentWidget?.model?.cells;
    if(this.notebooks.activeCell && cells){
      let last_markdown_cell = null;
      //find the last markdown cell before the active cell
      for( let i = 0; i < cells.length; i++ ){
        let cell = cells.get(i);
        if( cell.sharedModel.cell_type === 'markdown') {
          last_markdown_cell = cell;
        }
        if( cell == this.notebooks.activeCell.model ){
          break;
        }
      }
      //set the instructions to this cell's contents
      if(last_markdown_cell){
        markdown_instructions = last_markdown_cell.sharedModel.getSource();
      }
    }
    return markdown_instructions;
  }

  ExplainError(): void {
    // this.LogToConsole("ExplainError called");
    if (this.notebooks.activeCell) {
      let code: string = this.notebooks.activeCell.model.sharedModel.getSource();
      code = this.cleanCode(code);
      //we assume there is one output which is an error
      let output_model = (this.notebooks.activeCell as cells.CodeCell).outputArea.model.get(0);
      //Jupyter does not give nice access to output, so there is some formatting junk (TODO use renderer?)
      let error = output_model.toJSON();
      let error_message = `${error.ename?.toString()}\n${error.traceback?.toString()}`;

      let markdown_instructions = this.getPreviousMarkdownInstructions();

      llm_explain_error(this.llm_api_key, code, markdown_instructions, error_message)
        .then<any>((reply): void => this.showLLMReply( reply, 'Explanation of Error'))
        .catch(error => window.alert(error));
    }
  }

  ExplainCode(): void {
    // this.LogToConsole("ExplainCode called");
    if (this.notebooks.activeCell) {
      let code: string = this.notebooks.activeCell.model.sharedModel.getSource();
      code = this.cleanCode(code);

      llm_explain_code(this.llm_api_key, code)
        .then<any>((reply): void => this.showLLMReply( reply, 'Explanation of Code'))
        .catch(error => window.alert(error));
    }
  }

  NextStepHint(): void {
    // this.LogToConsole("NextStepHint called");
    if (this.notebooks.activeCell) {
      let code: string = this.notebooks.activeCell.model.sharedModel.getSource();
      code = this.cleanCode(code);      

      let markdown_instructions = this.getPreviousMarkdownInstructions();

      llm_next_step_hint(this.llm_api_key, code, markdown_instructions)
        .then<any>((reply): void => this.showLLMReply( reply, 'Hint on the Next Step'))
        .catch(error => window.alert(error));
    }
  }

} //end BlocklyWidget


/**
 * Return a MainAreaWidget wrapping a BlocklyWidget
 */
export function createMainAreaWidget(bw: BlocklyWidget): MainAreaWidget<BlocklyWidget> {
  const w: MainAreaWidget<BlocklyWidget> = new MainAreaWidget({
    content: bw as any,
  });
  w.id = "blockly-jupyterlab-polyglot";
  w.title.label = "Blockly Polyglot";
  w.title.closable = true;
  return w;
};

/**
 * Attach a MainAreaWidget by splitting the viewing area and placing in the left hand pane, if possible
 */
export function attachWidget(app: JupyterFrontEnd, notebooks: INotebookTracker, widget: MainAreaWidget): void {
  if (!widget.isAttached) {
    if (notebooks.currentWidget != null) {
      const options: DocumentRegistry.IOpenOptions = {
        ref: notebooks.currentWidget.id,
        mode: "split-left",
      };
      notebooks.currentWidget.context.addSibling(widget, options);
      //Forcing a left split when there is no notebook open results in partially broken behavior, so we must add to the main area
    } else {
      app.shell.add(widget, "main");
    }
    app.shell.activateById(widget.id);
  }
};

/**
 * Catch notebook changed event for enabling extension and attaching to left side when query string command is given
 * @param this 
 * @param sender 
 * @param args 
 * @returns 
 */
export const runCommandOnNotebookChanged = function (this: any, sender: IWidgetTracker<NotebookPanel>, args: NotebookPanel | null): boolean {
  if (sender.currentWidget != null) {
    console.log("notebook changed, autorunning blockly polyglot command");
    this.commands.execute("blockly_polyglot:open");
  }
  return true;
};

/**
 * The kernel has changed. Make sure we are logging kernel messages and load the appropriate langauge toolbox
 * @param this
 * @param sender 
 * @param args 
 * @returns 
 */
export function onKernelChanged(this: any, sender: ISessionContext, args: Session.ISessionConnection.IKernelChangedArgs): boolean {
  const widget: BlocklyWidget = this;
  //NOTE: removing "notHooked" logic
  // if (widget.notHooked) {
  if (sender.session?.kernel != null) {
    //listend for kernel messages
    let connection_status = sender.session.kernel.iopubMessage.connect(widget.onKernelExecuted(), widget);
    this.LogToConsole(`onKernelExecuted event is ${connection_status ? "now" : "already"} connected for ${sender.session.kernel.name}`);
    // console.log("jupyterlab_blockly_polyglot_extension: Listening for kernel messages");
    //connect appropriate toolbox
    widget.GetToolBox(sender.session.kernel.name);
    // console.log("jupyterlab_blockly_polyglot_extension: Attaching toolbox for " + `${sender.session.kernel.name}`);

    // widget.notHooked = false;
  }
  return true;
  // }
  // else {
  //   return false;
  // }
};

/**
 * The notebook has changed
 * @param this 
 * @param sender 
 * @param args 
 * @returns 
 */
export function onNotebookChanged(this: any, sender: IWidgetTracker<NotebookPanel>, args: NotebookPanel | null): boolean {
  const blocklyWidget: BlocklyWidget = this;
  if (sender.currentWidget != null) {
    this.LogToConsole("notebook changed to " + sender.currentWidget.context.path);
    LogToServer(createJupyterLogEntry("notebook-changed", sender.currentWidget.context.path));
    let connection_status = sender.currentWidget.sessionContext.kernelChanged.connect(onKernelChanged, blocklyWidget);
    this.LogToConsole(`kernelChanged event is ${connection_status ? "now" : "already"} connected`);

    //onKernelChanged will only fire the first time a kernel is loaded
    //so if a user switches back and forth between notebooks with different kernels that are
    //already loaded, we need to catch that here to update the toolbox
    // if the kernel is known, update the toolbox
    if (sender.currentWidget.sessionContext?.session?.kernel?.name) {
      blocklyWidget.GetToolBox(sender.currentWidget.sessionContext?.session?.kernel?.name);
    }
  }
  return true;
};


/**
 * ID for the plugin; a special naming convention is required for using settings
 */
const PLUGIN_ID = 'jupyterlab-blockly-polyglot-extension:blockly-polyglot';

/**
 * LLM commands, crossref with blockly-polyglot.json
 */
const CommandIds = {
  explainError: "toolbar-button:explain-error",
  explainCode: "toolbar-button:explain-code",
  nextStepHint: "toolbar-button:next-step-hint"
};

/**
 * Plugin definition for Jupyter; makes use of BlocklyWidget
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID, //'jupyterlab_blockly_polyglot_extension',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, ILayoutRestorer, ISettingRegistry],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, notebooks: INotebookTracker, restorer: ILayoutRestorer, settings: ISettingRegistry) => {
    console.log("jupyterlab_blockly_polyglot_extension: activated");

    //Create a blockly widget and place inside main area widget
    const blocklyWidget: BlocklyWidget = new BlocklyWidget(notebooks);
    let widget: MainAreaWidget<BlocklyWidget> = createMainAreaWidget(blocklyWidget);

    //Set up widget tracking to restore state
    const tracker: WidgetTracker<MainAreaWidget<BlocklyWidget>> = new WidgetTracker({
      namespace: "blockly_polyglot",
    });
    if (restorer) {
      restorer.restore(tracker, {
        command: "blockly_polyglot:open",
        name: (): string => "blockly_polyglot",
      });
    }

    //wait until a notebook is displayed to hook kernel messages
    notebooks.currentChanged.connect(onNotebookChanged, blocklyWidget);

    //Add application command to display
    app.commands.addCommand("blockly_polyglot:open", {
      label: "Blockly Polyglot",
      execute: (): void => {
        //Recreate the widget if the user previously closed it
        if (widget == null || widget.isDisposed) {
          widget = createMainAreaWidget(blocklyWidget);
        }
        //Attach the widget to the UI in a smart way
        attachWidget(app, notebooks, widget);
        //Track the widget to restore its state if the user does a refresh
        if (!tracker.has(widget)) {
          tracker.add(widget);
        }
      },
    } as CommandRegistry.ICommandOptions);

    //Add command to command palette
    palette.addItem({ command: "blockly_polyglot:open", category: 'Blockly' });

    //add llm commands
    app.commands.addCommand(CommandIds.explainCode, {
      icon: explainCodeIcon,
      caption: 'Explain code',
      execute: () => {
        blocklyWidget.ExplainCode();
      },
      isVisible: () => notebooks.activeCell?.model.type === 'code'
    });

    app.commands.addCommand(CommandIds.explainError, {
      icon: explainErrorIcon,
      caption: 'Explain error',
      execute: () => {
        blocklyWidget.ExplainError();
      },
      isVisible: () => notebooks.activeCell?.model.type === 'code'
    });

    app.commands.addCommand(CommandIds.nextStepHint, {
      icon: nextStepHintIcon,
      caption: 'Next step hint',
      execute: () => {
        blocklyWidget.NextStepHint();
      },
      isVisible: () => notebooks.activeCell?.model.type === 'code'
    });

    //----------------------
    // Process query string
    //----------------------
    const searchParams = new URLSearchParams(window.location.search);

    //If query string has bl=1, trigger the open command once the application is ready
    if (searchParams.get("bl") == "1") {
      blocklyWidget.LogToConsole("triggering open command based on query string input");
      //wait until a notebook is displayed so we dock correctly (e.g. nbgitpuller deployment)
      //NOTE: workspaces are stateful, so the notebook must be closed, then openned in the workspace for this to fire
      app.restored.then<void>((): void => {
        notebooks.currentChanged.connect(runCommandOnNotebookChanged, app);
        //If we force blockly to be open, do not allow blockly to be closed; useful for classes and experiments
        widget.title.closable = false;
      });
    }

    //If query string has id=, set up logging with this id
    let id = searchParams.get("id");
    if ( id ) {
      set_id( id );
    }

    //If query string has log=, set up logging with this log endpoint url
    let log_url = searchParams.get("log");
    if ( log_url ) {
      set_log_url( log_url );
    }

    //Load user settings
    let GEMINI_API_KEY = null;
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type (composite if there is a default)
      GEMINI_API_KEY = setting.get('GEMINI_API_KEY').composite as string;
      // save API key(s) to widget
      blocklyWidget.llm_api_key = GEMINI_API_KEY;
      console.log(`jupyterlab_blockly_polyglot_extension: GEMINI_API_KEY is ${GEMINI_API_KEY != null && GEMINI_API_KEY != "" ? "found" : "not found"}`);
    }

    //Wait for app and settings to be ready; the extension example does this
    Promise.all([app.restored, settings.load(PLUGIN_ID)])
      .then(([, setting]) => {
        // Read the settings
        loadSetting(setting);

        // Listen for setting changes
        setting.changed.connect(loadSetting);
      }); //end promise all
  } //end activate
}; //end plugin

export default plugin;