#img to img script 
# needs API fork to accept local files, otherwise works with http https only
# 
# Checks the folder save bataches of variable amount of images per image in the folder
# Uses random combination of prompts 
# Choice of cfg scale settings, sampler, steps combo and generates random seed, subseed
# Settings are saved to json along with unique DNA of the settings used.  

#1 Import 

import json
import requests
import io
import base64
from PIL import Image
import random
from random import sample
import os
from itertools import product
import hashlib
import argparse

#2 Payload 

sampler_step_combos = [("Euler", 45), ("Euler a", 25), ("DPM++ 2M Karras", 25), ("DPM++ 2S a Karras", 30)]
cfg_scale =[7.5,8,9]

# Convert indices to DNA string
def index_to_dna(indices):
    return ''.join(str(i) for i in indices)

# Create hash from a string value
def hash_to_int(value):
    return str(hashlib.sha256(str(value).encode()).hexdigest())[:5]

# Generate payload for API request
def get_payload(prompt, sampler, steps, dna, cfg, input_img_path):
    seed = random.randint(1, 10000000000) 
    subseed = random.randint(1, 10000000000)

    return {
        "prompt": prompt,
        "negative_prompt": "cropped, watermark, logo, text, signature, copyright, writing, letters, low quality, artefacts, bad art, poorly drawn, lowres, simple, pixelated, grain, noise, man, waman, woman face, face, human body, blurry",
        "sampler_name": sampler,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": cfg,
        "width": 1024,
        "height": 1024,
        "denoising_strength": 0.55,
      # "model_hash": "0538f9319d",
        "model": "protovisionXLHighFidelity3D_beta0520Bakedvae",
      # "version": "20230919_experimental",
        "seed": seed,
        "subseed": subseed,
        "init_images": [input_img_path],
        "outdir_samples": "./outputs/API-outputs",
        "info": {
            "dna": dna,
            "image_used":""
        }
    }

# Generate combinations of prompts and their DNA

def generate_prompts():
    elements = ["wood", "metal", "liquid", "plastic", "crystals"]
    characters = ["DesignerToy", "Drippyworld", "Hovering Glitch Toy", "3Dworld",  "Mythic Guardian"]
    environments = ["jungle", "universe", "desert", "city", "ocean"]
    aesthetics = ["cyberpunk", "generative art", "indigenous art", "glitch art", "3D modeling"]
    styles = ["Computer-generated Imagery", "video art", "anime", "comic"]
    artists = ["Alberto Seveso", "Bernie Wrightson", "Brian Sum", "Georg Jensen", "teamLab", "Yoshiyuki Tomino", "Masamune Shirow", "Takashi Murakami", "Tristan Eaton"]
    cameras = ["FujiFilm X-T4 with Fujinon XF 35mm f-2 R WR", "Fujifilm X-S10 with Fujinon XF 10-24mm f-4 R OIS WR", "Canon EOS 5D Mark IV with Canon EF 24-70mm f-2.8L II", "Fujifilm X-Pro3 with Fujinon XF 56mm f-1.2 R", "Hasselblad X1D II with Hasselblad XCD 65mm f-2.8", "Kodak PIXPRO AZ901 with Built-in 4.3-258mm f-2.9-6.7", "with nothing"]
    points_of_view = ["profile", "front camera", "from the top", "from the bottom"]

    all_lists = [elements, characters, environments, aesthetics, styles, artists, cameras, points_of_view]

    prompts = []
    indices_list = []

# Generate prompt add commas and context for nuances 

    for element, character, environment, aesthetic, style, artist, camera, point_of_view in product(elements, characters, environments, aesthetics, styles, artists, cameras, points_of_view):
        prompt = f"{element} {character}, in the {environment} in {aesthetic} aesthetics, with {style}, inspired by {artist}, using {camera} from {point_of_view} perspective."
        prompts.append(prompt)
        
        indices = [lst.index(item) for lst, item in zip(all_lists, [element, character, environment, aesthetic, style, artist, camera, point_of_view])]
        dna = index_to_dna(indices)
        indices_list.append(dna)

    return prompts, indices_list



#3 Generate images 

def generate_and_save_img2img_images(base_url, state, batch_prompts, save_path, cfg_scale, input_img_path, dna_list):
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    try:
         for i, prompt in enumerate(batch_prompts):
            dna = dna_list[i]  # Get the corresponding DNA

            print(f"Selected prompt: {prompt}, DNA: {dna}")  #Print DNA selection in CLI

            sampler, steps = random.choice(sampler_step_combos)
            cfg=random.choice(cfg_scale)
            payload = get_payload(prompt, sampler, steps, dna, cfg, input_img_path)  # Pass in dna
          
            print("Payload:", json.dumps(payload, indent=4))


            response = requests.post(f"{base_url}/sdapi/v1/img2img", json=payload, headers=headers)
            response.raise_for_status()

            r = response.json()
            if 'images' not in r:
                print(f"Unexpected response: {r}")
                continue

            image_data = r['images'][0]
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))

            state["image_count"] += 1  # Increment the counter here
            image_filename = os.path.join(save_path, f'img_{state["image_count"]:04d}.png')
            json_filename = os.path.join(save_path, f'img_{state["image_count"]:04d}.json')

            image.save(image_filename)

            json_data = get_payload(prompt, sampler, steps, dna, cfg, input_img_path)

            with open(json_filename, 'w') as f:
                json.dump(json_data, f, indent=4)

            print(f"Generated and saved: {image_filename}, {json_filename}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")


#4 Main function 


def main():
    
    parser = argparse.ArgumentParser(description='Generate images from source images.')
    parser.add_argument('source_folder', type=str, help='Path to source images')
    args = parser.parse_args()
    
    
    base_url = 'http://127.0.0.1:7860'
    save_path = "./outputs/API-outputs"
    state_json_path = "./outputs/API-outputs/counter_and_prompt.json"
    #  source_folder = "./source_images"  # Path to the source images folder
    source_folder = args.source_folder  # Get the source folder from the command line argument

    # Create output directory if it doesn't exist
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    generation_count = 0

    state = {
        "image_count": 0,
        "dna": {}
    } 
    
    batch_prompts, dna_list = generate_prompts()
    
    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f)) and (f.endswith('.jpg') or f.endswith('.png'))]
    total_images = len(image_files)
    total_generations = len(batch_prompts) * total_images
    
    print(f"Total source images: {total_images}")
    print(f"Total generations to be made: {total_generations}")

    batch_size = 3  # Change this to set your batch size

    for img_file in image_files:
        input_img_path = os.path.join(source_folder, img_file)
        selected_prompts = sample(batch_prompts, batch_size)  # Randomly select 'batch_size' number of prompts
        selected_dna = [dna_list[batch_prompts.index(prompt)] for prompt in selected_prompts]  # Corresponding DNA
    
        generate_and_save_img2img_images(base_url, state, selected_prompts, save_path, cfg_scale, input_img_path, selected_dna)  # Pass in input_img_path as variable

     #   state[generation_count] += 1  # Increment generation counter


    try:  
        with open(state_json_path, 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"Failed to save state: {e}")

if __name__ == "__main__":
    main()