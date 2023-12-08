# pigen
This repo is oriented for optimizaton of generation pictures for DALLE.



## Installation
1. Clone the repo
2. Install the requirements
`pip install -r requirements.txt`
3. setup YOUR OPENAI API KEY in your environment variables
for windows:
### TODO
`powershell`
for linux:
### TODO
`bash `



## Usage image generator

## Example usage of the 'idea' command
`python pg.py idea --prompt "Generate a new project idea" --outputfile idea.txt`

Generates an idea based on the provided prompt and saves it to 'idea.txt'

## Example usage of the 'multistyle' command
`python pg.py multistyle --numOfPictures 5 --numOfRandomStyles 3`
Generates 5 pictures with 3 random styles applied

`python pg.py multistyle --numOfPictures 3 --listofStyles "style1,style2,style3"
`
Generates 3 pictures with specific styles "style1," "style2," and "style3"

## Example usage of the 'picByStyle' command
`python pg.py picByStyle -i <input_file> -p <prompt> -s <style> -o <output_file>`

Command-Line options:

`-i, --input_file <file_name>` : The input file with the prompt text. This should be a readable file.
  
`-p, --prompt <text>` : Additional Prompt text for generating a picture. and fix your initial prompt.
  
`-s, --style <style_name>` : Style to apply to the picture.
 
`-o, --output_file <file_name>` : The filename where the resulting picture will be saved.

Example of usage
`python pg.py picByStyle -i prompt.txt -p "Generate a beautiful landscape" -s landscape_style -o output.png`

Generates a picture with the specified style "artistic_style" based on the input prompt from 'input_prompt.txt'
