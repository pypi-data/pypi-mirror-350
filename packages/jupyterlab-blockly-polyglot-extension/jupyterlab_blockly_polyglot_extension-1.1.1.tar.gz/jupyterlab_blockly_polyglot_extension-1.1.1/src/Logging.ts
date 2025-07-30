import { SHA256, enc } from 'crypto-js';

export interface LogEntry {
    username: string;
    json: string;
}

export interface BlocklyLogEntry050824 {
    schema: string;
    name: string;
    object: any;
}

export interface JupyterLogEntry050824 {
    schema: string;
    name: string;
    // payload?: string | null;
    payload: object;
}

/**
 * Hash a string
 * @param inputString 
 * @returns string
 */
function createSHA256Hash(inputString: string): string {
    return SHA256(inputString).toString(enc.Hex);
}

export function createBlocklyLogEntry(name: string, object: any): BlocklyLogEntry050824 {
    return {
        schema: "ble050824",
        name: name,
        object: object
    };
}

export function createJupyterLogEntry(name: string, payload: any): JupyterLogEntry050824 {
    return {
        schema: "jle050824",
        name: name,
        payload: payload
    };
}

let logUrl: string | undefined = undefined;
export function set_log_url(url: string) {
    logUrl = url;
}
let idOption: string | undefined = undefined;
let hashedIdOption: string | undefined = undefined;

/**
 * Set the ID we are logging for, and create a hashed option for anonymous logging
 * @param id
 */
export function set_id(id: string) {
    idOption = id;
    hashedIdOption = createSHA256Hash(id);
}

function filterJson(o: any): string {
    if (o?.object?.element?.toString().indexOf("drag") === 0) {
        o.object.newValue = undefined;
        o.object.oldValue = undefined;
    }
    return o;
}

/**
 * Logs to endpoint if logUrl is set
 * @param logObject 
 */
export function LogToServer(logObject: any): void {
    //autologging for olney.ai domains; don't log here ;)
    if (window.location.href.includes("olney.ai")) {
        //only autolog here if no logUrl specified
        logUrl = logUrl ?? 'https://logging2.olney.ai/datawhys/log';
    }

    //normal logging, only log if logUrl is set
    if (logUrl) {
        // if no id has been specified, use the href
        let id = window.location.href;
        // if the href has an anonymous component, use a hashed version
        if( id.includes('user/x-')) {
            // cache the hashed version
            if( !hashedIdOption ){
                hashedIdOption = createSHA256Hash(id);
            }
            id = hashedIdOption;
        }
        // if an id has been manually specified for logging, log it
        if (idOption && hashedIdOption) { 
            // if the id has an anonymous prefix, use the hashed version
            if( idOption.startsWith('x-')) {
                id = hashedIdOption;
            } else {
                id = idOption; 
            }
        }
        // post it
        window.fetch(logUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: id,
                //base64 encode the payload because it can have all kinds of craziness inside it
                json: btoa(JSON.stringify(filterJson(logObject)))

            })
        }).then(response => {
            if (!response.ok) {
                console.log(response.statusText);
            }
        })
    }
}