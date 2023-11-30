# pigen
This repo is oriented for optimizaton of generation pictures for DALLE.


Usage image generator

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
`python pg.py picByStyle input_prompt.txt "Create a beautiful landscape" "artistic_style"`

Generates a picture with the specified style "artistic_style" based on the input prompt from 'input_prompt.txt'
