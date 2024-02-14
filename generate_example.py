import json

# Base JSON structure for Deforum settings
deforum_settings_template = """


"""


# Base JSON structure for NFT DNA
nft_base = {
    "Name": "",
    "Description": "Supernatural Creature",
    "Image": "",
    "Movement": "",
    "Material": "",
    "Morph_type": "",
    "DNA": "",
    "Script_url": ""
}

# Script Attributes and URLs Mappings
script_data = {
    "Metal1": {
        "attributes": {"Movement": "1", "Material": "Wood", "Morph_type": "Single"},
        "url": "https://firebasestorage.googleapis.com/v0/b/sd-parseq.appspot.com/o/rendered%2FpwQAo1uN74Myzxb2D7aszFnL7nZ2%2Fdoc-14621217-e46a-4a9b-981a-07d91adb0cdc.json?alt=media&token=d5afe706-c284-4866-8402-61f396cdb6d2"
    },
    "Metal2": {
        "attributes": {"Movement": "3_zoom", "Material": "Wood", "Morph_type": "Single"},
        "url": "https://firebasestorage.googleapis.com/v0/b/sd-parseq.appspot.com/o/rendered%2FpwQAo1uN74Myzxb2D7aszFnL7nZ2%2Fdoc-29bd3aac-ac05-4f3d-b8bf-be743c70c63d.json?alt=media&token=99a22a89-969a-4663-98c1-ce4b3a55a3aa"
    },

    # ...other traits potentially here
}

