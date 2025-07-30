import { GoogleGenAI } from '@google/genai';
import { LabIcon } from '@jupyterlab/ui-components';

/**
 * Make an LLM request (currently Gemini only). See https://ai.google.dev/gemini-api/docs#javascript
 * @param api_key
 * @param prompt 
 * @returns 
 */
async function llm_request(api_key: string, prompt: string) {

    const ai = new GoogleGenAI({ apiKey: api_key });

    const response = await ai.models.generateContent({
        model: "gemini-2.0-flash",
        contents: prompt,
    });
    return response.text;

    //alternatively could stream response in chunks, see https://ai.google.dev/gemini-api/docs/text-generation#streaming-responses
}

export async function llm_explain_error(api_key: string, code: string,  markdown_instructions: string, error_message: string) {
    let prompt = markdown_instructions + "\n\n" + code + "\n\n" + "In simple terms, why do I get:\n" + error_message + "\n\n" + "Give a brief answer.";
    return llm_request(api_key, prompt);
}

export async function llm_next_step_hint(api_key: string, code: string, markdown_instructions: string) {
    let prompt = markdown_instructions + "\n\n" + code + "\n\n" + "What should I do next? Only give me a single step.";
    return llm_request(api_key, prompt);
}

export async function llm_explain_code(api_key: string, code: string) {
    let prompt = "In simple terms, explain this code:" + "\n\n" + code + "\n\n" + "Give a brief answer.";
    return llm_request(api_key, prompt);
}

export const explainCodeIcon = new LabIcon({
    name: 'jupyterlab-blockly-polyglot-extension:explain-code',
    svgstr: `<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="56" height="40" x="4" y="12" rx="4" stroke="#333" stroke-width="2"/>
<path d="M14 20h12" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M14 26h24" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M14 32h18" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M14 38h28" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M44 18l6 6-6 6" stroke="#333" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M52 26h-8" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M10 46h44" stroke="#333" stroke-width="2" stroke-linecap="round"/>
<path d="M20 52h24" stroke="#333" stroke-width="2" stroke-linecap="round"/>
</svg>`
});

export const explainErrorIcon = new LabIcon({
    name: 'jupyterlab-blockly-polyglot-extension:explain-error',
    svgstr: `<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M22 22a12 12 0 1024 0 12 12 0 00-24 0zM32 10v12M32 34v-8" stroke="#FF4500" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="4" y="40" width="56" height="16" rx="4" stroke="#333" stroke-width="2"/>
<path d="M12 44h16M36 44h8M12 52h32" stroke="#333" stroke-width="2" stroke-linecap="round"/>
</svg>`
});

export const nextStepHintIcon = new LabIcon({
    name: 'jupyterlab-blockly-polyglot-extension:next-step-hint',
    svgstr: `<svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M16 32h32M32 16l16 16-16 16" stroke="#007BFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`
});

