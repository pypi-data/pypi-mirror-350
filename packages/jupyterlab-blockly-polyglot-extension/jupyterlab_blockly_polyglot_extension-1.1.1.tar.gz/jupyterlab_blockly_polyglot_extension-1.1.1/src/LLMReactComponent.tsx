import * as React from 'react';
import { ReactWidget } from '@jupyterlab/ui-components';

//NOTE: see https://jupyterlab.readthedocs.io/en/latest/extension/virtualdom.html#react
//If we wanted  to subscribe to incremental blocks from the LLM, we could use props
//https://github.com/google-gemini/live-api-web-console
//However since the LLM prompts specifically ask it to be brief, the wait time as-is is 
//pretty short, 1-2 seconds, so further optimization seems unnecessary 

function LLMReactComponent({html}:{html:string}) : React.JSX.Element{
    //potential xss vulnerability
    return <div dangerouslySetInnerHTML={{ __html: html }} />
    // return (<div>{html}</div>) //still returns html as text
}

export function getLLMReactComponent(html:string) : ReactWidget{
    return ReactWidget.create(<LLMReactComponent html={html} />);
}