# Function to generate JSON files
def generate_json_files():
    deforum_json_configs = []
    nft_json_configs = []
    batch_counter = 100

    for img_num in range(1, 37):  # 37 images
        for script, data in script_data.items():
            # Building Deforum config as a dictionary
            deforum_config = {
    "W": 1024,
    "H": 1024,
    "show_info_on_ui": True,
    "tiling": False,
    "restore_faces": False,
    "seed_resize_from_w": 0,
    "seed_resize_from_h": 0,
    "seed": -1,
    "sampler": "Euler",
    "steps": 40,
    "batch_name": f"Creature_{batch_counter}",  ## this is for name easy to rename after 
    "seed_behavior": "iter",
    "seed_iter_N": 1,
    "use_init": True,
    "strength": 0.8,
    "strength_0_no_init": False,
    "init_image": f"/workspace/source/metal/{img_num}.png",   ## change init img folder 
    "use_mask": False,
    "use_alpha_as_mask": False,
    "mask_file": "https://deforum.github.io/a1/M1.jpg",
    "invert_mask": False,
    "mask_contrast_adjust": 1.0,
    "mask_brightness_adjust": 1.0,
    "overlay_mask": True,
    "mask_overlay_blur": 4,
    "fill": 1,
    "full_res_mask": True,
    "full_res_mask_padding": 4,
    "reroll_blank_frames": "ignore",
    "reroll_patience": 10.0,
    "motion_preview_mode": False,
    "prompts": {
        "0": "tiny cute bunny, vibrant diffraction, highly detailed, intricate, ultra hd, sharp photo, crepuscular rays, in focus",
        "30": "anthropomorphic clean cat, surrounded by fractals, epic angle and pose, symmetrical, 3d, depth of field",
        "60": "a beautiful coconut --neg photo, realistic",
        "90": "a beautiful durian, award winning photography"
    },
    "animation_prompts_positive": "",
    "animation_prompts_negative": "nsfw, nude",
    "animation_mode": "3D",
    "max_frames": 120,
    "border": "replicate",
    "angle": "0: (0)",
    "zoom": "0: (1.0025+0.002*sin(1.25*3.14*t/30))",
    "translation_x": "0: (0)",
    "translation_y": "0: (0)",
    "translation_z": "0: (1.75)",
    "transform_center_x": "0: (0.5)",
    "transform_center_y": "0: (0.5)",
    "rotation_3d_x": "0: (0)",
    "rotation_3d_y": "0: (0)",
    "rotation_3d_z": "0: (0)",
    "enable_perspective_flip": False,
    "perspective_flip_theta": "0: (0)",
    "perspective_flip_phi": "0: (0)",
    "perspective_flip_gamma": "0: (0)",
    "perspective_flip_fv": "0: (53)",
    "noise_schedule": "0: (0.065)",
    "strength_schedule": "0: (0.65)",
    "contrast_schedule": "0: (1.0)",
    "cfg_scale_schedule": "0: (7)",
    "enable_steps_scheduling": False,
    "steps_schedule": "0: (25)",
    "fov_schedule": "0: (70)",
    "aspect_ratio_schedule": "0: (1)",
    "aspect_ratio_use_old_formula": False,
    "near_schedule": "0: (200)",
    "far_schedule": "0: (10000)",
    "seed_schedule": "0:(s), 1:(-1), \"max_f-2\":(-1), \"max_f-1\":(s)",
    "pix2pix_img_cfg_scale_schedule": "0:(1.5)",
    "enable_subseed_scheduling": False,
    "subseed_schedule": "0: (1)",
    "subseed_strength_schedule": "0: (0)",
    "enable_sampler_scheduling": False,
    "sampler_schedule": "0: (\"Euler a\")",
    "use_noise_mask": False,
    "mask_schedule": "0: (\"{video_mask}\")",
    "noise_mask_schedule": "0: (\"{video_mask}\")",
    "enable_checkpoint_scheduling": False,
    "checkpoint_schedule": "0: (\"model1.ckpt\"), 100: (\"model2.safetensors\")",
    "enable_clipskip_scheduling": False,
    "clipskip_schedule": "0: (2)",
    "enable_noise_multiplier_scheduling": True,
    "noise_multiplier_schedule": "0: (1.05)",
    "resume_from_timestring": False,
    "resume_timestring": "20240104234824",
    "enable_ddim_eta_scheduling": False,
    "ddim_eta_schedule": "0: (0)",
    "enable_ancestral_eta_scheduling": False,
    "ancestral_eta_schedule": "0: (1)",
    "amount_schedule": "0: (0.1)",
    "kernel_schedule": "0: (5)",
    "sigma_schedule": "0: (1)",
    "threshold_schedule": "0: (0)",
    "color_coherence": "LAB",
    "color_coherence_image_path": "",
    "color_coherence_video_every_N_frames": 1,
    "color_force_grayscale": False,
    "legacy_colormatch": False,
    "diffusion_cadence": 1,
    "optical_flow_cadence": "RAFT",
    "cadence_flow_factor_schedule": "0: (1)",
    "optical_flow_redo_generation": "None",
    "redo_flow_factor_schedule": "0: (1)",
    "diffusion_redo": "0",
    "noise_type": "perlin",
    "perlin_octaves": 4,
    "perlin_persistence": 0.5,
    "use_depth_warping": False,
    "depth_algorithm": "Zoe",
    "midas_weight": 0.2,
    "padding_mode": "border",
    "sampling_mode": "bicubic",
    "save_depth_maps": False,
    "video_init_path": "https://deforum.github.io/a1/V1.mp4",
    "extract_nth_frame": 1,
    "extract_from_frame": 0,
    "extract_to_frame": -1,
    "overwrite_extracted_frames": False,
    "use_mask_video": False,
    "video_mask_path": "https://deforum.github.io/a1/VM1.mp4",
    "hybrid_comp_alpha_schedule": "0:(0.5)",
    "hybrid_comp_mask_blend_alpha_schedule": "0:(0.5)",
    "hybrid_comp_mask_contrast_schedule": "0:(1)",
    "hybrid_comp_mask_auto_contrast_cutoff_high_schedule": "0:(100)",
    "hybrid_comp_mask_auto_contrast_cutoff_low_schedule": "0:(0)",
    "hybrid_flow_factor_schedule": "0:(1)",
    "hybrid_generate_inputframes": False,
    "hybrid_generate_human_masks": "None",
    "hybrid_use_first_frame_as_init_image": True,
    "hybrid_motion": "None",
    "hybrid_motion_use_prev_img": False,
    "hybrid_flow_consistency": False,
    "hybrid_consistency_blur": 2,
    "hybrid_flow_method": "RAFT",
    "hybrid_composite": "None",
    "hybrid_use_init_image": False,
    "hybrid_comp_mask_type": "None",
    "hybrid_comp_mask_inverse": False,
    "hybrid_comp_mask_equalize": "None",
    "hybrid_comp_mask_auto_contrast": False,
    "hybrid_comp_save_extra_frames": False,
    "parseq_manifest": data["url"],
    "parseq_use_deltas": True,
    "parseq_non_schedule_overrides": True,
    "use_looper": False,
    "init_images": "{\n    \"0\": \"https://deforum.github.io/a1/Gi1.png\",\n    \"max_f/4-5\": \"https://deforum.github.io/a1/Gi2.png\",\n    \"max_f/2-10\": \"https://deforum.github.io/a1/Gi3.png\",\n    \"3*max_f/4-15\": \"https://deforum.github.io/a1/Gi4.jpg\",\n    \"max_f-20\": \"https://deforum.github.io/a1/Gi1.png\"\n}",
    "image_strength_schedule": "0:(0.75)",
    "blendFactorMax": "0:(0.35)",
    "blendFactorSlope": "0:(0.25)",
    "tweening_frames_schedule": "0:(20)",
    "color_correction_factor": "0:(0.075)",
    "cn_1_overwrite_frames": True,
    "cn_1_vid_path": "",
    "cn_1_mask_vid_path": "",
    "cn_1_enabled": False,
    "cn_1_low_vram": False,
    "cn_1_pixel_perfect": False,
    "cn_1_module": "none",
    "cn_1_model": "None",
    "cn_1_weight": "0:(1)",
    "cn_1_guidance_start": "0:(0.0)",
    "cn_1_guidance_end": "0:(1.0)",
    "cn_1_processor_res": 64,
    "cn_1_threshold_a": 64,
    "cn_1_threshold_b": 64,
    "cn_1_resize_mode": "Inner Fit (Scale to Fit)",
    "cn_1_control_mode": "Balanced",
    "cn_1_loopback_mode": False,
    "cn_2_overwrite_frames": True,
    "cn_2_vid_path": "",
    "cn_2_mask_vid_path": "",
    "cn_2_enabled": False,
    "cn_2_low_vram": False,
    "cn_2_pixel_perfect": False,
    "cn_2_module": "none",
    "cn_2_model": "None",
    "cn_2_weight": "0:(1)",
    "cn_2_guidance_start": "0:(0.0)",
    "cn_2_guidance_end": "0:(1.0)",
    "cn_2_processor_res": 64,
    "cn_2_threshold_a": 64,
    "cn_2_threshold_b": 64,
    "cn_2_resize_mode": "Inner Fit (Scale to Fit)",
    "cn_2_control_mode": "Balanced",
    "cn_2_loopback_mode": False,
    "cn_3_overwrite_frames": True,
    "cn_3_vid_path": "",
    "cn_3_mask_vid_path": "",
    "cn_3_enabled": False,
    "cn_3_low_vram": False,
    "cn_3_pixel_perfect": False,
    "cn_3_module": "none",
    "cn_3_model": "None",
    "cn_3_weight": "0:(1)",
    "cn_3_guidance_start": "0:(0.0)",
    "cn_3_guidance_end": "0:(1.0)",
    "cn_3_processor_res": 64,
    "cn_3_threshold_a": 64,
    "cn_3_threshold_b": 64,
    "cn_3_resize_mode": "Inner Fit (Scale to Fit)",
    "cn_3_control_mode": "Balanced",
    "cn_3_loopback_mode": False,
    "cn_4_overwrite_frames": True,
    "cn_4_vid_path": "",
    "cn_4_mask_vid_path": "",
    "cn_4_enabled": False,
    "cn_4_low_vram": False,
    "cn_4_pixel_perfect": False,
    "cn_4_module": "none",
    "cn_4_model": "None",
    "cn_4_weight": "0:(1)",
    "cn_4_guidance_start": "0:(0.0)",
    "cn_4_guidance_end": "0:(1.0)",
    "cn_4_processor_res": 64,
    "cn_4_threshold_a": 64,
    "cn_4_threshold_b": 64,
    "cn_4_resize_mode": "Inner Fit (Scale to Fit)",
    "cn_4_control_mode": "Balanced",
    "cn_4_loopback_mode": False,
    "cn_5_overwrite_frames": True,
    "cn_5_vid_path": "",
    "cn_5_mask_vid_path": "",
    "cn_5_enabled": False,
    "cn_5_low_vram": False,
    "cn_5_pixel_perfect": False,
    "cn_5_module": "none",
    "cn_5_model": "None",
    "cn_5_weight": "0:(1)",
    "cn_5_guidance_start": "0:(0.0)",
    "cn_5_guidance_end": "0:(1.0)",
    "cn_5_processor_res": 64,
    "cn_5_threshold_a": 64,
    "cn_5_threshold_b": 64,
    "cn_5_resize_mode": "Inner Fit (Scale to Fit)",
    "cn_5_control_mode": "Balanced",
    "cn_5_loopback_mode": False,
    "skip_video_creation": False,
    "fps": 15,
    "make_gif": False,
    "delete_imgs": False,
    "delete_input_frames": False,
    "add_soundtrack": "None",
    "soundtrack_path": "https://deforum.github.io/a1/A1.mp3",
    "r_upscale_video": False,
    "r_upscale_factor": "x2",
    "r_upscale_model": "realesr-animevideov3",
    "r_upscale_keep_imgs": True,
    "store_frames_in_ram": False,
    "frame_interpolation_engine": "FILM",
    "frame_interpolation_x_amount": 2,
    "frame_interpolation_slow_mo_enabled": False,
    "frame_interpolation_slow_mo_amount": 2,
    "frame_interpolation_keep_imgs": False,
    "frame_interpolation_use_upscaled": False,
    "sd_model_name": "protovisionXLHighFidelity3D_release0630Bakedvae.safetensors",
    "sd_model_hash": "2d24c634",
    "deforum_git_commit_id": "d3b00b3c"
}
            deforum_json_configs.append(deforum_config)


            batch_counter = 1

            # NFT DNA Config
            nft_config = nft_base.copy()
            nft_config["Name"] = f"Creature_{batch_counter}"
            nft_config["Image"] = f"https://example.com/nft/creature_{batch_counter}.png"
            nft_config["Movement"] = data["attributes"]["Movement"]
            nft_config["Material"] = data["attributes"]["Material"]
            nft_config["Morph_type"] = data["attributes"]["Morph_type"]
            nft_config["DNA"] = f"IMG_{img_num}-{script}-MOV_{data['attributes']['Movement']}-MAT_{data['attributes']['Material']}-MORPH_{data['attributes']['Morph_type']}"
            nft_config["Script_url"] = data["url"]
            nft_json_configs.append(nft_config)

            batch_counter += 1

    return deforum_json_configs, nft_json_configs

# Generate JSON configurations
deforum_configs, nft_configs = generate_json_files()

# Saving each Deforum and NFT config to separate files
for i, (deforum_config, nft_config) in enumerate(zip(deforum_configs, nft_configs), start=1):
    with open(f'deforum_creature_{i}_config.json', 'w') as file:
        json.dump(deforum_config, file, indent=4)
    with open(f'nft_creature_{i}_config.json', 'w') as file:
        json.dump(nft_config, file, indent=4)
