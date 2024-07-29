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

# 2. API_img2img
 
 Needs A1111 API fork to accept local files on M1 Mac, still WIP. Usuful for generating variaty of images based on input and sample data.

Few features
- Checks the folder save bataches of variable amount of images per image in the folder.
- Uses random combination of prompts. 
- Choice of cfg scale settings, sampler, steps combo and generates random seed, subseed.
- Settings are saved to json along with unique DNA of the settings used similar to API_img_gen.

# 3. image2image Init 

This Python script is designed for generating initial images for animations and blending them together, leveraging a local server API. It operates within a structured workflow that involves selecting source images, invoking an image-to-image API, and systematically storing the output along with configuration details. Here's a structured overview:

- Initial Setup: It initializes by setting up a server URL and output directory, ensuring the latter's existence.
- Batch Management: Implements functionality to determine the next batch number for organizing outputs, enhancing scalability and organization.
- Image Processing: Utilizes a series of functions to encode images to Base64 for API transmission, decode API responses, and save both images and their settings in a specified directory structure. This approach facilitates traceability and reproducibility.
- API Interaction: Central to its functionality is the call_api method, which handles communication with a specified image-to-image API endpoint. This method sends a payload containing the initial image (in Base64 format) and parameters dictating the transformation characteristics.
- Dynamic Parameterization: The script supports dynamic input for transformation parameters, such as prompts, denoising strength, model specifications, and image dimensions. This flexibility allows for a wide range of creative outputs based on the source material.
- Iterative Processing: Iterates through a directory of source images, applying the transformation to each and incrementally saving the results. It ensures each image is processed and stored with a unique identifier, alongside a JSON file capturing the settings used for generation.
- Efficiency and Traceability: By printing progress messages and systematically organizing outputs, the script ensures efficiency in processing and ease in tracing outputs back to their source images and settings.

In essence, this script is a comprehensive tool for automated generation and blending of images for animation projects, optimized for ease of use, scalability, and creative flexibility. It's akin to a modular system that accepts varied input, applies complex transformations via API interaction, and outputs a structured collection of transformed images ready for further use in animation workflows.

# 4. Generate 

Configuration and NFT Metadata Generation for Deforum API

This Python script is designed to automate the generation of configuration files for the Deforum API and NFT (Non-Fungible Token) metadata, facilitating the creation of digital art with predefined traits and properties. The script follows a multi-step process to ensure each piece of digital art is unique and its characteristics are well-documented for blockchain minting. Below is a detailed breakdown of its core functionalities:

- **Template Initialization**: Establishes base templates for Deforum API settings and NFT DNA to set the stage for dynamic configuration.

- **Attribute and URL Mapping**: Utilizes a `script_data` dictionary for mapping specific attributes (movement, material, morph type) to URLs, defining the NFT characteristics and resource locations.

- **Configuration Generation**: Through the `generate_json_files` function, it iterates over images and script data to create Deforum API settings and NFT DNA configurations, embedding details such as dimensions, animation prompts, image paths, and NFT attributes.

- **Dynamic Parameter Inclusion**: Dynamically incorporates various parameters into the Deforum configuration, including dimensions, seeds, sampler types, and animation settings, to guide the processing of each image.

- **Batch Processing and Output Management**: Assigns unique batch and creature names to configurations for easy identification and management, supporting scalable digital art production.

- **NFT Metadata Customization**: Generates customized NFT metadata for each image, including name, image URL, and a unique DNA string, facilitating the blockchain minting process.

- **File Output**: Saves the generated configurations and NFT metadata as JSON files, preparing for blockchain integration and digital art minting.

This script streamlines the digital art creation process, from configuring the Deforum API for specific artistic outputs to preparing NFT metadata for minting, enhancing both productivity and creativity in digital art distribution.

# 5. Combine 

Combining Deforum Configuration Files

This utility script is crafted to streamline the process of combining multiple JSON configuration files, specifically designed for Deforum API settings, into a single consolidated file. This allows generating multiple files as a single job.

This approach is particularly useful for projects where digital art generation involves multiple configurations, allowing for streamlined setup and execution of the Deforum API with a unified configuration file.

# 6. ComfyUI models install. 

Jupyter Notebook for installing ComfyUI models on Runpods. It takes about 5-10 minutes to download all the models required for AnimateDiff to work on ComfyUI.
Note: ComfyUI and Comfy Manager need to be installed separately.

Example for Controlnet install command using aria
```!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sai_xl_canny_256lora.safetensors?download=true -d /workspace/ComfyUI/models/controlnet -o sai_xl_canny_256lora.safetensors```

Here Dreamshaper 

```!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://civitai.com/api/download/models/128713 -d /workspace/ComfyUI/models/checkpoints -o Dreamshaper_8.safetensors```
