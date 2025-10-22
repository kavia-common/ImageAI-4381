from typing import Dict

def get_device_info() -> Dict:
    """Return information about available compute devices."""
    info = {"cpu": True, "cuda": False, "cuda_device_count": 0, "device_preference": "cpu"}
    try:
        import torch  # type: ignore
        if torch.cuda.is_available():
            info["cuda"] = True
            info["cuda_device_count"] = torch.cuda.device_count()
            info["device_preference"] = "cuda"
    except Exception:
        # torch not installed or fails to import; remain CPU-first
        pass
    return info

def select_device() -> str:
    """Selects the best device identifier for pytorch and returns 'cuda' or 'cpu'."""
    try:
        import torch  # type: ignore
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"
