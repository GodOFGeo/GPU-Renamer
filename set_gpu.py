import plistlib
import subprocess
import os

def load_config(plist_path):
    try:
        with open(plist_path, 'rb') as f:
            return plistlib.load(f)
    except Exception as e:
        print(f"Error loading your config.plist: {e}")
        return None

def save_config(plist_path, plist_data):
    try:
        with open(plist_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        print("config.plist saved successfully!")
    except Exception as e:
        print(f"Error saving your config.plist: {e}")

def change_gpu_name(plist_data, new_name):
    if "DeviceProperties" not in plist_data:
        plist_data["DeviceProperties"] = {}

    if device_key not in plist_data["DeviceProperties"]:
        plist_data["DeviceProperties"][device_key] = {}

    plist_data["DeviceProperties"][device_key]["model"] = new_name
    return plist_data

def add_pci_root(plist_data, pci_root):
    if "DeviceProperties" not in plist_data:
        plist_data["DeviceProperties"] = {}

    if "Add" not in plist_data["DeviceProperties"]:
        plist_data["DeviceProperties"]["Add"] = {}

    plist_data["DeviceProperties"]["Add"][pci_root] = {
    }

    return plist_data

def get_pci_root():
    try: 
        result = subprocess.run(["./gfxutil", "-f", "display"], capture_output=True, text=True)
        output = result.stdout.strip()
        for line in output.splitlines():
            if "PciRoot" in line:
                pci_root = line.split("= ")[1].strip()
                return pci_root
    except Exception as e:
        print(f"Error running gfxutil: {e}")
        return None

def clean_path(plist_path):
    return plist_path.strip().strip("'").strip('"').replace('\\ ', ' ')

def main():
    print("########################################")
    print("#--------------GPURenamer--------------#")
    print("########################################")
    
    while True:
        print("\nSelect an option:")
        print("1. Auto-detect PCI Root and update GPU name")
        print("2. Manually enter PCI Root and update GPU name")
        print("3. Exit")

        choice = input("Enter your choice (1, 2 or 3): ")

        if choice == '1':
            print("Drag and drop your config.plist file here:")
            plist_path = input().strip()
            plist_path = clean_path(plist_path)

            pci_root = get_pci_root()
            if not pci_root:
                print("Error detecting PCI Root. Please try manually or ensure gfxutil is present.")
                continue
            
            gpu_name = input("Enter the new GPU name:")
            plist_data = load_config(plist_path)
            plist_data = add_pci_root(plist_data, pci_root)
            plist_data["DeviceProperties"]["Add"][pci_root]["model"] = gpu_name
            save_config(plist_path, plist_data)
            print(f"Updated {pci_root} with GPU name '{gpu_name}'.")

        if choice == '2':
            print("Drag and drop your config.plist file here:")
            plist_path = input().strip()
            plist_path = clean_path(plist_path)

            pci_root = input("Enter the PCI Root to add: ")
            gpu_name = input("Enter the GPU name: ")
            plist_data = load_config(plist_path)
            plist_data = add_pci_root(plist_data, pci_root)
            plist_data["DeviceProperties"]["Add"][pci_root]["model"] = gpu_name
            save_config(plist_path, plist_data)
            print(f"Updated {pci_root} with GPU name '{gpu_name}'.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
