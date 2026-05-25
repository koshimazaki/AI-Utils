# AI Tooling for Agents and Audiovisual Media

A living archive of Python scripts, Jupyter notebooks, ComfyUI setup helpers, RunPod workflows, and generative media utilities built across 2023-2026.

This repository contains the notebooks and scripts listed below. It started with A1111 and Deforum production scripts, then expanded into ComfyUI, FLUX/LTX/WAN video workflows and cloud GPU setup. The older scripts are kept because they show the working history behind the current audiovisual AI stack: prompt generation, batch production, metadata, model setup, video pipelines, and cloud inference infrastructure.

Related open source repos and public case studies are listed here as a map of the broader tooling ecosystem.

## Open Source Tooling Ecosystem

| Tool / repo | Focus | Status |
| --- | --- | --- |
| [AI-Utils](https://github.com/koshimazaki/AI-Utils) | This repo: Python scripts, notebooks, A1111/Deforum history, RunPod/ComfyUI setup, WAN install tooling | Active archive |
| [ComfyUI-Koshi-Nodes](https://github.com/koshimazaki/ComfyUI-Koshi-Nodes) | ComfyUI nodes for FLUX motion, shaders, procedural visuals, OLED/SIDKIT export | Open source |
| [Koshi Flux](https://github.com/koshimazaki/Koshi-Flux) | Python-first FLUX/Klein animation workflows and Deforum-style motion pipelines | Open source |
| [VibeComfy](https://github.com/peteromallet/VibeComfy) | Agentic interface for ComfyUI workflow authoring, editing, conversion, templates, and local/RunPod runtimes | Open source contribution |
| [ComfyUI Frontend Health](https://github.com/koshimazaki/comfy-frontend-health) | Repo-specific quality stack for ComfyUI frontend, curated on top of `desloppify` with Claude Code agents, Vue detectors, and pre-PR gates | Open source |
| [Muzed](https://github.com/koshimazaki/Mused) | LTX-2 motion LoRA, Kling 3.0 motion transfer production pipeline, H200 training, dance/video workflow | Open source |
| [Muzed production pipeline](https://muzed.pages.dev/#production) | Public write-up of the production workflow, model training, and tools used | Case study |
| [Koshi Vox](https://github.com/koshimazaki/koshi-vox) | Voice-to-text terminal workflow for Claude Code and agentic coding sessions | Open source |
| [LMStudio-MCP-Bridge](https://github.com/koshimazaki/LMStudio-MCP-Bridge) | MCP bridge that lets Claude Code/Desktop call local LM Studio models for docs, summaries, code analysis, refactors, and tests | Open source |
| [tailscale-runpod](https://github.com/koshimazaki/tailscale-runpod) | Claude Skill for SSH into RunPod, Vast.ai, and cloud GPU instances via Tailscale | Open source |

## Repository Utilities

### 1. API_img_gen

Addresses the A1111 API for generative prompt creation and batch generation of regularisation images. Built with DreamBooth training in mind, though the approach can be adapted for other dataset generation workflows.

Inspired by:
- [A1111 API](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API)
- Dr Furkan Gozukara's [DreamBooth and model training tutorials](https://github.com/FurkanGozukara/Stable-Diffusion/blob/main/Tutorials/How-To-Do-SDXL-DreamBooth-Training-With-Best-Settings.md)

Features:
- **Prompt generation:** Dynamically generates prompt combinations from elements, characters, environments, aesthetics, styles, artists, cameras, and points of view.
- **Image generation:** Uses generated prompts to produce images via the A1111 API and save them locally.
- **DNA assignment:** Creates a unique DNA string for each image from source-list indices and saves it as metadata.
- **State management:** Tracks generated image count and persists state between script runs.
- **Sampler selection:** Randomly selects sampler and step-size combinations from predefined options.
- **Maximum generations:** Allows a generation cap for controlled batches.
- **Random sampling:** Uses shuffled combinations to avoid repeated prompt sets.
- **Error handling:** Handles API request failures and other runtime issues.
- **Metadata saving:** Saves a JSON file beside each generated image with prompt/settings metadata.
- **CLI output:** Prints progress and state in the command line for long-running jobs.

### 2. API_img2img

Uses an A1111 image-to-image API workflow for generating variations from input and sample data. Originally tested against a fork that accepted local files on M1 Mac.

Features:
- Checks a source folder and saves batches of generated images per input image.
- Uses random prompt combinations.
- Randomises CFG scale, sampler, steps, seed, and subseed combinations.
- Saves settings to JSON with a unique DNA string, matching the API_img_gen traceability pattern.

### 3. image2image Init

Python workflow for generating images, animation starting points, and blended image sets through a local server API.

Workflow:
- **Initial setup:** Sets server URL and output directory.
- **Batch management:** Determines the next batch number for organised outputs.
- **Image processing:** Encodes images to Base64 for API transmission, decodes responses, and saves outputs plus settings.
- **API interaction:** Sends payloads with initial images and transformation parameters.
- **Dynamic parameters:** Supports prompts, denoising strength, model settings, and image dimensions.
- **Iterative processing:** Processes source-directory images and writes per-image JSON settings.
- **Traceability:** Organises output so generated images can be traced back to source images and settings.

### 4. Generate

Configuration and NFT metadata generation for Deforum API workflows.

This script automates generation of Deforum API settings and NFT metadata so batches of audiovisual digital art can be configured, rendered, and tracked consistently.

Core functions:
- **Template initialisation:** Creates base templates for Deforum settings and NFT DNA.
- **Attribute and URL mapping:** Uses a script data dictionary to map movement, material, and morph traits to source URLs.
- **Configuration generation:** Iterates over source images and script data to create Deforum settings and NFT DNA files.
- **Dynamic parameter inclusion:** Inserts dimensions, seeds, sampler types, animation settings, image paths, and prompts.
- **Batch processing:** Assigns batch and creature names for scalable production.
- **NFT metadata customisation:** Writes name, image URL, traits, and DNA strings for minting.
- **File output:** Saves generated configurations and metadata as JSON files.

### 5. Combine

Utility for combining multiple Deforum JSON configuration files into a single consolidated job file.

This is useful when a project needs multiple generated configurations but the renderer expects a unified configuration input.

### 6. ComfyUI Models Install

Jupyter notebook for installing ComfyUI models on RunPod. The notebook was built for quickly downloading models required for AnimateDiff and related ComfyUI workflows.

ComfyUI and ComfyUI Manager need to be installed separately.

Example ControlNet install command using `aria2c`:

```bash
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M \
  "https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sai_xl_canny_256lora.safetensors?download=true" \
  -d /workspace/ComfyUI/models/controlnet \
  -o sai_xl_canny_256lora.safetensors
```

Example Dreamshaper install:

```bash
aria2c --console-log-level=error -c -x 16 -s 16 -k 1M \
  "https://civitai.com/api/download/models/128713" \
  -d /workspace/ComfyUI/models/checkpoints \
  -o Dreamshaper_8.safetensors
```

### 6b. ComfyUI FLUX Models Install

Notebook for installing FLUX model dependencies into a RunPod ComfyUI template. Paths may need adjustment depending on the image/template used. Fast community cloud networking or equivalent bandwidth is recommended because the model files are large.

### 7. WAN Video ComfyUI Setup Script

Automated bash script for installing WAN video generation models and ComfyUI setup on RunPod.

Features:
- **Complete ComfyUI installation:** Automated setup with virtual environment and GPU-optimised PyTorch.
- **WAN model management:** Downloads WAN 2.1 T2V models and ControlNet depth variants.
- **Custom node integration:** Installs WAN-specific nodes and utility packages.
- **Vace-Warper models:** Uses optimised fp8 quantised models for reduced VRAM usage.
- **GPU compatibility:** Includes automatic detection with RTX 5080/5090 support.
- **Interactive menu:** Ten installation options including `Install All`.
- **Error handling:** Robust install flow with fallback mirror support.

Setup:

```bash
chmod +x run_wan.sh
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
./run_wan.sh
```

Requirements: CUDA GPU, 16GB+ VRAM recommended, 50GB+ storage, and a Hugging Face token for gated model access.
