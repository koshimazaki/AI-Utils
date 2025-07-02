#!/bin/bash

set -e

# ANSI color codes for better UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Path to the venv's Python interpreter
VENV_PYTHON="/workspace/ComfyUI/venv/bin/python"

# Default Hugging Face token (replace with your token or leave empty to require HF_TOKEN env var)
DEFAULT_HF_TOKEN="your HF token here"  # Set to your token (e.g., "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") or leave empty

# Function to install system dependencies
install_system_deps() {
    echo "Installing system dependencies..."
    apt-get update
    if ! apt-get install -y --fix-missing python3 python3-pip git aria2 ffmpeg libsm6 libxext6 build-essential ninja-build cmake libopenblas-dev; then
        echo "${RED}Initial install failed. Switching to fallback mirror...${NC}"
        cp /etc/apt/sources.list /etc/apt/sources.list.bak
        cat << EOF > /etc/apt/sources.list
deb http://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb http://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
EOF
        apt-get update
        if ! apt-get install -y --fix-missing python3 python3-pip git aria2 ffmpeg libsm6 libxext6 build-essential ninja-build cmake libopenblas-dev; then
            echo "${YELLOW}Fallback mirror failed. Attempting manual libzmq5 installation...${NC}"
            wget http://mirrors.ustc.edu.cn/ubuntu/pool/universe/z/zeromq3/libzmq5_4.3.4-2_amd64.deb
            dpkg -i libzmq5_4.3.4-2_amd64.deb
            apt-get install -f
            rm libzmq5_4.3.4-2_amd64.deb
            if ! apt-get install -y --fix-missing python3 python3-pip git aria2 ffmpeg libsm6 libxext6 build-essential ninja-build cmake libopenblas-dev; then
                echo "${RED}Failed to install system dependencies. Check network or repository settings.${NC}"
                exit 1
            fi
        fi
    fi
    if ! command -v pip3 >/dev/null 2>&1; then
        echo "${YELLOW}pip3 not found. Installing manually...${NC}"
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        if [ $? -ne 0 ]; then
            echo "${RED}Failed to install pip manually.${NC}"
            rm -f get-pip.py
            exit 1
        fi
        rm -f get-pip.py
    fi
}

# Function to check GPU compatibility
check_gpu_compatibility() {
    echo "Checking GPU compatibility..."
    if "$VENV_PYTHON" -c "import torch; exit(0 if torch.cuda.get_device_capability(0) == (12, 0) else 1)" 2>/dev/null; then
        echo "${RED}Detected SM_120 GPU (e.g., RTX 5080/5090). PyTorch nightly may not support SM_120. Run option 8 to compile PyTorch from source.${NC}"
        return 1
    else
        echo "${GREEN}GPU is compatible with PyTorch (SM_50, SM_60, SM_70, SM_75, SM_80, SM_86, or SM_90).${NC}"
        return 0
    fi
}

# Function to install or update ComfyUI
install_comfyui() {
    echo "Installing/Updating ComfyUI..."
    if [ -d "/workspace/ComfyUI" ]; then
        echo "Updating ComfyUI..."
        cd /workspace/ComfyUI
        git pull
    else
        echo "Cloning ComfyUI..."
        git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI
    fi
    cd /workspace/ComfyUI
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r requirements.txt
    "$VENV_PYTHON" -m pip install --force-reinstall --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128
    "$VENV_PYTHON" -m pip install huggingface_hub tqdm requests opencv-python numexpr imageio-ffmpeg simpleeval pandas matplotlib triton
    # Clean up ~umpy if present
    rm -rf /workspace/ComfyUI/venv/lib/python3.11/site-packages/~umpy*
    "$VENV_PYTHON" -m pip install numpy
    # Check GPU compatibility
    check_gpu_compatibility
    mkdir -p models/checkpoints models/controlnet custom_nodes models/diffusion_models models/loras models/vae models/text_encoders
    echo "ComfyUI installed/updated. To start, select option 1 or run: $VENV_PYTHON /workspace/ComfyUI/main.py"
}

