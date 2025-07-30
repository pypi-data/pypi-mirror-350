import openai
import spacy
import string
import argparse
from typing import Dict, Tuple, List, Union, Iterator
from enum import Enum
from openai import OpenAI
import json
from string import Template
from abc import abstractmethod
import os


class PromptTemplate:
    """
    Wrapper around string.Template. Use to generate prompts fast.

    Example usage:
        prompt_temp = PromptTemplate('Can you list all the cities in the country ${country} by the cheapest ${domain} prices?')
        concrete_prompt = prompt_temp.fill({
            "country": "France",
            "domain": "rent"
        });
        print(concrete_prompt)

        # Fill can also fill the prompt only partially, which gives us a new prompt template: 
        partial_prompt = prompt_temp.fill({
            "domain": "rent"
        });
        print(partial_prompt)
    """
    def __init__(self, templateStr):
        """
            Initialize a PromptTemplate with a string in string.Template format.
            (See https://docs.python.org/3/library/string.html#template-strings for more details.)
        """
        try:
            Template(templateStr)
        except:
            raise Exception("Invalid template formatting for string:", templateStr)
        self.template = templateStr
        self.fill_history = {}

    def __str__(self) -> str:
        return self.template
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def is_concrete(self) -> bool:
        """ Returns True if no template variables are left in template string.
        """
        try:
            Template(self.template).substitute({})
            return True # no exception raised means there was nothing to substitute...
        except KeyError as e:
            return False
        
    def fill(self, paramDict: Dict[str, str]) -> 'PromptTemplate':
        """
            Formats the template string with the given parameters, returning a new PromptTemplate.
            Can return a partial completion. 

            Example usage:
                prompt = prompt_template.fill({
                    "className": className,
                    "library": "Kivy",
                    "PL": "Python"
                });
        """
        filled_pt = PromptTemplate(
            Template(self.template).safe_substitute(paramDict)
        )

        # Deep copy prior fill history from this version over to new one
        filled_pt.fill_history = { key: val for (key, val) in self.fill_history.items() }

        # Add the new fill history using the passed parameters that we just filled in
        for key, val in paramDict.items():
            if key in filled_pt.fill_history:
                print(f"Warning: PromptTemplate already has fill history for key {key}.")
            filled_pt.fill_history[key] = val
        
        return filled_pt


class PromptPermutationGenerator:
    """
    Given a PromptTemplate and a parameter dict that includes arrays of items, 
    generate all the permutations of the prompt for all permutations of the items.

    Example usage:
        prompt_gen = PromptPermutationGenerator('Can you list all the cities in the country ${country} by the cheapest ${domain} prices?')
        for prompt in prompt_gen({"country":["Canada", "South Africa", "China"], 
                                  "domain": ["rent", "food", "energy"]}):
            print(prompt)
    """
    def __init__(self, template: Union[PromptTemplate, str]):
        if isinstance(template, str):
            template = PromptTemplate(template)
        self.template = template
    
    def _gen_perm(self, template, params_to_fill, paramDict):
        if len(params_to_fill) == 0: return []

        # Peel off first element
        param = params_to_fill[0]
        params_left = params_to_fill[1:]

        # Generate new prompts by filling in its value(s) into the PromptTemplate
        val = paramDict[param]
        if isinstance(val, list):
            new_prompt_temps = [template.fill({param: v}) for v in val]
        elif isinstance(val, str):
            new_prompt_temps = [template.fill({param: val})]
        else:
            raise ValueError("Value of prompt template parameter is not a list or a string, but of type " + str(type(val)))
        
        # Recurse
        if len(params_left) == 0:
            return new_prompt_temps
        else:
            res = []
            for p in new_prompt_temps:
                res.extend(self._gen_perm(p, params_to_fill[1:], paramDict))
            return res

    def __call__(self, paramDict: Dict[str, Union[str, List[str]]]):
        for p in self._gen_perm(self.template, list(paramDict.keys()), paramDict):
            yield p




""" Supported LLM coding assistants """
class LLM(Enum):
    ChatGPT = 0

def call_chatgpt(prompt: str, n: int = 1, temperature: float = 1.0) -> Tuple[Dict, Dict]:
    query = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "n": n,
        "temperature": temperature,
    }
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(**query)
    return query, response

