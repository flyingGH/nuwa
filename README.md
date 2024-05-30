# nuwa

## Get started

Installation:
```bash
pip install git+https://github.com/jetd1/nuwa.git

# (optional) to use segmentation
pip install git+https://github.com/facebookresearch/segment-anything.git
```

Demo:
```python
import nuwa

db = nuwa.from_image_folder(img_dir)
# db = nuwa.from_video(video_dir, out_img_dir)
# db = nuwa.from_colmap(img_dir, colmap_dir)
# db = nuwa.from_polycam(polycam_dir)

masks = db.calculate_object_mask(mask_save_dir)
db.dump("db.json")
```

## Nuwa metadata format

Example:

```
{
  "source": "colmap",                      // source of the data, choices [colmap, blender]
  
  "up": [                                  // up vector of the scene
    0.018489610893192888,
    0.2981818762436387,
    -0.7178426463982863
  ],
  
  "frames": [                              // list of frames
    {                                      // frame 1
      "file_path": "./000000.png",         // path to the referenced frame
      "mask_path": "./000000_mask.png",    // path to the mask associated with the referenced frame (optional, "")
      "org_path": "./_0001.png",           // path to the original image of the referenced frame (optional, "")
      "c2w": MATRIX (4x4),                 // "c2w", "w2c", "transform_matrix" are the camera matrices in different conventions
      "w2c": MATRIX (4x4),                 // please refer to the camera_matrices_hints for more information
      "transform_matrix": MATRIX (4x4),
      "sharpness": 209.16439819335938,     // frame sharpness (higher better)
      "seq_id": 1,                         // sequence id of the frame from e.g. colmap (do not use this for now)
      "camera_matrices_hints": {           // hints for the camera matrices, format: "key_name: convention"
        "c2w": "OPENCV_c2w",
        "w2c": "OPENCV_w2c",
        "transform_matrix": "BLENDER_c2w"
      },
      "w": 512,                            // camera intrinsics
      "h": 512,
      "fx": 756.2237500859011,
      "fy": 755.1240357896131,
      "cx": 250.32151789051335,
      "cy": 219.18349060141304,
      "is_fisheye": false,
      "fl_x": 756.2237500859011,
      "fl_y": 755.1240357896131,
      "camera_angle_x": 0.6528299784,
      "camera_angle_y": 0.6537144781,
      "fovx": 37.40440250475687,
      "foxy": 37.455080603392624,
      "intrinsic_matrix": MATRIX (3x3),     // camera intrinsics matrix
      "camera_param_model": "PINHOLE"       // camera model, choices: [PINHOLE, OPENCV]
                                            // https://colmap.github.io/cameras.html
    },
    ...                                     // frame 2 and more
  ]
}
```