# Function to check and set Hugging Face token
check_hf_token() {
    HF_TOKEN=${HF_TOKEN:-$DEFAULT_HF_TOKEN}
    if [ -z "$HF_TOKEN" ] || [ "$HF_TOKEN" = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ]; then
        echo "${RED}Hugging Face token not set or invalid. Please set HF_TOKEN environment variable or update DEFAULT_HF_TOKEN in the script.${NC}"
        echo "Generate a token at https://huggingface.co/settings/tokens with read permissions."
        echo "Set it with: export HF_TOKEN='hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'"
        echo "Or run: HF_TOKEN='hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' ./run_wan.sh"
        exit 1
    fi
    cd /workspace/ComfyUI
    "$VENV_PYTHON" -c "
from huggingface_hub import login
login(token='$HF_TOKEN')
"
    if [ $? -ne 0 ]; then
        echo "${RED}Failed to log in with Hugging Face token. Verify token and repository access at https://huggingface.co/lightx2v/Wan2.1-T2V-14B-CausVid${NC}"
        exit 1
    fi
}

# Function to install WAN model and custom nodes
install_wan_model() {
    if [ ! -d "/workspace/ComfyUI" ]; then
        echo "${RED}ComfyUI is not installed. Please install ComfyUI first.${NC}"
        exit 1
    fi
    echo "Installing WAN custom nodes..."
    cd /workspace/ComfyUI/custom_nodes
    if [ -d "WanVideo_comfy" ]; then
        echo "Updating WAN custom nodes..."
        cd WanVideo_comfy
        git pull
        cd ..
    else
        git clone https://huggingface.co/Kijai/WanVideo_comfy.git
    fi
    if [ -f "WanVideo_comfy/requirements.txt" ]; then
        cd /workspace/ComfyUI
        "$VENV_PYTHON" -m pip install -r custom_nodes/WanVideo_comfy/requirements.txt
    fi
    check_hf_token
    echo "Select WAN model to install:"
    echo "1. Main WAN model (Wan2.1-T2V-14B-CausVid)"
    echo "2. ControlNet Depth variant (wan2.1-t2v-14b-controlnet-depth-v1)"
    echo "3. Both WAN models"
    echo "4. Skip model installation"
    read -p "Select an option (1-4): " model_choice
    cd /workspace/ComfyUI
    case $model_choice in
        1|3)
            echo "Downloading main WAN model..."
            "$VENV_PYTHON" -c "
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id='lightx2v/Wan2.1-T2V-14B-CausVid', filename='Wan2.1-T2V-14B-CausVid.safetensors', local_dir='/workspace/ComfyUI/models/checkpoints')
"
            if [ $? -ne 0 ]; then
                echo "${RED}Failed to download main WAN model. Check token permissions or repository access at https://huggingface.co/lightx2v/Wan2.1-T2V-14B-CausVid${NC}"
                exit 1
            fi
            ;;
    esac
    case $model_choice in
        2|3)
            echo "Downloading ControlNet Depth WAN model..."
            "$VENV_PYTHON" -c "
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id='TheDenk/wan2.1-t2v-14b-controlnet-depth-v1', filename='wan2.1-t2v-14b-controlnet-depth-v1.safetensors', local_dir='/workspace/ComfyUI/models/controlnet')
"
            if [ $? -ne 0 ]; then
                echo "${RED}Failed to download ControlNet Depth WAN model. Check token permissions or repository access at https://huggingface.co/TheDenk/wan2.1-t2v-14b-controlnet-depth-v1${NC}"
                exit 1
            fi
            ;;
    esac
    case $model_choice in
        4)
            echo "Skipping WAN model installation."
            ;;
        *)
            echo "${RED}Invalid option. Skipping model installation.${NC}"
            ;;
    esac
    echo "${GREEN}WAN model(s) and custom nodes installed successfully.${NC}"
}