def _extract_chatgpt_responses(response: dict) -> List[dict]:
    """
        Extracts the text part of a response JSON from ChatGPT. If there are more
        than 1 response (e.g., asking the LLM to generate multiple responses), 
        this produces a list of all returned responses.
    """
    choices = response['response'].choices
    return [
        c.message.content
        for i, c in enumerate(choices)
    ]

def extract_responses(response: dict, llm: LLM) -> List[dict]:
    """
        Given a LLM and a response object from its API, extract the
        text response(s) part of the response object.
    """
    if llm is LLM.ChatGPT or llm == LLM.ChatGPT.name:
        return _extract_chatgpt_responses(response)
    else:
        raise ValueError(f"LLM {llm} is unsupported.")

def is_valid_filepath(filepath: str) -> bool:
    try:
        with open(filepath, 'r'):
            pass
    except IOError:
        try:
            # Create the file if it doesn't exist, and write an empty json string to it
            with open(filepath, 'w+') as f:
                f.write("{}")
                pass
        except IOError:
            return False
    return True

def is_valid_json(json_dict: dict) -> bool:
    if isinstance(json_dict, dict):
        try:
            json.dumps(json_dict)
            return True
        except:
            pass
    return False


class PromptPipeline:
    def __init__(self, storageFile: str):
        if not is_valid_filepath(storageFile):
            raise IOError(f"Filepath {storageFile} is invalid, or you do not have write access.")

        self._filepath = storageFile

    @abstractmethod
    def gen_prompts(self, properties) -> List[PromptTemplate]:
        raise NotImplementedError("Please Implement the gen_prompts method")
    
    @abstractmethod
    def analyze_response(self, response) -> bool:
        """
            Analyze the response and return True if the response is valid.
        """
        raise NotImplementedError("Please Implement the analyze_response method")
    
    def gen_responses(self, properties, llm: LLM, n: int = 1, temperature: float = 1.0) -> Iterator[Dict]:
        """
            Calls LLM 'llm' with all prompts, and yields responses as dicts in format {prompt, query, response, llm, info}.

            By default, for each response, this also saves reponses to disk as JSON at the filepath given during init. 
            (Very useful for saving money in case something goes awry!)
            To clear the cached responses, call clear_cached_responses(). 

            Do not override this function.
        """
        # Double-check that properties is the correct type (JSON dict):
        if not is_valid_json(properties):
            raise ValueError(f"Properties argument is not valid JSON.")

        # Generate concrete prompts using properties dict
        prompts = self.gen_prompts(properties)

        # Load any cache'd responses
        responses = self._load_cached_responses()

        # Query LLM with each prompt, yield + cache the responses
        for prompt in prompts:
            if isinstance(prompt, PromptTemplate) and not prompt.is_concrete():
                raise Exception(f"Cannot send a prompt '{prompt}' to LLM: Prompt is a template.")
            
            # Each prompt has a history of what was filled in from its base template.
            # This data --like, "class", "language", "library" etc --can be useful when parsing responses.
            info = prompt.fill_history
            prompt_str = str(prompt)
            
            # First check if there is already a response for this item. If so, we can save an LLM call:
            if prompt_str in responses:
                print(f"   - Found cache'd response for prompt {prompt_str}. Using...")
                yield {
                    "prompt": prompt_str,
                    "query": responses[prompt_str]["query"],
                    "response": responses[prompt_str]["response"],
                    "llm": responses[prompt_str]["llm"] if "llm" in responses[prompt_str] else LLM.ChatGPT.name,
                    "info": responses[prompt_str]["info"],
                }
                continue

            # Call the LLM to generate a response
            query, response = self._prompt_llm(llm, prompt_str, n, temperature)

            # Save the response to a JSON file
            # NOTE: We do this to save money --in case something breaks between calls, can ensure we got the data!
            responses[prompt_str] = {
                "query": query, 
                "response": response,
                "llm": llm.name,
                "info": info,
            }
            # self._cache_responses(responses)

            yield {
                "prompt":prompt_str, 
                "query":query, 
                "response":response,
                "llm": llm.name,
                "info": info,
            }
    
    def _load_cached_responses(self) -> Dict:
        """
            Loads saved responses of JSON at self._filepath. 
            Useful for continuing if computation was interrupted halfway through. 
        """
        if os.path.isfile(self._filepath):
            with open(self._filepath, encoding="utf-8") as f:
                responses = json.load(f)
            return responses
        else:
            return {}
    
    def _cache_responses(self, responses) -> None:
        with open(self._filepath, "w") as f:
            json.dump(responses, f)
    
    def clear_cached_responses(self) -> None:
        self._cache_responses({})

    def _prompt_llm(self, llm: LLM, prompt: str, n: int = 1, temperature: float = 1.0) -> Tuple[Dict, Dict]:
        if llm is LLM.ChatGPT:
            return call_chatgpt(prompt, n=n, temperature=temperature)
        else:
            raise Exception(f"Language model {llm} is not supported.")


