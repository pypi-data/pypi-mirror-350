# vlm_inference

This repository contains code for performing inference using a Vision-Language Model (VLM) for robotic navigation tasks.

## Setup Instructions

Follow these steps to use the library, it is already available by PyP:

1.  **Intall library:**

Here you have two options, install twrought the PyP:
```bash
    pip install openai==1.78.1 opencv-python==4.11.0.86 pyyaml dotenv==0.9.9 pillow==9.0.1
```

```bash
    pip install vlm_inference
```
You can try the library in action using this Colab notebook:  
📎 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/11CpTjpGd-fZ2qdRMq8kt_fb5nq7TQD9b?usp=sharing)



Install since the repostitory:

```bash
    git clone ssh://git@gitlab.iri.upc.edu:2202/mobile_robotics/moonshot_project/vlm/vlm_inference.git

    cd vlm_inference
```

```bash
    python3 pip install -r requirements.txt
```
Install by the repository

```bash
    pip install -e .
```




2.  **Create a `.env` file and add your OpenAI API key and the VLM configuration path:**

    Create a file named `.env` in the root directory of the repository and add the following content, replacing `sk-proj-_HFJE2I64...........` with your actual OpenAI API key and ensuring the `VLM_CONFIG_PATH` points to your configuration file:

```
    # .env
    OPENAI_API_KEY=sk-proj-_HFJE2I64...........
    VLM_CONFIG_PATH=vlm_inference/config.yaml
```

If you have can´t not modify the python version use the following command:
```bash
    python3 pip install -r requirements.txt
```


5.  **Set the navigation goal (optional):**

    If you want to specify a navigation goal as an object or person with a description, open the following file:

```
    vlm_navigation/prompt_manager/navigation_prompt.txt
```

    Locate line 7, which defines the `navigation_goal` variable, and modify it according to your desired goal. For example:

```
    navigation_goal = "a red chair near the window"
```

6.  **Run the inference script:**

    Execute the main inference script using Python 3:

```bash
    python3 vlm_navigation/inference.py
```

This script will load the VLM, potentially process images (depending on the script's functionality), and output the inference results based on the configuration and any specified navigation goal.
