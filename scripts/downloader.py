import os
import subprocess

import gradio as gr
from modules import script_callbacks, paths
from pathlib import Path
# Path to aria2c binary file
extensions_dir = Path(paths.script_path, "extensions")
aria2c_path = f'{extensions_dir}/sd.webui-model-downloader/scripts/aria2c.exe'


def download_with_aria2c(url, destination):
    process = subprocess.Popen(
        [aria2c_path, "-x", "16", "-s", "16", "-o", destination, url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(
            f"Download failed with error code {process.returncode}:\n{stderr.decode('utf-8')}")
    print("Download complete.")
    return "Download complete."


def download_model(download_url, dropdown, filename):

    filename = filename or os.path.basename(download_url)

    if dropdown == "Stable Diffusion":
        destination = "models/Stable-diffusion/" + filename
    elif dropdown == "LoRA":
        destination = "models/Lora/" + filename
    elif dropdown == "VAE":
        destination = "models/vae/" + filename
    else:
        destination = "embeddings/" + filename
        print(destination)

    download_with_aria2c(download_url, destination)


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        download_url = gr.Textbox(label="Download URL")
        dropdown = gr.Dropdown(
            label="Download Path",
            choices=["Stable Diffusion", "LoRA", "VAE", "Embeddings"],
            value="Stable Diffusion"
        )
        filename = gr.Textbox(label="Filename")
        download_button = gr.Button(value="Download")

        download_button.click(
            fn=download_model,
            inputs=[download_url, dropdown, filename],
            outputs=[],
        )
        return [(ui_component, "Model Downloader", "model_downloader_tab")]


script_callbacks.on_ui_tabs(on_ui_tabs)
