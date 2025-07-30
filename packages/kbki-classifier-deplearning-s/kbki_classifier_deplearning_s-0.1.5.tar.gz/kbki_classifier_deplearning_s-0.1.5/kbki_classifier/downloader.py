import gdown
import os
import zipfile
from pathlib import Path

class ModelDownloader:
    """Download and setup model files"""
    
    def __init__(self, model_dir="./models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
    
    def download_models(self):
        """Download all required model files"""
        files_to_download = {
            'modelh2o': '1dgBIQj8Ey8yLJ9R2ml8C5pI7SWwtP4rY',
            'tfidf_vectorizer.pkl': '1Aw_ET5shSiI72N-ETJAA3U_DPeDv2yj-',
            'feature_names.pkl': '1p8q-l39XNZz8M6cwJUyDsUs_dPRTNOCd',
            'models.zip': '1RIgZOCVmCjS1vgK2KihdwcUjORXNSd0H'
        }
        
        for filename, file_id in files_to_download.items():
            output_path = self.model_dir / filename
            if not output_path.exists():
                print(f"Downloading {filename}...")
                gdown.download(
                    f'https://drive.google.com/uc?id={file_id}',
                    str(output_path),
                    quiet=False
                )
        
        # Extract models.zip
        models_zip = self.model_dir / 'models.zip'
        if models_zip.exists():
            print("Extracting models.zip...")
            with zipfile.ZipFile(models_zip, 'r') as zip_ref:
                zip_ref.extractall(self.model_dir)
    
    def check_models_exist(self):
        """Check if all required models exist"""
        required_files = [
            'modelh2o',
            'tfidf_vectorizer.pkl',
            'feature_names.pkl',
            'models/metadata.pkl'
        ]
        
        for file_path in required_files:
            if not (self.model_dir / file_path).exists():
                return False
        return True
