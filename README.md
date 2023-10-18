# AI Utils 
 Python scripts and notebooks for generative AI

# 1. API_img_gen

Address A1111 API, generative prompt creation for making batches of regularisation images. 
Made with Dreambooth training in mind. Usecases may vary. 
Inspired by [A1111 API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
and Dr FurkanGozukara [Dreambooth tutorials](https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Do-SDXL-DreamBooth-Training-With-Best-Settings.md)

Few features.
- **Prompt Generation**: To dynamically generate a list of prompts based on combinations of elements, characters, environments, aesthetics, styles, artists, cameras, and points of view.
- **Image Generation**: To use the generated prompts to produce images via A1111 API and save these images.
- **DNA Assigning**: To create a unique 'DNA' string for each image based on its indices in the original lists, which is saved as metadata.
- **State Management**: To keep track of the number of generated images and persist this information between script runs.
- **Sampler Selection**: Independent random selection of a sampler and step size for image generation from a predefined list.

- **Maximum Generations**: Ability to set a maximum number of image generations.
- **Random Sampling**: Uses random shuffling to generate unique combinations of prompts.
- **Error Handling**: Exception handling for API request failures and other issues.
- **Metadata Saving**: Each generated image is accompanied by a JSON file containing its metadata, including its unique DNA.
- **CLI Output**: Produces informative output in the command-line interface, allowing for real-time monitoring.

# 2. API_img_gen
 
 Needs A1111 API fork to accept local files on M1 Mac, still WIP. Usuful for generating variaty of images based on input and sample data.

Few features
- Checks the folder save bataches of variable amount of images per image in the folder.
- Uses random combination of prompts. 
- Choice of cfg scale settings, sampler, steps combo and generates random seed, subseed.
- Settings are saved to json along with unique DNA of the settings used similar to API_img_gen.