nlp = spacy.load("en_core_web_sm")

TEMPERATURE = 1 #The temperature for ChatGPT calls

PHRASE_SPLITTER_PROMPT_TEMPLATE = \
"""Does the following sentence end properly?
"${sentence}"

Please answer only Yes or No."""

class PhraseSplitterPromptPipeline(PromptPipeline):
    def __init__(self):
        self._template = PromptTemplate(PHRASE_SPLITTER_PROMPT_TEMPLATE)
        storageFile = 'phrase_splitter_responses.json'
        super().__init__(storageFile)
    def gen_prompts(self, properties):
        gen_prompts = PromptPermutationGenerator(self._template)
        return list(gen_prompts({
            "sentence": properties["sentence"]
        }))

def split_and_concatenate(sentence):
    """
        This splits the sentence into NLP-based phrase boundaries as a first pass to minimize queries to the LLM about grammatical breaks
    """
    
    result = []
    stripped = sentence.rstrip(string.punctuation)
    # The difference is the punctuation at the end
    ending_punctuation = sentence[len(stripped):]
    # Split the sentence into words
    tokens = []
    doc = nlp(stripped.strip())
    for token in doc:
        tokens.append(token.text)
        if token.head.i > token.i: # current word has a parent on the right of it, so ending the sentence here will not make sense.
            continue
        result.append((' '.join(tokens)))
    return result, ending_punctuation

def strip_wrapping_quotes(s: str) -> str:
    if s[0] == '"': s = s[1:]
    if s[-1] == '"': s = s[0:-1]
    return s

def extract_new_phrases(sentences):
    new_phrases = []
    previous_sentence = ""
    for sentence in sentences:
        # Find the part of the sentence that is new compared to the previous one
        if sentence.startswith(previous_sentence):
            new_phrase = sentence[len(previous_sentence):]
        else:
            new_phrase = sentence
        new_phrases.append(new_phrase)
        previous_sentence = sentence
    return new_phrases

def collect_false_segment(pairs):
    if not pairs:
        return ''
    st = pairs[-1][0]
    tmp = ''
    for p in reversed(pairs):
        tmp = p[0]
        if p[1]:
            break
    return st[len(tmp):]

# the function to invoke if you're working within a Python environment
def find_segments(sentence, k):
    openai.api_key = k
    phrase_splitter = PhraseSplitterPromptPipeline()
    result = []
    s, punc = split_and_concatenate(sentence)
    for i, candidate in enumerate(s):
        responses = []
        phrase_splitter.clear_cached_responses()
        for res in phrase_splitter.gen_responses({"sentence": candidate}, LLM.ChatGPT, n=1, temperature=TEMPERATURE):
            responses.extend(extract_responses(res, llm=LLM.ChatGPT))
        responses = [strip_wrapping_quotes(r) for r in responses]
        if 'yes' in responses[0].lower():
            result.append((candidate, True))
        else:
            result.append((candidate, False))
    output = {"grammatical_phrases" : extract_new_phrases([element[0] for element in result if element[1]]), "last_ungrammatical_phrase" : collect_false_segment(result), "final_puncutation" : punc}
    print(output)
    # return output

# for commandline invocation
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sentence", help="The sentence to process")
    parser.add_argument("api_key", help="Your OpenAI API key")  # API key argument
    args = parser.parse_args()

    find_segments(args.sentence, args.api_key)  # Pass both sentence and API key to find_segments