# Function to install Vace-Warper-Models
install_vace_warper_models() {
    if [ ! -d "/workspace/ComfyUI" ]; then
        echo "${RED}ComfyUI is not installed. Please install ComfyUI first.${NC}"
        exit 1
    fi
    echo "Installing Vace-Warper-Models..."
    cd /workspace/ComfyUI
    check_hf_token
    mkdir -p models/diffusion_models models/loras models/vae models/text_encoders
    declare -A models
    models["Wan2_1-T2V-14B_fp8_e4m3fn.safetensors"]="models/diffusion_models"
    models["Wan2_1-VACE_module_14B_fp8_e4m3fn.safetensors"]="models/diffusion_models"
    models["Wan21_CausVid_14B_T2V_lora_rank32_v2.safetensors"]="models/loras"
    models["Wan2_1_VAE_bf16.safetensors"]="models/vae"
    models["umt5-xxl-enc-bf16.safetensors"]="models/text_encoders"
    for filename in "${!models[@]}"; do
        local_dir="${models[$filename]}"
        if [ ! -f "$local_dir/$filename" ]; then
            echo "Downloading $filename to $local_dir..."
            "$VENV_PYTHON" -c "
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id='Kijai/WanVideo_comfy', filename='$filename', local_dir='/workspace/ComfyUI/$local_dir')
"
            if [ $? -ne 0 ]; then
                echo "${RED}Failed to download $filename. Check token permissions or repository access.${NC}"
                exit 1
            fi
        else
            echo "$filename already exists in $local_dir. Skipping download."
        fi
    done
    echo "${GREEN}Vace-Warper-Models installed successfully.${NC}"
}

# Function to install ComfyUI-Manager
install_comfyui_manager() {
    if [ ! -d "/workspace/ComfyUI" ]; then
        echo "${RED}ComfyUI is not installed. Please install ComfyUI first.${NC}"
        exit 1
    fi
    echo "Installing ComfyUI-Manager..."
    cd /workspace/ComfyUI/custom_nodes
    if [ -d "ComfyUI-Manager" ]; then
        echo "Updating ComfyUI-Manager..."
        cd ComfyUI-Manager
        git pull
        cd ..
    else
        git clone https://github.com/Comfy-Org/ComfyUI-Manager.git
    fi
    if [ -f "ComfyUI-Manager/requirements.txt" ]; then
        cd /workspace/ComfyUI
        "$VENV_PYTHON" -m pip install -r custom_nodes/ComfyUI-Manager/requirements.txt
    fi
    echo "${GREEN}ComfyUI-Manager installed successfully.${NC}"
}

# Function to install a custom node from a repository URL
install_custom_node() {
    local repo_url=$1
    local repo_name=$(basename $repo_url .git)
    cd /workspace/ComfyUI/custom_nodes
    if [ -d "$repo_name" ]; then
        echo "Updating $repo_name..."
        cd $repo_name
        git pull
        cd ..
    else
        echo "Cloning $repo_name..."
        git clone $repo_url
    fi
    if [ -f "$repo_name/requirements.txt" ]; then
        cd /workspace/ComfyUI
        "$VENV_PYTHON" -m pip install -r custom_nodes/$repo_name/requirements.txt
    fi
}

# List of additional custom node packs to install
additional_node_packs=(
    "https://github.com/kijai/ComfyUI-WanVideoWrapper"
    "https://github.com/yuvraj108c/ComfyUI-Video-Depth-Anything"
    "https://github.com/shinich39/comfyui-get-meta"
    "https://github.com/kijai/ComfyUI-KJNodes"
    "https://github.com/aria1th/ComfyUI-LogicUtils"
    "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite"
    "https://github.com/Fannovel16/comfyui_controlnet_aux"
    "https://github.com/SageAttention/ComfyUI-SageAttention"
    "https://github.com/welltop-cn/ComfyUI-TeaCache"
)

# Function to install additional custom node packs
install_additional_node_packs() {
    if [ ! -d "/workspace/ComfyUI" ]; then
        echo "${RED}ComfyUI is not installed. Please install ComfyUI first.${NC}"
        exit 1
    fi
    echo "Installing additional custom node packs..."
    for repo_url in "${additional_node_packs[@]}"; do
        install_custom_node $repo_url
    done
    echo "Installing onnxruntime-gpu for DWPreprocessor..."
    "$VENV_PYTHON" -m pip install --force-reinstall onnxruntime-gpu==1.19.2
    if [ $? -ne 0 ]; then
        echo "${RED}Failed to install onnxruntime-gpu. Check pip and CUDA compatibility.${NC}"
        exit 1
    fi
    echo "${GREEN}Additional custom node packs and onnxruntime-gpu installed successfully.${NC}"
}

