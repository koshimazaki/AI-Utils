# AI Utils 
Python scripts and Jupyter notebooks designed to streamline various tasks in generative AI, specifically focused on image generation, animation, and setting up models.

# 1. API_img_gen

Address A1111 API, generative prompt creation for making batches of regularisation images. 
Made with Dreambooth training in mind. Usecases may vary. 
Inspired by [A1111 API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
Dr FurkanGozukara [Dreambooth and model training tutorials](https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Do-SDXL-DreamBooth-Training-With-Best-Settings.md)

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

This Python script is designed for generating images, including initial images for animations and blending them together, using a local server API. It follows a structured workflow to select source images, call an image-to-image API, and save the results along with configuration details.

Workflow Overview:

- Initial Setup: Sets up the server URL and output directory.
- Batch Management: Determines the next batch number for organizing outputs.
- Image Processing: Encodes images to Base64 for API transmission, decodes API responses, and saves images and settings in a specified directory.
- API Interaction: Uses the call_api method to communicate with the image-to-image API, sending a payload with the initial image and transformation parameters.
- Dynamic Parameterization: Supports dynamic input for transformation parameters, such as prompts, denoising strength, model specifications, and image dimensions.
- Iterative Processing: Processes and saves each image from the source directory with a unique identifier and JSON file containing the generation settings.
- Efficiency and Traceability: Prints progress messages and organizes outputs for easy tracing back to source images and settings.

In essence, this script is a comprehensive tool for automated image generation, useful for both general image creation and animation projects. It is optimised for ease of use, scalability, and creative flexibility.

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

Example for Controlnet install command aria2c, a high-speed download utility:

```!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sai_xl_canny_256lora.safetensors?download=true -d /workspace/ComfyUI/models/controlnet -o sai_xl_canny_256lora.safetensors```

Here Dreamshaper: 

```!aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://civitai.com/api/download/models/128713 -d /workspace/ComfyUI/models/checkpoints -o Dreamshaper_8.safetensors```

# 6b. ComfyUI FLUX models install. 

Added all needed FLUX models in one install. This is optimised for Comfy UI tamplete on runpod. Adjust file paths as needed. Extreme speed Community Cloud network recommended or equivlent for quick download. These are large models.   
