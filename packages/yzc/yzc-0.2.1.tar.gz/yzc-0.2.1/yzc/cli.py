import argparse
import os
import subprocess

PLUGIN_INFOS = {
    "UsePluginV2DynamicExt": {
        "url": "http://8.148.226.184/index.php/s/TnzTDJCasg7xdSG/download/UsePluginV2DynamicExt.tar.gz",
        "tar": "UsePluginV2DynamicExt.tar.gz",
        "dir": "UsePluginV2DynamicExt"
    },
    "HttpSharedMemoryTisC++": {
        "url": "http://8.148.226.184/index.php/s/2wQw6k8k7k8k7k8/download/HttpSharedMemoryTisC++.tar.gz",
        "tar": "HttpSharedMemoryTisC++.tar.gz",
        "dir": "HttpSharedMemoryTisC++"
    }
}

def main():
    parser = argparse.ArgumentParser(description="A simple CLI tool for yzc.")
    parser.add_argument('--hello', action='store_true', help="Print Hello, World!")
    parser.add_argument('--get', nargs='+', choices=list(PLUGIN_INFOS.keys()), help="Download and extract plugin(s) by name.")
    parser.add_argument('--list', action='store_true', help="Show available plugins.")

    args = parser.parse_args()

    if args.hello:
        print("Hello, World!")

    if args.list:
        print("Available samples:")
        for name in PLUGIN_INFOS:
            print(f"\033[32m- {name}\033[0m")

    if args.get:
        for plugin_name in args.get:
            info = PLUGIN_INFOS[plugin_name]
            file_url = info["url"]
            tar_file_name = info["tar"]
            extract_dir_name = info["dir"]
            current_dir = os.getcwd()
            tar_file_path = os.path.join(current_dir, tar_file_name)
            try:
                print(f"Downloading file from {file_url}...")
                subprocess.run(["wget", file_url, "-O", tar_file_path], check=True)
                print(f"File downloaded to {tar_file_path}")
                print(f"Extracting {tar_file_name}...")
                subprocess.run(["tar", "-xzvf", tar_file_path], check=True)
                subprocess.run(["rm", tar_file_path], check=True)
                print(f"Changing directory to {extract_dir_name}...")
                os.chdir(os.path.join(current_dir, extract_dir_name))
                print(f"Current working directory: {os.getcwd()}")
                os.chdir(current_dir)  # 回到原目录，避免影响后续操作
            except subprocess.CalledProcessError as e:
                print(f"Command execution failed with error:\n{e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()