import gradio as gr
import os
import subprocess

# from modules import script_callbacks

# Path to aria2c binary file
aria2c_path = "./aria2c.exe"

def download_with_aria2c(url, destination):
    process = subprocess.Popen(
        [aria2c_path, "-x", "16", "-s", "16", "-o", destination, url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Download failed with error code {process.returncode}:\n{stderr.decode('utf-8')}")
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

        def download_model():
            url = download_url.value
            filename_value = filename.value or "downloaded_file"
            destination = ""
            if dropdown.value == "Stable Diffusion":
                destination = os.path.join("/../../../models/Stable-diffusion", "models", f"{filename_value}.pt")
            elif dropdown.value == "LoRA":
                destination = os.path.join("/../../../models/Lora", "models", f"{filename_value}.pt")
            elif dropdown.value == "VAE":
                destination = os.path.join("/../../../models/vae", "models", f"{filename_value}.pt")
            elif dropdown.value == "Embeddings":
                destination = os.path.join("/../../../embeddings", "models", f"{filename_value}.pt")
            download_with_aria2c(url, destination)

        download_button.action = download_model
        return [(ui_component, "Model Downloader", "model_downloader_tab")]


# script_callbacks.on_ui_tabs(on_ui_tabs)