# Function to install Triton
install_triton() {
    echo "Installing Triton..."
    if "$VENV_PYTHON" -c "import triton" 2>/dev/null; then
        echo "${GREEN}Triton is already installed. Skipping installation.${NC}"
    else
        "$VENV_PYTHON" -m pip install triton
        if [ $? -ne 0 ]; then
            echo "${RED}Failed to install Triton. Check pip and CUDA compatibility.${NC}"
            exit 1
        fi
        echo "${GREEN}Triton installed successfully.${NC}"
    fi
}

# Function to compile PyTorch from source for SM_120
install_pytorch_source() {
    echo "Installing PyTorch from source for SM_120 support..."
    apt-get update && apt-get install -y build-essential ninja-build cmake libopenblas-dev
    "$VENV_PYTHON" -m pip install numpy pyyaml setuptools
    cd /workspace
    if [ -d "pytorch" ]; then
        echo "Updating PyTorch repository..."
        cd pytorch
        git pull
        cd ..
    else
        echo "Cloning PyTorch repository..."
        git clone --recursive https://github.com/pytorch/pytorch
    fi
    cd pytorch
    export TORCH_CUDA_ARCH_LIST="12.0"
    export USE_CUDA=1
    export CUDA_HOME=/usr/local/cuda
    "$VENV_PYTHON" setup.py install
    if [ $? -ne 0 ]; then
        echo "${RED}Failed to compile PyTorch. Check build logs for errors.${NC}"
        exit 1
    fi
    "$VENV_PYTHON" -c "import torch; assert torch.cuda.get_device_capability(0) == (12, 0), 'PyTorch compilation failed to support SM_120'; print('PyTorch supports SM_120')"
    echo "${GREEN}PyTorch compiled and installed successfully.${NC}"
}

# Function to start ComfyUI
start_comfyui() {
    if [ ! -d "/workspace/ComfyUI" ]; then
        echo "${RED}ComfyUI not found. Please install ComfyUI first.${NC}"
        exit 1
    fi
    echo "Starting ComfyUI..."
    read -p "Enable CUDA_LAUNCH_BLOCKING for debugging? (y/n): " debug_choice
    if [ "$debug_choice" = "y" ] || [ "$debug_choice" = "Y" ]; then
        export CUDA_LAUNCH_BLOCKING=1
        echo "${YELLOW}CUDA_LAUNCH_BLOCKING enabled for debugging.${NC}"
    else
        unset CUDA_LAUNCH_BLOCKING
        echo "CUDA_LAUNCH_BLOCKING disabled."
    fi
    cd /workspace/ComfyUI
    "$VENV_PYTHON" main.py --listen 0.0.0.0 --port 8188 
}

# Display main menu
while true; do
    clear
    echo "Welcome to the ComfyUI Installation Menu"
    echo "1. Start ComfyUI"
    echo "2. Install ComfyUI"
    echo "3. Install WAN model and custom nodes"
    echo "4. Install Vace-Warper-Models"
    echo "5. Install ComfyUI-Manager"
    echo "6. Install additional custom node packs"
    echo "7. Install Triton"
    echo "8. Compile PyTorch from source (for RTX 5080/5090)"
    echo "9. Install all (ComfyUI, WAN, Vace-Warper-Models, Manager, node packs, Triton)"
    echo "10. Exit"
    read -p "Select an option (1-10): " choice

    case $choice in
        1) start_comfyui; break ;;
        2) install_system_deps; install_comfyui; break ;;
        3) install_wan_model; break ;;
        4) install_vace_warper_models; break ;;
        5) install_comfyui_manager; break ;;
        6) install_additional_node_packs; break ;;
        7) install_triton; break ;;
        8) install_pytorch_source; break ;;
        9) install_system_deps; install_comfyui; install_wan_model; install_vace_warper_models; install_comfyui_manager; install_additional_node_packs; install_triton; break ;;
        10) exit 0 ;;
        *) echo "${RED}Invalid option. Please select 1-10.${NC}"; sleep 2 ;;
    esac
done

echo "${GREEN}Operation completed.${NC}"