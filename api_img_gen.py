# Script made for creation of regularisation images for Dreambooth Training 
# It addresses A1111 API, creates permutations of given prompts, keeps counter on file.
# Generates random selection of prompts and given sampler, steps combos
# Saves png files and coresponding json files with settings and unique DNA for tracking.
# Requirenments start A1111 with --api flag 
# Inspiration and docs: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API


import json
import requests
import io
import base64
from PIL import Image
import random
import os
from itertools import product
import hashlib

sampler_step_combos = [("Euler", 45), ("Euler a", 25), ("DPM++ 2M Karras", 25), ("DPM++ 2S a Karras", 30)]

def index_to_dna(indices):
    return ''.join(str(i) for i in indices)

def hash_to_int(value):
    return str(hashlib.sha256(str(value).encode()).hexdigest())[:5]

def get_payload(prompt, sampler, steps, dna):

    seed = random.randint(1, 10000000000) 
    subseed = random.randint(1, 10000000000)


    return {
        "prompt": prompt,
        "negative_prompt": "cropped, watermark, logo, text, signature, copyright, writing, letters, low quality, artefacts, bad art, poorly drawn, lowres, simple, pixelated, grain, noise, blurry",
        "sampler_name": sampler,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": 7,
        "width": 256,
        "height": 256,
        "denoising_strength": 0.63,
      # "model_hash": "0538f9319d",
        "model": "protovisionXLHighFidelity3D_beta0520Bakedvae",
      # "version": "20230919_experimental",
        "seed": seed,
        "subseed": subseed,
        "outdir_samples": "./outputs/API-outputs",
        "info": {
            "dna": dna
        }
    }

# Generate combinations of prompts and their DNA

def generate_prompts():
    elements = ["wood", "metal", "liquid", "plastic", "crystals"]
    characters = ["Glitchyokai", "Drippyworld", "Hovering Glitch Toy", "metaverse",  "Mythic Guardian"]
    environments = ["fiordland", "iceland", "oasis", "rural Thailand", "volcano"]
    aesthetics = ["cyberpunk", "generative art", "indigenous art", "glitch art", "3D modeling"]
    styles = ["Computer-generated Imagery", "video art", "anime", "comic"]
    artists = ["Alberto Seveso", "Bernie Wrightson", "Brian Sum", "Georg Jensen", "teamLab", "Yoshiyuki Tomino", "Masamune Shirow", "Takashi Murakami", "Tristan Eaton"]
    cameras = ["FujiFilm X-T4 with Fujinon XF 35mm f-2 R WR", "Fujifilm X-S10 with Fujinon XF 10-24mm f-4 R OIS WR", "Canon EOS 5D Mark IV with Canon EF 24-70mm f-2.8L II", "Fujifilm X-Pro3 with Fujinon XF 56mm f-1.2 R", "Hasselblad X1D II with Hasselblad XCD 65mm f-2.8", "Kodak PIXPRO AZ901 with Built-in 4.3-258mm f-2.9-6.7", "with nothing"]
    points_of_view = ["profile", "front camera", "distant shot", "from the bottom", "macro shot", "wide angle"]

    all_lists = [elements, characters, environments, aesthetics, styles, artists, cameras, points_of_view]

    prompts = []
    indices_list = []

    for element, character, environment, aesthetic, style, artist, camera, point_of_view in product(elements, characters, environments, aesthetics, styles, artists, cameras, points_of_view):
        prompt = f"{element} {character}, in the {environment} in {aesthetic} aesthetics, with {style}, inspired by {artist}, shot with {camera} from {point_of_view} perspective."
        prompts.append(prompt)
        
        indices = [lst.index(item) for lst, item in zip(all_lists, [element, character, environment, aesthetic, style, artist, camera, point_of_view])]
        dna = index_to_dna(indices)
        indices_list.append(dna)

    return prompts, indices_list

# Function to generate and save images

def generate_and_save_images(base_url, batch_prompts, state, save_path, dna_list):
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
         for i, prompt in enumerate(batch_prompts):
            dna = dna_list[i]  # Get the corresponding DNA

            print(f"Selected prompt: {prompt}, DNA: {dna}")  #Print DNA selection in CLI


            sampler, steps = random.choice(sampler_step_combos)
            payload = get_payload(prompt, sampler, steps, dna)  # Pass in dna
            response = requests.post(f"{base_url}/sdapi/v1/txt2img", json=payload, headers=headers)
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

            json_data = get_payload(prompt, sampler, steps, dna)
            with open(json_filename, 'w') as f:
                json.dump(json_data, f, indent=4)

            print(f"Generated and saved: {image_filename}, {json_filename}")

    except requests.RequestException as e:
        print(f"Request failed: {e}")

# Main function

def main():
    base_url = 'http://127.0.0.1:7860'  # API endpoint
    save_path = "./outputs/API-outputs"  # Output directory
    state_json_path = "./outputs/API-outputs/counter_and_prompt.json"  # Add the extension ".json"
    
    # Create output directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Load or initialize state

    try:
        with open(state_json_path, 'r') as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {"image_count": 0}

        max_generations = 10  # Specify your maximum number of generations here
        generation_count = 0

        prompts, dna_list = generate_prompts()

        max_permutations = len(prompts)
        print(f"Maximum number of permutations: {max_permutations}")

        # Shuffling for random selection without repetition

        combined = list(zip(prompts, dna_list))
        random.shuffle(combined)
        prompts, dna_list = zip(*combined)

        # Loop through the prompts and break when max_generations is reached

    for prompt, dna in zip(prompts, dna_list):
        if generation_count >= max_generations:
            break
        generate_and_save_images(base_url, [prompt], state, save_path, [dna])
        generation_count += 1  # Increment generation counter

   

    try:   # Save the state

        with open(state_json_path, 'w') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"Failed to save state: {e}")

if __name__ == "__main__":
    main()