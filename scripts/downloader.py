import os
import subprocess

import gradio as gr
from modules import script_callbacks

# Path to aria2c binary file
aria2c_path = "extensions/sd.webui-model-downloader/scripts/aria2c.exe"

def download_with_aria2c(url, destination):
    process = subprocess.Popen(
        [aria2c_path, "-x", "16", "-s", "16", "-o", destination, url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Download failed with error code {process.returncode}:\n{stderr.decode('utf-8')}")
    print("Download complete.")
    return "Download complete."

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        download_url = gr.Textbox(label="Download URL")
        dropdown = gr.Dropdown(
            label="Download Path",
            choices=["Stable Diffusion", "LoRA", "VAE","Embeddings"]
        )
        filename = gr.Textbox(label="Filename")
        download_button = gr.Button(value="Download")

        def download_model(download_url, dropdown, filename):
            url = download_url
            filename = filename or "downloaded_file"
            destination = ""
            
            if dropdown == "Stable Diffusion":
                destination = "models/Stable-diffusion/models/" + filename
            elif dropdown == "LoRA":
                destination = "models/Lora/models/" + filename
            elif dropdown == "VAE":
                destination = "models/vae/models/" + filename
            elif dropdown == "Embeddings":
                destination = "embeddings/models/" + filename
                print(destination)
            download_with_aria2c(url, destination)

        download_button.click(
            fn=download_model,
            inputs=[download_url,dropdown,filename],
            outputs=[],
        )
        return [(ui_component, "Model Downloader", "model_downloader_tab")]


script_callbacks.on_ui_tabs(on_ui_tabs)