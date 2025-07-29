import json

model_mapping = {
  "black_forest_labs/flux_1_1_pro": "black-forest-labs/flux-1.1-pro",
  "black_forest_labs/flux_1_1_pro_ultra": "black-forest-labs/flux-1.1-pro-ultra",
  "black_forest_labs/flux_1_canny_dev": "black-forest-labs/flux.1-canny-dev",
  "black_forest_labs/flux_1_canny_dev_lora": "black-forest-labs/flux.1-canny-dev-lora",
  "black_forest_labs/flux_1_canny_pro": "black-forest-labs/flux.1-canny-pro",
  "black_forest_labs/flux_1_depth_dev": "black-forest-labs/flux.1-depth-dev",
  "black_forest_labs/flux_1_depth_dev_lora": "black-forest-labs/flux.1-depth-dev-lora",
  "black_forest_labs/flux_1_depth_pro": "black-forest-labs/flux.1-depth-pro",
  "black_forest_labs/flux_1_dev": "black-forest-labs/flux.1-dev",
  "black_forest_labs/flux_1_fill_dev": "black-forest-labs/flux.1-fill-dev",
  "black_forest_labs/flux_1_fill_pro": "black-forest-labs/flux.1-fill-pro",
  "black_forest_labs/flux_1_pro": "black-forest-labs/flux.1-pro",
  "black_forest_labs/flux_1_redux_dev": "black-forest-labs/flux.1-redux-dev",
  "black_forest_labs/flux_1_redux_pro": "black-forest-labs/flux.1-redux-pro",
  "black_forest_labs/flux_1_schnell": "black-forest-labs/flux.1-schnell",
  
  "google_deepmind/imagen3": "google-deepmind/imagen3",
  "google_deepmind/veo2": "google-deepmind/veo2",
  
  "kling/kling_v1_5_pro": "kling/kling-v1.5-pro",
  "kling/kling_v1_5_standard": "kling/kling-v1.5-standard",
  "kling/kling_v1_6_pro": "kling/kling-v1.6-pro",
  "kling/kling_v1_6_standard": "kling/kling-v1.6-standard",
  "kling/kling_v2_master": "kling/kling-v2-master",
  "kling/kling_lip_sync": "kling/kling-lip-sync",
  
  "luma/photon_flash": "luma/photon-flash",
  "luma/photon": "luma/photon",
  "luma/ray_2": "luma/ray-2",
  "luma/ray_flash_2": "luma/ray-flash-2",
  
  "minimax/i2v_01": "minimax/i2v-01",
  "minimax/i2v_01_director": "minimax/i2v-01-director",
  "minimax/i2v_01_live": "minimax/i2v-01-live",
  "minimax/s2v_01": "minimax/s2v-01",
  "minimax/t2v_01": "minimax/t2v-01",
  "minimax/t2v_01_director": "minimax/t2v-01-director",
  
  "pixverse/pixverse_v3_5": "pixverse/pixverse-v3.5",
  "pixverse/pixverse_v4": "pixverse/pixverse-v4",
  "pixverse/pixverse_v4_5": "pixverse/pixverse-v4.5",
  
  "sunra/lcm": "sunra/lcm",

  "vidu/audio1_0": "vidu/audio1.0",
  "vidu/upscale_pro": "vidu/upscale-pro",
  "vidu/vidu1_5": "vidu/vidu1.5",
  "vidu/vidu2_0": "vidu/vidu2.0",
  "vidu/viduq1": "vidu/viduq1",
  
  "wan/wan2_1_1_3b_inpaint": "wan/wan2.1-1.3b-inpaint",
  "wan/wan2_1_flf2v_14b_720p": "wan/wan2.1-flf2v-14b-720p",
  "wan/wan2_1_i2v_14b_480p": "wan/wan2.1-i2v-14b-480p",
  "wan/wan2_1_i2v_14b_720p": "wan/wan2.1-i2v-14b-720p",
  "wan/wan2_1_t2v_1_3b_480p": "wan/wan2.1-t2v-1.3b-480p",
  "wan/wan2_1_t2v_14b_480p": "wan/wan2.1-t2v-14b-480p",
  "wan/wan2_1_t2v_14b_720p": "wan/wan2.1-t2v-14b-720p",
  "wan/wan2_1_vace_1_3b": "wan/wan2.1-vace-1.3b",
  "wan/wan2_1_vace_14b": "wan/wan2.1-vace-14b",

  "tencent_hunyuan/hunyuan_video_i2v": "tencent-hunyuan/hunyuan-video-i2v",
  "tencent_hunyuan/hunyuan_video_t2v": "tencent-hunyuan/hunyuan-video-t2v",
  "tencent_hunyuan/hunyuan_video_v2v": "tencent-hunyuan/hunyuan-video-v2v",

  "pika/pika_1_5": "pika/pika-1.5",
  "pika/pika_2_2": "pika/pika-2.2",
}


if __name__ == "__main__":
    print(json.dumps(model_mapping, indent=2))
