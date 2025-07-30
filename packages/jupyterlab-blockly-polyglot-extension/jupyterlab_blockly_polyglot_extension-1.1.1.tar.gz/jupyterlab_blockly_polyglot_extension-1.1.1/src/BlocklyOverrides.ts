import * as Blockly from 'blockly/core';

/**
 * Functions in this file trivially override Blockly functions. 
 * See https://github.com/google/blockly for relevant licenses
 */


export function dropdownCreateOverride(this: Blockly.FieldVariable): Blockly.MenuOption[] {
    //@ts-ignore
    if (!this.variable) {
    throw Error(
    'Tried to call dropdownCreate on a variable field with no' +
        ' variable selected.',
    );
    }
    const name = this.getText();
    let variableModelList: Blockly.VariableModel[] = [];
    if (this.sourceBlock_ && !this.sourceBlock_.isDeadOrDying()) {
        //@ts-ignore
        const variableTypes = this.getVariableTypes();
        // Get a copy of the list, so that adding rename and new variable options
        // doesn't modify the workspace's list.
        for (let i = 0; i < variableTypes.length; i++) {
            const variableType = variableTypes[i];
            const variables =
                this.sourceBlock_.workspace.getVariablesOfType(variableType);
            variableModelList = variableModelList.concat(variables);
        }
    }
    variableModelList.sort(Blockly.VariableModel.compareByName);

    const options: [string, string][] = [];
    for (let i = 0; i < variableModelList.length; i++) {
      // Set the UUID as the internal representation of the variable.
        options[i] = [variableModelList[i].name, variableModelList[i].getId()];
    }
    // AO: disable renaming variables
    // options.push([
    //   Blockly.Msg['RENAME_VARIABLE'],
    //   Blockly.internalConstants.RENAME_VARIABLE_ID,
    // ]);
    // AO: looked at creating variables here, but not easy to patch it with the OO style of FieldVariable (see below)
    // options.push([
    // Blockly.Msg['NEW_VARIABLE'],
    // 'CREATE_VARIABLE',
    // ]);

    if (Blockly.Msg['DELETE_VARIABLE']) {
        options.push([
        Blockly.Msg['DELETE_VARIABLE'].replaceAll('%1', name),
        // internalConstants.DELETE_VARIABLE_ID,
        'DELETE_VARIABLE_ID',
        ]);
    }

    // Blockly.Variables.createVariableButtonHandler()

    return options;
}


// export function onItemSelected_(menu: Blockly.Menu, menuItem: Blockly.MenuItem) {
//     const id = menuItem.getValue();
//     // Handle special cases.
//     if (this.sourceBlock_ && !this.sourceBlock_.isDeadOrDying()) {
//       if (id === internalConstants.RENAME_VARIABLE_ID) {
//         // Rename variable.
//         Variables.renameVariable(
//           this.sourceBlock_.workspace,
//           this.variable as VariableModel,
//         );
//         return;
//       } else if (id === internalConstants.DELETE_VARIABLE_ID) {
//         // Delete variable.
//         this.sourceBlock_.workspace.deleteVariableById(this.variable!.getId());
//         return;
//       }
//     }
//     // Handle unspecial case.
//     this.setValue(id);
//   }

